import pytest
from nad_ch.application.use_cases.column_maps import (
    add_column_map,
    get_column_map,
    get_column_maps_by_producer,
    update_column_mapping,
    update_column_mapping_field,
)
from nad_ch.application.view_models import ColumnMapViewModel
from nad_ch.core.entities import DataProducer, User
from nad_ch.config import create_app_context


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_add_column_map_is_valid(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))

    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    result = add_column_map(app_context, user.id, "Test", mapping)

    assert isinstance(result, ColumnMapViewModel)
    assert result.name == "Test"


def test_add_column_map_is_invalid(app_context):
    mapping = {"a": "b", "c": "d"}
    with pytest.raises(ValueError):
        add_column_map(app_context, 1, "Test", mapping)


def test_get_column_map(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))

    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    saved_column_map = add_column_map(app_context, user.id, "Test", mapping)
    result = get_column_map(app_context, saved_column_map.id)

    assert isinstance(result, ColumnMapViewModel)
    assert result.name == "Test"


def test_get_column_maps_by_producer(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))

    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    add_column_map(app_context, user.id, "Test", mapping)
    result = get_column_maps_by_producer(app_context, "New Jersey")

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], ColumnMapViewModel)
    assert result[0].name == "Test"


def test_update_column_mapping(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))

    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    cm = add_column_map(app_context, user.id, "Test", mapping)
    result = update_column_mapping(
        app_context,
        cm.id,
        {
            "Add_Number": "address_number",
            "St_Name": "street_name",
            "St_PosTyp": "street_position_type",
            "Unit": "unit",
            "Inc_Muni": "city",
            "Post_City": "post_city",
            "DataSet_ID": "guid",
        },
    )
    assert isinstance(result, ColumnMapViewModel)
    assert result.mapping["DataSet_ID"] == "guid"


def test_update_column_mapping_field(app_context):
    nj = app_context.producers.add(DataProducer("New Jersey"))
    user = app_context.users.add(User("test@test.org", "foo", "bar", True, nj))

    mapping = {
        "Add_Number": "address_number",
        "St_Name": "street_name",
        "St_PosTyp": "street_position_type",
        "Unit": "unit",
        "Inc_Muni": "city",
        "Post_City": "post_city",
        "DataSet_ID": "id",
    }

    cm = add_column_map(app_context, user.id, "Test", mapping)
    result = update_column_mapping_field(app_context, cm.id, "guid", "DataSet_ID")

    assert isinstance(result, ColumnMapViewModel)
    assert result.mapping["DataSet_ID"] == "guid"
