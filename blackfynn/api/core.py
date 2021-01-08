# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from blackfynn.api.base import APIBase
from blackfynn.models import (
    BaseDataNode,
    Collection,
    DataPackage,
    Dataset,
    Model,
    Organization,
    Record,
    Relationship,
    RelationshipType,
    User,
    get_package_class,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Core API
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class CoreAPI(APIBase):
    """
    Special higher-level API actions that may use other registered APIs.
    All in the name of convenience.
    """

    name = "core"

    def __init__(self, *args, **kwargs):
        super(CoreAPI, self).__init__(*args, **kwargs)
        self._data_registry = {}

    def create(self, thing):
        """
        Create an object on the platform. This will create the
        object and all sub-objects (if they do not exist).
        """
        if thing.exists:
            thing._api = self.session
            return thing

        if isinstance(thing, (DataPackage, Collection)):
            if thing.dataset is None:
                raise Exception(
                    "{} not created. Must have property `dataset` set.".format(
                        type(thing)
                    )
                )
            item = self.session.packages.create(thing)
        elif isinstance(thing, Dataset):
            item = self.session.datasets.create(thing)
        elif isinstance(thing, Model):
            item = self.session.concepts.create(thing)
        elif isinstance(thing, Record):
            item = self.session.concepts.instances.create(thing)
        elif isinstance(thing, RelationshipType):
            item = self.session.concepts.relations.create_type(thing)
        elif isinstance(thing, Relationship):
            item = self.session.concepts.relations.create(thing)
        else:
            raise Exception("Unable to create object.")

        item._api = self.session

        return item

    def update(self, thing, **kwargs):
        """
        Updates an object on the platform. This will update all
        sub-objects as well, if available.
        """

        if isinstance(thing, (DataPackage, Collection)):
            item = self.session.packages.update(thing, **kwargs)
        elif isinstance(thing, Dataset):
            item = self.session.datasets.update(thing)
        elif isinstance(thing, Model):
            item = self.session.concepts.update(thing)
        elif isinstance(thing, Record):
            item = self.session.concepts.instances.update(thing)
        else:
            raise Exception("Unable to update object.")

        return item

    def get(self, thing, update=True):
        """
        Get any object from id. Assumes the below APIs are registered
        with the session.
        """
        id = self._get_id(thing)

        item = self.session.packages.get(id)
        return item

    def delete(self, *things):
        """
        Deletes objects from the platform. Assumes Data API is registered.
        """
        self.session.data.delete(*things)
        for thing in things:
            if hasattr(thing, "parent"):
                # attempt to remove from parent object
                p = self.get_local(thing.parent)

                if p is not None:
                    p._items = None

                thing.parent = None
            if isinstance(thing, BaseDataNode):
                thing.id = None

    def set_local(self, thing):
        self._data_registry.update({thing.id: thing})

    def get_local(self, thing):
        id = self._get_id(thing)
        return self._data_registry.get(id, None)

    def get_locals(self):
        return list(self._data_registry.values())

    def rm_local(self, thing):
        id = self._get_id(thing)
        return self._data_registry.pop(id, None)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Organizations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class OrganizationsAPI(APIBase):
    """
    Interface for task/workflow objects on Blackfynn platform
    """

    base_uri = "/organizations"
    name = "organizations"

    def get_all(self):
        """
        Get all organizations for logged-in user.
        """
        my_orgs = self._get("?includeAdmins=false")["organizations"]

        return [Organization.from_dict(x, api=self.session) for x in my_orgs]

    def get(self, org=None):
        """
        Get an organization.

        org: Organization class or id string
        """
        id = self._get_id(org)
        resp = self._get(self._uri("/{id}", id=id))
        return Organization.from_dict(resp, api=self.session)

    def get_teams(self, org):
        id = self._get_id(org)
        return self._get(self._uri("/{id}/teams", id=id))

    def get_members(self, org):
        id = self._get_id(org)
        resp = self._get(self._uri("/{id}/members", id=id))
        return [User.from_dict(r, api=self.session) for r in resp]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Search
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class SearchAPI(APIBase):
    """
    Interface for searching Blackfynn
    """

    base_uri = "/search"
    name = "search"

    def query(self, terms, max_results=10):
        data = dict(query=terms, maxResults=max_results)
        resp = self._post(endpoint="", json=data)

        results = []
        for r in resp:
            pkg_cls = get_package_class(r)
            if pkg_cls == Dataset:
                pkg = self.session.datasets.get(r["id"])
            else:
                pkg = self.session.packages.get(r["id"])

            results.append(pkg)

        return results
