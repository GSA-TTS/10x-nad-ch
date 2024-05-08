import pytest
from nad_ch.application.use_cases.admin import activate_user
from nad_ch.config import create_app_context
from nad_ch.core.entities import DataProducer, User, Role


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_activate_user(app_context):
    role = app_context.roles.add(Role("producer", ["permission_a", "permission_b"]))

    user = User(
        email="test@example.com",
        login_provider="test",
        logout_url="test",
        activated=False,
    )
    app_context.users.add(user)
    producer = app_context.producers.add(DataProducer("test"))

    result = activate_user(app_context, user.id, producer.name)
    assert result.activated
    assert result.producer.name == producer.name
    assert result.roles[0].name == role.name
