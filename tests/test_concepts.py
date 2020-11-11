import datetime
from collections import namedtuple

import pytest
from past.builtins import unicode  # Alias of str in Python 3

from blackfynn.models import (
    DataPackage,
    ModelProperty,
    ModelPropertyEnumType,
    ModelPropertyType,
)
from tests.utils import create_test_dataset, current_ts, get_test_client


@pytest.mark.parametrize(
    "from_type,blackfynn_type,data_type",
    [
        (int, "long", int),
        (ModelPropertyType(data_type=int), "long", int),
        (ModelPropertyType(data_type=unicode), "string", unicode),
        (datetime.date, "date", datetime.date),
        ("date", "date", datetime.datetime),
        (ModelPropertyType(data_type=str, format="date"), "string", str),
    ],
)
def test_model_type_conversion(from_type, blackfynn_type, data_type):
    property_type = ModelPropertyType._build_from(from_type)
    assert property_type.data_type == data_type
    assert property_type._blackfynn_type == blackfynn_type


@pytest.mark.parametrize(
    "json,data_type,format,unit",
    [
        ("string", unicode, None, None),
        ({"type": "string", "format": "date"}, unicode, "date", None),
        ({"type": "double", "unit": "kg"}, float, None, "kg"),
    ],
)
def test_model_type_from_dict(json, data_type, format, unit):
    decoded = ModelPropertyType._build_from(json)
    assert isinstance(decoded, ModelPropertyType)
    assert decoded.data_type == data_type
    assert decoded.format == format
    assert decoded.unit == unit


def test_rollback_model_creation_with_invalid_properties(dataset):
    model_name = "New_Model_{}".format(current_ts())
    invalid_schema = [("an_integer", int, "An Integer")]

    # Creating the model succeeds, but then creating properties fails
    with pytest.raises(Exception) as e:
        dataset.create_model(
            model_name,
            schema=invalid_schema,
        )
    assert "Could not create model properties" in str(e.value)

    # Model creation is rolled back
    assert model_name not in dataset.models()


def test_date_formatting():
    d1 = datetime.datetime(2018, 8, 24, 15, 11, 25)
    assert (
        ModelPropertyType(datetime.datetime)._encode_value(d1)
        == "2018-08-24T15:11:25.000000+00:00"
    )

    d2 = datetime.datetime(2018, 8, 24, 15, 11, 25, 1)
    assert (
        ModelPropertyType(datetime.datetime)._encode_value(d2)
        == "2018-08-24T15:11:25.000001+00:00"
    )


def test_boolean_string():
    assert ModelPropertyType(bool)._decode_value("false") == False
    assert ModelPropertyType(bool)._decode_value("true") == True
    assert ModelPropertyType(bool)._decode_value("nope") == True


