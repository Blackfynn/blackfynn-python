from __future__ import division
from future.utils import raise_from

import errno
import json
import os
import socket
import subprocess
import sys
from collections import OrderedDict
from time import sleep

import semver

from blackfynn.log import get_logger
from blackfynn.models import Collection, DataPackage, Dataset

logger = get_logger("blackfynn.agent")

try:
    from websocket import create_connection
except ModuleNotFoundError:
    logger.warn(
        "websocket-client is not installed - uploading with the Agent will not work"
    )


MINIMUM_AGENT_VERSION = semver.parse_version_info("0.2.2")
DEFAULT_LISTEN_PORT = 11235


class AgentError(Exception):
    pass


def agent_cmd():
    if sys.platform == "darwin":
        return "/usr/local/opt/blackfynn/bin/blackfynn_agent"

    elif sys.platform.startswith("linux"):
        return "/opt/blackfynn/bin/blackfynn_agent"

    elif sys.platform in ["win32", "cygwin"]:
        return "C:/Program Files/Blackfynn/blackfynn_agent.exe"

    raise AgentError("Platform {} is not supported".format(sys.platform))


def validate_agent_installation(settings):
    """
    Check whether the agent is installed and at least the minimum version.
    """
    try:
        version = subprocess.check_output(
            [agent_cmd(), "version"], env=agent_env(settings)
        )
    except (AgentError, subprocess.CalledProcessError, EnvironmentError) as e:
        raise AgentError(
            "Agent not installed. Visit https://developer.blackfynn.io/agent for installation directions."
        )

    try:
        agent_version = semver.parse_version_info(version.decode().strip())
    except ValueError as e:
        raise_from(AgentError("Invalid version string"), e)

    if agent_version < MINIMUM_AGENT_VERSION:
        raise AgentError(
            "Agent not compatible: found version {}, need version {}".format(
                agent_version, MINIMUM_AGENT_VERSION
            )
        )

    logger.info("Agent version %s found", agent_version)


def agent_env(settings):
    """
    Configure the agent environment to mirror the Python client
    The "local" environment looks for the host in BLACKFYNN_API_LOC
    (this is configured down in blackfynn-rust)
    """
    env = {
        "BLACKFYNN_API_ENVIRONMENT": "local",
        "BLACKFYNN_API_LOC": settings.api_host,
        "BLACKFYNN_API_TOKEN": settings.api_token,
        "BLACKFYNN_API_SECRET": settings.api_secret,
    }
    if sys.platform in ["win32", "cygwin"]:
        env["SYSTEMROOT"] = os.getenv("SYSTEMROOT")
    # On Windows, the SYSTEMROOT environment variable must be preserved for DLLs to correctly load.
    # ref: https://travis-ci.community/t/socket-the-requested-service-provider-could-not-be-loaded-or-initialized/1127

    if "BLACKFYNN_LOG_LEVEL" in os.environ:
        env["BLACKFYNN_LOG_LEVEL"] = os.environ.get("BLACKFYNN_LOG_LEVEL")

    logger.debug("Agent environment: %s", env)

    return env


class AgentListener(object):
    """
    Context manager that starts the agent in listen server mode.
    """

    def __init__(self, settings, port):
        self.settings = settings
        self.port = port
        self.proc = None
        self.devnull = None

    def __enter__(self):
        check_port(self.port)
        command = [agent_cmd(), "upload-status", "--listen", "--port", str(self.port)]

        self.devnull = open(os.devnull, "w")
        self.proc = subprocess.Popen(
            command,
            env=agent_env(self.settings),
            stdout=self.devnull,
            stderr=self.devnull,
        )
        return self.proc

    def __exit__(self, *exc):
        self.proc.kill()
        self.devnull.close()


def check_port(port):
    """
    Refuse to start up if the agent is already running in listen mode.
    This can cause problems with relative files paths and session credentials.
    """
    try:
        logger.debug("Checking port %s", port)
        create_connection(socket_address(port)).close()
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:  # ConnectionRefusedError for Python 3
            logger.debug("No agent found, port %s OK", port)
            return True
        else:
            raise
    else:
        raise AgentError(
            "The agent is already running. Please stop any running processes and try again"
        )


def socket_address(port):
    return "ws://0.0.0.0:{}".format(port)


def create_agent_socket(port):
    """
    Open a websocket connection to the agent

    If the agent is not available, wait using exponential backoff for it to
    come up and start responding to messages
    """
    for i in range(-2, 4):
        try:
            return create_connection(socket_address(port))
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:  # ConnectionRefusedError for Python 3
                sleep_time = 2 ** i
                logger.debug("Connection refused - sleeping for %s seconds", sleep_time)
                sleep(sleep_time)
            else:
                raise

    raise AgentError("Could not connect to Agent")


