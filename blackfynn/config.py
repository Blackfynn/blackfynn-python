"""
Blackfynn Configuration File
----------------------------

Blackfynn stores connection information in your Blackfynn configuration file.
Advanced users might want to edit their Blackfynn client tool configuration file directly
for control of the client libraries. Alternatively, users can modify client behavior using
environment variables.

Location
~~~~~~~~

Your configuration file is located in your ``.blackfynn/`` directory. The ``.blackfynn/`` directory
is found in the ``$HOME`` directory (Mac/Linux) or the ``User`` directory (Windows).

Full path: ``$HOME/.blackfynn/config.ini``

Format
~~~~~~

The config file is in `INI <https://en.wikipedia.org/wiki/INI_file>`_ format.
There are three types of sections: ``[global]``, ``[agent]``, and ``[<profile>]``.
You can have as many ``[<profile>]`` sections as you want.

Example of the ``config.ini`` file:

.. code-block:: ini

    # Global settings
    [global]
    default_profile = default

    # Profiles
    [default]
    api_token = c09be34d-5696-4c49-b174-7fe3fb3194af
    api_secret = 87092fd-b3ad-4de9-bf78-2dbcedb7737a

    [debug_mode]
    use_cache = false
    api_token = c09be34d-5696-4c49-b174-7fe3fb3194af
    api_secret = 87092fd-b3ad-4de9-bf78-2dbcedb7737a

    [super_conn]
    api_token = da064188-47e4-43b0-b5cd-91805b7522d7
    api_secret = 2a543888-d24d-4958-8833-3311a55e4ed6

    # Settings for the Blackfynn CLI Agent
    [agent]
    ...

The following settings (and their default values) are available under ``[<profile>]`` or ``[global]``:

.. code-block:: ini

    # Blackfynn API token/secret
    'api_token'                   : None,
    'api_secret'                  : None,

    'api_host'                    : 'https://api.blackfynn.io',

    # I/O
    'max_request_time'            : 120, # two minutes
    'max_request_timeout_retries' : 2,
    'max_upload_workers'          : 10,

    # Timeseries
    'max_points_per_chunk'        : 10000,

    # Directories
    'blackfynn_dir'               : $HOME/.blackfynn
    'cache_dir'                   : $HOME/.blackfynn/cache

    # Cache
    'cache_index'                 : $HOME/.blackfynn/cache/index.db
    'cache_max_size'              : 2048,
    'cache_inspect_interval'      : 1000,
    'ts_page_size'                : 3600,
    'use_cache'                   : True,

In addition to the above, these settings are available under ``[global]``:

.. code-block:: ini

    default_profile

To see your current configuration (and any variables), use the Python command line tool:

.. code-block:: bash

    $ bf profile keys

Environment Variables
---------------------

It is also possible to set configuration options using environment variables

.. note:

    Environment variables (if present) override any profile-defined settings
    in your Blackfynn Configuration File. They are useful for terminal-specific settings.

To switch between profiles in a given terminal session, set the environment variable:

.. code-block:: bash

    BLACKFYNN_PROFILE="your profile name"

Alternatively, you can specify your token/secret directly:

.. code-block:: bash

    BLACKFYNN_API_TOKEN="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    BLACKFYNN_API_SECRET="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

To control the verbosity of the Python client's logging:

.. code-block:: bash

    BLACKFYNN_LOG_LEVEL=("DEBUG" or "INFO" or "WARN" or "ERROR")

To specify an alternate directory to use as the Blackfynn config directory:

.. code-block:: bash

    BLACKFYNN_DIR="./some_other_dir"

If the ``BLACKFYNN_DIR`` environment variable is set, your configuration file will be:

.. code-block:: bash

    $BLACKFYNN_DIR/config.ini

Additional environment variables and their corresponding config options:

.. code-block:: bash

    BLACKFYNN_USE_CACHE: 0  (false) or 1  (true)  # `use_cache`
    BLACKFYNN_API_LOC                             # `api_host`
    BLACKFYNN_CACHE_MAX_SIZE                      # `cache_max_size`
    BLACKFYNN_CACHE_INSPECT_EVERY                 # `cache_inspect_interval`
    BLACKFYNN_TS_PAGE_SIZE                        # `ts_page_size`

"""

from __future__ import absolute_import, division, print_function

import configparser
import os

BLACKFYNN_DIR_DEFAULT = os.path.join(os.path.expanduser("~"), ".blackfynn")
CACHE_DIR_DEFAULT = os.path.join(BLACKFYNN_DIR_DEFAULT, "cache")
CACHE_INDEX_DEFAULT = os.path.join(CACHE_DIR_DEFAULT, "index.db")