def test_models(dataset):
    schema = [
        ("an_integer", int, "An Integer", True),
        ("a_bool", bool),
        ("a_string", str),
        ("a_datetime", datetime.datetime),
    ]
    display_name = "A New Property"
    description = "a new description"
    values = {
        "an_integer": 100,
        "a_bool": True,
        "a_string": "fnsdlkn#$#42nlfds$3nlds$#@$23fdsnfkls",
        "a_datetime": datetime.datetime.now(),
    }

    #################################
    ## Models
    ################################

    models = dataset.models()

    new_model = dataset.create_model(
        "New_Model_{}".format(current_ts()), "A New Model", "a new model", schema
    )

    assert len(dataset.models()) == len(models) + 1

    assert dataset.get_model(new_model.id) == new_model
    assert dataset.get_model(new_model.type) == new_model

    # Check that local changes get propagated
    new_model.add_property("a_new_property", str, display_name)
    new_model.description = description
    new_model.update()
    new_model = dataset.get_model(new_model.id)
    assert new_model.description == description
    assert new_model.get_property("a_new_property").display_name == display_name

    new_model.add_properties(
        [
            ("a_new_float", float),
            {"name": "a_new_int", "data_type": int},
            "a_new_string",
        ]
    )
    assert new_model.get_property("a_new_float").type == float
    assert new_model.get_property("a_new_int").type == int
    assert new_model.get_property("a_new_string").type == unicode

    nc_one = new_model.create_record(values)
    nc_two = new_model.create_record(
        {
            "an_integer": 1,
            "a_bool": False,
            "a_string": "",
            "a_datetime": datetime.datetime.now(),
        }
    )
    nc_three = new_model.create_record(
        {
            "an_integer": 10000,
            "a_bool": False,
            "a_string": "43132312",
            "a_datetime": datetime.datetime.now(),
        }
    )
    nc_four = new_model.create_record(
        {"an_integer": 9292, "a_datetime": datetime.datetime.now()}
    )

    nc_delete_one = new_model.create_record(
        {"an_integer": 28, "a_datetime": datetime.datetime.now()}
    )
    nc_delete_two = new_model.create_record(
        {"an_integer": 300, "a_datetime": datetime.datetime.now()}
    )

    with pytest.raises(Exception):
        new_model.create_record()

    new_models_old = new_model.get_all()
    assert new_model.get_all(limit=1) == new_models_old[:1]
    assert new_model.get_all(limit=2, offset=2) == new_models_old[2:4]

    new_model.delete_records(nc_delete_one, nc_delete_two.id)
    new_models = new_model.get_all()

    assert len(new_models) == (len(new_models_old) - 2)

    assert nc_two.model == new_model
    assert nc_two.get("a_string") == ""

    nc_four.set("a_string", "hello")
    assert nc_four.get("a_string") == new_model.get(nc_four).get("a_string")

    with pytest.raises(Exception):
        nc_four.set("an_integer", datetime.datetime.now())

    assert nc_four.get("an_integer") == 9292
    nc_four.set("an_integer", 10)
    assert nc_four.get("an_integer") == 10

    nc_delete_three = new_model.create_record(
        {"an_integer": 684, "a_string": "delete me"}
    )
    assert len(new_model.get_all()) == len(new_models) + 1
    nc_delete_three.delete()
    assert len(new_model.get_all()) == len(new_models)

    # cannot add a record id column using an existing name
    with pytest.raises(ValueError):
        new_model.get_all().as_dataframe(
            record_id_column_name=list(new_model.get_all().type.schema.keys())[0]
        )

    # assert no extra columns are added by default
    df_cs_no_rec = new_model.get_all().as_dataframe()
    assert len(df_cs_no_rec.columns) == len(new_model.get_all().type.schema.keys())

    # assert record id column is added when arg is present and valid
    df_cs = new_model.get_all().as_dataframe(record_id_column_name="record_id")

    # confirm that all record ids are present in this dataframe
    assert "record_id" in df_cs.columns
    for record in new_model.get_all():
        assert not df_cs.query("record_id == @record.id").empty

    #################################
    ## Relationships
    ################################

    relationships = dataset.relationships()

    new_relationship = dataset.create_relationship_type(
        "New_Relationship_{}".format(current_ts()), "a new relationship"
    )

    assert len(dataset.relationships()) == len(relationships) + 1

    assert dataset.get_relationship(new_relationship.id) == new_relationship
    assert dataset.get_relationship(new_relationship.type) == new_relationship

    nr_one = new_relationship.relate(nc_one, nc_two)
    nr_four = new_relationship.relate(nc_four, nc_one)
    nr_five = new_relationship.relate(nc_four, nc_two)

    nr_two = nc_two.relate_to(nc_three, new_relationship)
    nr_three = nc_three.relate_to(nc_four, new_relationship)
    nr_six = nc_four.relate_to(nc_three, new_relationship)
    nr_seven = nc_four.relate_to(nc_one, relationship_type="goes_to")

    assert nr_seven[0].destination == nc_one.id
    assert nr_seven[0].source == nc_four.id
    assert nr_seven[0].type == "goes_to"
    assert len(nc_four.get_related(new_model.type)) == 5

    new_relationships = new_relationship.get_all()

    nr_delete_three = new_relationship.relate(nc_one, nc_three)

    assert len(new_relationship.get_all()) == len(new_relationships) + 1
    nr_delete_three.delete()
    assert len(new_relationship.get_all()) == len(new_relationships)

    df_rs = new_relationship.get_all().as_dataframe()

    p = DataPackage("test-csv", package_type="CSV")
    dataset.add(p)
    dataset.update()
    assert p.exists

    p.relate_to(nc_one)
    p.relate_to(nc_two)
    nc_three.relate_to(p, new_relationship)
    new_relationship.relate(nc_four, p)

    assert len(nc_four.get_related(new_model.type)) == 5


