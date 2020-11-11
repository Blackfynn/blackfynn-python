# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from builtins import object, zip
from future.utils import PY2, as_native_str, string_types

import datetime
import io
import os
import re
import sys
from uuid import uuid4

import dateutil
import pytz
import requests
from dateutil.parser import parse

from blackfynn import log
from blackfynn.extensions import numpy as np
from blackfynn.extensions import pandas as pd
from blackfynn.extensions import require_extension
from blackfynn.utils import get_data_type, infer_epoch, usecs_to_datetime, value_as_type

try:  # Python 3
    from inspect import getfullargspec
except ImportError:  # Python 2
    from inspect import getargspec as getfullargspec


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_package_class(data):
    """
    Determines package type and returns appropriate class.
    """
    content = data.get("content", data)
    if "packageType" not in content:
        p = Dataset
    else:
        ptype = content["packageType"].lower()
        if ptype == "collection":
            p = Collection
        elif ptype == "timeseries":
            p = TimeSeries
        elif ptype == "dataset":
            p = Dataset
        else:
            p = DataPackage

    return p


def _update_self(self, updated):
    if self.id != updated.id:
        raise Exception("cannot update {} with {}".format(self, updated))

    self.__dict__.update(updated.__dict__)

    return self


def _flatten_file_args(files):
    """
    Flatten file arguments so that upload methods can be called either as

        dataset.upload(file1, file2)

    or as

        dataset.upload([file1, file2])
    """
    if len(files) == 1 and not isinstance(files[0], string_types):
        # single argument - is it iterable and not a string?
        try:
            files = list(files[0])
        except Exception:
            pass

    return files


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Basics
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Property(object):
    """
    Property of a blackfynn object.

    Args:
        key (str): the key of the property
        value (str,number): the value of the property

        fixed (bool): if true, the value cannot be changed after the property is created
        hidden (bool): if true, the value is hidden on the platform
        category (str): the category of the property, default: "Blackfynn"
        data_type (str): one of 'string', 'integer', 'double', 'date', 'user'

    """

    _data_types = ["string", "integer", "double", "date", "user", "boolean"]

    def __init__(
        self,
        key,
        value,
        fixed=False,
        hidden=False,
        category="Blackfynn",
        data_type=None,
    ):
        self.key = key
        self.fixed = fixed
        self.hidden = hidden
        self.category = category

        if data_type is None or (data_type.lower() not in self._data_types):
            dt, v = get_data_type(value)
            self.data_type = dt
            self.value = v
        else:
            self.data_type = data_type
            self.value = value_as_type(value, data_type.lower())

    def as_dict(self):
        """
        Representation of instance as dictionary, used when calling API.
        """
        return {
            "key": self.key,
            "value": str(self.value),  # value needs to be string :-(
            "dataType": self.data_type,
            "fixed": self.fixed,
            "hidden": self.hidden,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data, category="Blackfynn"):
        """
        Create an instance from dictionary, used when handling API response.
        """
        return cls(
            key=data["key"],
            value=data["value"],
            category=category,
            fixed=data["fixed"],
            hidden=data["hidden"],
            data_type=data["dataType"],
        )

    def __str__(self):
        return self.__repr__()

    @as_native_str()
    def __repr__(self):
        return u"<Property key='{}' value='{}' type='{}' category='{}'>".format(
            self.key, self.value, self.data_type, self.category
        )


def _get_all_class_args(cls):
    # possible class arguments
    if cls == object:
        return set()
    class_args = set()

    for base in cls.__bases__:
        # get all base class argument variables
        class_args.update(_get_all_class_args(base))

    # get args from this class
    spec = getfullargspec(cls.__init__)
    class_args.update(spec[0])  # arguments
    if spec[1] is not None:
        class_args.add(spec[1])  # variable arguments
    if spec[2] is not None:
        class_args.add(spec[2])  # variable keyword arguments

    return class_args


class BaseNode(object):
    """
    Base class to serve all objects
    """

    _api = None
    _object_key = "content"

    def __init__(self, id=None, int_id=None, *args, **kargs):
        self.id = id
        self.int_id = int_id

    @classmethod
    def from_dict(cls, data, api=None, object_key=None):
        # which object_key are we going to use?
        if object_key is not None:
            obj_key = object_key
        else:
            obj_key = cls._object_key

        # validate obj_key
        if obj_key == "" or obj_key is None:
            content = data
        else:
            content = data[obj_key]

        class_args = _get_all_class_args(cls)

        # find overlapping keys
        kwargs = {}
        thing_id = content.pop("id", None)
        thing_int_id = content.pop("intId", None)
        for k, v in content.items():
            # check lower case var names
            k_lower = k.lower()
            # check camelCase --> camel_case
            k_camel = re.sub(r"[A-Z]", lambda x: "_" + x.group(0).lower(), k)
            # check s3case --> s3_case
            k_camel_num = re.sub(r"[0-9]", lambda x: x.group(0) + "_", k)

            # match with existing args
            if k_lower in class_args:
                key = k_lower
            elif k_camel in class_args:
                key = k_camel
            elif k_camel_num in class_args:
                key = k_camel_num
            else:
                key = k

            # assign
            kwargs[key] = v

        # init class with args
        item = cls.__new__(cls)
        cls.__init__(item, **kwargs)

        if thing_id is not None:
            item.id = thing_id

        if thing_int_id is not None:
            item.int_id = thing_int_id

        if api is not None:
            item._api = api
            item._api.core.set_local(item)
        return item

    def __eq__(self, item):
        if not isinstance(item, BaseNode):
            return False
        elif self.exists and item.exists:
            return self.id == item.id
        else:
            return self is item

    @property
    def exists(self):
        """
        Whether or not the instance of this object exists on the platform.
        """
        return self.id is not None

    def _check_exists(self):
        if not self.exists:
            raise Exception(
                "Object must be created on the platform before method is called."
            )

    def __str__(self):
        return self.__repr__()


class BaseDataNode(BaseNode):
    """
    Base class to serve all "data" node-types on platform, e.g. Packages and Collections.
    """

    _type_name = "packageType"

    def __init__(
        self,
        name,
        type,
        parent=None,
        owner_id=None,
        dataset_id=None,
        id=None,
        provenance_id=None,
        **kwargs
    ):

        super(BaseDataNode, self).__init__(id=id)

        self.name = name
        self._properties = {}
        if isinstance(parent, string_types) or parent is None:
            self.parent = parent
        elif isinstance(parent, Collection):
            self.parent = parent.id
        else:
            raise Exception("Invalid parent {}".format(parent))
        self.type = type
        self.dataset = dataset_id
        self.owner_id = owner_id
        self.provenance_id = provenance_id

        self.state = kwargs.pop("state", None)
        self.created_at = kwargs.pop("createdAt", None)
        self.updated_at = kwargs.pop("updatedAt", None)

    def update_properties(self):
        self._api.data.update_properties(self)

    def _set_properties(self, *entries):
        # Note: Property is stored as dict of key:properties-entry to enable
        #       over-write of properties values based on key
        for entry in entries:
            assert type(entry) is Property, "Properties wrong type"
            if entry.category not in self._properties:
                self._properties[entry.category] = {}
            self._properties[entry.category].update({entry.key: entry})

    def add_properties(self, *entries):
        """
        Add properties to object.

        Args:
            entries (list): list of Property objects to add to this object

        """
        self._set_properties(*entries)

        # update on platform
        if self.exists:
            self.update_properties()

    def insert_property(
        self,
        key,
        value,
        fixed=False,
        hidden=False,
        category="Blackfynn",
        data_type=None,
    ):
        """
        Add property to object using simplified interface.

        Args:
            key (str): the key of the property
            value (str,number): the value of the property

            fixed (bool): if true, the value cannot be changed after the property is created
            hidden (bool): if true, the value is hidden on the platform
            category (str): the category of the property, default: "Blackfynn"
            data_type (str): one of 'string', 'integer', 'double', 'date', 'user'

        Note:
            This method is being depreciated in favor of ``set_property()`` method (see below).

        """
        return self.set_property(
            key=key,
            value=value,
            fixed=fixed,
            hidden=hidden,
            category=category,
            data_type=data_type,
        )

    def set_property(
        self,
        key,
        value,
        fixed=False,
        hidden=False,
        category="Blackfynn",
        data_type=None,
    ):
        """
        Add property to object using simplified interface.

        Args:
            key (str): the key of the property
            value (str,number): the value of the property

            fixed (bool): if true, the value cannot be changed after the property is created
            hidden (bool): if true, the value is hidden on the platform
            category (str): the category of the property, default: "Blackfynn"
            data_type (str): one of 'string', 'integer', 'double', 'date', 'user'

        """
        self._set_properties(
            Property(
                key=key,
                value=value,
                fixed=fixed,
                hidden=hidden,
                category=category,
                data_type=data_type,
            )
        )
        # update on platform, if possible
        if self.exists:
            self.update_properties()

    @property
    def properties(self):
        """
        Returns a list of properties attached to object.
        """
        props = []
        for category in self._properties.values():
            props.extend(category.values())
        return props

    def get_property(self, key, category="Blackfynn"):
        """
        Returns a single property for the provided key, if available

        Args:
            key (str): key of the desired property
            category (str, optional): category of property

        Returns:
            object of type ``Property``

        Example::

            pkg.set_property('quality', 85.0)
            pkg.get_property('quality')

        """
        return self._properties[category].get(key, None)

    def remove_property(self, key, category="Blackfynn"):
        """
        Removes property of key ``key`` and category ``category`` from the object.

        Args:
            key (str): key of property to remove
            category (str, optional): category of property to remove

        """
        if key in self._properties[category]:
            # remove by setting blank
            self._properties[category][key].value = ""
            # update remotely
            self.update_properties()
            # get rid of it locally
            self._properties[category].pop(key)

    def update(self, **kwargs):
        """
        Updates object on the platform (with any local changes) and syncs
        local instance with API response object.

        Exmple::

            pkg = bf.get('N:package:1234-1234-1234-1234')
            pkg.name = "New name"
            pkg.update()

        """
        self._check_exists()
        r = self._api.core.update(self, **kwargs)
        _update_self(self, r)

    def delete(self):
        """
        Delete object from platform.
        """
        self._check_exists()
        r = self._api.core.delete(self)
        self.id = None

    def as_dict(self):
        d = {
            "name": self.name,
            self._type_name: self.type,
            "properties": [m.as_dict() for m in self.properties],
        }

        for k in ["parent", "state", "dataset"]:
            kval = self.__dict__.get(k, None)
            if hasattr(self, k) and kval is not None:
                d[k] = kval

        if self.provenance_id is not None:
            d["provenanceId"] = self.provenance_id

        return d

    @classmethod
    def from_dict(cls, data, *args, **kwargs):
        item = super(BaseDataNode, cls).from_dict(data, *args, **kwargs)
        try:
            item.state = data["content"]["state"]
        except:
            pass

        item.owner_id = (
            data.get("owner")
            or data.get(
                "ownerId",
            )
            or data.get("content", {}).get("ownerId")  # For packages
        )

        # parse, store parent (ID only)
        parent = data.get("parent", None)
        if parent is not None:
            if isinstance(parent, string_types):
                item.parent = parent
            else:
                pkg_cls = get_package_class(parent)
                p = pkg_cls.from_dict(parent, *args, **kwargs)
                item.parent = p.id

        def cls_add_property(prop):
            cat = prop.category
            if cat not in item._properties:
                item._properties[cat] = {}
            item._properties[cat].update({prop.key: prop})

        # parse properties
        if "properties" in data:
            for entry in data["properties"]:
                if "properties" not in entry:
                    # flat list of properties: [entry]
                    prop = Property.from_dict(entry, category=entry["category"])
                    cls_add_property(prop)
                else:
                    # nested properties list [ {category,entry} ]
                    category = entry["category"]
                    for prop_entry in entry["properties"]:
                        prop = Property.from_dict(prop_entry, category=category)
                        cls_add_property(prop)
        return item


