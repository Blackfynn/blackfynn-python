import pytest

from blackfynn.models import ModelProperty, ModelTemplate


@pytest.mark.skip(reason="Model schema service is soon to be deprecated")
def test_templates(client, dataset):

    template_1 = ModelTemplate(
        name="Test Template",
        description="This is a test",
        category="Person",
        properties=dict(
            name=dict(type="string", description="Name"),
            DOB=dict(type="string", format="date", description="Date of Birth"),
            Weight=dict(type="number", unit="lbs", description="Weight"),
        ),
        required=["name"],
    )

    # Validate template schema
    validation_response_1 = client.validate_model_template(template=template_1)

    assert validation_response_1 == True

    validation_response_2 = client.validate_model_template(
        name="Validation Test",
        category="Person",
        properties=[("name", "string"), ("Weight", "number")],
    )

    assert validation_response_2 == True

    with pytest.raises(Exception):
        client.validate_model_template(
            name="Invalid Template",
            category="Test",
            properties=[("name", "string"), ("Weight", "invalid-type")],
        )

    # Create a new template
    new_template = client.create_model_template(template=template_1)
    assert isinstance(new_template, ModelTemplate)

    # Create another new template
    template_2 = client.create_model_template(
        name="Another Test Template",
        category="Person",
        properties=[("name", "string"), ("DOB", "date"), ("Weight", "number")],
    )
    assert isinstance(template_2, ModelTemplate)

    # Try to create an invalid template
    with pytest.raises(Exception):
        client.create_model_template(
            name="Bad Template",
            category="Person",
            properties=[("invalid:name", "string")],
        )

    # Get a template
    result = client.get_model_template(new_template.id)
    assert isinstance(result, ModelTemplate)
    assert result.description == "This is a test"
    assert result.category == "Person"

    # Get all templates belonging to the current organization
    all_templates = client.get_model_templates()
    assert isinstance(all_templates[0], ModelTemplate)

    # Apply a template to a dataset
    applied = dataset.import_model(new_template)
    assert isinstance(applied[0], ModelProperty)

    # Delete templates
    client.delete_model_template(new_template.id)
    client.delete_model_template(template_2.id)

    with pytest.raises(Exception):
        client.get_model_template(new_template.id)