def test_simple_model_properties(dataset):

    # Define properties as tuples
    model_with_basic_props_1 = dataset.create_model(
        "Basic_Props_1",
        description="a new description",
        schema=[
            ("an_integer", int, "An Integer", True),
            ("a_bool", bool),
            ("a_string", str),
            ("a_date", datetime.datetime),
        ],
    )

    assert dataset.get_model(model_with_basic_props_1.id) == model_with_basic_props_1

    # Add a property with a description
    model_with_basic_props_1.add_property(
        "a_new_property", float, display_name="Weight", description="some metric"
    )

    updated_model_1 = dataset.get_model(model_with_basic_props_1.id)

    test_prop = updated_model_1.get_property("a_new_property")
    assert test_prop.display_name == "Weight"
    assert test_prop.description == "some metric"

    # Define properties as ModelProperty objects
    model_with_basic_props_2 = dataset.create_model(
        "Basic_Props_2",
        description="a new description",
        schema=[
            ModelProperty("name", data_type=str, title=True, required=True),
            ModelProperty("age", data_type=int),
            ModelProperty("DOB", data_type=datetime.datetime),
        ],
    )

    assert dataset.get_model(model_with_basic_props_2.id) == model_with_basic_props_2

    # Add a property
    model_with_basic_props_2.add_property(
        "weight2", ModelPropertyType(data_type=float), display_name="Weight"
    )

    updated_model_2 = dataset.get_model(model_with_basic_props_2.id)

    assert updated_model_2.get_property("weight2").display_name == "Weight"
    assert updated_model_2.get_property("name").required == True

    # Define properties as ModelProperty objects with ModelPropertyType data_type
    model_with_basic_props_3 = dataset.create_model(
        "Basic_Props_3",
        description="a new description",
        schema=[
            ModelProperty(
                "name", data_type=ModelPropertyType(data_type=str), title=True
            ),
            ModelProperty("age", data_type=ModelPropertyType(data_type=int)),
            ModelProperty("DOB", data_type=ModelPropertyType(data_type=str)),
        ],
    )

    assert dataset.get_model(model_with_basic_props_3.id) == model_with_basic_props_3

    # Add a property
    model_with_basic_props_3.add_property(
        "weight3", ModelPropertyType(data_type=float), display_name="Weight"
    )

    updated_model_3 = dataset.get_model(model_with_basic_props_3.id)

    assert updated_model_3.get_property("weight3").display_name == "Weight"

    # Reverse look up property data types
    ModelProperty("name", data_type="string", title=True, required=True)
    model_with_basic_props_4 = dataset.create_model(
        "Basic_Props_4",
        description="a new description",
        schema=[
            ModelProperty("name", data_type="string", title=True, required=True),
            ModelProperty("age", data_type="long"),
            ModelProperty("DOB", data_type="date"),
        ],
    )

    assert dataset.get_model(model_with_basic_props_4.id) == model_with_basic_props_4

    # Add a property
    model_with_basic_props_4.add_property(
        "weight4", ModelPropertyType(data_type="double"), display_name="Weight"
    )

    updated_model_4 = dataset.get_model(model_with_basic_props_4.id)

    assert updated_model_4.get_property("weight4").display_name == "Weight"
    assert updated_model_4.get_property("name").required == True


