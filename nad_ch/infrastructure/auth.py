from flask import url_for
import jwt
import requests
from urllib.parse import urlencode
from nad_ch.application.interfaces import Authentication


class AuthenticationImplementation(Authentication):
    def __init__(
        self, providers: dict, allowed_domains: list, callback_url_scheme: str
    ):
        self._providers = providers
        self._allowed_domains = allowed_domains
        self._callback_url_scheme = callback_url_scheme

    def fetch_oauth2_token(self, provider_name: str, code: str) -> str | None:
        provider_config = self._providers[provider_name]
        if not provider_config:
            return None

        token_url = provider_config["token_url"]
        request_data = {
            "client_id": provider_config["client_id"],
            "client_secret": provider_config["client_secret"],
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "auth.oauth2_callback",
                provider=provider_name,
                _scheme=self._callback_url_scheme,
                _external=True,
            ),
        }

        response = requests.post(
            token_url,
            data=request_data,
            headers={"Accept": "application/json"},
            timeout=4,
        )

        if response.status_code != 200:
            return None

        oauth2_token = response.json().get("access_token")

        if not oauth2_token:
            return None

        return oauth2_token

    def fetch_user_email_from_login_provider(
        self, provider_name: str, oauth2_token: str
    ) -> str | list[str] | None:
        provider_config = self._providers[provider_name]
        if not provider_config:
            return None

        if provider_config["userinfo"]["url"] == "access_token":
            decoded_data = jwt.decode(
                oauth2_token,
                options={"verify_signature": False},
            )

            return decoded_data.get("email")
        else:
            # TODO handle login.gov case here
            pass

        return None

    def make_login_url(self, provider_name: str, state_token: str) -> str | None:
        provider_config = self._providers[provider_name]
        if not provider_config:
            return None

        query_string = urlencode(
            {
                "client_id": provider_config["client_id"],
                "redirect_uri": url_for(
                    "auth.oauth2_callback",
                    provider=provider_name,
                    _scheme=self._callback_url_scheme,
                    _external=True,
                ),
                "response_type": "code",
                "scope": " ".join(provider_config["scopes"]),
                "state": state_token,
            },
        )

        return provider_config["authorize_url"] + "?" + query_string

    def make_logout_url(self, provider_name: str) -> str | None:
        provider_config = self._providers[provider_name]
        if not provider_config:
            return None

        redirect_uri = url_for(
            "index",
            _scheme=self._callback_url_scheme,
            _external=True,
        )

        query_string = urlencode(
            {
                "client_id": provider_config["client_id"],
                "redirect_uri": redirect_uri,
                "post_logout_redirect_uri": redirect_uri,
            },
        )

        return provider_config["logout_url"] + "?" + query_string

    def user_email_address_has_permitted_domain(self, email: str | list[str]) -> bool:
        def is_domain_allowed(email_address: str) -> bool:
            domain = email_address.split("@")[1]
            return domain in self._allowed_domains

        if isinstance(email, list):
            for email_address in email:
                if is_domain_allowed(email_address):
                    return True
        else:
            if is_domain_allowed(email):
                return True

        return False
