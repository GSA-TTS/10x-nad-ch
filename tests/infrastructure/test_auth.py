import pytest
from nad_ch.infrastructure.auth import AuthenticationImplementation


@pytest.fixture
def auth_impl():
    providers = {
        "test_provider": {
            "token_url": "https://example.com/oauth/token",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "authorize_url": "https://example.com/oauth/authorize",
            "scopes": ["openid", "email"],
            "userinfo": {"url": "https://example.com/userinfo"},
        }
    }
    allowed_domains = ["example.com"]
    callback_url_scheme = "https"
    return AuthenticationImplementation(providers, allowed_domains, callback_url_scheme)


def test_fetch_oauth2_token_success(mocker, auth_impl):
    mock_post = mocker.patch("nad_ch.infrastructure.auth.requests.post")
    mocker.patch("nad_ch.infrastructure.auth.url_for", return_value="mock_callback_url")

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "mocked_access_token"}
    mock_post.return_value = mock_response

    token = auth_impl.fetch_oauth2_token("test_provider", "dummy_code")

    print("token", token)
    assert token == "mocked_access_token"
    mock_post.assert_called_once_with(
        "https://example.com/oauth/token",
        data=mocker.ANY,
        headers={"Accept": "application/json"},
        timeout=4,
    )


def test_fetch_user_email_from_login_provider_with_token(mocker, auth_impl):
    auth_impl._providers["test_provider"]["userinfo"]["url"] = "access_token"

    mocker.patch(
        "nad_ch.infrastructure.auth.jwt.decode",
        return_value={"email": "test@example.com"},
    )

    email = auth_impl.fetch_user_email_from_login_provider(
        "test_provider", "mocked_oauth2_token"
    )

    assert email == "test@example.com"


def test_make_login_url(mocker, auth_impl):
    mocker.patch("nad_ch.infrastructure.auth.url_for", return_value="mock_callback_url")

    state_token = "mock_state_token"
    login_url = auth_impl.make_login_url("test_provider", state_token)

    assert login_url is not None
    assert "client_id=test_client_id" in login_url
    assert "redirect_uri=mock_callback_url" in login_url
    assert "response_type=code" in login_url
    assert f"state={state_token}" in login_url


def test_user_email_address_has_permitted_domain_single_allowed():
    providers = {}  # Assuming providers are not relevant for this test
    allowed_domains = ["example.com"]
    auth_impl = AuthenticationImplementation(providers, allowed_domains, "https")

    email = "user@example.com"
    result = auth_impl.user_email_address_has_permitted_domain(email)

    assert result


def test_user_email_address_has_permitted_domain_single_not_allowed():
    providers = {}  # Assuming providers are not relevant for this test
    allowed_domains = ["example.com"]
    auth_impl = AuthenticationImplementation(providers, allowed_domains, "https")

    email = "user@nonpermitted.com"
    result = auth_impl.user_email_address_has_permitted_domain(email)

    assert result is False


def test_user_email_address_has_permitted_domain_multiple_one_allowed():
    providers = {}  # Assuming providers are not relevant for this test
    allowed_domains = ["example.com"]
    auth_impl = AuthenticationImplementation(providers, allowed_domains, "https")

    email = ["user1@example.com", "user2@nonpermitted.com"]
    result = auth_impl.user_email_address_has_permitted_domain(email)

    assert result


def test_user_email_address_has_permitted_domain_multiple_none_allowed():
    providers = {}  # Assuming providers are not relevant for this test
    allowed_domains = ["example.com"]
    auth_impl = AuthenticationImplementation(providers, allowed_domains, "https")

    email = ["user1@nonpermitted.com", "user2@nonpermitted.com"]
    result = auth_impl.user_email_address_has_permitted_domain(email)

    assert result is False