class BaseCollection(BaseDataNode):
    """
    Base class used for both ``Dataset`` and ``Collection``.
    """

    def __init__(self, name, package_type, **kwargs):
        self.storage = kwargs.pop("storage", None)
        super(BaseCollection, self).__init__(name, package_type, **kwargs)

        # items is None until an API response provides the item objects
        # to be parsed, which then updates this instance.
        self._items = None

    def add(self, *items):
        """
        Add items to the Collection/Dataset.
        """
        self._check_exists()
        for item in items:
            # initialize if need be
            if self._items is None:
                self._items = []
            if isinstance(self, Dataset):
                item.parent = None
                item.dataset = self.id
            elif hasattr(self, "dataset"):
                item.parent = self.id
                item.dataset = self.dataset

            # create, if not already created
            new_item = self._api.core.create(item)
            item.__dict__.update(new_item.__dict__)

            # add item
            self._items.append(item)

    def remove(self, *items):
        """
        Removes items, where items can be an object or the object's ID (string).
        """
        self._check_exists()
        for item in items:
            if item not in self._items:
                raise Exception("Cannot remove item, not in collection:{}".format(item))

        self._api.data.delete(*items)

        # remove locally
        for item in items:
            self._items.remove(item)

    @property
    def items(self):
        """
        Get all items inside Dataset/Collection (i.e. non-nested items).

        Note:
            You can also iterate over items inside a Dataset/Colleciton without using ``.items``::

                for item in my_dataset:
                    print("item name = ", item.name)

        """
        self._check_exists()
        if self._items is None:
            new_self = self._get_method(self)
            new_items = new_self._items
            self._items = new_items if new_items is not None else []

        return self._items

    @property
    def _get_method(self):
        pass

    def print_tree(self, indent=0):
        """
        Prints a tree of **all** items inside object.
        """
        self._check_exists()
        print(u"{}{}".format(" " * indent, self))
        for item in self.items:
            if isinstance(item, BaseCollection):
                item.print_tree(indent=indent + 2)
            else:
                print(u"{}{}".format(" " * (indent + 2), item))

    def get_items_by_name(self, name):
        """
        Get an item inside of object by name (if match is found).

        Args:
            name (str): the name of the item

        Returns:
            list of matches

        Note:
            This only works for **first-level** items, meaning it must exist directly inside the current object;
            nested items will not be returned.

        """
        self._check_exists()
        # note: non-hierarchical
        return [x for x in self.items if x.name == name]

    def get_items_names(self):
        self._check_exists()
        return [x.name for x in self.items]

    def upload(self, *files, **kwargs):
        """
        Upload files into current object.

        Args:
            files: list of local files to upload. If the Blackfynn CLI Agent is
                installed you can also upload a directory. See :ref:`agent` for
                more information.

        Keyword Args:
            display_progress (boolean): If ``True``, a progress bar will be
                shown to track upload progress. Defaults to ``False``.
            use_agent (boolean): If ``True``, and a compatible version of the
                Agent is installed, uploads will be performed by the
                Blackfynn CLI Agent. This allows large file upload in excess
                of 1 hour. Defaults to ``True``.
            recursive (boolean): If ``True``, the nested folder structure of
                the uploaded directory will be preversed. This can only be used
                with the Blackfynn CLI Agent. Defaults to ``False``.

        Example::

            my_collection.upload('/path/to/file1.nii.gz', '/path/to/file2.pdf')

        """
        self._check_exists()
        files = _flatten_file_args(files)
        return self._api.io.upload_files(self, files, append=False, **kwargs)

    def create_collection(self, name):
        """
        Create a new collection within the current object. Collections can be created within
        datasets and within other collections.

        Args:
            name (str): The name of the to-be-created collection

        Returns:
            The created ``Collection`` object.

        Example::

              from blackfynn import Blackfynn()

              bf = Blackfynn()
              ds = bf.get_dataset('my_dataset')

              # create collection in dataset
              col1 = ds.create_collection('my_collection')

              # create collection in collection
              col2 = col1.create_collection('another_collection')

        """
        c = Collection(name)
        self.add(c)
        return c

    # sequence-like method
    def __getitem__(self, i):
        self._check_exists()
        return self.items[i]

    # sequence-like method
    def __len__(self):
        self._check_exists()
        return len(self.items)

    # sequence-like method
    def __delitem__(self, key):
        self._check_exists()
        self.remove(key)

    def __iter__(self):
        self._check_exists()
        for item in self.items:
            yield item

    # sequence-like method
    def __contains__(self, item):
        """
        Tests if item is in the collection, where item can be either
        an object's ID (string) or an object's instance.
        """
        self._check_exists()
        if isinstance(item, string_types):
            some_id = self._api.data._get_id(item)
            item_ids = [x.id for x in self.items]
            contains = some_id in item_ids
        elif self._items is None:
            return False
        else:
            return item in self._items

        return contains

    def as_dict(self):
        d = super(BaseCollection, self).as_dict()
        if self.owner_id is not None:
            d["owner"] = self.owner_id
        return d

    @classmethod
    def from_dict(cls, data, *args, **kwargs):
        item = super(BaseCollection, cls).from_dict(data, *args, **kwargs)

        item.storage = data.get("storage", None)
        children = []
        if "children" in data:
            for child in data["children"]:
                pkg_cls = get_package_class(child)
                kwargs["api"] = item._api
                pkg = pkg_cls.from_dict(child, *args, **kwargs)
                children.append(pkg)
        item.add(*children)
        return item

    @as_native_str()
    def __repr__(self):
        return u"<BaseCollection name='{}' id='{}'>".format(self.name, self.id)


