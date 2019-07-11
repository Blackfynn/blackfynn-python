import uuid
import pytest
import time

from pkg_resources import resource_filename

from blackfynn.models import DataPackage, TimeSeries
from blackfynn.api.agent import AgentError


def _resource_path(fname):
    return resource_filename('tests.resources', fname)

# All test assets need to use this "test-78f3ea50" prefix so failures caused by
# deleting datasets before processing all assests can be filtered out of
# production error notifications.
FILE1      = _resource_path('test-78f3ea50.txt')
FILE2      = _resource_path('test-78f3ea50.csv')
FILE3      = _resource_path('test-78f3ea50.png')
FILE_EMPTY = _resource_path('test-78f3ea50.empty')
FLAT_DIR   = _resource_path('flat_dir')
NESTED_DIR = _resource_path('nested_dir')
INNER_DIR  = 'inner_dir'


@pytest.mark.agent
def test_upload_with_agent_to_dataset(client, dataset):
    n = len(dataset.items)
    dataset.upload(FILE1, use_agent=True, display_progress=True)
    dataset.update()

    # Check that we've added an item to the dataset root
    assert n + 1 == len(dataset.items)


@pytest.mark.agent
@pytest.mark.parametrize('upload_args,n_files', [
    (['requirements.txt'], 1),  # Single file
    ([FILE1], 1),               # Single file with path
    ([[FILE1, FILE2]], 2),      # Multiple files
])
def test_upload_with_agent_to_collection(client, dataset, upload_args, n_files):
    collection = dataset.create_collection(str(uuid.uuid4()))
    resp = collection.upload(*upload_args, use_agent=True)

    assert len(collection.items) == n_files


@pytest.mark.agent
@pytest.mark.parametrize('upload_args, n_files', [
    ([FLAT_DIR], 3),
    ([NESTED_DIR], 1),
    ([NESTED_DIR + '/' + INNER_DIR], 2),
])
def test_upload_with_agent_directory(client, dataset, upload_args, n_files):
    collection = dataset.create_collection(str(uuid.uuid4()))
    collection.upload(upload_args, use_agent=True)
    assert len(collection.items) == n_files


@pytest.mark.agent
def test_upload_with_agent_recursive(client, dataset):
    collection = dataset.create_collection(str(uuid.uuid4()))
    collection.upload(NESTED_DIR, recursive=True, use_agent=True)

    assert len(collection.items) == 1
    nested_dir = collection.items[0]
    assert len(nested_dir.items) == 2
    inner_dir = next(pkg for pkg in nested_dir.items if pkg.name == INNER_DIR)
    assert len(inner_dir.items) == 2


@pytest.mark.agent
def test_upload_with_agent_recursive_flag_is_not_allowed_with_file(client, dataset):
    collection = dataset.create_collection(str(uuid.uuid4()))
    with pytest.raises(AgentError):
        collection.upload(FILE1, recursive=True, use_agent=True)


@pytest.mark.agent
def test_upload_with_agent_cannot_upload_multiple_directories(client, dataset):
    with pytest.raises(AgentError):
        dataset.upload(FLAT_DIR, FILE1, use_agent=True)


@pytest.mark.agent
@pytest.mark.parametrize('append_args,n_files', [
    ([FILE1], 1),          # Single file
    ([FILE1, FILE2], 2),   # Multiple files, separate arguments
    ([[FILE1, FILE2]], 2), # Multiple files, single argument list
])
def test_append_with_agent(client, dataset, append_args, n_files):
    # TimeSeries package to append into...
    pkg = TimeSeries('Rando Timeseries')
    dataset.add(pkg)

    # TODO: test results/platform state
    pkg.append_files(*append_args, use_agent=True)


@pytest.mark.parametrize('upload_args,n_files', [
    ([FILE1], 1),          # Single file
    ([FILE1, FILE2], 2),   # Multiple files, separate arguments
    ([[FILE1, FILE2]], 2), # Multiple files, single argument list
])
def test_upload(client, dataset, upload_args, n_files):
    """
    Note: ETL will fail since destination will likely be removed
          before being processed.
    """
    resp = dataset.upload(*upload_args, use_agent=False)
    assert len(resp) == n_files

    for r in resp:
        manifest = r[0]['manifest']
        assert manifest['content'] is not None
        assert manifest['type'] == 'upload'


def test_cannot_upload_to_package(client, dataset):
    pkg = DataPackage('Rando Thing', package_type='MRI')
    dataset.add(pkg)

    with pytest.raises(Exception):
        pkg.upload(FILE1, use_agent=False)


def test_cannot_upload_directory_using_s3(client, dataset):
    with pytest.raises(Exception):
        dataset.upload(FLAT_DIR, use_agent=False)


@pytest.mark.parametrize('append_args,n_files', [
    ([FILE1], 1),          # Single file
    ([FILE1, FILE2], 2),   # Multiple files, separate arguments
    ([[FILE1, FILE2]], 2), # Multiple files, single argument list
])
def test_append(client, dataset, append_args, n_files):
    """
    Note: ETL will fail for append, because... it's a text file.
          But also because the destination will likely be removed
          before the ETL actually places the new node there.
    """
    # TimeSeries package to append into...
    pkg = TimeSeries('Rando Timeseries')
    dataset.add(pkg)

    # upload/append file into package
    resp = pkg.append_files(*append_args, use_agent=False)
    assert len(resp) == n_files

    for r in resp:
        manifest = r[0]['manifest']
        assert manifest['content'] is not None
        assert manifest['type'] == 'append'


def test_progress_for_empty_files(dataset):
    dataset.upload(FILE_EMPTY, display_progress=True, use_agent=False)
