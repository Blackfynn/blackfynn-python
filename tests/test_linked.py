from uuid import uuid4

import pytest

from blackfynn.models import LinkedModelProperty, ModelProperty
from tests.utils import create_test_dataset


def make_id():
    return str(uuid4()).replace("-", "_")


### Testing linked properties locally:
def test_make_linked_property(dataset):
    # make a new model
    model = dataset.create_model(
        "my_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )

    # create a linked property linking to that model,
    # and make sure the link initialized correctly
    link1 = LinkedModelProperty("link1", model, "1st linked property")

    dct1 = link1.as_dict()
    assert dct1["name"] == "link1"
    assert dct1["displayName"] == "1st linked property"
    assert dct1["to"] == model.id

    # make a linked property from a dict,
    # and make sure it initialized correctly
    link2 = LinkedModelProperty.from_dict(
        {
            "link": {
                "name": "link2",
                "displayName": "2nd linked property",
                "to": model.id,
                "id": "XXX-XXX-XXX",
                "position": 0,
            }
        }
    )
    assert link2.id == "XXX-XXX-XXX"
    assert link2.position == 0

    dct2 = link2.as_dict()
    assert dct2["name"] == "link2"
    assert dct2["displayName"] == "2nd linked property"
    assert dct2["to"] == model.id


### Testing linked property API methods:
def test_add_linked_property(dataset):
    # Create two models and link one to the other
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    source.add_linked_property("link", target, "my linked property")

    # Make sure newly created link is accessible through the API
    assert any(
        l.name == "link" and l.target == target.id
        for l in dataset.get_topology()["linked_properties"]
    )
    assert "link" in source.linked

    # Prevent user from adding duplicate linked properties
    with pytest.raises(Exception):
        source.add_linked_property("link", source, "duplicate linked property")
    assert not any(
        l.display_name == "duplicate linked property"
        for l in dataset.get_topology()["linked_properties"]
    )


def test_add_linked_property_bulk(dataset):
    # Link one model to three others
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    link1 = LinkedModelProperty("link1", target, "bulk-added")
    link2 = LinkedModelProperty("link2", target, "bulk-added")
    link3 = LinkedModelProperty("link3", target, "bulk-added")
    source.add_linked_properties([link1, link2, link3])

    # Make sure newly created links are accessible through the API
    bulk = [
        x
        for x in dataset.get_topology()["linked_properties"]
        if x.display_name == "bulk-added"
    ]
    assert len(bulk) == 3
    assert len(source.linked) == 3


def test_edit_linked_property(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    link = source.add_linked_property("link", target, "my linked property")

    # edit the linked property and update model
    link.display_name = "updated linked property"
    link.position = 99
    source.update()

    # Make sure changes were saved
    new_link = source.get_linked_property("link")
    assert new_link.position == 99
    assert new_link.display_name == "updated linked property"


def test_delete_linked_property(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    source.add_linked_property("link", target, "my linked property")

    # delete the link
    source.remove_linked_property("link")

    # Make sure changes were saved
    assert "link" not in source.linked


def test_retrieve_linked_properties(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    source.add_linked_property("link", target, "my linked property")

    new_source = dataset.get_model(source.type)
    assert "link" in new_source.linked


### Testing linked property values
def test_add_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    prop = source.add_linked_property("link", target, "my linked property")

    # make records and link them
    source_rec = source.create_record({"name": "source_record"})
    target_rec = target.create_record({"name": "target_record"})
    link = source_rec.add_linked_value(target_rec, prop)
    assert link.id == source_rec.get_linked_value("link").id

    # prevent duplicate links from being created
    target_rec2 = target.create_record({"name": "second_target"})
    link2 = source_rec.add_linked_value(target_rec2, prop)
    links = source_rec.get_linked_values()
    assert len(links) == 1
    assert links[0].target_record_id == target_rec2.id


def test_get_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    prop = source.add_linked_property("link", target, "my linked property")

    # make records and link them
    source_rec = source.create_record({"name": "source_record"})
    target_rec = target.create_record({"name": "target_record"})
    link = source_rec.add_linked_value(target_rec, prop)
    link2 = source_rec.get_linked_value("link")
    link3 = source_rec.get_linked_value(link.id)
    assert link.id == link2.id == link3.id
    assert link.source_model.id == source.id
    assert link.target_model.id == target.id


def test_remove_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model(
        "source_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    target = dataset.create_model(
        "target_model_{}".format(make_id()), schema=[ModelProperty("name", title=True)]
    )
    prop = source.add_linked_property("link", target, "my linked property")

    # make records and link them
    source_rec = source.create_record({"name": "source_record"})
    target_rec = target.create_record({"name": "target_record"})
    link = source_rec.add_linked_value(target_rec, prop)

    # delete the link
    source_rec.delete_linked_value(link.id)
    assert not any(
        link.target == target_rec.id for link in source_rec.get_linked_values()
    )
