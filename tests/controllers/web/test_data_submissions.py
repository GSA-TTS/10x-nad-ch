from flask_login import login_user, logout_user
import pytest
from nad_ch.config import create_app_context
from nad_ch.controllers.web.flask import create_flask_application
from nad_ch.core.entities import DataProducer, User


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

        yield client

        logout_user()


def test_data_submissions_index_route_should_be_protected_by_auth(client):
    response = client.get("/data-submissions")
    assert response.status_code == 401


def test_data_submissions_index_route(logged_in_client):
    response = logged_in_client.get("/data-submissions")
    assert response.status_code == 200
    assert "Submissions" in response.data.decode("utf-8")


def test_data_submission_show_route_should_be_protected_by_auth(client):
    submission_id = "some_valid_id"
    response = client.get(f"/data-submissions/{submission_id}")
    assert response.status_code == 401
