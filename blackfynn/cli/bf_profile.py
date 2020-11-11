"""
Description
  The profile management system is used to create multiple profiles for
  different Blackfynn accounts or organizations. The user can also set/unset
  global settings which apply to all profiles.

  Settings are loaded in the following order, with each tier overriding the
  last:

    1. Global settings are loaded first
    2. Default profile, if configured
    3. Command line arguments, e.g.: --profile=<name>
    4. Environment variables, e.g.: BLACKFYNN_API_TOKEN

Usage:
  bf_profile create [<name>]
  bf_profile show [<name>]
  bf_profile delete [<name>] [-f | --force]
  bf_profile list [-c | --contents]
  bf_profile set-default [<name>]
  bf_profile unset-default [-f | --force]
  bf_profile status
  bf_profile set <key> <value> [-f | --force] [--profile=<name>]
  bf_profile unset <key> [-f | --force] [--profile=<name>]
  bf_profile keys [--profile=<name>]
  bf_profile version
  bf_profile help

Options:
  -c --contents       List profiles with contents. Also lists global settings, if any
  -f --force          Attempt action without prompting for confirmation. Use with care
  --profile=<name>    Use specified profile (instead of default)
  -h --help           Show help

Advanced commands:
  set (global|<name>) <key> <value>   Set key/value pair for given profile, or globally
  unset (global|<name>) <key>         Unset key/value pair for given profile, or globally
  keys                                List all available keys and their default values

For additional features, install the Blackfynn CLI Agent:
https://developer.blackfynn.io/agent
"""

from __future__ import absolute_import, print_function
from builtins import input

import io
import os

from docopt import docopt

import blackfynn
from blackfynn import DEFAULT_SETTINGS, Blackfynn, Settings


def main():
    args = docopt(__doc__, version=blackfynn.__version__)

    # Test for these two commands first as they
    # do not require a Blackfynn client or reading the settings file
    if args["help"]:
        print(__doc__.strip("\n"))
        return
    elif args["version"]:
        print(blackfynn.__version__)
        return

    settings = Settings(args["--profile"])
    if not os.path.exists(settings.config_file):
        setup_assistant(settings)
    elif args["create"]:
        create_profile(settings, args["<name>"])
    elif args["show"]:
        show_profile(settings, args["<name>"])
    elif args["delete"]:
        delete_profile(settings, args["<name>"], args["--force"])
    elif args["list"]:
        list_profiles(settings, args["--contents"])
    elif args["set-default"]:
        set_default(settings, args["<name>"])
    elif args["unset-default"]:
        unset_default(settings, args["--force"])
    elif args["set"]:
        set_key(
            settings, args["<key>"], args["<value>"], args["--profile"], args["--force"]
        )
    elif args["unset"]:
        unset_key(settings, args["<key>"], args["--profile"], args["--force"])
    elif args["keys"]:
        list_keys(settings, args["--profile"])
    elif args["status"]:
        bf = Blackfynn(args["--profile"])
        show_status(bf)
    else:
        invalid_usage()

    with io.open(settings.config_file, "w") as configfile:
        settings.config.write(configfile)


def setup_assistant(settings):
    settings.config.clear()

    print("Blackfynn profile setup assistant")

    settings.config["global"] = {"default_profile": "none"}

    print("Create a profile:")
    create_profile(settings)

    print("Setup complete. Run 'bf_profile help' for available commands and actions")


# User commands
# =======================================================


def create_profile(settings, name=None):
    if not name:
        name = input("  Profile name [default]: ") or "default"

    if name in settings.config:
        if name in ("global", "agent", "none"):
            print(
                "Profile name '{}' reserved for system. Please try a different name".format(
                    name
                )
            )
        else:
            print("Profile '{}' already exists".format(name))
        abort()

    print("Creating profile '{}'".format(name))
    settings.config[name] = {}

    settings.config[name]["api_token"] = input("  API token: ")
    settings.config[name]["api_secret"] = input("  API secret: ")

    if settings.config["global"]["default_profile"] == "none":
        settings.config["global"]["default_profile"] = name
        print("Default profile: {}".format(name))

    else:
        if yesno_prompt("Would you like to set '{}' as default (Y/n)? ".format(name)):
            set_default(settings, [name])


def delete_profile(settings, name, force):
    if not name:
        name = input("  Profile to delete: ")

    if not valid_name(settings, name):
        abort()

    if not force:
        if not yesno_prompt("Delete profile '{}' (Y/n)? ".format(name)):
            print("abort")
            abort()

    print("Deleting profile '{}'".format(name))
    settings.config.remove_section(name)

    if settings.config["global"]["default_profile"] == name:
        settings.config["global"]["default_profile"] = "none"
        print(
            "\033[31m* Warning: default profile unset. Use 'bf profile set-default <name>' to set a new default\033[0m"
        )


def list_profiles(settings, contents):
    """
    Lists all profiles
    """
    print("Profiles:")
    for section in settings.config.sections():
        if section not in ["global"]:
            if section == settings.config["global"]["default_profile"]:
                print("* \033[32m{}\033[0m".format(section))
            else:
                print("  {}".format(section))
            if contents:
                print_profile(settings, section, 4)
    if contents:
        if len(settings.config["global"]) > 1:
            print("Global Settings:")
            print_profile(settings, "global", 2)