def agent_upload(
    destination, files, dataset, append, recursive, display_progress, settings
):
    """
    Push an upload through the agent.
    """
    directory_upload = any(os.path.isdir(f) for f in files)

    if directory_upload and len(files) > 1:
        raise AgentError(
            "Can only upload a single directory.\n"
            'Please pass a single directory argument: `pkg.upload("/experiment/dir")`'
        )

    if recursive and not directory_upload:
        raise AgentError(
            "Recursive uploads are only allowed with directories.\n"
            "Upload a directory or pass `recursive=False`."
        )

    if recursive and append:
        raise AgentError("Cannot use `recursive=True` when appending`")

    # Figure out what files the agent is going to upload.
    # We cannot count on the agent to send "upload queued" messages for
    # all files before it starts uploading, so we generate the files we
    # plan to wait for.
    if directory_upload:
        directory = files[0]
        if recursive:
            expected_files = []
            for dirpath, _, filenames in os.walk(directory):
                for f in filenames:
                    expected_files.append(os.path.join(dirpath, f))
        else:
            expected_files = []
            for f in os.listdir(directory):
                path = os.path.join(directory, f)
                if os.path.isfile(path):
                    expected_files.append(path)
    else:
        expected_files = files

    # Agent uses absolute paths
    expected_files = [os.path.abspath(f) for f in expected_files]

    if isinstance(destination, Dataset):
        dataset_id = destination.id
        package_id = None
    elif isinstance(destination, (Collection, DataPackage)):
        dataset_id = dataset.id
        package_id = destination.id
    else:
        raise ValueError("Can only upload to a Dataset, Package, or Collection")

    with AgentListener(settings, DEFAULT_LISTEN_PORT):
        try:
            ws = create_agent_socket(DEFAULT_LISTEN_PORT)

            ws.send(
                json.dumps(
                    {
                        "message": "queue_upload",
                        "body": {
                            "dataset": dataset_id,
                            "package": package_id,
                            "files": files,
                            "append": append,
                            "recursive": recursive,
                        },
                    }
                )
            )

            upload_manager = UploadManager(expected_files, display_progress)
            upload_manager.print_progress()

            for msg in ws:
                msg = json.loads(msg)

                if msg["message"] == "file_queued_for_upload":
                    upload_manager.set_queued(msg["path"], msg["import_id"])

                elif msg["message"] == "upload_progress":
                    upload_manager.set_progress(
                        msg["path"], msg["import_id"], msg["percent_done"], msg["done"]
                    )

                elif msg["message"] == "upload_complete":
                    upload_manager.set_complete(msg["import_id"])

                elif msg["message"] == "upload_error":
                    logger.error(msg["context"])
                    upload_manager.set_error(msg["import_id"])

                elif msg["message"] == "error":
                    raise AgentError(msg["context"])

                else:
                    logger.debug("Unknown message", msg)

                upload_manager.print_progress()
                if upload_manager.done:
                    break

        finally:
            try:
                ws.close()
            except UnboundLocalError:
                pass


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix) :]


class UploadManager(object):
    """
    Manager for file status and messages.

    This is complicated by that fact that the agent sends status information
    for files that are already in the queue or started by other processes.
    This makes it possible for the same file to be queued twice, so we
    have to track both the filename and import id. We only want to wait for
    all "our" files to upload.
    """

    def __init__(self, files, display_progress):
        # Should we show progress bars?
        self.display_progress = display_progress

        # map of filepath -> list(FileProgress)
        self.uploads = OrderedDict()

        for file in files:
            self.track_file(file, import_id=None, ours=True)

        # Keep track of whether progress bars have already been rendered so
        # we know if/what to erase when re-drawing
        self.lines_on_screen = 0

    def track_file(self, file, import_id, ours):
        progress = FileProgress(file, import_id, ours)
        if file in self.uploads:
            self.uploads[file].append(progress)
        else:
            self.uploads[file] = [progress]
        return progress

    def get_tracked_file(self, file, import_id):
        if sys.platform in ["win32", "cygwin"]:
            file = remove_prefix(
                file, "\\\\?\\"
            )  # windows OS sometimes prefix the filepath with \\?\, so we remove it if we see if
        if file in self.uploads:
            for p in self.uploads[file]:
                if p.import_id == import_id:
                    return p

    def all_tracked_files(self):
        for filegroup in self.uploads.values():
            for progress in filegroup:
                yield progress

    def set_queued(self, file, import_id):
        # Update the unqueued version of the file with an import id
        progress = self.get_tracked_file(file, None)

        # This import is queued from a different process - we don't care
        if progress is None:
            return

        progress.queued = True
        progress.import_id = import_id

    def set_progress(self, file, import_id, percent_done, done):
        # Absorb any files that are in the DB/already queued
        if self.get_tracked_file(file, import_id) is None:
            self.track_file(file, import_id, ours=False)

        progress = self.get_tracked_file(file, import_id)
        progress.percent_done = percent_done

    def set_complete(self, import_id):
        for progress in self.all_tracked_files():
            if progress.import_id == import_id:
                progress.done = True

    def set_error(self, import_id):
        for progress in self.all_tracked_files():
            if progress.import_id == import_id:
                progress.errored = True

    @property
    def done(self):
        return all([fstat.done for fstat in self.all_tracked_files() if fstat.ours])

    def print_progress(self, width=24):
        if not self.display_progress:
            return

        # move cursor to relative beginning
        sys.stdout.write("\033[F" * self.lines_on_screen)

        for fstat in self.all_tracked_files():
            if fstat.done:
                state = "DONE"
            elif fstat.errored:
                state = "ERRORED"
            elif fstat.queued:
                state = "UPLOADING"
            else:
                state = "WAITING"

            text = " [ {bars}{dashes} ] {state:12s} {percent:05.1f}% {name}\n".format(
                bars="#" * int(fstat.progress * width),
                dashes="-" * (width - int(fstat.progress * width)),
                percent=fstat.percent_done,
                name=fstat.name,
                state=state,
            )

            sys.stdout.write("{}\r".format(text))
            sys.stdout.flush()

        self.lines_on_screen = len(list(self.all_tracked_files()))


class FileProgress(object):
    def __init__(self, filename, import_id, ours):
        # We only care about the state of uploads started by this process
        self.ours = ours
        self.filename = filename
        self.import_id = import_id
        self.name = os.path.basename(filename)
        self._percent_done = 0
        self.done = False
        self.errored = False
        self.queued = False

    @property
    def percent_done(self):
        if self.done:
            return 100
        return self._percent_done

    @percent_done.setter
    def percent_done(self, value):
        # Only increment progress (in case messages come out of order)
        if value > self._percent_done:
            self._percent_done = value

    @property
    def progress(self):
        return self.percent_done / 100
