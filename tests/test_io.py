import time
import uuid

import pytest
from pkg_resources import resource_filename

from blackfynn.api.agent import AgentError
from blackfynn.models import TimeSeries


def _resource_path(fname):
    return resource_filename("tests.resources", fname)


# All test assets need to use this "test-78f3ea50" prefix so failures caused by
# deleting datasets before processing all assests can be filtered out of
# production error notifications.
FILE1 = _resource_path("test-78f3ea50.txt")
FILE2 = _resource_path("test-78f3ea50.csv")
FILE3 = _resource_path("test-78f3ea50.png")
FILE4 = _resource_path("test-78f3ea50-b.txt")
FILE_EMPTY = _resource_path("test-78f3ea50.empty")
FLAT_DIR = _resource_path("flat_dir")
NESTED_DIR = _resource_path("nested_dir")
INNER_DIR = "inner_dir"


@pytest.mark.agent
@pytest.mark.parametrize(
    "upload_args,n_files",
    [
        ([FILE4], 1),
    ],
)  # Single file
def test_get_by_filename(dataset, upload_args, n_files):

    dataset.upload(*upload_args)
    dataset.update()

    for i in range(10):
        pp = dataset.get_items_by_name("test-78f3ea50-b.txt")
        if len(pp) > 0 and pp[0].state == "READY":
            break
        else:
            time.sleep(0.5)

    packages = dataset.get_packages_by_filename("test-78f3ea50-b.txt")
    assert len(packages) == 1
    assert packages[0].name == "test-78f3ea50-b.txt"


@pytest.mark.parametrize(
    "upload_args,n_files",
    [
        ([FILE1], 1),
        ([[FILE1, FILE2]], 2),
    ],  # Single file  # Multiple files
)
def test_upload_legacy_to_collection(dataset, upload_args, n_files):
    collection = dataset.create_collection(str(uuid.uuid4()))
    collection.upload(*upload_args, use_agent=False)

    assert len(collection.items) == n_files


@pytest.mark.agent
@pytest.mark.parametrize(
    "upload_args, n_files",
    [
        ([FLAT_DIR], 3),
        ([NESTED_DIR], 1),
        ([NESTED_DIR + "/" + INNER_DIR], 2),
    ],
)
def test_upload_directory(dataset, upload_args, n_files):
    collection = dataset.create_collection(str(uuid.uuid4()))
    collection.upload(upload_args)
    assert len(collection.items) == n_files


@pytest.mark.agent
def test_upload_recursive(dataset):
    collection = dataset.create_collection(str(uuid.uuid4()))
    collection.upload(NESTED_DIR, recursive=True)

    assert len(collection.items) == 1
    nested_dir = collection.items[0]
    assert len(nested_dir.items) == 2
    inner_dir = next(pkg for pkg in nested_dir.items if pkg.name == INNER_DIR)
    assert len(inner_dir.items) == 2


@pytest.mark.agent
def test_upload_recursive_flag_is_not_allowed_with_file(dataset):
    collection = dataset.create_collection(str(uuid.uuid4()))
    with pytest.raises(AgentError):
        collection.upload(FILE1, recursive=True)


@pytest.mark.agent
def test_upload_cannot_upload_multiple_directories(dataset):
    with pytest.raises(AgentError):
        dataset.upload(FLAT_DIR, FILE1)


@pytest.mark.agent
@pytest.mark.parametrize(
    "upload_args,n_files",
    [
        ([FILE1], 1),  # Single file
        ([FILE1, FILE2], 2),  # Multiple files, separate arguments
        ([[FILE1, FILE2]], 2),  # Multiple files, single argument list
    ],
)
def test_upload_to_dataset(dataset, upload_args, n_files):
    """
    Note: ETL will fail since destination will likely be removed
          before being processed.
    """
    c = len(dataset.items)
    dataset.upload(*upload_args)
    dataset.update()
    assert len(dataset.items) == c + n_files


@pytest.mark.agent
@pytest.mark.parametrize(
    "append_args,n_files",
    [
        ([FILE1], 1),  # Single file
        ([FILE1, FILE2], 2),  # Multiple files, separate arguments
        ([[FILE1, FILE2]], 2),  # Multiple files, single argument list
    ],
)
def test_append(dataset, append_args, n_files):
    """
    Note: ETL will fail for append, because... it's a text file.
          But also because the destination will likely be removed
          before the ETL actually places the new node there.
    """
    # TimeSeries package to append into...
    pkg = TimeSeries("Rando Timeseries")
    dataset.add(pkg)

    # upload/append file into package
    pkg.append_files(*append_args)
    # TODO: assert append was successful


@pytest.mark.agent
def test_progress_for_empty_files(dataset):
    dataset.upload(FILE_EMPTY, display_progress=True)
