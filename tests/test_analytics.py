import uuid
import pytest


@pytest.fixture(scope='module')
def graph_view(simple_graph):
    dataset = simple_graph.dataset
    name = 'patient-view-{}'.format(uuid.uuid4())

    view = dataset.create_graph_view(name, 'patient', ['medication'])

    assert view.name == name
    assert view.root_model == 'patient'
    assert view.included_models == ['medication']

    return view


def test_get_graph_view(simple_graph, graph_view):
    dataset = simple_graph.dataset

    # TODO: update this to retrieve by name
    got_view = dataset.get_graph_view(graph_view.id)
    assert got_view.name == graph_view.name
    assert got_view.root_model == 'patient'
    assert got_view.included_models == ['medication']


def test_graph_view_instances(simple_graph, graph_view):

    graph_view.snapshot()
