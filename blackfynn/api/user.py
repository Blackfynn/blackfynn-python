# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from blackfynn.api.base import APIBase
from blackfynn.models import User


class UserAPI(APIBase):
    base_uri = "/user"
    name = 'user'

    # Begin: Added by Doc Sewell, Alpine Security

    def get(self):
        """
        Get the current user.
        """
        resp = self._get(self._uri(''))
        return User.from_dict(resp, api=self.session)

    def set_two_factor(self, phone_number, country_code="+1"):
        json = {
            "phoneNumber": phone_number,
            "countryCode": country_code
        }

        resp = self._post('/twofactor', json=json)
        if "authyId" in resp:
            return resp["authyId"]
        else:
            return None

    def delete_two_factor(self):
        return self._del(self._uri('/twofactor'))

    def set_orcid(self, orc_id):
        json = {"authorizationCode": orc_id}
        resp = self._post('/orcid', json=json)
        if "orcid" in resp:
            return resp["orcid"]
        else:
            return None

    def delete_orcid(self):
        return self._del(self._uri('/orcid'))

    def update(self, organization, email, url, color, last_name, first_name, credential):
        json = {
            #"organization": organization,
            "email": email,
            "url": url,
            "color": color,
            "lastName": last_name,
            "firstName": first_name,
            "credential": credential
        }

        resp = self._put('', json=json)
        return User.from_dict(resp, api=self.session)

    def custom_terms_of_service(self, version):
        json = {
            "version": version
        }

        resp = self._put('/custom-terms-of-service', json=json)
        return User.from_dict(resp, api=self.session)

    def blackfynn_terms_of_service(self, version):
        json = {
            "version": version
        }

        resp = self._put('/blackfynn-terms-of-service', json=json)
        return User.from_dict(resp, api=self.session)

    # End: Added by Doc Sewell, Alpine Security


    def switch_organization(self, orgId):
        return self._put( self._uri('/organization/{orgId}/switch'.format(orgId=orgId)))
