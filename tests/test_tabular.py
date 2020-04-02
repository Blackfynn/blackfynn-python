import pdb

import pytest

from blackfynn import Tabular, TabularSchema
from blackfynn.models import TabularSchemaColumn


def test_tabular(client, dataset):
    """
    TODO: parsing of tabular/schema response from API not implemented.
    """
    t = Tabular("Some tabular data")
    assert not t.exists
    assert t.schema is None

    # create
    dataset.add(t)
    assert t.exists
    assert t.schema is None

    schema = [
        TabularSchemaColumn(
            name="",
            display_name="index",
            datatype="Integer",
            primary_key=True,
            internal=True,
        ),
        TabularSchemaColumn(
            name="",
            display_name="email",
            datatype="String",
            primary_key=False,
            internal=False,
        ),
    ]

    s = TabularSchema(name="schema", column_schema=schema)

    t.set_schema(s)
    assert t.exists
    a = t.get_schema()
    assert a.exists
