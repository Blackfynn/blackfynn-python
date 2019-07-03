import pytest

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
from tests.utils import create_test_dataset, current_ts

### Create a fresh dataset for each test:
@pytest.fixture(scope='function')
def dataset(client):
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
def test_make_linked_property(dataset):
    # make a new model
    model = dataset.create_model('my_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])

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
def test_add_linked_property(dataset):
    dataset.models()
    # Create two models and link one to the other
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link', target, 'my linked property')

    # Make sure newly created link is accessible through the API
    assert any(prop.name == 'link' for prop in dataset.get_linked_properties())
    assert dataset.get_topology()['linked_properties'][0].name == 'link'
    assert 'link' in source.linked
    
def test_add_linked_property_bulk(dataset):
    # Link one model to three others
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target1 = dataset.create_model('target_model1_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target2 = dataset.create_model('target_model2_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target3 = dataset.create_model('target_model3_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link1', target1, '1st linked property')
    source.add_linked_property('link2', target2, '2nd linked property')
    source.add_linked_property('link3', target3, '3rd linked property')

    # Make sure newly created link is accessible through the API
    assert len(dataset.get_linked_properties()) == 3
    assert len(dataset.get_topology()['linked_properties']) == 3
    assert len(source.linked) == 3

def test_edit_linked_property(dataset):
    # make a model and add a linked property
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    link = source.add_linked_property('link', target, 'my linked property')

    # edit the linked property and update model
    link.display_name = 'updated linked property'
    link.position = 99
    source.update()
    
    # Make sure changes were saved
    #new_link = next(p for p in dataset.get_linked_properties() if p.name == 'link')
    new_link = source.get_linked_property('link')
    assert new_link.position == 99
    assert new_link.display_name == 'updated linked property'

def test_delete_linked_property(dataset):
    # make a model and add a linked property
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    source.add_linked_property('link', target, 'my linked property')

    # delete the link
    source.remove_linked_property('link')

    # Make sure changes were saved
    assert 'link' not in source.linked
    assert len(dataset.get_linked_properties()) == 0


### Testing linked property values
def test_add_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert any(link.target == target_rec.id for link in source_rec.get_links())

def test_get_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert link.id == source_rec.get_link(link.id).id

def test_remove_link(dataset):
    # make a model and add a linked property
    source = dataset.create_model('source_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    target = dataset.create_model('target_model_{}'.format(current_ts()), schema=[ModelProperty('name', title=True)])
    prop = source.add_linked_property('link', target, 'my linked property')

    # make records and link them
    source_rec = source.create_record({'name': 'source_record'})
    target_rec = target.create_record({'name': 'target_record'})
    link = source_rec.link_to(target_rec, prop)
    assert link.id == source_rec.get_link(link.id).id

    # delete the link
    source_rec.unlink(link.id)
    assert not any(link.target == target_rec.id for link in source_rec.get_links())