def test_model_property_default_field_inherits_from_required_field(dataset):
    """
    Unless explictly set, the `default` field on a property takes the value of
    the `required` field.
    """
    model = dataset.create_model(
        "Default_properties_model",
        description="",
        schema=[
            ModelProperty("name", data_type="string", title=True),
            ModelProperty("required", data_type="string", required=True),
            ModelProperty("not_required", data_type="string", required=False),
        ],
    )

    model = dataset.get_model(model)
    assert model.get_property("required").required is True
    assert model.get_property("required").default is True

    assert model.get_property("not_required").required is False
    assert model.get_property("not_required").default is False

    model.create_record({"name": "Record #1", "required": "yes"})


def test_model_title_is_a_required_property_by_default(dataset):
    model = dataset.create_model(
        "Concept_title_model",
        description="",
        schema=[
            ModelProperty("name", data_type="string", title=True),
        ],
    )

    model = dataset.get_model(model)
    assert model.get_property("name").title is True
    assert model.get_property("name").required is True


def test_complex_model_properties(dataset):
    model_with_complex_props = dataset.create_model(
        "Complex_Props",
        description="a new description",
        schema=[
            ModelProperty(
                "name", data_type=ModelPropertyType(data_type=str), title=True
            ),
            ModelProperty("age", data_type=ModelPropertyType(data_type=int)),
            ModelProperty(
                "email", data_type=ModelPropertyType(data_type=str, format="email")
            ),
        ],
    )

    assert dataset.get_model(model_with_complex_props.id) == model_with_complex_props

    # Add a property
    model_with_complex_props.add_property(
        "weight", ModelPropertyType(data_type=float, unit="kg"), display_name="Weight"
    )

    updated_model = dataset.get_model(model_with_complex_props.id)

    weight_property = updated_model.get_property("weight")
    assert weight_property.display_name == "Weight"
    assert weight_property.type == float
    assert weight_property._type.data_type == float
    assert weight_property._type.format == None
    assert weight_property.unit == "kg"

    email_property = model_with_complex_props.get_property("email")
    assert email_property.type == unicode
    assert email_property._type.data_type == unicode
    assert email_property._type.format.lower() == "email"
    assert email_property.unit == None

    good_values = {"name": "Bob", "age": 1, "email": "test@test.com", "weight": 10}
    good_record = updated_model.create_record(good_values)

    bad_values = {"name": "Bob", "age": 1, "email": "123455", "weight": 10}

    with pytest.raises(Exception):
        bad_record = updated_model.create_record(bad_values)


