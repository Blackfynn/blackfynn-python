import datetime
import os

import pytest
import requests
from dateutil.parser import parse

from blackfynn import Blackfynn
from blackfynn.base import UnauthorizedException
from blackfynn.models import (
    BaseNode,
    DataPackage,
    Dataset,
    File,
    PublishInfo,
    TeamCollaborator,
    UserCollaborator,
)

from .utils import get_test_client


def test_basenode(client, dataset):
    node1 = dataset
    node2 = client.get_dataset(dataset.id)
    node3 = BaseNode()
    assert node1 == node2
    assert node1 != node3
    assert node1 != object()
    assert [node1, node2] == [node2, node1]


def test_update_dataset(client, dataset, session_id):
    # update name of dataset
    ds_name = "Same Dataset, Different Name {}".format(session_id)
    dataset.name = ds_name
    dataset.update()
    ds2 = client.get_dataset(dataset.id)
    assert ds2.id == dataset.id
    assert isinstance(ds2.int_id, int)
    assert ds2.int_id == dataset.int_id
    assert ds2.name == ds_name
    assert ds2.owner_id == client.profile.id


def test_dataset_status_log(client, dataset):
    dataset_status_log = dataset.status_log()
    assert dataset_status_log.limit == 25
    assert dataset_status_log.offset == 0
    assert dataset_status_log.total_count == 1
    assert len(dataset_status_log.entries) == 1
    assert dataset_status_log.entries[0].user.node_id == client.profile.id
    assert dataset_status_log.entries[0].user.first_name == client.profile.first_name
    assert dataset_status_log.entries[0].user.last_name == client.profile.last_name
    assert dataset_status_log.entries[0].updated_at == parse(dataset.created_at)
    assert dataset_status_log.entries[0].status.id is not None
    assert dataset_status_log.entries[0].status.name is not None
    assert dataset_status_log.entries[0].status.display_name is not None


def test_status_is_readonly(client, dataset):
    with pytest.raises(AttributeError) as excinfo:
        dataset.status = "New Thing"
        dataset.update()
    assert "Dataset.status is read-only." in str(excinfo.value)


def test_tags_is_list_of_strings_only(client, dataset):
    with pytest.raises(AttributeError) as excinfo:
        dataset.tags = "New Thing"
    assert "Dataset.tags should be a list of strings." in str(excinfo.value)
    with pytest.raises(AttributeError) as excinfo:
        dataset.tags = [1, 2, 3]
    assert "Dataset.tags should be a list of strings." in str(excinfo.value)
    dataset.tags = ["a", "b", "c"]
    dataset.update()
    dataset_from_platform = client.get_dataset(dataset.id)
    assert dataset_from_platform.tags == ["a", "b", "c"]


def test_datasets(client, dataset):
    ds_items = len(dataset)

    # create package locally
    pkg = DataPackage("Child of Dataset", package_type="Text")

    assert not pkg.exists
    assert pkg not in dataset

    # add package to dataset
    dataset.add(pkg)

    assert pkg.exists
    assert pkg in dataset
    assert pkg.id in dataset
    assert len(dataset) == ds_items + 1

    # remove from dataset
    dataset.remove(pkg)

    assert not pkg.exists
    assert pkg not in dataset
    assert len(dataset) == ds_items

    # can't create dataset with same name
    with pytest.raises(Exception):
        client.create_dataset(dataset.name)


def test_packages_create_delete(client, dataset):

    # init
    pkg = DataPackage("Some MRI", package_type="MRI")
    assert not pkg.exists

    # create
    dataset.add(pkg)
    assert pkg.exists
    assert pkg.id is not None
    assert pkg.name == "Some MRI"
    assert pkg.owner_id == client.profile.int_id

    # TODO: (once we auto-include in parent)
    assert pkg in dataset

    # update package name
    pkg.name = "Some Other MRI"
    pkg = client.update(pkg)

    pkg2 = client.get(pkg.id)

    assert pkg2.name == "Some Other MRI"
    assert pkg2.id == pkg.id
    assert pkg2.owner_id == client.profile.int_id

    # delete all packages
    client.delete(pkg)

    assert not pkg.exists

    pkg = DataPackage("Something else", package_type="TimeSeries")
    assert not pkg.exists
    dataset.add(pkg)
    assert pkg.exists
    pid = pkg.id
    pkg.delete()
    assert not pkg.exists

    pkg2 = client.get(pid)
    assert pkg2 is None

    # TODO: (once we auto-remove from parent)
    # assert pkg not in dataset


