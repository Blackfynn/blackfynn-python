"""
Configure a --skip-agent command line argument for py.test that skips agent-
dependent tests.
"""
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-agent", action="store_true", help="run agent integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "agent: marks tests which require the blackfynn agent"
    )


def pytest_runtest_setup(item):
    if "agent" in item.keywords and item.config.getoption("--skip-agent"):
        pytest.skip("Skipping agent tests")