class DataPackage(BaseDataNode):
    """
    DataPackage is the core data object representation on the platform.

    Args:
        name (str):          The name of the data package
        package_type (str):  The package type, e.g. 'TimeSeries', 'MRI', etc.

    Note:
        ``package_type`` must be a supported package type. See our data type
        registry for supported values.

    """

    def __init__(self, name, package_type, **kwargs):
        self.storage = kwargs.pop("storage", None)
        super(DataPackage, self).__init__(name=name, type=package_type, **kwargs)
        # local-only attribute
        self.session = None

    @property
    def sources(self):
        """
        Returns the sources of a DataPackage. Sources are the raw, unmodified
        files (if they exist) that contains the package's data.
        """
        self._check_exists()
        return self._api.packages.get_sources(self)

    @property
    def files(self):
        """
        Returns the files of a DataPackage. Files are the possibly modified
        source files (e.g. converted to a different format), but they could also
        be the source files themselves.
        """
        self._check_exists()
        return self._api.packages.get_files(self)

    @property
    def view(self):
        """
        Returns the object(s) used to view the package. This is typically a set of
        file objects, that may be the DataPackage's sources or files, but could also be
        a unique object specific for the viewer.
        """
        self._check_exists()
        return self._api.packages.get_view(self)

    def process(self):
        """
        Process a data package that has successfully uploaded it's source
        files but has not yet been processed by the Blackfynn ETL.
        """
        self._check_exists()
        return self._api.packages.process(self)

    def relate_to(self, *records):
        """
        Relate current ``DataPackage`` to one or more ``Record`` objects.

        Args:
            records (list of Records): Records to relate to data package

        Returns:
            ``Relationship`` that defines the link

        Example:

            Relate package to a single record::

                eeg.relate_to(participant_123)

            Relate package to multiple records::

                # relate to explicit list of records
                eeg.relate_to(
                    participant_001
                    participant_002,
                    participant_003,
                )

                # relate to all participants
                eeg.relate_to(participants.get_all())

        Note:
            The created relationship will be of the form ``DataPackage`` --(``belongs_to``)--> ``Record``.
        """
        self._check_exists()
        if isinstance(records, Record):
            records = [records]

        assert all(
            [isinstance(r, Record) for r in records]
        ), "all records must be object of type Record"

        # auto-create relationship type
        relationships = self._api.concepts.relationships.get_all(self.dataset)
        if "belongs_to" not in relationships:
            r = RelationshipType(
                dataset_id=self.dataset, name="belongs_to", description="belongs_to"
            )
            self._api.concepts.relationships.create(self.dataset, r)

        return [
            self._api.concepts.proxies.create(
                self.dataset, self.id, "belongs_to", r, {}
            )
            for r in records
        ]

    def as_dict(self):
        d = super(DataPackage, self).as_dict()
        if self.owner_id is not None:
            d["owner"] = self.owner_id
        return d

    @classmethod
    def from_dict(cls, data, *args, **kwargs):
        data["content"]["id"] = data["content"]["nodeId"]
        item = super(DataPackage, cls).from_dict(data, *args, **kwargs)
        # parse objects
        objects = data.get("objects", None)
        if objects is not None:
            for otype in ["sources", "files", "view"]:
                if otype not in data["objects"]:
                    continue
                odata = data["objects"][otype]
                item.__dict__[otype] = [File.from_dict(x) for x in odata]
        return item

    @classmethod
    def from_id(cls, id):
        return self._api.packages.get(id)

    @as_native_str()
    def __repr__(self):
        return u"<DataPackage name='{}' id='{}'>".format(self.name, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class File(BaseDataNode):
    """
    File node on the Blackfynn platform. Points to some S3 location.

    Args:
        name (str):      Name of the file (without extension)
        s3_key (str):    S3 key of file
        s3_bucket (str): S3 bucket of file
        file_type (str): Type of file, e.g. 'MPEG', 'PDF'
        size (long): Size of file

    Note:
        ``file_type`` must be a supported file type. See our file type registry
        for a list of supported file types.


    """

    _type_name = "fileType"

    def __init__(self, name, s3_key, s3_bucket, file_type, size, pkg_id=None, **kwargs):
        super(File, self).__init__(name, type=file_type, **kwargs)

        # data
        self.s3_key = s3_key
        self.s3_bucket = s3_bucket
        self.size = size
        self.pkg_id = pkg_id
        self.local_path = None

    def as_dict(self):
        d = super(File, self).as_dict()
        d.update({"s3bucket": self.s3_bucket, "s3key": self.s3_key, "size": self.size})
        d.pop("parent", None)
        props = d.pop("properties")
        return {"objectType": "file", "content": d, "properties": props}

    @property
    def url(self):
        """
        The presigned-URL of the file.
        """
        self._check_exists()
        return self._api.packages.get_presigned_url_for_file(self.pkg_id, self.id)

    def download(self, destination):
        """
        Download the file.

        Args:
            destination (str): path for downloading; can be absolute file path,
                               prefix or destination directory.

        """
        if self.type == "DirectoryViewerData":
            raise NotImplementedError(
                "Downloading S3 directories is currently not supported"
            )

        if os.path.isdir(destination):
            # destination dir
            f_local = os.path.join(destination, os.path.basename(self.s3_key))
        if "." not in os.path.basename(destination):
            # destination dir + prefix
            f_local = destination + "_" + os.path.basename(self.s3_key)
        else:
            # exact location
            f_local = destination

        r = requests.get(self.url, stream=True)
        with io.open(f_local, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # set local path
        self.local_path = f_local

        return f_local

    @as_native_str()
    def __repr__(self):
        return (
            u"<File name='{}' type='{}' key='{}' bucket='{}' size='{}' id='{}'>".format(
                self.name, self.type, self.s3_key, self.s3_bucket, self.size, self.id
            )
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Time series
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TimeSeries(DataPackage):
    """
    Represents a timeseries package on the platform. TimeSeries packages
    contain channels, which contain time-dependent data sampled at some
    frequency.

    Args:
        name:  The name of the timeseries package

    """

    def __init__(self, name, **kwargs):
        kwargs.pop("package_type", None)
        super(TimeSeries, self).__init__(name=name, package_type="TimeSeries", **kwargs)

    @property
    def start(self):
        """
        The start time of time series data (over all channels)
        """
        self._check_exists()
        return sorted([x.start for x in self.channels])[0]

    @property
    def end(self):
        """
        The end time (in usecs) of time series data (over all channels)
        """
        self._check_exists()
        return sorted([x.end for x in self.channels])[-1]

    def limits(self):
        """
        Returns time limit tuple (start, end) of package.
        """
        channels = self.channels
        start = sorted([x.start for x in channels])[0]
        end = sorted([x.end for x in channels])[-1]
        return start, end

    def segments(self, start=None, stop=None, gap_factor=2):
        """
        Returns list of contiguous data segments available for package. Segments are
        assesssed for all channels, and the union of segments is returned.

        Args:
            start (int, datetime, optional):
                Return segments starting after this time
                (default earliest start of any channel)

            stop (int, datetime, optional):
                Return segments starting before this time
                (default latest end time of any channel)

            gap_factor (int, optional):
                Gaps are computed by ``sampling_rate * gap_factor`` (default 2)

        Returns:
            List of tuples, where each tuple represents the (start, stop) of contiguous data.
        """
        # flattenened list of segments across all channels
        channel_segments = [
            segment
            for channel in self.channels
            for segment in channel.segments(
                start=start, stop=stop, gap_factor=gap_factor
            )
        ]
        # union all segments
        union_segments = []
        for begin, end in sorted(channel_segments):
            if union_segments and union_segments[-1][1] >= begin - 1:
                new_segment = (union_segments[-1][0], max(union_segments[-1][1], end))
                union_segments.pop()
                union_segments.append(new_segment)
            else:
                union_segments.append((begin, end))
        return union_segments

    @property
    def channels(self):
        """
        Returns list of Channel objects associated with package.

        Note:
            This is a dynamically generated property, so every call will make an API request.

            Suggested usage::

                channels = ts.channels
                for ch in channels:
                    print(ch)

            This will be much slower, as the API request is being made each time.::

                for ch in ts.channels:
                    print(ch)

        """
        self._check_exists()
        # always dynamically return channel list
        return self._api.timeseries.get_channels(self)

    def get_channel(self, channel):
        """
        Get channel by ID.

        Args:
            channel (str): ID of channel
        """
        self._check_exists()
        return self._api.timeseries.get_channel(self, channel)

    def add_channels(self, *channels):
        """
        Add channels to TimeSeries package.

        Args:
            channels: list of Channel objects.

        """
        self._check_exists()
        for channel in channels:
            ch = self._api.timeseries.create_channel(self, channel)
            channel.__dict__.update(ch.__dict__)

    def remove_channels(self, *channels):
        """
        Remove channels from TimeSeries package.

        Args:
            channels: list of Channel objects or IDs
        """
        self._check_exists()
        for channel in channels:
            if isinstance(channel, TimeSeriesChannel):
                self._api.timeseries.delete_channel(channel)
                channel.id = None
                channel._pkg = None
            else:
                self._api.timeseries.delete_channel_by_id(self.id, channel)

    # ~~~~~~~~~~~~~~~~~~
    # Data
    # ~~~~~~~~~~~~~~~~~~
    def get_data(
        self, start=None, end=None, length=None, channels=None, use_cache=True
    ):
        """
        Get timeseries data between ``start`` and ``end`` or ``start`` and ``start + length``
        on specified channels (default all channels).

        Args:
            start (optional): start time of data (usecs or datetime object)
            end (optional): end time of data (usecs or datetime object)
            length (optional): length of data to retrieve, e.g. '1s', '5s', '10m', '1h'
            channels (optional): list of channel objects or IDs, default all channels.

        Note:
            Data requests will be automatically chunked and combined into a single Pandas
            DataFrame. However, you must be sure you request only a span of data that
            will properly fit in memory.

            See ``get_data_iter`` for an iterator approach to timeseries data retrieval.

        Example:

            Get 5 seconds of data from start over all channels::

                data = ts.get_data(length='5s')

            Get data betwen 12345 and 56789 (representing usecs since Epoch)::

                data = ts.get_data(start=12345, end=56789)

            Get first 10 seconds for the first two channels::

                data = ts.get_data(length='10s', channels=ts.channels[:2])

        """
        self._check_exists()
        return self._api.timeseries.get_ts_data(
            self,
            start=start,
            end=end,
            length=length,
            channels=channels,
            use_cache=use_cache,
        )

    def get_data_iter(
        self,
        channels=None,
        start=None,
        end=None,
        length=None,
        chunk_size=None,
        use_cache=True,
    ):
        """
        Returns iterator over the data. Must specify **either ``end`` OR ``length``**, not both.

        Args:
            channels (optional): channels to retrieve data for (default: all)
            start: start time of data (default: earliest time available).
            end: end time of data (default: latest time avialable).
            length: some time length, e.g. '1s', '5m', '1h' or number of usecs
            chunk: some time length, e.g. '1s', '5m', '1h' or number of usecs

        Returns:
            iterator of Pandas Series, each the size of ``chunk_size``.

        """
        self._check_exists()
        return self._api.timeseries.get_ts_data_iter(
            self,
            channels=channels,
            start=start,
            end=end,
            length=length,
            chunk_size=chunk_size,
            use_cache=use_cache,
        )

    def write_annotation_file(self, file, layer_names=None):
        """
        Writes all layers to a csv .bfannot file

        Args:
            file : path to .bfannot output file. Appends extension if necessary
            layer_names (optional): List of layer names to write

        """

        return self._api.timeseries.write_annotation_file(self, file, layer_names)

    def append_annotation_file(self, file):
        """
        Processes .bfannot file and adds to timeseries package.

        Args:
            file : path to .bfannot file

        """
        self._check_exists()
        return self._api.timeseries.process_annotation_file(self, file)

    def append_files(self, *files, **kwargs):

        """
        Append files to this timeseries package.

        Args:
            files: list of local files to upload.

        Keyword Args:
            display_progress (boolean): If ``True``, a progress bar will be
                shown to track upload progress. Defaults to ``False``.
            use_agent (boolean): If ``True``, and a compatible version of the
                Agent is installed, uploads will be performed by the
                Blackfynn CLI Agent. This allows large file upload in excess
                of 1 hour. Defaults to ``True``.
        """
        self._check_exists()
        files = _flatten_file_args(files)
        return self._api.io.upload_files(self, files, append=True, **kwargs)

    def stream_data(self, data):
        self._check_exists()
        return self._api.timeseries.stream_data(self, data)

    # ~~~~~~~~~~~~~~~~~~
    # Annotations
    # ~~~~~~~~~~~~~~~~~~

    @property
    def layers(self):
        """
        List of annotation layers attached to TimeSeries package.
        """
        self._check_exists()
        # always dynamically return annotation layers
        return self._api.timeseries.get_annotation_layers(self)

    def get_layer(self, id_or_name):
        """
        Get annotation layer by ID or name.

        Args:
            id_or_name: layer ID or name
        """
        self._check_exists()
        layers = self.layers
        matches = [x for x in layers if x.id == id_or_name]
        if len(matches) == 0:
            matches = [x for x in layers if x.name == id_or_name]

        if len(matches) == 0:
            raise Exception("No layers match criteria.")
        if len(matches) > 1:
            raise Exception("More than one layer matched criteria")

        return matches[0]

    def add_layer(self, layer, description=None):
        """
        Args:
            layer:   TimeSeriesAnnotationLayer object or name of annotation layer
            description (str, optional):   description of layer

        """
        self._check_exists()
        return self._api.timeseries.create_annotation_layer(
            self, layer=layer, description=description
        )

    def add_annotations(self, layer, annotations):
        """
        Args:
            layer: either TimeSeriesAnnotationLayer object or name of annotation layer.
                   Note that non existing layers will be created.
            annotations: TimeSeriesAnnotation object(s)

        Returns:
            list of TimeSeriesAnnotation objects
        """
        self._check_exists()
        cur_layer = self._api.timeseries.create_annotation_layer(
            self, layer=layer, description=None
        )
        return self._api.timeseries.create_annotations(
            layer=cur_layer, annotations=annotations
        )

    def insert_annotation(
        self,
        layer,
        annotation,
        start=None,
        end=None,
        channel_ids=None,
        annotation_description=None,
    ):
        """
        Insert annotations using a more direct interface, without the need for layer/annotation objects.

        Args:
            layer: str of new/existing layer or annotation layer object
            annotation: str of annotation event

            start (optional): start of annotation
            end (optional): end of annotation
            channels_ids (optional): list of channel IDs to apply annotation
            annotation_description (optional): description of annotation

        Example:
            To add annotation on layer "my-events" across all channels::

                ts.insert_annotation('my-events', 'my annotation event')

            To add annotation to first channel::

                ts.insert_annotation('my-events', 'first channel event', channel_ids=ts.channels[0])

        """
        self._check_exists()
        cur_layer = self._api.timeseries.create_annotation_layer(
            self, layer=layer, description=None
        )
        return self._api.timeseries.create_annotation(
            layer=cur_layer,
            annotation=annotation,
            start=start,
            end=end,
            channel_ids=channel_ids,
            description=annotation_description,
        )

    def delete_layer(self, layer):
        """
        Delete annotation layer.

        Args:
            layer: annotation layer object

        """
        self._check_exists()
        return self._api.timeseries.delete_annotation_layer(layer)

    def annotation_counts(self, start, end, layers, period, channels=None):
        """
        Get annotation counts between ``start`` and ``end``.

        Args:
            start (datetime or microseconds) : The starting time of the range to query
            end (datetime or microseconds)   : The ending time of the the range to query
            layers ([TimeSeriesLayer])       : List of layers for which to count annotations
            period (string)                  : The length of time to group the counts.
                                               Formatted as a string - e.g. '1s', '5m', '3h'
            channels ([TimeSeriesChannel])   : List of channel (if omitted, all channels will be used)
        """
        self._check_exists()
        return self._api.timeseries.query_annotation_counts(
            ts=self,
            layers=layers,
            channels=channels,
            start=start,
            end=end,
            period=period,
        )

    @as_native_str()
    def __repr__(self):
        return u"<TimeSeries name='{}' id='{}'>".format(self.name, self.id)


class TimeSeriesChannel(BaseDataNode):
    """
    TimeSeriesChannel represents a single source of time series data. (e.g. electrode)

    Args:
        name (str):                   Name of channel
        rate (float):                 Rate of the channel (Hz)
        start (optional):             Absolute start time of all data (datetime obj)
        end (optional):               Absolute end time of all data (datetime obj)
        unit (str, optional):         Unit of measurement
        channel_type (str, optional): One of 'continuous' or 'event'
        source_type (str, optional):  The source of data, e.g. "EEG"
        group (str, optional):        The channel group, default: "default"

    """

    def __init__(
        self,
        name,
        rate,
        start=0,
        end=0,
        unit="V",
        channel_type="continuous",
        source_type="unspecified",
        group="default",
        last_annot=0,
        spike_duration=None,
        **kwargs
    ):
        self.channel_type = channel_type.upper()

        super(TimeSeriesChannel, self).__init__(
            name=name, type=self.channel_type, **kwargs
        )

        self.rate = rate
        self.unit = unit
        self.last_annot = last_annot
        self.group = group
        self.start = start
        self.end = end
        self.spike_duration = spike_duration

        self.set_property(
            "Source Type",
            source_type.upper(),
            fixed=True,
            hidden=True,
            category="Blackfynn",
        )

        ###  local-only
        # parent package
        self._pkg = None
        # sample period (in usecs)
        self._sample_period = 1.0e6 / self.rate

    @property
    def start(self):
        """
        The start time of channel data (microseconds since Epoch)
        """
        return self._start

    @start.setter
    def start(self, start):
        self._start = infer_epoch(start)

    @property
    def start_datetime(self):
        return usecs_to_datetime(self._start)

    @property
    def end(self):
        """
        The end time (in usecs) of channel data (microseconds since Epoch)
        """
        return self._end

    @end.setter
    def end(self, end):
        self._end = infer_epoch(end)

    @property
    def end_datetime(self):
        return usecs_to_datetime(self._end)

    def _page_delta(self, page_size):
        return int((1.0e6 / self.rate) * page_size)

    def update(self):
        self._check_exists()
        r = self._api.timeseries.update_channel(self)
        self.__dict__.update(r.__dict__)

    def segments(self, start=None, stop=None, gap_factor=2):
        """
        Return list of contiguous segments of valid data for channel.

        Args:
            start (long, datetime, optional):
                Return segments starting after this time (default start of channel)

            stop (long, datetime, optional):
                Return segments starting before this time (default end of channel)

            gap_factor (int, optional):
                Gaps are computed by ``sampling_period * gap_factor`` (default 2)

        Returns:
            List of tuples, where each tuple represents the (start, stop) of contiguous data.
        """
        start = self.start if start is None else start
        stop = self.end if stop is None else stop
        return self._api.timeseries.get_segments(
            self._pkg, self, start=start, stop=stop, gap_factor=gap_factor
        )

    @property
    def gaps(self):
        # TODO: infer gaps from segments
        raise NotImplementedError

    def update_properties(self):
        self._api.timeseries.update_channel_properties(self)

    def get_data(self, start=None, end=None, length=None, use_cache=True):
        """
        Get channel data between ``start`` and ``end`` or ``start`` and ``start + length``

        Args:
            start     (optional): start time of data (usecs or datetime object)
            end       (optional): end time of data (usecs or datetime object)
            length    (optional): length of data to retrieve, e.g. '1s', '5s', '10m', '1h'
            use_cache (optional): whether to use locally cached data

        Returns:
            Pandas Series containing requested data for channel.

        Note:
            Data requests will be automatically chunked and combined into a single Pandas
            Series. However, you must be sure you request only a span of data that
            will properly fit in memory.

            See ``get_data_iter`` for an iterator approach to timeseries data retrieval.

        Example:

            Get 5 seconds of data from start over all channels::

                data = channel.get_data(length='5s')

            Get data betwen 12345 and 56789 (representing usecs since Epoch)::

                data = channel.get_data(start=12345, end=56789)
        """

        return self._api.timeseries.get_ts_data(
            ts=self._pkg,
            start=start,
            end=end,
            length=length,
            channels=[self],
            use_cache=use_cache,
        )

    def get_data_iter(
        self, start=None, end=None, length=None, chunk_size=None, use_cache=True
    ):
        """
        Returns iterator over the data. Must specify **either ``end`` OR ``length``**, not both.

        Args:
            start      (optional): start time of data (default: earliest time available).
            end        (optional): end time of data (default: latest time avialable).
            length     (optional): some time length, e.g. '1s', '5m', '1h' or number of usecs
            chunk_size (optional): some time length, e.g. '1s', '5m', '1h' or number of usecs
            use_cache  (optional): whether to use locally cached data

        Returns:
            Iterator of Pandas Series, each the size of ``chunk_size``.
        """

        return self._api.timeseries.get_ts_data_iter(
            ts=self._pkg,
            start=start,
            end=end,
            length=length,
            channels=[self],
            chunk_size=chunk_size,
            use_cache=use_cache,
        )

    def as_dict(self):
        return {
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "unit": self.unit,
            "rate": self.rate,
            "channelType": self.channel_type,
            "lastAnnotation": self.last_annot,
            "group": self.group,
            "spikeDuration": self.spike_duration,
            "properties": [x.as_dict() for x in self.properties],
        }

    @as_native_str()
    def __repr__(self):
        return u"<TimeSeriesChannel name='{}' id='{}'>".format(self.name, self.id)


class TimeSeriesAnnotationLayer(BaseNode):
    """
    Annotation layer containing one or more annotations. Layers are used
    to separate annotations into logically distinct groups when applied
    to the same data package.

    Args:
        name:           Name of the layer
        time_series_id: The TimeSeries ID which the layer applies
        description:    Description of the layer

    """

    _object_key = None

    def __init__(self, name, time_series_id, description=None, **kwargs):
        super(TimeSeriesAnnotationLayer, self).__init__(**kwargs)
        self.name = name
        self.time_series_id = time_series_id
        self.description = description

    def iter_annotations(self, window_size=10, channels=None):
        """
        Iterate over annotations according to some window size (seconds).

        Args:
            window_size (float): Number of seconds in window
            channels:            List of channel objects or IDs

        Yields:
            List of annotations found in current window.
        """
        self._check_exists()
        ts = self._api.core.get(self.time_series_id)
        return self._api.timeseries.iter_annotations(
            ts=ts, layer=self, channels=channels, window_size=window_size
        )

    def add_annotations(self, annotations):
        """
        Add annotations to layer.

        Args:
            annotations (str): List of annotation objects to add.

        """
        self._check_exists()
        return self._api.timeseries.create_annotations(
            layer=self, annotations=annotations
        )

    def insert_annotation(
        self, annotation, start=None, end=None, channel_ids=None, description=None
    ):
        """
        Add annotations; proxy for ``add_annotations``.

        Args:
            annotation (str): Annotation string
            start:            Start time (usecs or datetime)
            end:              End time (usecs or datetime)
            channel_ids:      list of channel IDs

        Returns:
            The created annotation object.
        """
        self._check_exists()
        return self._api.timeseries.create_annotation(
            layer=self,
            annotation=annotation,
            start=start,
            end=end,
            channel_ids=channel_ids,
            description=description,
        )

    def annotations(self, start=None, end=None, channels=None):
        """
        Get annotations between ``start`` and ``end`` over ``channels`` (all channels by default).

        Args:
            start:    Start time
            end:      End time
            channels: List of channel objects or IDs

        """
        self._check_exists()
        ts = self._api.core.get(self.time_series_id)
        return self._api.timeseries.get_annotations(
            ts=ts, layer=self, channels=channels, start=start, end=end
        )

    def annotation_counts(self, start, end, period, channels=None):
        """
        The number of annotations between ``start`` and ``end`` over selected
        channels (all by default).

        Args:
            start (datetime or microseconds) : The starting time of the range to query
            end (datetime or microseconds)   : The ending time of the the range to query
            period (string)                  : The length of time to group the counts.
                                               Formatted as a string - e.g. '1s', '5m', '3h'
            channels ([TimeSeriesChannel])   : List of channel (if omitted, all channels will be used)
        """
        self._check_exists()
        ts = self._api.core.get(self.time_series_id)
        return self._api.timeseries.query_annotation_counts(
            ts=ts, layers=[self], channels=channels, start=start, end=end, period=period
        )

    def delete(self):
        """
        Delete annotation layer.
        """
        self._check_exists()
        return self._api.timeseries.delete_annotation_layer(self)

    def as_dict(self):
        return {"name": self.name, "description": self.description}

    @as_native_str()
    def __repr__(self):
        return u"<TimeSeriesAnnotationLayer name='{}' id='{}'>".format(
            self.name, self.id
        )


class TimeSeriesAnnotation(BaseNode):
    """
    Annotation is an event on one or more channels in a dataset

    Args:
        label (str):    The label for the annotation
        channel_ids:    List of channel IDs that annotation applies
        start:          Start time
        end:            End time
        name:           Name of annotation
        layer_id:       Layer ID for annoation (all annotations exist on a layer)
        time_series_id: TimeSeries package ID
        description:    Description of annotation

    """

    _object_key = None

    def __init__(
        self,
        label,
        channel_ids,
        start,
        end,
        name="",
        layer_id=None,
        time_series_id=None,
        description=None,
        **kwargs
    ):
        self.user_id = kwargs.pop("userId", None)
        super(TimeSeriesAnnotation, self).__init__(**kwargs)
        self.name = ""
        self.label = label
        self.channel_ids = channel_ids
        self.start = start
        self.end = end
        self.description = description
        self.layer_id = layer_id
        self.time_series_id = time_series_id

    def delete(self):
        self._check_exists()
        return self._api.timeseries.delete_annotation(annot=self)

    def as_dict(self):
        channel_ids = self.channel_ids
        if not isinstance(channel_ids, list):
            channel_ids = [channel_ids]
        return {
            "name": self.name,
            "label": self.label,
            "channelIds": channel_ids,
            "start": self.start,
            "end": self.end,
            "description": self.description,
            "layer_id": self.layer_id,
            "time_series_id": self.time_series_id,
        }

    @as_native_str()
    def __repr__(self):
        date = datetime.datetime.fromtimestamp(self.start / 1e6)
        return u"<TimeSeriesAnnotation label='{}' layer='{}' start='{}'>".format(
            self.label, self.layer_id, date.isoformat()
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class User(BaseNode):

    _object_key = ""

    def __init__(
        self,
        email,
        first_name,
        last_name,
        credential="",
        photo_url="",
        url="",
        authy_id=0,
        accepted_terms="",
        color=None,
        is_super_admin=False,
        *args,
        **kwargs
    ):
        kwargs.pop("preferredOrganization", None)
        self.storage = kwargs.pop("storage", None)
        super(User, self).__init__(*args, **kwargs)

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.credential = credential
        self.photo_url = photo_url
        self.color = color
        self.url = url
        self.authy_id = authy_id
        self.accepted_terms = ""
        self.is_super_admin = is_super_admin

    @as_native_str()
    def __repr__(self):
        return u"<User email='{}' id='{}'>".format(self.email, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Organizations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Organization(BaseNode):
    _object_key = "organization"

    def __init__(
        self,
        name,
        encryption_key_id="",
        slug=None,
        terms=None,
        features=None,
        subscription_state=None,
        *args,
        **kwargs
    ):
        self.storage = kwargs.pop("storage", None)
        super(Organization, self).__init__(*args, **kwargs)

        self.name = name
        self.terms = terms
        self.features = features or []
        self.subscription_state = subscription_state
        self.encryption_key_id = encryption_key_id
        self.slug = name.lower().replace(" ", "-") if slug is None else slug

    @property
    def datasets(self):
        """
        Return all datasets for user for an organization (current context).
        """
        self._check_exists()
        return self._api.datasets.get_all()

    @property
    def members(self):
        return self._api.organizations.get_members(self)

    @as_native_str()
    def __repr__(self):
        return u"<Organization name='{}' id='{}'>".format(self.name, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Datasets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Dataset(BaseCollection):
    def __init__(
        self,
        name,
        description=None,
        status=None,
        tags=None,
        automatically_process_packages=False,
        **kwargs
    ):
        kwargs.pop("package_type", None)
        kwargs.pop("type", None)
        super(Dataset, self).__init__(name, "DataSet", **kwargs)
        self.description = description or ""
        self._status = status
        self._tags = tags or []
        self.automatically_process_packages = automatically_process_packages

        # remove things that do not apply (a bit hacky)
        for k in (
            "parent",
            "type",
            "set_ready",
            "set_unavailable",
            "set_error",
            "state",
            "dataset",
        ):
            self.__dict__.pop(k, None)

    @as_native_str()
    def __repr__(self):
        return u"<Dataset name='{}' id='{}'>".format(self.name, self.id)

    @property
    def status(self):
        """Get the current status."""
        return self._status

    @property
    def tags(self):
        """Get the current tags."""
        return self._tags

    @status.setter
    def status(self, value):
        raise AttributeError("Dataset.status is read-only.")

    @tags.setter
    def tags(self, value):
        if isinstance(value, list) and all(
            isinstance(elem, string_types) for elem in value
        ):
            self._tags = value
        else:
            raise AttributeError("Dataset.tags should be a list of strings.")

    def get_topology(self):
        """Returns the set of Models and Relationships defined for the dataset

        Returns:
            dict: Keys are either ``models`` or ``relationships``. Values are
            the list of objects of that type

        """
        return self._api.concepts.get_topology(self)

    def get_graph_summary(self):
        """ Returns summary metrics about the knowledge graph """
        return self._api.concepts.get_summary(self)

    def published(self):
        return self._api.datasets.published(self.id)

    def status_log(self, limit=25, offset=0):
        return self._api.datasets.status_log(self.id, limit, offset)

    def package_count(self):
        return self._api.datasets.package_count(self.id)

    def team_collaborators(self):
        return self._api.datasets.team_collaborators(self.id)

    def user_collaborators(self):
        return self._api.datasets.user_collaborators(self.id)

    def get_packages_by_filename(self, filename):
        return self._api.datasets.get_packages_by_filename(self.id, filename)

    def owner(self):
        return self._api.datasets.owner(self.id)

    def models(self):
        """
        Returns:
            List of models defined in Dataset
        """
        return self._api.concepts.get_all(self.id)

    def relationships(self):
        """
        Returns:
            List of relationships defined in Dataset
        """
        return self._api.concepts.relationships.get_all(self.id)

    def get_model(self, name_or_id):
        """
        Retrieve a ``Model`` by name or id

        Args:
            name_or_id (str or int): name or id of the model

        Returns:
            The requested ``Model`` in Dataset

        Example::

            mouse = ds.get_model('mouse')
        """
        return self._api.concepts.get(self.id, name_or_id)

    def get_relationship(self, name_or_id):
        """
        Retrieve a ``RelationshipType`` by name or id

        Args:
            name_or_id (str or int): name or id of the relationship

        Returns:
            The requested ``RelationshipType``

        Example::

            belongsTo = ds.get_relationship('belongs-to')
        """
        return self._api.concepts.relationships.get(self.id, name_or_id)

    def get_connected_models(self, name_or_id):
        """Retrieve all models connected to the given model

            Connected is defined as model that can be reached by following
            outgoing relationships starting at the current model

        Args:
            name_or_id: Name or id of the model

        Return:
            List of ``Model`` objects


        Example::
            connected_models = ds.get_related_models('patient')

        """
        return self._api.concepts.get_connected(self.id, name_or_id)

    def create_model(
        self, name, display_name=None, description=None, schema=None, **kwargs
    ):
        """
        Defines a ``Model`` on the platform.

        Args:
            name (str):                  Name of the model
            description (str, optional): Description of the model
            schema (list, optional):     Definition of the model's schema as list of ModelProperty objects.

        Returns:
            The newly created ``Model``

        Note:
            It is required that a model includes at least _one_ property that serves as the "title".

        Example:

            Create a participant model, including schema::

                from blackfynn import ModelProperty

                ds.create_model('participant',
                    description = 'a human participant in a research study',
                    schema = [
                        ModelProperty('name', data_type=str, title=True),
                        ModelProperty('age',  data_type=int)
                    ]
                )

            Or define schema using dictionary::

                ds.create_model('participant',
                    schema = [
                        {
                            'name': 'full_name',
                            'data_type': str,
                            'title': True
                        },
                        {
                            'name': 'age',
                            'data_type': int,
                        }
                ])

            You can also create a model and define schema later::

                # create model
                pt = ds.create_model('participant')

                # define schema
                pt.add_property('name', str, title=True)
                pt.add_property('age', int)

        """

        c = Model(
            dataset_id=self.id,
            name=name,
            display_name=display_name if display_name else name,
            description=description,
            schema=schema,
            **kwargs
        )
        return self._api.concepts.create(self.id, c)

    def create_relationship_type(
        self, name, description, schema=None, source=None, destination=None, **kwargs
    ):
        """
        Defines a ``RelationshipType`` on the platform.

        Args:
            name (str):                  name of the relationship
            description (str):           description of the relationship
            schema (dict, optional):     definitation of the relationship's schema

        Returns:
            The newly created ``RelationshipType``

        Example::

            ds.create_relationship_type('belongs-to', 'this belongs to that')
        """
        r = RelationshipType(
            dataset_id=self.id,
            name=name,
            description=description,
            source=source,
            destination=destination,
            schema=schema,
            **kwargs
        )
        return self._api.concepts.relationships.create(self.id, r)

    def import_model(self, template):
        """
        Imports a model based on the given template into the dataset

        Args:
            template (ModelTemplate): the ModelTemplate to import

        Returns:
            A list of ModelProperty objects that have been imported into the dataset

        """
        return self._api.templates.apply(self, template)

    @property
    def _get_method(self):
        return self._api.datasets.get

    def as_dict(self):
        return dict(
            name=self.name,
            description=self.description,
            automaticallyProcessPackages=self.automatically_process_packages,
            properties=[p.as_dict() for p in self.properties],
            tags=self.tags,
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Collection(BaseCollection):
    def __init__(self, name, **kwargs):
        kwargs.pop("package_type", None)
        super(Collection, self).__init__(name, package_type="Collection", **kwargs)

    @property
    def _get_method(self):
        return self._api.packages.get

    @as_native_str()
    def __repr__(self):
        return u"<Collection name='{}' id='{}'>".format(self.name, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PublishInfo
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PublishInfo(BaseNode):
    def __init__(self, status, doi, dataset_id, version_count, last_published):
        self.status = status
        self.doi = doi

        self.dataset_id = dataset_id
        self.version_count = version_count
        self.last_published = last_published

    @classmethod
    def from_dict(cls, data):
        return cls(
            status=data.get("status"),
            doi=data.get("latest_doi"),
            dataset_id=data.get("publishedDatasetId"),
            version_count=data.get("publishedVersionCount"),
            last_published=data.get("lastPublishedDate"),
        )

    @as_native_str()
    def __repr__(self):
        return u"<PublishInfo status='{}' dataset_id='{}' version_count='{}' last_published='{}' doi='{}'>".format(
            self.status,
            self.dataset_id,
            self.version_count,
            self.last_published,
            self.doi,
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UserStubDTO
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class UserStubDTO(BaseNode):
    def __init__(self, node_id, first_name, last_name):
        self.node_id = node_id
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_dict(cls, data):
        return cls(
            node_id=data.get("nodeId"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
        )

    @as_native_str()
    def __repr__(self):
        return u"<User node_id='{}' first_name='{}' last_name='{}' >".format(
            self.node_id, self.first_name, self.last_name
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DatasetStatusStub
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DatasetStatusStub(BaseNode):
    def __init__(self, id, name, display_name):
        self.id = id
        self.name = name
        self.display_name = display_name

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            display_name=data.get("displayName"),
        )

    @as_native_str()
    def __repr__(self):
        return u"<DatasetStatus id='{}' name='{}' display_name='{}'>".format(
            self.id, self.name, self.display_name
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# StatusLogEntry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class StatusLogEntry(BaseNode):
    def __init__(self, user, status, updated_at):
        self.user = user
        self.status = status
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data):
        return cls(
            user=UserStubDTO.from_dict(data.get("user")),
            status=DatasetStatusStub.from_dict(data.get("status")),
            updated_at=parse(data.get("updatedAt")),
        )

    @as_native_str()
    def __repr__(self):
        return u"<StatusLogEntry user='{}' status='{}' updated_at='{}' >".format(
            self.user, self.status, self.updated_at
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# StatusLogResponse
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class StatusLogResponse(BaseNode):
    def __init__(self, limit, offset, total_count, entries):
        self.limit = limit
        self.offset = offset

        self.total_count = total_count
        self.entries = entries

    @classmethod
    def from_dict(cls, data):
        return cls(
            limit=data.get("limit"),
            offset=data.get("offset"),
            total_count=data.get("totalCount"),
            entries=[StatusLogEntry.from_dict(e) for e in data.get("entries")],
        )

    @as_native_str()
    def __repr__(self):
        return u"<StatusLogResponse limit='{}' offset='{}' total_count='{}' entries='{}' >".format(
            self.limit, self.offset, self.total_count, self.entries
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Collaborators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class UserCollaborator(BaseNode):
    def __init__(self, id, first_name, last_name, email, role):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            email=data["email"],
            role=data["role"],
        )

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @as_native_str()
    def __repr__(self):
        return u"<UserCollaborator name='{}' email='{}' role='{}' id='{}'>".format(
            self.name, self.email, self.role, self.id
        )


class TeamCollaborator(BaseNode):
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], name=data["name"], role=data["role"])

    @as_native_str()
    def __repr__(self):
        return u"<TeamCollaborator name='{}' role='{}' id='{}'>".format(
            self.name, self.role, self.id
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Models & Relationships
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model Helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Python 2
if PY2:
    python_to_blackfynn_type_map = {
        str: "string",
        unicode: "string",
        int: "long",
        long: "long",
        float: "double",
        bool: "boolean",
        datetime.date: "date",
        datetime.datetime: "date",
    }

    blackfynn_to_python_type_map = {
        "string": unicode,
        "long": int,
        "double": float,
        "boolean": bool,
        "date": datetime.datetime,
    }

# Python 3
else:
    python_to_blackfynn_type_map = {
        str: "string",
        int: "long",
        float: "double",
        bool: "boolean",
        datetime.date: "date",
        datetime.datetime: "date",
    }

    blackfynn_to_python_type_map = {
        "string": str,
        "long": int,
        "double": float,
        "boolean": bool,
        "date": datetime.datetime,
    }

valid_python_types = tuple(python_to_blackfynn_type_map.keys())


def target_type_string(target):
    if isinstance(target, Model):
        return target.type
    elif isinstance(target, str):
        return target
    else:
        raise Exception("target must be a string or model")


class ModelPropertyType(object):
    """
    Representation of model property types in the platform.
    """

    def __init__(self, data_type, format=None, unit=None):
        # Is this a supported literal Python type?
        if isinstance(data_type, type) and data_type in python_to_blackfynn_type_map:
            self.data_type = data_type

        # Otherwise this must be a string representation of a Blackfynn type
        elif (
            isinstance(data_type, string_types)
            and data_type.lower() in blackfynn_to_python_type_map
        ):
            self.data_type = blackfynn_to_python_type_map[data_type.lower()]

        else:
            raise Exception(
                "Cannot create ModelPropertyType with data_type={}".format(data_type)
            )

        self.format = format
        self.unit = unit

    @property
    def _blackfynn_type(self):
        return python_to_blackfynn_type_map[self.data_type]

    @staticmethod
    def _build_from(data):
        """
        Construct a ``ModelPropertyType`` from any data source. This is responsible
        for dispatching construction to subclasses for special cases such as
        enumerated and array types.
        """
        if isinstance(data, ModelPropertyType):
            return data

        elif isinstance(data, dict) and (
            data["type"].lower() == "array" or "items" in data
        ):
            return ModelPropertyEnumType.from_dict(data)

        return ModelPropertyType.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, dict):
            return cls(
                data_type=data["type"], format=data.get("format"), unit=data.get("unit")
            )

        # Single string
        return cls(data_type=data)

    def as_dict(self):
        if (self.format is None) and (self.unit is None):
            return self._blackfynn_type

        return dict(type=self._blackfynn_type, format=self.format, unit=self.unit)

    def _decode_value(self, value):
        """
        Decode a model value received from the Blackfynn API into the Python
        representation mandated by this `ModelPropertyType`.
        """
        if value is None:
            return None

        elif self.data_type == bool:
            if isinstance(value, bool):
                return value
            elif isinstance(value, str) or isinstance(value, unicode):
                if value.lower() == "false":
                    return False
                elif value.lower() == "true":
                    return True
                else:
                    return bool(value)
            else:
                return bool(value)

        elif self.data_type in (datetime.date, datetime.datetime):
            if isinstance(value, (datetime.date, datetime.datetime)):
                return value
            else:
                return dateutil.parser.parse(value)

        return self.data_type(value)

    def _encode_value(self, value):
        """
        Encode a Python value into something that can be sent to the Blackfynn API.
        """
        if value is None:
            return None

        elif isinstance(value, (datetime.date, datetime.datetime)):
            if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
                value = pytz.utc.localize(value)

            v = value.isoformat()

            # isoformat() does not include microseconds if microseconds is
            # 0, but we always need microseconds in the formatted string
            if not value.microsecond:
                v = "{}.000000{}".format(v[:-6], v[-6:])

            return v

        return self.data_type(value)

    @as_native_str()
    def __repr__(self):
        return u"<ModelPropertyType data_type='{}' format='{}' unit='{}'".format(
            self.data_type, self.format, self.unit
        )


class ModelPropertyEnumType(ModelPropertyType):
    """
    A special case of a ``ModelPropertyType`` that contains enumerated values
    and arrays of values.

    This can take one of several forms:

      * If ``enum`` is a list of objects, then the values of this property may
        only be one of the given values.
      * If ``multi_select`` is ``True``, then values of this property may be lists
        of objects.
      * If ``enum`` is a list of objects *and* ``multi_select`` is ``True``, then
        values of this property must be lists of items in ``enum``.
    """

    def __init__(
        self, data_type, format=None, unit=None, enum=None, multi_select=False
    ):
        super(ModelPropertyEnumType, self).__init__(data_type, format, unit)

        if enum is not None:
            enum = list(enum)
        self.enum = enum

        self.multi_select = multi_select
        self.selection_type = "array" if self.multi_select else "enum"

    def _decode_value(self, value):
        """
        Decode a model value received from the Blackfynn API into the Python
        representation mandated by this ``ModelPropertyType``.
        """
        if value is None:
            return None

        self._assert_value_in_enum(value)

        if self.multi_select:
            return [super(ModelPropertyEnumType, self)._decode_value(v) for v in value]

        return super(ModelPropertyEnumType, self)._decode_value(value)

    def _encode_value(self, value):
        """
        Encode a Python value into something that can be sent to the Blackfynn API.
        """
        if value is None:
            return None

        self._assert_value_in_enum(value)

        if self.multi_select:
            return [super(ModelPropertyEnumType, self)._encode_value(v) for v in value]

        return super(ModelPropertyEnumType, self)._encode_value(value)

    def _assert_value_in_enum(self, value):
        """Check that values are in the enumerated type."""
        if self.enum and self.multi_select:
            for v in value:
                if v not in self.enum:
                    raise Exception(
                        "Value '{}' is not a member of {}".format(v, self.enum)
                    )

        elif self.enum and value not in self.enum:
            raise Exception("Value '{}' is not a member of {}".format(value, self.enum))

    @classmethod
    def from_dict(cls, data):
        selection_type = data["type"].lower()
        multi_select = selection_type == "array"
        data_type = data["items"].get("type")
        format = data["items"].get("format")
        unit = data["items"].get("unit")
        enum = data["items"].get("enum")

        return cls(
            data_type=data_type,
            format=format,
            unit=unit,
            enum=enum,
            multi_select=multi_select,
        )

    def as_dict(self):
        return dict(
            type=self.selection_type,
            items=dict(
                type=self._blackfynn_type,
                format=self.format,
                unit=self.unit,
                enum=self.enum,
            ),
        )

    @as_native_str()
    def __repr__(self):
        return u"<ModelPropertyEnumType data_type='{}' format='{}' unit='{}' enum='{}'".format(
            self.data_type, self.format, self.unit, self.enum
        )


class BaseModelProperty(object):
    """
    Fallback values for property fields are resolved as follows:

    (1) A property is `required` if it is the title of the model

    (2) A property is `default` if it is `required`. `default` is deprecated and
    `required` is now the source of truth.

    (3) If the `display_name` for a property is not provided use `name` instead

    The default values of both `required` and `default` can be on be overridden
    by passing in explicit
    """

    def __init__(
        self,
        name,
        display_name=None,
        data_type=str,
        id=None,
        locked=False,
        default=None,
        title=False,
        description="",
        required=None,
    ):
        assert (
            " " not in name
        ), "name cannot contain spaces, alternative names include {} and {}".format(
            name.replace(" ", "_"), name.replace(" ", "-")
        )

        if required is None:
            required = title

        if default is None:
            default = required

        if display_name is None:
            display_name = name

        self.id = id
        self.name = name
        self.display_name = display_name
        self.type = data_type  # passed through @type.setter
        self.locked = locked
        self.default = default
        self.title = title
        self.description = description
        self.required = required

    @classmethod
    def from_tuple(cls, data):
        name = data[0]
        data_type = data[1]

        try:
            display_name = data[2]
        except:
            display_name = name

        try:
            title = data[3]
        except:
            title = False

        try:
            required = data[4]
        except:
            required = False

        return cls(
            name=name,
            display_name=display_name,
            data_type=data_type,
            title=title,
            required=required,
        )

    @classmethod
    def from_dict(cls, data):
        display_name = data.get("displayName", data.get("display_name"))
        data_type = data.get("data_type", data.get("dataType"))
        locked = data.get("locked", False)
        default = data.get("default")
        title = data.get("title", data.get("conceptTitle", False))
        id = data.get("id", None)
        required = data.get("required")
        description = data.get("description", "")

        return cls(
            name=data["name"],
            display_name=display_name,
            data_type=data_type,
            id=id,
            locked=locked,
            default=default,
            title=title,
            required=required,
            description=description,
        )

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            displayName=self.display_name,
            dataType=self._type.as_dict(),
            locked=self.locked,
            default=self.default,
            conceptTitle=self.title,
            description=self.description,
            required=self.required,
        )

    def as_tuple(self):
        return (self.name, self.type, self.display_name, self.title, self.required)

    @property
    def type(self):
        return self._type.data_type

    @type.setter
    def type(self, type):
        self._type = ModelPropertyType._build_from(type)

    @property
    def unit(self):
        return self._type.unit

    @property
    def format(self):
        return self._type.format

    @property
    def enum(self):
        return self._type.enum

    @property
    def multi_select(self):
        return self._type.multi_select

    @as_native_str()
    def __repr__(self):
        return u"<BaseModelProperty name='{}' {}>".format(self.name, self.type)


class LinkedModelProperty(BaseNode):
    def __init__(self, name, target, display_name=None, id=None, position=None):
        assert (
            " " not in name
        ), "name cannot contain spaces, alternative names include {} and {}".format(
            name.replace(" ", "_"), name.replace(" ", "-")
        )
        self._object_key = ""
        self.name = name
        self.id = id
        self.position = position

        if display_name is None:
            self.display_name = name
        else:
            self.display_name = display_name

        if isinstance(target, Model):
            self.target = target.id
        elif isinstance(target, string_types):
            self.target = target
        else:
            raise Exception("'target' must be an id or a Model object")

    def as_dict(self):
        dct = {"name": self.name, "displayName": self.display_name, "to": self.target}
        if self.position is not None:
            dct["position"] = self.position
        return dct

    @classmethod
    def from_dict(cls, data):
        if "link" in data:
            # data came from a GET request
            link = data["link"]
        else:
            # data came from a POST or PUT
            link = data
        name = link["name"]
        display_name = link.get("displayName", link.get("display_name", name))
        target = link["to"]
        id = link.get("id")
        position = link.get("position")
        return cls(
            name=name,
            target=target,
            display_name=display_name,
            id=id,
            position=position,
        )

    @as_native_str()
    def __repr__(self):
        return "<LinkedModelProperty name='{}' id='{}'>".format(self.name, self.id)


class BaseModelValue(object):
    def __init__(self, name, value, data_type=None):
        assert (
            " " not in name
        ), "name cannot contain spaces, alternative names include {} and {}".format(
            name.replace(" ", "_"), name.replace(" ", "-")
        )

        self.name = name
        self.data_type = ModelPropertyType._build_from(data_type)
        self.value = value  # Decoded in @value.setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.data_type._decode_value(value)

    @property
    def type(self):
        return self.data_type.data_type

    @classmethod
    def from_tuple(cls, data):
        return cls(name=data[0], value=value[1])

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            value=data["value"],
            data_type=data.get("data_type", data.get("dataType")),
        )

    def as_dict(self):
        return dict(
            name=self.name,
            value=self.data_type._encode_value(self.value),
            dataType=self.data_type._blackfynn_type,
        )

    def as_tuple(self):
        return (self.name, self.value)

    @as_native_str()
    def __repr__(self):
        return u"<BaseModelValue name='{}' value='{}' {}>".format(
            self.name, self.value, self.type
        )


class LinkedModelValue(BaseNode):
    def __init__(
        self,
        source_model,
        target_model,
        source_record,
        target_record,
        link_type,
        id=None,
    ):
        self.source_model = source_model
        self.target_model = target_model
        self.source_record_id = source_record
        self.target_record_id = target_record
        self.type = link_type
        self.id = id

    @classmethod
    def from_dict(cls, data, source_model, target_model, link_type):
        return cls(
            source_model=source_model,
            target_model=target_model,
            source_record=data["from"],
            target_record=data["to"],
            link_type=link_type,
            id=data["id"],
        )

    def as_dict(self):
        return dict(schemaLinkedPropertyId=self.type.id, to=self.target_record_id)

    @property
    def source_record(self):
        return self.source_model.get(self.source_record_id)

    @property
    def target_record(self):
        return self.target_model.get(self.target_record_id)
        return self.model.get(self.target_id)

    @as_native_str()
    def __repr__(self):
        return "<LinkedModelValue type={} id={}>".format(self.type, self.id)


class BaseModelNode(BaseNode):
    _object_key = ""
    _property_cls = BaseModelProperty

    def __init__(
        self,
        dataset_id,
        name,
        display_name=None,
        description=None,
        locked=False,
        default=True,
        *args,
        **kwargs
    ):
        assert (
            " " not in name
        ), "type cannot contain spaces, alternative types include {} and {}".format(
            name.replace(" ", "_"), name.replace(" ", "-")
        )

        self.type = name
        self.dataset_id = dataset_id
        self.display_name = display_name or name
        self.description = description or ""
        self.locked = locked
        self.created_at = kwargs.pop("createdAt", None)
        self.updated_at = kwargs.pop("updatedAt", None)
        schema = kwargs.pop("schema", None)
        self.linked = kwargs.pop("linked", {})

        super(BaseModelNode, self).__init__(*args, **kwargs)

        self.schema = dict()
        if schema is None:
            return

        self._add_properties(schema)

    def _add_property(
        self, name, display_name=None, data_type=str, title=False, description=""
    ):
        prop = self._property_cls(
            name=name,
            display_name=display_name,
            data_type=data_type,
            title=title,
            description=description,
        )
        self.schema[prop.name] = prop
        return prop

    def _add_properties(self, properties):
        if isinstance(properties, list):
            for p in properties:
                if isinstance(p, dict):
                    prop = self._property_cls.from_dict(p)
                elif isinstance(p, tuple):
                    prop = self._property_cls.from_tuple(p)
                elif isinstance(p, string_types):
                    prop = self._property_cls(name=p)
                elif isinstance(p, self._property_cls):
                    prop = p
                else:
                    raise Exception("unsupported property value: {}".format(type(p)))

                self.schema[prop.name] = prop
        elif isinstance(properties, dict):
            for k, v in properties.items():
                self._add_property(name=k, data_type=v)
        else:
            raise Exception(
                "invalid type {}; properties must either be a dict or list".format(
                    type(properties)
                )
            )

    def _validate_values_against_schema(self, values):
        data_keys = set(values.keys())
        schema_keys = set(self.schema.keys())

        assert (
            data_keys <= schema_keys
        ), "Invalid properties: {}.\n\nAn instance of {} should only include values for properties defined in its schema: {}".format(
            data_keys - schema_keys, self.type, schema_keys
        )

    # should be overridden by sub-class
    def update(self):
        pass

    def add_property(
        self, name, data_type=str, display_name=None, title=False, description=""
    ):
        """
        Appends a property to the object's schema and updates the object on the platform.

        Args:
          name (str): Name of the property
          data_type (type, optional): Python type of the property. Defaults to ``string_types``.
          display_name (str, optional): Display name for the property.
          title (bool, optional): If True, the property will be used in the title on the platform
          description (str, optional): Description of the property

        Example:
          Adding a new property with the default data_type::
            mouse.add_property('name')

          Adding a new property with the ``float`` data_type::
            mouse.add_property('weight', float)
        """
        prop = self._add_property(
            name,
            data_type=data_type,
            display_name=display_name,
            title=title,
            description=description,
        )
        self.update()
        return prop

    def add_properties(self, properties):
        """
        Appends multiple properties to the object's schema and updates the object
        on the platform.

        Args:
          properties (list): List of properties to add

        Note:
            At least one property on a model needs to serve as the model's title.
            See ``title`` argument in example(s) below.

        Example:

            Add properties using ``ModelProperty`` objects::

                model.add_properties([
                    ModelProperty('name', data_type=str, title=True),
                    ModelProperty('age',  data_type=int)
                ])

            Add properties defined as list of dictionaries::

                model.add_properties([
                        {
                            'name': 'full_name',
                            'type': str,
                            'title': True
                        },
                        {
                            'name': 'age',
                            'type': int,
                        }
                ])
        """
        self._add_properties(properties)
        self.update()

    def add_linked_property(self, name, target_model, display_name=None):
        """
        Add a linked property to the model.

        Args:
          name (str): Name of the property
          target_model (Model): Model that the property will link to
          display_name (str, optional): Display name of the property
        """
        payload = LinkedModelProperty(
            name, target=target_model, display_name=display_name
        )
        prop = self._api.concepts.create_linked_property(self.dataset_id, self, payload)
        self.linked[prop.name] = prop
        return prop

    def add_linked_properties(self, properties):
        """
        Add multiple linked properties to the model.

        Args:
          properties (list): List of LinkedModelProperty objects
        """
        props = self._api.concepts.create_linked_properties(
            self.dataset_id, self, properties
        )
        for prop in props:
            self.linked[prop.name] = prop
        return props

    def remove_property(self, property):
        """
        Remove property from model schema.

        Args:
            property (string, ModelProperty): Property to remove. Can be property name, id, or object.

        """

        # verify property in schema
        prop_name = None
        if isinstance(property, string_types):
            # assume property name first, then assume ID
            if property in self.schema:
                # property is name
                prop_name = property
            else:
                # property may be id
                ids = [x.id for x in self.schema.values()]
                if property in ids:
                    prop_name = self.schema.value()[ids.index(property)].name

        elif isinstance(property, ModelProperty):
            prop_name = property.name

        else:
            raise Exception(
                "Expected 'property' argument of type string or ModelProperty, found type {}".format(
                    type(property)
                )
            )

        if prop_name is None:
            raise Exception(
                "Property '{}' not found in model's schema.".format(property)
            )

        prop_id = self.schema.get(prop_name).id

        self._api.concepts.delete_property(self.dataset_id, self, prop_id)
        self.schema.pop(prop_name)

    def remove_linked_property(self, prop):
        """
        Delete the linked property with the given name or id.
        """
        # verify linked property is in schema
        if isinstance(prop, string_types):
            # assume property name or ID
            for p in self.linked.values():
                if prop == p.id or prop == p.name:
                    prop_id = p.id
                    prop_name = p.name
                    break
            else:
                raise Exception(
                    "Property '{}' not found in model's schema.".format(property)
                )

        elif isinstance(prop, ModelProperty):
            prop_name = prop.name
            prop_id = prop.id
        else:
            raise Exception(
                "Expected a LinkedModelProperty, found type {}".format(type(property))
            )

        self._api.concepts.delete_linked_property(self.dataset_id, self, prop_id)
        self.linked.pop(prop_name)

    def get_property(self, name):
        """
        Gets the property object by name.

        Example:
            >>> mouse.get_propery('weight').type
            float
        """
        return self.schema.get(name, None)

    def get_linked_properties(self):
        """
        Get all linked properties attached to this Model.
        """
        return self._api.concepts.get_linked_properties(self.dataset_id, self)

    def get_linked_property(self, name):
        """
        Get a linked property by name or id.
        """
        for k, v in self.get_linked_properties().items():
            if k == name or v.id == name:
                return v
        raise Exception("No linked property found with name or id '{}'".format(name))

    def as_dict(self):
        return dict(
            name=self.type,
            displayName=self.display_name,
            description=self.description,
            locked=self.locked,
            schema=[p.as_dict() for p in self.schema.values()],
        )


class BaseRecord(BaseNode):
    _object_key = ""
    _value_cls = BaseModelValue

    def __init__(self, dataset_id, type, *args, **kwargs):

        self.type = type
        self.dataset_id = dataset_id
        self.created_at = kwargs.pop("createdAt", None)
        self.created_by = kwargs.pop("createdBy", None)
        self.updated_at = kwargs.pop("updatedAt", None)
        self.updated_by = kwargs.pop("updatedBy", None)
        values = kwargs.pop("values", None)

        super(BaseRecord, self).__init__(*args, **kwargs)

        self._values = dict()
        if values is None:
            return

        self._set_values(values)

    def _set_value(self, name, value):
        if name in self._values:
            v = self._values[name]
            v.value = value
        else:
            v = self._value_cls(name=name, value=value)
            self._values[v.name] = v

    def _set_values(self, values):
        if isinstance(values, list):
            for v in values:
                if isinstance(v, dict):
                    value = self._value_cls.from_dict(v)
                elif isinstance(v, tuple):
                    value = self._value_cls.from_tuple(v)
                elif isinstance(v, self._value_cls):
                    value = v
                else:
                    raise Exception("unsupported value: {}".format(type(v)))

                self._values[value.name] = value
        elif isinstance(values, dict):
            for k, v in values.items():
                self._set_value(name=k, value=v)
        else:
            raise Exception(
                "invalid type {}; values must either be a dict or list".format(
                    type(values)
                )
            )

    @property
    def values(self):
        return {v.name: v.value for v in self._values.values()}

    # should be overridden by sub-class
    def update(self):
        pass

    def get(self, name):
        """
        Returns:
            The value of the property if it exists. None otherwise.
        """
        value = self._values.get(name, None)
        return value.value if value is not None else None

    def set(self, name, value):
        """
        Updates the value of an existing property or creates a new property
        if one with the given name does not exist.

        Note:
            Updates the object on the platform.
        """
        self._set_value(name, value)

        try:
            self.update()
        except:
            raise Exception("local object updated, but failed to update remotely")

    def as_dict(self):
        return {"values": [v.as_dict() for v in self._values.values()]}

    @as_native_str()
    def __repr__(self):
        return u"<BaseRecord type='{}' id='{}'>".format(self.type, self.id)


class ModelTemplate(BaseNode):
    _object_key = None

    def __init__(
        self,
        name,
        properties,
        category=None,
        id=None,
        display_name=None,
        schema=None,
        description=None,
        required=None,
        *args,
        **kwargs
    ):
        assert name is not None, "ModelTemplate name must be defined"
        assert properties is not None, "ModelTemplate properties must be defined"

        self.id = id
        self.schema = schema or "http://schema.blackfynn.io/model/draft-01/schema"
        self.name = name
        self.display_name = display_name
        self.description = description or name
        self.category = category
        self.required = required or []

        if isinstance(properties, list) and isinstance(properties[0], tuple):
            self.properties = ModelTemplate.properties_from_tuples(properties)
        else:
            self.properties = properties

        super(ModelTemplate, self).__init__(*args, **kwargs)

    @classmethod
    def properties_from_tuples(cls, tuples):
        d = dict()
        nested = dict()
        for tuple in tuples:
            name = "{}".format(tuple[0])
            data_type = tuple[1]
            nested["type"] = data_type
            nested["description"] = name
            d[name] = nested
        return d

    def as_dict(self):
        return {
            "$schema": self.schema,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "properties": self.properties,
            "required": self.required,
        }

    @classmethod
    def from_dict(cls, data, *args, **kwargs):

        template = cls(
            schema=data["$schema"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            required=data["required"],
            properties=data["properties"],
            display_name=data.get("displayName", None),
        )

        template.id = data.get("$id", None)

        return template

    @as_native_str()
    def __repr__(self):
        return u"<ModelTemplate name='{}' id='{}'>".format(self.name, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelProperty(BaseModelProperty):
    @as_native_str()
    def __repr__(self):
        return u"<ModelProperty name='{}' {}>".format(self.name, self.type)


class ModelValue(BaseModelValue):
    @as_native_str()
    def __repr__(self):
        return u"<ModelValue name='{}' value='{}' {}>".format(
            self.name, self.value, self.type
        )


class ModelSelect(object):
    def __init__(self, *join_keys):
        self.join_keys = [target_type_string(k) for k in join_keys]

    def as_dict(self):
        return {"Concepts": {"joinKeys": self.join_keys}}

    @as_native_str()
    def __repr__(self):
        join_keys = [target_type_string(k) for k in self.join_keys]
        return u"<ModelSelect join_keys='{}'>".format(",".join(join_keys))


class ModelFilter(object):
    def __init__(self, key, operator, value):
        self.key = key
        self.operator = operator
        self.value = value

    def as_dict(self):
        return {
            "key": self.key,
            "predicate": {"operation": self.operator, "value": self.value},
        }

    @as_native_str()
    def __repr__(self):
        return u"<ModelFilter key='{}' operator='{}' value='{}'>".format(
            self.key, self.operator, self.value
        )


class ModelJoin(object):
    def __init__(self, target, *filters):
        self.target = target
        self.filters = [
            ModelFilter(*f) if not isinstance(f, ModelFilter) else f for f in filters
        ]

    def as_dict(self):
        key = target_type_string(self.target)
        return {
            "targetType": {"concept": {"type": key}},
            "filters": [f.as_dict() for f in self.filters],
            "key": key,
        }

    @as_native_str()
    def __repr__(self):
        return u"<ModelJoin targetType='{}' filter='{}', key='{}'>".format(
            target_type_string(self.target), self.filters, self.key
        )


class Model(BaseModelNode):
    """
    Representation of a Model in the knowledge graph.
    """

    _object_key = ""
    _property_cls = ModelProperty

    def __init__(
        self,
        dataset_id,
        name,
        display_name=None,
        description=None,
        locked=False,
        *args,
        **kwargs
    ):
        self.count = kwargs.pop("count", None)
        self.state = kwargs.pop("state", None)

        self._logger = log.get_logger("blackfynn.models.Model")

        super(Model, self).__init__(
            dataset_id, name, display_name, description, locked, *args, **kwargs
        )

    def update(self):
        """
        Updates the details of the ``Model`` on the platform.

        Example::

          mouse.update()

        Note:
            Currently, you can only append new properties to a ``Model``.
        """
        self._check_exists()

        _update_self(self, self._api.concepts.update(self.dataset_id, self))

    def delete(self):
        """
        Deletes a model from the platform. Must not have any instances.
        """
        return self._api.concepts.delete(self.dataset_id, self)

    def get_all(self, limit=100, offset=0):
        """
        Retrieves all records of the model from the platform.

        Returns:
            List of ``Record``

        Example::

          mice = mouse.get_all()
        """
        return self._api.concepts.instances.get_all(
            self.dataset_id, self, limit=limit, offset=offset
        )

    def get(self, id):
        """
        Retrieves a record of the model by id from the platform.

        Args:
            id: the Blackfynn id of the model

        Returns:
            A single ``Record``

        Example::

          mouse_001 = mouse.get(123456789)
        """
        return self._api.concepts.instances.get(self.dataset_id, id, self)

    def query(self):
        """
        Run a query with this model as the join target.
        """
        return self._api.concepts.query.new(self, self.dataset_id)

    def get_connected(self):
        """Retrieves all connected models

            Connected is defined as model that can be reached by following
            outgoing relationships starting at the current model

        Args:
            id: The Blackfynn id of the "root" model

        Returns:
            A list of models connected to the given model

        Example::

            connected_models = mouse.get_connected()
        """
        return self._api.concepts.get_connected(self.dataset_id, self.id)

    def create_record(self, values=dict()):
        """
        Creates a record of the model on the platform.

        Args:
            values (dict, optional): values for properties defined in the `Model` schema

        Returns:
            The newly created ``Record``

        Example::

          mouse_002 = mouse.create_record({"id": 2, "weight": 2.2})

        """
        self._check_exists()

        data_keys = set(values.keys())
        schema_keys = set(self.schema.keys())
        assert (
            len(data_keys & schema_keys) > 0
        ), "An instance of {} must include values for at least one of its properties: {}".format(
            self.type, schema_keys
        )

        self._validate_values_against_schema(values)

        values = [
            dict(name=k, value=v, dataType=self.schema.get(k)._type)
            for k, v in values.items()
        ]
        ci = Record(dataset_id=self.dataset_id, type=self.type, values=values)
        ci = self._api.concepts.instances.create(self.dataset_id, ci)
        return ci

    def create_records(self, values_list):
        """
        Creates multiple records of the model on the platform.

        Args:
            values_list (list): array of dictionaries corresponding to record values.

        Returns:
            List of newly created ``Record`` objects.

        Example::

            mouse.create_records([
                { 'id': 311, 'weight': 1.9 },
                { 'id': 312, 'weight': 2.1 },
                { 'id': 313, 'weight': 1.8 },
                { 'id': 314, 'weight': 2.3 },
                { 'id': 315, 'weight': 2.0 }
            ])

        """
        self._check_exists()
        schema_keys = set(self.schema.keys())

        for values in values_list:
            data_keys = set(values.keys())
            assert (
                len(data_keys & schema_keys) > 0
            ), "An instance of {} must include values for at least one of its propertes: {}".format(
                self.type, schema_keys
            )
            self._validate_values_against_schema(values)

        ci_list = [
            Record(
                dataset_id=self.dataset_id,
                type=self.type,
                values=[
                    dict(name=k, value=v, dataType=self.schema.get(k)._type)
                    for k, v in values.items()
                ],
            )
            for values in values_list
        ]
        return self._api.concepts.instances.create_many(self.dataset_id, self, *ci_list)

    def from_dataframe(self, df):
        return self.create_many(*df.to_dict(orient="records"))

    def delete_records(self, *records):
        """
        Deletes one or more records of a concept from the platform.

        Args:
            *records: instances and/or ids of records to delete

        Returns:
            ``None``

        Logs the list of records that failed to delete.

        Example::

            mouse.delete(mouse_002, 123456789, mouse_003.id)

        """
        result = self._api.concepts.delete_instances(self.dataset_id, self, *records)

        for error in result["errors"]:
            self._logger.error(
                "Failed to delete instance {} with error: {}".format(error[0], error[1])
            )

    def get_related(self):
        """
        Returns a list of related model types and counts of those
        relationships.

        "Related" indicates that the model could be connected to the current
        model via some relationship, i.e.  ``B`` is "related to" ``A`` if there
        exist ``A -[relationship]-> B``. Note that the directionality
        matters. If ``B`` is the queried model, ``A`` would not appear in the
        list of "related" models.

        Returns:
            List of ``Model`` objects related via a defined relationship

        Example::

            related_models = mouse.get_related()

        """
        return self._api.concepts.get_related(self.dataset_id, self)

    def __iter__(self):
        for record in self.get_all():
            yield record

    @as_native_str()
    def __repr__(self):
        return u"<Model type='{}' id='{}'>".format(self.type, self.id)


class Record(BaseRecord):
    """
    Represents a record of a ``Model``.

    Includes its neighbors, relationships, and links.
    """

    _object_key = ""
    _value_cls = ModelValue

    def _get_relationship_type(self, relationship):
        return (
            relationship.type
            if isinstance(relationship, RelationshipType)
            else relationship
        )

    def _get_links(self, model):
        return self._api.concepts.instances.relations(self.dataset_id, self, model)

    def get_related(self, model=None, group=False):
        """
        Returns all related records.

        Args:
            model (str, Model, optional):         Return only related records of this type
            group (bool, optional):               If true, group results by model type (dict)

        Returns:
            List of ``Record`` objects. If ``group`` is ``True``, then the result
            is a dictionary of ``RecordSet`` objects keyed by model names.

        Example:
            Get all connected records of type ``disease`` with relationship ``has``::

                mouse_001.get_related('disease', 'has')

            Get all connected records::

                mouse_001.get_related()
        """
        if model is None:
            # return all connected records
            related_by_model = self._api.concepts.instances.get_all_related(
                self.dataset_id, self
            )
            if group:
                return related_by_model
            else:
                if len(related_by_model) == 1:
                    # try to retain RecordSet type
                    return list(related_by_model.values())[0]
                # mixed return types, cannot keep RecordSets
                related = []
                for model_name, model_related in related_by_model.items():
                    related.extend(model_related)
                return related
        else:
            return self._api.concepts.instances.get_all_related_of_type(
                self.dataset_id, self, model
            )

    def get_files(self):
        """
        All files related to the current record.

        Returns:
            List of data objects i.e. ``DataPackage``

        Example::
            mouse_001.get_files()

        """
        return self._api.concepts.files(self.dataset_id, self.type, self)

    def relate_to(
        self, destinations, relationship_type="related_to", values=None, direction="to"
    ):
        """
        Relate record to one or more ``Record`` or ``DataPackage`` objects.

        Args:
            destinations (list of Record or DataPackage):
                A list containing the ``Record`` or ``DataPackage`` objects to relate to current record
            relationship_type (RelationshipType, str, optional):
                Type of relationship to create
            values (list of dictionaries, optional):
                A list of dictionaries corresponding to relationship values
            direction (str, optional):
                Relationship direction. Valid values are ``'to'`` and ``'from'``

        Returns:
            List of created ``Relationship`` objects.

        .. note::

            Destinations must all be of type ``DataPackage`` or ``Record``; you cannot mix destination types.

        Example:
            Relate to a single ``Record``, define relationship type::

                mouse_001.relate_to(lab_009, 'located_at')

            Relate to multiple ``DataPackage`` objects::

                mouse_001.relate_to([eeg, mri1, mri2])
        """
        self._check_exists()

        # accept object or list
        if isinstance(destinations, (Record, DataPackage)):
            destinations = [destinations]
        if isinstance(destinations, Collection):
            destinations = destinations.items

        if not destinations:
            return None

        # default values
        if values is None:
            values = [dict() for _ in destinations] if values is None else values
        else:
            values = [dict(name=k, value=v) for val in values for k, v in val.items()]

        assert len(destinations) == len(
            values
        ), "Length of values must match length of destinations"

        # check type
        if not (
            all([isinstance(d, DataPackage) for d in destinations])
            or all([isinstance(d, Record) for d in destinations])
        ):
            raise Exception(
                "All destinations must be of object type Record or DataPackage"
            )

        # auto-create relationship type
        if isinstance(relationship_type, string_types):
            relationships_types = self._api.concepts.relationships.get_all(
                self.dataset_id
            )
            if relationship_type not in relationships_types:
                r = RelationshipType(
                    dataset_id=self.dataset_id,
                    name=relationship_type,
                    description=relationship_type,
                    source=self.model.id,
                    destination=destinations[0].model.id,
                )
                relationship_type = self._api.concepts.relationships.create(
                    self.dataset_id, r
                )
            else:
                relationship_type = relationships_types[relationship_type]

        # relationships (to packages)
        if isinstance(destinations[0], DataPackage):
            # if linking packages, link one at a time
            result = [
                self._api.concepts.relationships.instances.link(
                    self.dataset_id, relationship_type, self, d, values=v
                )
                for d, v in zip(destinations, values)
            ]
            return RelationshipSet(relationship_type, result)

        # relationships (to records)
        if direction == "to":
            relationships = [
                Relationship(
                    type=relationship_type.type,
                    dataset_id=self.dataset_id,
                    source=self,
                    destination=d.id,
                    values=v,
                )
                for d, v in zip(destinations, values)
            ]
        elif direction == "from":
            relationships = [
                Relationship(
                    type=relationship_type.type,
                    dataset_id=self.dataset_id,
                    source=d.id,
                    destination=self,
                    values=v,
                )
                for d, v in zip(destinations, values)
            ]
        else:
            raise Exception('Direction must be value "to" or "from"')

        # use batch endpoint to create relationships
        return self._api.concepts.relationships.instances.create_many(
            self.dataset_id, relationship_type, *relationships
        )

    def get_linked_values(self):
        """
        Get all link values attached to this Record.
        """
        return self._api.concepts.instances.get_linked_values(
            self.dataset_id, self.model, self
        )

    def get_linked_value(self, link):
        """
        Get a link value by name or id.
        """
        all_links = self.get_linked_values()

        # First assume link is a link value id:
        for l in all_links:
            if link == l.id:
                return l

        # Then assume link is a linked property name:
        try:
            prop_id = self.model.get_linked_property(link).id
        except:
            raise Exception(
                "No link found with a name or ID matching '{}'".format(link)
            )
        else:
            for l in all_links:
                if prop_id == l.type.id:
                    return l
        raise Exception("No link found with a name or ID matching '{}'".format(link))

    def add_linked_value(self, target, link):
        """
        Attach a linked property value to the Record.
        target: the id or Record object of the target record
        link: the id or LinkedModelProperty object of the link type
        """
        model = self.model

        if isinstance(target, Record):
            target = target.id

        if isinstance(link, LinkedModelProperty):
            link_id = link.id
        elif isinstance(link, string_types):
            link_id = model.get_linked_property(link).id

        payload = dict(
            name=model.type,
            displayName=model.display_name,
            schemaLinkedPropertyId=link_id,
            to=target,
        )
        return self._api.concepts.instances.create_link(
            self.dataset_id, self.model, self, payload
        )

    def delete_linked_value(self, link_name):
        """
        Delete a link by name or id.
        """
        link = self.get_linked_value(link_name)
        self._api.concepts.instances.remove_link(
            self.dataset_id, self.model, self, link
        )

    @property
    def model(self):
        """
        The ``Model`` of the current record.

        Returns:
           A single ``Model``.
        """
        return self._api.concepts.get(self.dataset_id, self.type)

    def update(self):
        """
        Updates the values of the record on the platform (after modification).

        Example::

          mouse_001.set('name', 'Mickey')
          mouse_001.update()
        """
        self._check_exists()

        _update_self(self, self._api.concepts.instances.update(self.dataset_id, self))

    def delete(self):
        """
        Deletes the instance from the platform.

        Example::

          mouse_001.delete()
        """
        return self._api.concepts.instances.delete(self.dataset_id, self)

    @as_native_str()
    def __repr__(self):
        return u"<Record type='{}' id='{}'>".format(self.type, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Query Result
#
#   Returned per "row" result of a query
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class QueryResult(object):
    def __init__(self, dataset_id, target, joined):
        self.dataset_id = dataset_id
        self._target = target
        self._joined = joined

    @property
    def target(self):
        """
        Get the target of the query.

        Returns:
            the target of the query.

        Example::

            For the following query,

                Review.query() \
                    .filter("is_complete", "eq", False) \
                    .join("reviewer", ("id", "eq", "12345")) \
                    .select(reviewer")
                    .run()

            a record whose type is `review` would be the target.
        """
        return self._target

    def get(self, model):
        """
        Get the result for a specific join key appearing in a `select()`.

        Args:

            model: (string|Model) The type of the record to retrieve from this
                query result.

        Returns:
            the record whose type matches the given model, or None if no such
            record exists.

        Example::

            For the following query,

                result = Review.query() \
                    .filter("is_complete", "eq", False) \
                    .join("reviewer", ("id", "eq", "12345")) \
                    .select(reviewer")
                    .run()

                reviewer_record = result.get("reviewer") # Also equivalent to `result.get(Reviewer)`
        """
        return self._joined.get(target_type_string(model), None)

    def items(self):
        """
        Gets all (model:string, record:Record) instances contained in this
        query result.

        Returns:
            A list of (model:string, record:Record) pairs contained in this
            query result.
        """
        return self._joined.items()

    def __getitem__(self, model):
        return self.get(model)

    def __contains__(self, model):
        return target_type_string(model) in self._joined

    def as_dict(self):
        d = {t: record.as_dict() for (t, record) in self._joined.items()}
        d["targetValue"] = self.target.as_dict()
        return d

    @as_native_str()
    def __repr__(self):
        return u"<QueryResult dataset='{}' target='{}'>".format(
            self.dataset_id, self._target.id
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Relationships
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class RelationshipProperty(BaseModelProperty):
    @as_native_str()
    def __repr__(self):
        return u"<RelationshipProperty name='{}' {}>".format(self.name, self.type)


class RelationshipValue(BaseModelValue):
    @as_native_str()
    def __repr__(self):
        return u"<RelationshipValue name='{}' value='{}' {}>".format(
            self.name, self.value, self.type
        )


class RelationshipType(BaseModelNode):
    """
    Model for defining a relationships.
    """

    _object_key = ""
    _property_cls = RelationshipProperty

    def __init__(
        self,
        dataset_id,
        name,
        display_name=None,
        description=None,
        locked=False,
        source=None,
        destination=None,
        *args,
        **kwargs
    ):
        kwargs.pop("type", None)
        self.destination = destination
        self.source = source
        super(RelationshipType, self).__init__(
            dataset_id, name, display_name, description, locked, *args, **kwargs
        )

    def update(self):
        raise Exception("Updating Relationships is not available at this time.")
        # TODO: _update_self(self, self._api.concepts.relationships.update(self.dataset_id, self))

    # TODO: delete when update is supported, handled in super-class
    def add_property(self, name, display_name=None, data_type=str):
        raise Exception("Updating Relationships is not available at this time.")

    # TODO: delete when update is supported, handled in super-class
    def add_properties(self, properties):
        raise Exception("Updating Relationships is not available at this time.")

    def delete(self):
        raise Exception("Deleting Relationships is not available at this time.")
        # TODO: self._api.concepts.relationships.delete(self.dataset_id, self)

    def get_all(self):
        """
        Retrieves all relationships of this type from the platform.

        Returns:
            List of ``Relationship``

        Example::

            belongs_to_relationships = belongs_to.get_all()
        """
        return self._api.concepts.relationships.instances.get_all(self.dataset_id, self)

    def get(self, id):
        """
        Retrieves a relationship by id from the platform.

        Args:
            id (int): the id of the instance

        Returns:
            A single ``Relationship``

        Example::

            mouse_001 = mouse.get(123456789)
        """
        return self._api.concepts.relationships.instances.get(self.dataset_id, id, self)

    def relate(self, source, destination, values=dict()):
        """
        Relates a ``Record`` to another ``Record`` or ``DataPackage`` using current relationship.

        Args:
            source (Record, DataPackage):      record or data package the relationship orginates from
            destination (Record, DataPackage): record or data package the relationship points to
            values (dict, optional):           values for properties defined in the relationship's schema

        Returns:
            The newly created ``Relationship``

        Example:
            Create a relationship between a ``Record`` and a ``DataPackage``::

                from_relationship.relate(mouse_001, eeg)

            Create a relationship (with values) between a ``Record`` and a ``DataPackage``::

                from_relationship.relate(mouse_001, eeg, {"date": datetime.datetime(1991, 02, 26, 07, 0)})
        """
        self._check_exists()
        self._validate_values_against_schema(values)
        return self._api.concepts.relationships.instances.link(
            self.dataset_id, self, source, destination, values
        )

    def create(self, items):
        """
        Create multiple relationships between records using current relationship type.

        Args:
            items (list): List of relationships to be created.
                Each relationship should be either a dictionary or tuple.

                If relationships are dictionaries, they are required to have
                ``from``/``to`` or ``source``/``destination`` keys.
                There is an optional ``values`` key which can be used
                to attach metadata to the relationship;
                ``values`` should be a dictionary with key/value pairs.

                If relationships are tuples, they must be in the form
                ``(source, dest)``.

        Returns:
            Array of newly created ``Relationships`` objects

        Example:

            Create multiple relationships (dictionary format)::

                diagnosed_with.create([
                    { 'from': participant_001, 'to': parkinsons},
                    { 'from': participant_321, 'to': als}
                ])

            Create multiple relationships (tuple format)::

                diagnosed_with.create([
                    (participant_001, parkinsons),
                    (participant_321, als)
                ])
        """
        self._check_exists()

        # handle non-array
        if isinstance(items, (dict, tuple)):
            items = [items]

        relations = []
        for value in items:
            # get source, destination, and values
            if isinstance(value, tuple):
                src, dest = value
                vals = {}
            elif isinstance(value, dict):
                src = value.get("from", value.get("source"))
                dest = value.get("to", value.get("destination"))
                vals = value.get("values", {})
            else:
                raise Exception(
                    "Expected relationship as tuple or dictionary, found {}".format(
                        type(value)
                    )
                )

            # Check sources and destinations
            if not isinstance(src, (Record, DataPackage, string_types)):
                raise Exception(
                    "source must be object of type Record, DataPackage, or UUID"
                )
            if not isinstance(dest, (Record, DataPackage, string_types)):
                raise Exception(
                    "destination must be object of type Record, DataPackage, or UUID"
                )

            # create local relationship object
            relations.append(
                Relationship(
                    dataset_id=self.dataset_id,
                    type=self.type,
                    source=src,
                    destination=dest,
                    values=[
                        dict(name=k, value=v, dataType=self.schema.get(k).type)
                        for k, v in vals.items()
                    ],
                )
            )

        return self._api.concepts.relationships.instances.create_many(
            self.dataset_id, self, *relations
        )

    def as_dict(self):
        d = super(RelationshipType, self).as_dict()
        d["type"] = "relationship"
        if self.source is not None:
            d["from"] = self.source
        if self.destination is not None:
            d["to"] = self.destination
        return d

    @as_native_str()
    def __repr__(self):
        return u"<RelationshipType type='{}' id='{}'>".format(self.type, self.id)


class Relationship(BaseRecord):
    """
    A single instance of a ``RelationshipType``.
    """

    _object_key = ""

    def __init__(self, dataset_id, type, source, destination, *args, **kwargs):
        assert isinstance(
            source, (Record, string_types, DataPackage)
        ), "source must be Model, UUID, or DataPackage"
        assert isinstance(
            destination, (Record, string_types, DataPackage)
        ), "destination must be Model, UUID, or DataPackage"

        if isinstance(source, (Record, DataPackage)):
            source = source.id
        if isinstance(destination, (Record, DataPackage)):
            destination = destination.id

        self.source = source
        self.destination = destination

        kwargs.pop("schemaRelationshipId", None)
        super(Relationship, self).__init__(dataset_id, type, *args, **kwargs)

    def relationship(self):
        """
        Retrieves the relationship definition of this instance from the platform

        Returns:
           A single ``RelationshipType``.
        """
        return self._api.concepts.relationships.get(self.dataset_id, self.type)

    # TODO: delete when update is supported, handled in super-class
    def set(self, name, value):
        raise Exception("Updating a Relationship is not available at this time.")

    def update(self):
        raise Exception("Updating a Relationship is not available at this time.")
        # TODO: _update_self(self, self._api.concepts.relationships.instances.update(self.dataset_id, self))

    def delete(self):
        """
        Deletes the instance from the platform.

        Example::

          mouse_001_eeg_link.delete()
        """
        return self._api.concepts.relationships.instances.delete(self.dataset_id, self)

    @classmethod
    def from_dict(cls, data, *args, **kwargs):
        d = dict(
            source=data.pop("from", None), destination=data.pop("to", None), **data
        )
        item = super(Relationship, cls).from_dict(d, *args, **kwargs)
        return item

    def as_dict(self):
        d = super(Relationship, self).as_dict()
        d["to"] = self.destination
        d["from"] = self.source

        return d

    @as_native_str()
    def __repr__(self):
        return u"<Relationship type='{}' id='{}' source='{}' destination='{}'>".format(
            self.type, self.id, self.source, self.destination
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Proxies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProxyInstance(BaseRecord):
    _object_key = ""

    def __init__(self, dataset_id, type, *args, **kwargs):
        super(ProxyInstance, self).__init__(dataset_id, type, *args, **kwargs)

    def item(self):
        if self.type == "proxy:package":
            package_id = self.get("id")
            return self._api.packages.get(package_id)
        else:
            raise Exception("unsupported proxy type: {}".format(self.type))

    def update(self):
        raise Exception("Updating a ProxyInstance is not available at this time.")

    def set(self, name, value):
        raise Exception("Updating a ProxyInstance is not available at this time.")

    @as_native_str()
    def __repr__(self):
        return u"<ProxyInstance type='{}' id='{}'>".format(self.type, self.id)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Model/Relation Instance Sets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class BaseInstanceList(list):
    _accept_type = None

    def __init__(self, type, *args, **kwargs):
        super(BaseInstanceList, self).__init__(*args, **kwargs)
        assert isinstance(type, self._accept_type), "type must be type {}".format(
            self._accept_type
        )
        self.type = type

    def as_dataframe(self):
        pass


class RecordSet(BaseInstanceList):
    _accept_type = Model

    @require_extension
    def as_dataframe(self, record_id_column_name=None):
        """
        Convert the list of ``Record`` objects to a pandas DataFrame

        Args:
            record_id_column_name (string): If set, a column with the desired
                name will be prepended to this dataframe that contains record ids.

        Returns:
            pd.DataFrame

        """
        cols = list(self.type.schema.keys())

        if record_id_column_name:
            if record_id_column_name in cols:
                raise ValueError(
                    "There is already a column called '{}' in this data set.".format(
                        record_id_column_name
                    )
                )
            cols.insert(0, record_id_column_name)

        data = []
        for instance in self:
            values = dict(instance.values)
            if record_id_column_name:
                values[record_id_column_name] = instance.id
            data.append(values)

        df = pd.DataFrame(data=data, columns=cols)
        return df


class RelationshipSet(BaseInstanceList):
    _accept_type = RelationshipType

    @require_extension
    def as_dataframe(self):
        """
        Converts the list of ``Relationship`` objects to a pandas DataFrame

        Returns:
            pd.DataFrame

        .. note::

          In addition to the values in each relationship instance, the DataFrame
          contains three columns that describe each instance:

            - ``__source__``: ID of the instance's source
            - ``__destination__``: ID of the instance's destination
            - ``__type__``: Type of relationship that the instance is
        """
        cols = ["__source__", "__destination__", "__type__"]
        cols.extend(self.type.schema.keys())

        data = []
        for instance in self:
            d = {}
            d["_type"] = self.type.type
            d["_source"] = instance.source
            d["_destination"] = instance.destination

            for name, value in instance.values.items():
                d[name] = value

            data.append(d)

        df = pd.DataFrame(data=data, columns=cols)
        return df
