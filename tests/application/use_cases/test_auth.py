import pytest
from nad_ch.application.exceptions import (
    InvalidEmailDomainError,
    InvalidEmailError,
    OAuth2TokenError,
)
from nad_ch.application.use_cases.auth import (
    get_logged_in_user_redirect_url,
    get_logged_out_user_redirect_url,
    get_or_create_user,
    get_oauth2_token,
    get_user_email,
    get_user_email_domain_status,
)
from nad_ch.core.entities import User
from nad_ch.config import create_app_context


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_get_or_create_user_existing_user(app_context):
    app_context.auth.make_login_url = lambda x: "test"
    email = "johnny@test.org"
    login_provider = "test"
    user = User(email=email, login_provider=login_provider, logout_url="test")
    app_context.users.add(user)
    result = get_or_create_user(app_context, login_provider, email)
    assert result == user


def test_get_or_create_user_new_user(app_context):
    email = "johnny@test.org"
    login_provider = "test"
    result = get_or_create_user(app_context, login_provider, email)
    assert isinstance(result, User)
    assert result.email == email
    assert result.login_provider == login_provider


def test_get_or_create_user_invalid_email(app_context):
    email = "my_cool_email_address"
    login_provider = "test"
    with pytest.raises(InvalidEmailError):
        get_or_create_user(app_context, login_provider, email)


def test_get_logged_in_user_redirect_url(app_context):
    app_context.auth.make_login_url = (
        lambda provider_name, state_token, acr_values=None, nonce=None: "test"
    )

    provider_name = "test_provider_name"
    state_token = "test_state_token"
    acr_values = "test_acr_value"
    nonce = "test_nonce"

    result = get_logged_in_user_redirect_url(
        app_context, provider_name, state_token, acr_values, nonce
    )

    assert result == "test"


def test_get_logged_out_user_redirect_url(app_context):
    app_context.auth.make_logout_url = lambda provider_name: "test"
    provider_name = "test"
    result = get_logged_out_user_redirect_url(app_context, provider_name)
    assert result == "test"


def test_get_oauth2_token_succeeds(app_context):
    app_context.auth.fetch_oauth2_token = lambda provider_name, code: "test"
    provider_name = "test"
    code = "some-code"
    result = get_oauth2_token(app_context, provider_name, code)
    assert result == "test"


def test_get_oauth2_token_fails(app_context):
    app_context.auth.fetch_oauth2_token = lambda provider_name, code: (
        _ for _ in ()
    ).throw(OAuth2TokenError("Error message"))
    provider_name = "test"
    code = "some-code"
    with pytest.raises(OAuth2TokenError):
        get_oauth2_token(app_context, provider_name, code)


def test_get_user_email(app_context):
    app_context.auth.fetch_user_email_from_login_provider = (
        lambda provider_name, oauth2_token: "johnny@test.org"
    )
    provider_name = "test"
    oauth2_token = "here-is-a-token"
    result = get_user_email(app_context, provider_name, oauth2_token)
    assert result == "johnny@test.org"


def test_get_user_email_domain_status(app_context):
    email = "johnny@test.org"
    result = get_user_email_domain_status(app_context, email)
    assert result


def test_get_user_email_domain_status_multiple(app_context):
    email = ["johnny@test.org", "ringo@test.org"]
    result = get_user_email_domain_status(app_context, email)
    assert result


def test_get_user_email_domain_status_invalid(app_context):
    with pytest.raises(InvalidEmailDomainError):
        email = "johnny@google.com"
        get_user_email_domain_status(app_context, email)