def test_get_connected(dataset):
    model_1 = dataset.create_model(
        "Model_A",
        description="model a",
        schema=[
            ModelProperty(
                "prop1", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    related_models = model_1.get_connected()
    # For a single, unconnected model, it should return nothing
    assert len(related_models) == 0

    model_2 = dataset.create_model(
        "Model_B",
        description="model b",
        schema=[
            ModelProperty(
                "prop1", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    relationship = dataset.create_relationship_type(
        "New_Relationship_{}".format(current_ts()), "a new relationship"
    )

    model_instance_1 = model_1.create_record({"prop1": "val1"})
    model_instance_2 = model_2.create_record({"prop1": "val1"})
    model_instance_1.relate_to(model_instance_2, relationship)

    related_models = model_1.get_connected()
    assert len(related_models) == 2

    # For a connected model, return all connections + the model itself
    related_models = model_2.get_connected()
    assert len(related_models) == 2

    # Check that get_connected_models from the dataset object also works
    related_models = dataset.get_connected_models(model_1.id)
    assert len(related_models) == 2

    related_models = dataset.get_connected_models(model_2.id)
    assert len(related_models) == 2


def test_array_model_properties(dataset):
    model = dataset.create_model(
        "Array_Properties",
        description="Description",
        schema=[
            ModelProperty("name", data_type=str, title=True),
            ModelProperty(
                "int_array",
                data_type=ModelPropertyEnumType(data_type=int, multi_select=True),
            ),
        ],
    )

    int_array = model.get_property("int_array")
    assert int_array.type == int
    assert int_array.multi_select == True
    assert int_array.enum == None

    record = model.create_record({"name": "A", "int_array": [1, 2, 3]})
    bulk_records = model.create_records(
        [
            {"name": "B", "int_array": [1, 2, 3]},
            {"name": "B", "int_array": [1, 2, 3]},
            {"name": "B", "int_array": [1, 2, 3]},
        ]
    )

    gotten = model.get_all()
    assert all(x.values["int_array"] == [1, 2, 3] for x in gotten)


def test_enum_model_properties(dataset):
    model = dataset.create_model(
        "Enum_Props",
        description="a new description",
        schema=[
            ModelProperty("name", data_type=str, title=True),
            ModelProperty(
                "int_enum",
                data_type=ModelPropertyEnumType(
                    data_type=float, enum=[1.0, 2.0, 3.0], unit="cm", multi_select=False
                ),
            ),
            ModelProperty(
                "str_enum",
                data_type=ModelPropertyEnumType(
                    data_type=str, enum=["foo", "bar", "baz"], multi_select=True
                ),
            ),
        ],
    )

    assert model == dataset.get_model(model.id)

    int_enum = model.get_property("int_enum")
    str_enum = model.get_property("str_enum")

    assert int_enum.type == float
    assert int_enum.multi_select == False
    assert int_enum.enum == [1.0, 2.0, 3.0]
    assert int_enum.unit == "cm"

    assert str_enum.type == unicode
    assert str_enum.multi_select == True
    assert str_enum.enum == ["foo", "bar", "baz"]

    record = model.create_record(
        {"name": "A", "int_enum": 1.0, "str_enum": ["foo", "bar"]}
    )

    gotten = model.get_all()[0]
    assert gotten.values["int_enum"] == 1.0
    assert set(gotten.values["str_enum"]) == set(["foo", "bar"])

    with pytest.raises(Exception, match=r"Value '5' is not a member*"):
        model.create_record({"name": "A", "int_enum": 5, "str_enum": ["foo", "bar"]})

    with pytest.raises(Exception, match=r"Value 'blah' is not a member*"):
        model.create_record({"name": "A", "int_enum": 1.0, "str_enum": ["blah"]})


Graph = namedtuple(
    "TestGraph",
    ["dataset", "models", "model_records", "relationships", "relationship_records"],
)


@pytest.fixture(scope="module")
def simple_graph(client):
    """
    Creates a small test graph in an independent dataset to de-couple
    from other tests
    """
    test_dataset = create_test_dataset(client)
    model_1 = test_dataset.create_model(
        "Model_A",
        description="model a",
        schema=[
            ModelProperty(
                "prop1", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    model_2 = test_dataset.create_model(
        "Model_B",
        description="model b",
        schema=[
            ModelProperty(
                "prop1", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    relationship = test_dataset.create_relationship_type(
        "New_Relationship_{}".format(current_ts()), "a new relationship"
    )

    model_instance_1 = model_1.create_record({"prop1": "val1"})
    model_instance_2 = model_2.create_record({"prop1": "val1"})
    model_instance_1.relate_to(model_instance_2, relationship)

    graph = Graph(
        test_dataset,
        models=[model_1, model_2],
        model_records=[model_instance_1, model_instance_2],
        relationships=[relationship],
        relationship_records=None,
    )
    yield graph

    ds_id = test_dataset.id
    client._api.datasets.delete(test_dataset)
    all_dataset_ids = [x.id for x in client.datasets()]
    assert ds_id not in all_dataset_ids
    assert not test_dataset.exists


def test_get_related_models(simple_graph):
    related_models = simple_graph.models[0].get_related()
    assert len(related_models) == 1
    assert related_models[0].type == simple_graph.models[1].type


def test_related_records_pagination(dataset):
    patient = dataset.create_model(
        "patient",
        description="patient",
        schema=[
            ModelProperty(
                "name", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    visit = dataset.create_model(
        "visit",
        description="visit",
        schema=[
            ModelProperty(
                "field", data_type=ModelPropertyType(data_type=str), title=True
            )
        ],
    )

    attends = dataset.create_relationship_type("attends", "an attendance")

    fred = patient.create_record({"name": "Fred"})
    visits = visit.create_records([{"field": str(i)} for i in range(200)])

    fred.relate_to(visits, attends)

    # Get all records
    gotten = fred.get_related()
    assert len(gotten) == 200
    assert [int(r.get("field")) for r in gotten] == list(range(200))


def test_stringified_boolean_values(dataset):
    ppatient = dataset.create_model(
        "potential_patient",
        description="potential patient",
        schema=[
            ModelProperty(
                "name", data_type=ModelPropertyType(data_type=str), title=True
            ),
            ModelProperty("sick", data_type=ModelPropertyType(data_type=bool)),
        ],
    )

    ppatient.create_record({"name": "Fred", "sick": "false"})
    ppatient.create_record({"name": "Joe", "sick": "true"})
    ppatient.create_record({"name": "Adele", "sick": "plop"})

    # Get all records
    gotten = ppatient.get_all()
    assert len(gotten) == 3
    assert gotten[0]._values["sick"].value == False
    assert gotten[1]._values["sick"].value == True
    assert gotten[2]._values["sick"].value == True


def test_get_topology(simple_graph):
    topology = simple_graph.dataset.get_topology()
    assert "models" in topology
    assert len(topology["models"]) == 2
    assert "relationships" in topology
    assert len(topology["relationships"]) == 1


def test_get_graph_summary(simple_graph):
    summary = simple_graph.dataset.get_graph_summary()
    expected_fields = [
        "modelCount",
        "modelRecordCount",
        "modelSummary",
        "relationshipCount",
        "relationshipRecordCount",
        "relationshipSummary",
        "relationshipTypeCount",
        "relationshipTypeSummary",
    ]
    for f in expected_fields:
        assert f in summary.keys()

    assert summary["modelCount"] == 2
    assert summary["modelRecordCount"] == 2
    assert summary["relationshipCount"] == 1
    assert summary["relationshipRecordCount"] == 1
    assert summary["relationshipTypeCount"] == 1


def test_simple_query(simple_graph):
    model_a = simple_graph.dataset.get_model("Model_A")
    model_b = simple_graph.dataset.get_model("Model_B")

    # Filter via a model name:
    assert len(model_a.query().filter("prop1", "eq", "val1").run()) == 1
    assert len(model_a.query().filter("prop1", "eq", "not-present").run()) == 0

    # Join via a model name:
    assert len(model_a.query().join("Model_B", ("prop1", "eq", "val1")).run()) == 1
    assert len(model_a.query().join("Model_B", ("prop1", "eq", "val2")).run()) == 0

    # Filter via a model instance:
    assert len(model_a.query().filter("prop1", "eq", "val1").run()) == 1
    assert len(model_a.query().filter("prop1", "eq", "not-present").run()) == 0

    # Join via a model instance:
    assert len(model_a.query().join(model_b, ("prop1", "eq", "val1")).run()) == 1
    assert len(model_a.query().join(model_b, ("prop1", "eq", "val2")).run()) == 0

    # use select, join, and filter:
    result = (
        model_a.query()
        .select(model_b)
        .filter("prop1", "eq", "val1")
        .join(model_b, ("prop1", "eq", "val1"))
        .run()
    )

    assert len(result) == 1
    assert len(result[0].items()) == 1
    assert result[0].target.type == model_a.type
    assert result[0].get(model_b).type == model_b.type

    # and with an offset of 1:
    result = (
        model_a.query()
        .select(model_b)
        .filter("prop1", "eq", "val1")
        .join(model_b, ("prop1", "eq", "val1"))
        .offset(1)
        .run()
    )
    assert len(result) == 0

    # and with a limit of 0:
    result = (
        model_a.query()
        .select(model_b)
        .filter("prop1", "eq", "val1")
        .join(model_b, ("prop1", "eq", "val1"))
        .limit(0)
        .run()
    )
    assert len(result) == 0
