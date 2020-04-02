# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from blackfynn.api.base import APIBase


class UserAPI(APIBase):
    base_uri = "/user"
    name = "user"

    def switch_organization(self, orgId):
        return self._put(self._uri("/organization/{orgId}/switch".format(orgId=orgId)))
