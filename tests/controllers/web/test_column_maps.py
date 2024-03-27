from flask_login import login_user, logout_user
import pytest
from nad_ch.config import create_app_context
from nad_ch.controllers.web.flask import create_flask_application
from nad_ch.core.entities import ColumnMap, DataProducer, User


@pytest.fixture
def app():
    context = create_app_context()
    app = create_flask_application(context)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client, app):
    with app.app_context(), app.test_request_context():
        producer = DataProducer("New Jersey")
        saved_producer = app.extensions["ctx"]["producers"].add(producer)

        user = User(
            "test_user@test.org",
            "test_provider",
            "test_logout_url",
            True,
            saved_producer,
        )
        saved_user = app.extensions["ctx"]["users"].add(user)
        login_user(saved_user)
        print(saved_user)
        yield client

        logout_user()


def test_column_maps_route_empty(logged_in_client):
    response = logged_in_client.get("/column-maps")
    assert response.status_code == 200
    assert "Create Your First Mapping" in response.data.decode("utf-8")


def test_column_maps_route_has_two_column_maps(logged_in_client):
    nj = logged_in_client.application.extensions["ctx"]["producers"].get_by_name(
        "New Jersey"
    )
    cm = ColumnMap(
        "Test",
        nj,
        {
            "Add_Number": "address_number",
            "AddNo_Full": "address_number_full",
            "St_Name": "street_name",
            "StNam_Full": "street_name_full",
            "County": "county",
            "Inc_Muni": "city",
            "Post_City": "post_city",
            "State": "state",
            "UUID": "guid",
            "AddAuth": "address_authority",
            "Longitude": "long",
            "Latitude": "lat",
            "NatGrid": "nat_grid",
            "Placement": "placement",
            "AddrPoint": "address_point",
            "DateUpdate": "date_updated",
            "NAD_Source": "source",
            "DataSet_ID": "id",
        },
        1,
    )
    logged_in_client.application.extensions["ctx"]["column_maps"].add(cm)
    cm_2 = ColumnMap(
        "Test2",
        nj,
        {
            "Add_Number": "address_number",
            "AddNo_Full": "address_number_full",
            "St_Name": "street_name",
            "StNam_Full": "street_name_full",
            "County": "county",
            "Inc_Muni": "city",
            "Post_City": "post_city",
            "State": "state",
            "UUID": "guid",
            "AddAuth": "address_authority",
            "Longitude": "long",
            "Latitude": "lat",
            "NatGrid": "nat_grid",
            "Placement": "placement",
            "AddrPoint": "address_point",
            "DateUpdate": "date_updated",
            "NAD_Source": "source",
            "DataSet_ID": "id",
        },
        1,
    )
    logged_in_client.application.extensions["ctx"]["column_maps"].add(cm_2)

    response = logged_in_client.get("/column-maps")
    assert response.status_code == 200
    assert "Mappings" in response.data.decode("utf-8")
