# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from future.utils import string_types

import datetime
import math

import requests

from blackfynn import log
from blackfynn.api.base import APIBase
from blackfynn.extensions import numpy as np
from blackfynn.extensions import pandas as pd
from blackfynn.extensions import require_extension
from blackfynn.models import (
    BaseDataNode,
    Collection,
    DataPackage,
    Dataset,
    File,
    Organization,
    PublishInfo,
    StatusLogEntry,
    StatusLogResponse,
    TeamCollaborator,
    User,
    UserCollaborator,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Dataset
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DatasetsAPI(APIBase):
    """
    Interface for managing datasets on the platform.
    """

    base_uri = "/datasets"
    name = "datasets"

    def get(self, ds):
        id = self._get_id(ds)
        resp = self._get(self._uri("/{id}", id=id))
        return Dataset.from_dict(resp, api=self.session)

    def published(self, ds):
        id = self._get_id(ds)
        resp = self._get(self._uri("/{id}/published", id=id))
        if resp["status"] == "PUBLISH_SUCCEEDED":
            resp["latest_doi"] = self._get(self._uri("/{id}/doi", id=id))["doi"]
        return PublishInfo.from_dict(resp)

    def package_count(self, ds):
        id = self._get_id(ds)
        resp = self._get(self._uri("/{id}/packageTypeCounts", id=id))
        file_count = 0
        for key, value in resp.items():
            file_count += value
        return file_count

    def status_log(self, ds, limit, offset):
        id = self._get_id(ds)
        resp = self._get(
            self._uri(
                "/{id}/status-log?limit={limit}&offset={offset}",
                id=id,
                limit=limit,
                offset=offset,
            )
        )
        return StatusLogResponse.from_dict(resp)

    def team_collaborators(self, ds):
        id = self._get_id(ds)
        resp = self._get(self._uri("/{id}/collaborators/teams", id=id))
        return [TeamCollaborator.from_dict(t) for t in resp]

    def user_collaborators(self, ds):
        id = self._get_id(ds)
        resp = self._get(self._uri("/{id}/collaborators/users", id=id))
        return [UserCollaborator.from_dict(u) for u in resp]

    def get_packages_by_filename(self, ds, filename):
        id = self._get_id(ds)
        resp = self._get(
            self._uri("/{id}/packages?filename={filename}", id=id, filename=filename)
        )
        return [
            DataPackage.from_dict(p, api=self.session) for p in resp.get("packages")
        ]

    def owner(self, ds):
        return next(
            iter(filter(lambda x: x.role == "owner", self.user_collaborators(ds)))
        )

    def get_by_name_or_id(self, name_or_id):
        """
        Get Dataset by name or ID.

        When using name, this ignores case, spaces, hyphens, and underscores
        such that these are equivalent:

          - "My Dataset"
          - "My-dataset"
          - "mydataset"
          - "my_DataSet"
          - "mYdata SET"

        """

        def name_key(n):
            return n.lower().strip().replace(" ", "").replace("_", "").replace("-", "")

        search_key = name_key(name_or_id)

        def is_match(ds):
            return (name_key(ds.name) == search_key) or (ds.id == name_or_id)

        matches = [ds for ds in self.get_all() if is_match(ds)]
        return matches[0] if matches else None

    def get_all(self):
        resp = self._get(self._uri("/"))
        return [Dataset.from_dict(ds, api=self.session) for ds in resp]

    def create(self, ds):
        """
        Create a dataset on the platform
        """
        if self.get_by_name_or_id(ds.name) is not None:
            raise Exception("Dataset with name {} already exists".format(ds.name))

        resp = self._post("", json=ds.as_dict())
        return Dataset.from_dict(resp, api=self.session)

    def update(self, ds):
        """
        Update a dataset on the platform
        """
        id = self._get_id(ds)
        resp = self._put(self._uri("/{id}", id=id), json=ds.as_dict())
        return Dataset.from_dict(resp, api=self.session)

    def delete(self, ds):
        """
        Delete a dataset on the platform
        """
        id = self._get_id(ds)
        resp = self._del(self._uri("/{id}", id=id))
        ds.id = None
        return resp


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DataAPI(APIBase):
    """
    Interface for lower-level data operations on the platform.
    """

    base_uri = "/data"
    name = "data"

    def update_properties(self, thing):
        """
        Update properties for an object/package on the platform.
        """
        path = self._uri("/{id}/properties", id=thing.id)
        body = {"properties": [m.as_dict() for m in thing.properties]}

        return self._put(path, json=body)

    def delete(self, *things):
        """
        Deletes objects from the platform
        """
        ids = list(set([self._get_id(x) for x in things]))
        r = self._post("/delete", json=dict(things=ids))
        if len(r["success"]) != len(ids):
            failures = [f["id"] for f in r["failures"]]
            print("Unable to delete objects: {}".format(failures))

        for thing in things:
            if isinstance(thing, BaseDataNode):
                thing.id = None

        return r

    def move(self, destination, *things):
        """
        Moves objects to the destination package
        """
        ids = [self._get_id(x) for x in things]
        # if destination is None, things will get moved into their containing dataset
        dest = self._get_id(destination) if destination is not None else None
        return self._post("/move", json=dict(things=ids, destination=dest))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Packages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PackagesAPI(APIBase):
    """
    Interface for task/workflow objects on Blackfynn platform
    """

    base_uri = "/packages"
    name = "packages"

    def create(self, pkg):
        """
        Create data package on platform
        """
        resp = self._post("", json=pkg.as_dict())
        pkg = self._get_package_from_data(resp)
        return pkg

    def update(self, pkg, **kwargs):
        """
        Update package on platform
        """
        d = pkg.as_dict()
        d.update(kwargs)
        d.pop("state", None)
        resp = self._put(self._uri("/{id}", id=pkg.id), json=d)
        pkg = self._get_package_from_data(resp)
        return pkg

    def get(self, pkg, include=None):
        """
        Get package object

        pkg:     can be DataPackage ID or DataPackage object.
        include: list of fields to force-include in response (if available)
        """
        pkg_id = self._get_id(pkg)

        params = None
        if include is not None:
            if isinstance(include, string_types):
                params = {"include": include}
            if hasattr(include, "__iter__"):
                params = {"include": ",".join(include)}

        resp = self._get(self._uri("/{id}", id=pkg_id), params=params)

        # TODO: cast to specific DataPackages based on `type`
        pkg = self._get_package_from_data(resp)
        return pkg

    def process(self, pkg):
        """
        Process a package that has been successfully uploaded but not yet processed
        """
        try:
            self._put(self._uri("/{id}/process", id=pkg.id))
            return True
        except requests.exceptions.HTTPError as error:
            response = error.response
            status_code = response.status_code
            message = response.json().get("message")

            if status_code == requests.codes.bad_request and message is not None:
                raise Exception(message)
            else:
                raise error

    def get_sources(self, pkg):
        """
        Returns the sources of a DataPackage. Sources are the raw, unmodified
        files (if they exist) that contains the package's data.
        """
        pkg_id = self._get_id(pkg)
        resp = self._get(self._uri("/{id}/sources", id=pkg_id))
        for r in resp:
            r["content"].update(dict(pkg_id=pkg_id))

        return [File.from_dict(r, api=self.session) for r in resp]

    def get_files(self, pkg):
        """
        Returns the files of a DataPackage. Files are the possibly modified
        source files (e.g. converted to a different format), but they could also
        be the source files themselves.
        """
        pkg_id = self._get_id(pkg)
        resp = self._get(self._uri("/{id}/files", id=pkg_id))
        for r in resp:
            r["content"].update(dict(pkg_id=pkg_id))

        return [File.from_dict(r, api=self.session) for r in resp]

    def get_view(self, pkg):
        """
        Returns the object(s) used to view the package. This is typically a set of
        file objects, that may be the DataPackage's sources or files, but could also be
        a unique object specific for the viewer.
        """
        pkg_id = self._get_id(pkg)
        resp = self._get(self._uri("/{id}/view", id=pkg_id))
        for r in resp:
            r["content"].update(dict(pkg_id=pkg_id))

        return [File.from_dict(r, api=self.session) for r in resp]

    def get_presigned_url_for_file(self, pkg, file):
        args = dict(pkg_id=self._get_id(pkg), file_id=self._get_id(file))
        resp = self._get(self._uri("/{pkg_id}/files/{file_id}", **args))
        if "url" in resp:
            return resp["url"]
        else:
            raise Exception("Unable to get URL for file ID = {}".format(file_id))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class FilesAPI(APIBase):
    """
    Interface for managing file object in Blackfynn
    """

    base_uri = "/files"
    name = "files"

    def create(self, file, destination=None):
        """
        Creates a file under the given destination or its current parent
        """
        container = file.parent if destination is None else destination

        body = file.as_dict()
        body["container"] = container

        response = self._post("", json=body)

        return File.from_dict(response, api=self.session)

    def update(self, file):
        """
        Update a file on the platform
        """
        loc = self._uri("/{id}", id=file.id)
        return self._put(loc, json=file.as_dict())

    def url(self, file):
        """
        Get pre-signed URL for File object
        """
        loc = self._uri("/{id}", id=file.id)
        return self._get(loc)["url"]
