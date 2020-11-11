""" Utility functions for generating test fixtures """

import time
from uuid import uuid4

from blackfynn import Blackfynn


def current_ts():
    """ Gets current timestamp """
    return int(round(time.time() * 1000))


def get_test_client(profile=None, api_token=None, api_secret=None, **overrides):
    """ Utility function to get a Blackfynn client object """
    bf = Blackfynn(
        profile=profile, api_token=api_token, api_secret=api_secret, **overrides
    )
    assert bf.context is not None
    orgs = bf.organizations()
    assert len(orgs) > 0

    # explicitly set context to Blackfyn org
    assert bf.context is not None

    return bf


def create_test_dataset(bf_client):
    """Utility function to generate a dataset for testing. It is up to the
    caller to ensure the dataset is cleaned up
    """
    ds = bf_client.create_dataset("test_dataset_{}".format(uuid4()))
    ds_id = ds.id
    # Removing this check to limit the number of API calls:
    # all_dataset_ids = [x.id for x in bf_client.datasets()]
    # assert ds_id in all_dataset_ids
    return ds