def set_default(settings, name):
    if not name:
        name = input("  Profile name to set as default: ")

    if not valid_name(settings, name):
        abort()

    print("Default profile: {}".format(name))
    settings.config["global"]["default_profile"] = name


def unset_default(settings, force):
    original = settings.config["global"]["default_profile"]

    if not force:
        if not yesno_prompt("Unset default profile '{}' (Y/n)? ".format(original)):
            print("abort")
            abort()

    print(
        "Default profile '{}' unset. Using global settings and environment variables".format(
            original
        )
    )
    settings.config["global"]["default_profile"] = "none"


def show_profile(settings, profile):
    if profile:
        name = profile
    else:
        name = settings.default_profile

    if name == "global" or valid_name(settings, name):
        print("{} contents:".format(name))
        print_profile(settings, name, 2, True)


# Advanced commands
# =======================================================


def set_key(settings, key, value, profile, force):
    if not key in DEFAULT_SETTINGS:
        print(
            "Invalid key: '{}'\n see 'bf profile keys' for available keys".format(key)
        )
        return

    if profile:
        name = profile
    else:
        name = settings.default_profile

    if not name in settings.config:
        print("Profile '{}' does not exist".format(name))
        return

    if not force and key in settings.config[name]:
        if not yesno_prompt("{}: {} already set. Overwrite (Y/n)? ".format(name, key)):
            abort()

    print("{}: {}={}".format(name, key, value))
    settings.config[name][key] = value


def unset_key(settings, key, profile, force):
    if profile:
        name = profile
    else:
        name = settings.default_profile

    if not name in settings.config:
        print("Profile '{}' does not exist".format(name))
        abort()

    if not key in settings.config[name]:
        print("{}: {} not set".format(name, key))
        abort()

    if not force and key in settings.config[name]:
        if not yesno_prompt("{}: Unset {} (Y/n)? ".format(name, key)):
            abort()

    print("{}: {} unset".format(name, key))
    settings.config[name].pop(key)


def list_keys(settings, profile):
    if profile:
        name = profile
    else:
        name = settings.default_profile

    print("Keys and default values for '{}'".format(name))
    for key, value in sorted(settings.profiles[name].items()):
        print("  {} : {}".format(key, value))


def show_status(bf):
    print("Active profile:\n  \033[32m{}\033[0m\n".format(bf.settings.active_profile))

    if bf.settings.env:
        key_len = 0
        value_len = 0
        for key, value in bf.settings.env.items():
            valstr = "{}".format(value)
            key_len = max(key_len, len(key))
            value_len = max(value_len, len(valstr))

        print("Environment variables:")
        print(
            "  \033[4m{:{key_len}}    {:{value_len}}    {}".format(
                "Key",
                "Value",
                "Environment Variable\033[0m",
                key_len=key_len,
                value_len=value_len,
            )
        )
        for value, evar in sorted(bf.settings.env.items()):
            valstr = "{}".format(value)
            # get internal variable
            ivar = ""
            for k, v in bf.settings.__dict__.items():
                if str(v) == str(evar):
                    ivar = k
            print(
                "  {:{key_len}}    {:{value_len}}    {}".format(
                    ivar, evar, valstr, key_len=key_len, value_len=value_len
                )
            )
        print()

    print("Blackfynn environment:")
    print("  User               : {}".format(bf.profile.email))
    print("  Organization       : {} (id: {})".format(bf.context.name, bf.context.id))
    print("  API Location       : {}".format(bf.settings.api_host))


# Helper functions
# =======================================================


def abort():
    exit(1)


def yesno_prompt(msg):
    return input(msg).lower() in ("y", "yes")


def invalid_usage():
    print("Invalid usage. See `bf_profile help` for available commands")
    abort()


def valid_name(settings, name):
    if name not in settings.config or name == "global":
        print("Profile '{}' does not exist".format(name))
        return False
    return True


def print_profile(settings, name, indent=0, show_all=False):
    if show_all:
        key_len = 0
        for key in settings.profiles[name].keys():
            key_len = max(key_len, len(key))

        for key, value in sorted(settings.profiles[name].items()):
            if key != "default_profile":
                if key in settings.config[name] and name != "global":
                    print(
                        " " * indent
                        + "{:{key_len}} : \033[32m{}\033[0m ({})".format(
                            key, value, name, key_len=key_len
                        )
                    )
                elif key in settings.config["global"]:
                    print(
                        " " * indent
                        + "{:{key_len}} : \033[34m{}\033[0m (global)".format(
                            key, value, key_len=key_len
                        )
                    )
                else:
                    print(
                        " " * indent
                        + "{:{key_len}} : \033[0m{}\033[0m".format(
                            key, value, key_len=key_len
                        )
                    )

    else:
        key_len = 0
        for key in settings.config[name].keys():
            key_len = max(key_len, len(key))

        for key, value in sorted(settings.config[name].items()):
            if key != "default_profile":
                print(
                    " " * indent
                    + "{:{key_len}} : {}".format(key, value, key_len=key_len)
                )
