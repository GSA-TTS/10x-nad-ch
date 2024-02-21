from flask_login import login_user, logout_user, current_user
import pytest
from nad_ch.config import create_app_context
from nad_ch.controllers.web.flask import create_flask_application
from nad_ch.domain.entities import User


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
        user = User(
            "test_user", "test_user@test.org", "test_provider", "test_logout_url"
        )
        saved_user = app.extensions["ctx"]["users"].add(user)
        login_user(saved_user)

        yield client

        logout_user()


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Login" in response.data.decode("utf-8")


def test_reports_route_should_be_protected_by_auth(client):
    response = client.get("/reports")
    assert response.status_code == 401


def test_reports_route(logged_in_client):
    response = logged_in_client.get("/reports")
    assert response.status_code == 200
    assert "Reports" in response.data.decode("utf-8")


def test_view_report_route_should_be_protected_by_auth(client):
    submission_id = "some_valid_id"
    response = client.get(f"/reports/{submission_id}")
    assert response.status_code == 401


def test_view_report_route(logged_in_client):
    submission_id = "some_valid_id"
    response = logged_in_client.get(f"/reports/{submission_id}")
    assert response.status_code == 200
    assert "Report" in response.data.decode("utf-8")
