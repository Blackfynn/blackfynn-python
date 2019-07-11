import pytest
from uuid import uuid4

from blackfynn.models import (
    DataPackage,
    LinkedModelProperty,
    LinkedModelValue,
    ModelProperty,
    ModelPropertyEnumType,
    ModelPropertyType,
    convert_datatype_to_type,
    convert_type_to_datatype,
    uncast_value
)
from tests.utils import create_test_dataset

### Create a fresh dataset for each test:
@pytest.fixture(scope='function')
def empty_dataset(client):
    """
    Test Dataset to be used by other tests.
    """
    ds = create_test_dataset(client)
    # surface test dataset to other functions. Everything after the yield
    # serves as teardown code for the fixture
    yield ds

    # remove
    client._api.datasets.delete(ds)


### Testing linked properties locally:
def test_make_linked_property(empty_dataset):
    # make a new model
    model = empty_dataset.create_model('my_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])

    # create a linked property linking to that model,
    # and make sure the link initialized correctly
    link1 = LinkedModelProperty('link1', model, '1st linked property')

    dct1 = link1.as_dict()
    assert dct1['name'] == 'link1'
    assert dct1['displayName'] == '1st linked property'
    assert dct1['to'] == model.id

    # make a linked property from a dict,
    # and make sure it initialized correctly
    link2 = LinkedModelProperty.from_dict({'link': {
        'name': 'link2',
        'displayName': '2nd linked property',
        'to': model.id,
        'id': 'XXX-XXX-XXX',
        'position': 0}})
    assert link2.id == 'XXX-XXX-XXX'
    assert link2.position == 0

    dct2 = link2.as_dict()
    assert dct2['name'] == 'link2'
    assert dct2['displayName'] == '2nd linked property'
    assert dct2['to'] == model.id


### Testing linked property API methods:
def test_add_linked_property(empty_dataset):
    # Create two models and link one to the other
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link', target, 'my linked property')

    # Make sure newly created link is accessible through the API
    # assert any(prop.name == 'link' for prop in empty_dataset.get_linked_properties())
    assert empty_dataset.get_topology()['linked_properties'][0].name == 'link'
    assert 'link' in source.linked

    # Prevent user from adding duplicate linked properties
    with pytest.raises(Exception):
        source.add_linked_property('link', source, 'duplicate linked property')
    assert len(empty_dataset.get_topology()['linked_properties']) == 1
    
def test_add_linked_property_bulk(empty_dataset):
    # Link one model to three others
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    link1 = LinkedModelProperty('link1', target)
    link2 = LinkedModelProperty('link2', target)
    link3 = LinkedModelProperty('link3', target)
    source.add_linked_properties([link1, link2, link3])

    # Make sure newly created link is accessible through the API
    # assert len(empty_dataset.get_linked_properties()) == 3
    assert len(empty_dataset.get_topology()['linked_properties']) == 3
    assert len(source.linked) == 3

def test_edit_linked_property(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    link = source.add_linked_property('link', target, 'my linked property')

    # edit the linked property and update model
    link.display_name = 'updated linked property'
    link.position = 99
    source.update()
    
    # Make sure changes were saved
    new_link = source.get_linked_property('link')
    assert new_link.position == 99
    assert new_link.display_name == 'updated linked property'

def test_delete_linked_property(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link', target, 'my linked property')

    # delete the link
    source.remove_linked_property('link')

    # Make sure changes were saved
    assert 'link' not in source.linked
    # assert len(empty_dataset.get_linked_properties()) == 0

def test_retrieve_linked_properties(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link', target, 'my linked property')

    new_source = empty_dataset.get_model(source.type)
    assert 'link' in new_source.linked


### Testing linked property values
def test_add_link(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert any(link.target == target_rec.id for link in source_rec.get_linked_values())

    # prevent duplicate links from being created
    target_rec2 = target.create_record({'name': 'second_target'})
    link2 = source_rec.link_to(target_rec2, prop)
    links = source_rec.get_linked_values()
    assert len(links) == 1
    assert links[0].target == target_rec2.id

def test_get_link(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert link.id == source_rec.get_linked_value(link.id).id

def test_remove_link(empty_dataset):
    # make a model and add a linked property
    source = empty_dataset.create_model('source_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    target = empty_dataset.create_model('target_model_{}'.format(uuid4()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert link.id == source_rec.get_linked_value(link.id).id

    # delete the link
    source_rec.unlink(link.id)
    assert not any(link.target == target_rec.id for link in source_rec.get_linked_values())