DEFAULTS = {
    # blackfynn api locations
    "api_host": "https://api.blackfynn.io",
    "model_service_host": None,
    # blackfynn API token/secret
    "api_token": None,
    "api_secret": None,
    # blackfynn JWT
    "jwt": None,
    # global headers
    "headers": None,
    # all requests
    "max_request_time": 120,  # two minutes
    "max_request_timeout_retries": 2,
    # io
    "max_upload_workers": 10,
    # timeseries
    "max_points_per_chunk": 10000,
    # s3 (amazon/local)
    "s3_host": "",
    "s3_port": "",
    # directories
    "blackfynn_dir": BLACKFYNN_DIR_DEFAULT,
    "cache_dir": CACHE_DIR_DEFAULT,
    # cache
    "cache_index": CACHE_INDEX_DEFAULT,
    "cache_max_size": 2048,
    "cache_inspect_interval": 1000,
    "ts_page_size": 3600,
    "use_cache": True,
}

ENVIRONMENT_VARIABLES = {
    "api_host": ("BLACKFYNN_API_LOC", str),
    "api_token": ("BLACKFYNN_API_TOKEN", str),
    "api_secret": ("BLACKFYNN_API_SECRET", str),
    "jwt": ("BLACKFYNN_JWT", str),
    "blackfynn_dir": ("BLACKFYNN_LOCAL_DIR", str),
    "cache_dir": ("BLACKFYNN_CACHE_LOC", str),
    "cache_max_size": ("BLACKFYNN_CACHE_MAX_SIZE", int),
    "cache_inspect_interval": ("BLACKFYNN_CACHE_INSPECT_EVERY", int),
    "ts_page_size": ("BLACKFYNN_TS_PAGE_SIZE", int),
    "use_cache": ("BLACKFYNN_USE_CACHE", lambda x: bool(int(x))),
    "default_profile": ("BLACKFYNN_PROFILE", str),
    # advanced
    "s3_host": ("S3_HOST", str),
    "s3_port": ("S3_PORT", str),
}


class Settings(object):
    def __init__(self, profile=None, overrides=None, env_override=True):
        # hydrate with standard defaults first
        self._update(DEFAULTS)

        # load and apply environment variables
        environs = self._load_env()

        # check and create blackfynn directory so that we can load config file
        if not os.path.exists(self.blackfynn_dir):
            os.makedirs(self.blackfynn_dir)

        self.profiles = {}
        self._load_config()
        self._load_profiles()

        # use default profile first
        try:
            # first apply config default profile
            self._switch_profile(self.config["global"]["default_profile"])
        except:
            self._switch_profile("global")

        # apply BLACKFYNN_PROFILE
        self._switch_profile(environs.get("default_profile"))

        # use specific profile if specified
        self._switch_profile(profile)

        # override with env variables
        if env_override:
            self._update(environs)

        # update with override values passed into settings
        self._update(overrides)

        # check and create cache dir
        if not os.path.exists(self.cache_dir) and self.use_cache:
            os.makedirs(self.cache_dir)

    def _load_env(self):
        override = {}
        self.env = {}
        for key, (evar, typefunc) in ENVIRONMENT_VARIABLES.items():
            value = os.environ.get(evar, None)
            if value is not None:
                v = typefunc(value)
                self.env[evar] = v
                override[key] = v
        # apply envs
        self._update(override)
        return override

    def _load_config(self):
        self.config_file = os.path.join(self.blackfynn_dir, "config.ini")
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    # _update safely updates the internal __dict__
    def _update(self, settings):
        if settings is None or not isinstance(settings, dict):
            return
        for k in DEFAULTS:
            if k in settings:
                self.__dict__[k] = settings[k]

    def _load_profiles(self):
        # load global first
        self.profiles["global"] = DEFAULTS.copy()
        if "global" in self.config:
            self._parse_profile("global")
        for name in self.config.sections():
            if name is not "global":
                self.profiles[name] = self.profiles["global"].copy()
                self._parse_profile(name)

    def _parse_profile(self, name):
        for key, value in self.config[name].items():
            if value == "none":
                self.profiles[name][key] = None
            elif value.lower() == "true":
                self.profiles[name][key] = True
            elif value.lower() == "false":
                self.profiles[name][key] = False
            elif value.isdigit():
                self.profiles[name][key] = int(value)
            else:
                self.profiles[name][key] = str(value)

    def _switch_profile(self, name):
        if name is None:
            return
        if name not in self.profiles:
            raise Exception("Invalid profile name")
        else:
            self.__dict__.update(self.profiles[name])
            self.active_profile = name
            if name is "global":
                self.active_profile = None

    @property
    def host(self):
        return self.api_host


settings = Settings()
