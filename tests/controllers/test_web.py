import pytest
from nad_ch.config import create_app_context
from nad_ch.controllers.web.flask import create_flask_application


@pytest.fixture
def app():
    context = create_app_context()
    app = create_flask_application(context)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.data.decode("utf-8")


def test_reports_route(client):
    response = client.get("/reports")
    assert response.status_code == 200
    assert "Reports" in response.data.decode("utf-8")


def test_view_report_route(client):
    submission_id = "some_valid_id"
    response = client.get(f"/reports/{submission_id}")
    assert response.status_code == 200
    assert "Report" in response.data.decode("utf-8")
