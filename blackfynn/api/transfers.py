# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from builtins import dict, object
from future.utils import string_types

import io
import os
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

from blackfynn import log
from blackfynn.api.agent import agent_upload, validate_agent_installation
from blackfynn.api.base import APIBase
from blackfynn.models import Collection, DataPackage, Dataset, TimeSeries

# GLOBAL
UPLOADS = {}

logger = log.get_logger("blackfynn.api.transfers")


def check_files(files):
    for f in files:
        if not os.path.exists(f):
            raise Exception("File {} not found.".format(f))


class IOAPI(APIBase):
    """
    Input/Output interface.
    """

    name = "io"

    def upload_files(
        self,
        destination,
        files,
        dataset=None,
        append=False,
        display_progress=False,
        recursive=False,
        use_agent=True,
    ):
        if not use_agent:
            logger.warn(
                "uploading without the Blackfynn agent is no longer supported. Falling back to use_agent=True"
            )

        if isinstance(destination, Dataset):
            # uploading into dataset
            destination_id = None
            dataset = destination
            dataset_id = self._get_id(dataset)
        elif destination is None and dataset is not None:
            # uploading into dataset
            destination_id = None
            dataset_id = self._get_id(dataset)
        elif isinstance(destination, Collection):
            # uploading into collection
            destination_id = self._get_id(destination)
            dataset_id = self._get_id(destination.dataset)
        elif append and isinstance(destination, TimeSeries):
            # uploading into timeseries package must be an append
            destination_id = self._get_id(destination)
            dataset_id = self._get_id(destination.dataset)
        elif isinstance(destination, string_types):
            # assume ID is for collection
            if dataset is None:
                raise Exception(
                    "Must also supply dataset when specifying destination by ID"
                )
            destination_id = destination
            dataset_id = self.get_id(dataset)
        else:
            raise Exception(
                "Cannot upload to destination of type {}".format(type(destination))
            )

        # check input files
        check_files(files)

        # sanity check dataset
        try:
            if isinstance(dataset, Dataset) and dataset.exists:
                ds = dataset
            else:
                ds = self.session.datasets.get(dataset_id)
        except:
            raise Exception("dataset does not exist")

        if destination_id is not None:
            try:
                if (
                    isinstance(destination, (Dataset, Collection, DataPackage))
                    and destination.exists
                ):
                    pass
                else:
                    destination = self.session.packages.get(destination_id)
            except:
                raise Exception("destination does not exist")

            # check type for appends
            if append:
                if not isinstance(destination, TimeSeries):
                    raise Exception("Append destination must be TimeSeries package.")
            else:
                if not isinstance(destination, Collection):
                    raise Exception("Upload destination must be Collection or Dataset.")

        # Push uploads through the Blackfynn agent
        validate_agent_installation(self.session.settings)

        return agent_upload(
            destination=destination,
            files=files,
            dataset=ds,
            append=append,
            recursive=recursive,
            display_progress=display_progress,
            settings=self.session.settings,
        )
