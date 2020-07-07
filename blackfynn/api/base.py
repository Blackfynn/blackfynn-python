from __future__ import absolute_import, division, print_function
from future import standard_library
from future.utils import integer_types, string_types

from blackfynn import log
from blackfynn.models import get_package_class

# urllib compatibility
standard_library.install_aliases()
import urllib.parse  # isort:skip

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Base class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class APIBase(object):
    host = None
    base_uri = ""
    name = ""

    def __init__(self, session):
        """
        Base class to be used by all API components.
        """
        # api session
        self.session = session
        self._logger = log.get_logger("blackfynn.api")

    def _get_id(self, thing):
        """
        Get ID for object. Assumes string is already ID.
        """
        if isinstance(thing, (string_types, integer_types)):
            return thing
        elif thing is None:
            return None
        else:
            return thing.id

    def _get_int_id(self, thing):
        """
        Get internal ID for object.
        """
        if isinstance(thing, (string_types, integer_types)):
            return thing
        elif thing is None:
            return None
        else:
            return thing.int_id

    def _get_package_from_data(self, data):
        # parse json
        cls = get_package_class(data)
        pkg = cls.from_dict(data, api=self.session)

        return pkg

    def _uri(self, url_str, **kwvars):
        vals = {k: urllib.parse.quote(str(var)) for k, var in kwvars.items()}
        return url_str.format(**vals)

    def _get(self, endpoint, base=None, host=None, *args, **kwargs):
        base = self.base_uri if base is None else base
        host = self.host if host is None else host
        return self.session._call(
            "get", endpoint, host=host, base=base, *args, **kwargs
        )

    def _post(self, endpoint, base=None, host=None, *args, **kwargs):
        base = self.base_uri if base is None else base
        host = self.host if host is None else host
        return self.session._call(
            "post", endpoint, host=host, base=base, *args, **kwargs
        )

    def _put(self, endpoint, base=None, host=None, *args, **kwargs):
        base = self.base_uri if base is None else base
        host = self.host if host is None else host
        return self.session._call(
            "put", endpoint, host=host, base=base, *args, **kwargs
        )

    def _del(self, endpoint, base=None, host=None, *args, **kwargs):
        base = self.base_uri if base is None else base
        host = self.host if host is None else host
        return self.session._call(
            "delete", endpoint, host=host, base=base, *args, **kwargs
        )