def test_package_type_count(client, dataset):
    n = dataset.package_count()
    pkg = DataPackage("Some MRI", package_type="MRI")
    assert not pkg.exists
    # create
    dataset.add(pkg)
    assert pkg.exists
    client.update(pkg)

    pkg = DataPackage("Something else", package_type="TimeSeries")
    assert not pkg.exists
    dataset.add(pkg)
    assert pkg.exists
    client.update(pkg)

    m = dataset.package_count()
    assert m == n + 2


def test_publish_info(client, dataset):
    publish_info = dataset.published()
    assert publish_info.status == "NOT_PUBLISHED"
    assert publish_info.version_count == 0
    assert publish_info.last_published == None
    assert publish_info.doi == None


def test_owner(client, dataset):
    owner = dataset.owner()
    assert owner.email == client.profile.email


def test_collaborator_user(client, dataset):
    collaborators = dataset.user_collaborators()
    assert len(collaborators) == 1
    assert collaborators[0].email == client.profile.email


def test_collaborator_team(client, dataset):
    collaborators = dataset.team_collaborators()
    assert len(collaborators) == 0


def test_properties(client, dataset):

    pkg = DataPackage("Some Video", package_type="Video")
    assert not pkg.exists

    dataset.add(pkg)
    assert pkg.exists

    pkg.insert_property("my-key", "my-value")
    pkg2 = client.get(pkg)
    print("properties =", pkg2.properties)
    assert pkg2.id == pkg.id
    assert pkg2.get_property("my-key").data_type == "string"
    assert pkg2.get_property("my-key").value == "my-value"

    explicit_ptypes = {
        "my-int1": ("integer", 123123),
        "my-int2": ("integer", "123123"),
        "my-float": ("double", 123.123),
        "my-float2": ("double", "123.123"),
        "my-float3": ("double", "123123"),
        "my-date": ("date", 1488847449697),
        "my-date2": ("date", 1488847449697.123),
        "my-date3": ("date", datetime.datetime.now()),
        "my-string": ("string", "my-123123"),
        "my-string2": ("string", "123123"),
        "my-string3": ("string", "123123.123"),
        "my-string4": ("string", "According to plants, humans are blurry."),
    }
    for key, (ptype, val) in explicit_ptypes.items():
        pkg.insert_property(key, val, data_type=ptype)
        assert pkg.get_property(key).data_type == ptype

    inferred_ptypes = {
        "my-int1": ("integer", 123123),
        "my-int2": ("integer", "123123"),
        "my-float1": ("double", 123.123),
        "my-float2": ("double", "123.123"),
        "my-date": ("date", datetime.datetime.now()),
        "my-string": ("string", "i123123"),
        "my-string2": ("string", "#1231"),
    }
    for key, (ptype, val) in inferred_ptypes.items():
        pkg.insert_property(key, val)
        prop = pkg.get_property(key)
        assert prop.data_type == ptype

    # remove property
    pkg.remove_property("my-key")
    assert pkg.get_property("my-key") is None

    pkg2 = client.get(pkg.id)
    assert pkg2.get_property("my-key") is None


def test_can_remove_multiple_items(dataset):
    pkg1 = DataPackage("Some MRI", package_type="MRI")
    dataset.add(pkg1)
    pkg1.update()
    pkg2 = DataPackage("Some Video", package_type="Video")
    dataset.add(pkg2)
    pkg2.update()
    assert pkg1 in dataset.items
    assert pkg2 in dataset.items

    dataset.remove(pkg1)
    dataset.remove(pkg2)
    assert pkg1 not in dataset.items
    assert pkg2 not in dataset.items


def test_timeout():
    with pytest.raises(requests.exceptions.Timeout):
        # initial authentication calls should time out
        get_test_client(max_request_time=0.00001)


def test_client_host_overrides():
    host = "http://localhost"
    # fails authentication in Blackfynn.__init__
    with pytest.raises(requests.exceptions.RequestException):
        bf = Blackfynn(host=host)

    bf = Blackfynn(model_service_host=host)
    assert bf.settings.model_service_host == host


def test_exception_raise():
    bf = Blackfynn()
    with pytest.raises(Exception) as excinfo:
        bf._api._call("get", "/datasets/plop")
    assert "plop not found" in str(excinfo.value)


def test_client_global_headers():
    global_headers = {
        "X-Custom-Header1": "Custom Value",
        "X-Custom-Header2": "Custom Value2",
    }
    bf = Blackfynn(headers=global_headers)
    assert bf.settings.headers == global_headers

    for header, header_value in global_headers.items():
        assert header in bf._api._session.headers
        assert bf._api._session.headers[header] == header_value
