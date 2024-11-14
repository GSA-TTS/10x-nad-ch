import os
import secrets
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV")
PORT = os.getenv("PORT", 5000)
ALLOWED_LOGIN_DOMAINS = ["dot.gov", "gsa.gov"]
if os.environ.get("LOCAL_ALLOWED_DOMAIN"):
    ALLOWED_LOGIN_DOMAINS.append(os.environ.get("LOCAL_ALLOWED_DOMAIN"))
CALLBACK_URL_SCHEME = os.getenv("CALLBACK_URL_SCHEME", "http")
OAUTH2_CONFIG = {
    "logingov": {
        "client_id": os.getenv("LOGINGOV_CLIENT_ID"),
        "authorize_url": "https://idp.int.identitysandbox.gov/openid_connect/authorize",
        "token_url": "https://idp.int.identitysandbox.gov/api/openid_connect/token",
        "logout_url": "https://idp.int.identitysandbox.gov/openid_connect/logout",
        "userinfo": {
            "url": "https://idp.int.identitysandbox.gov/api/openid_connect/userinfo",
            "email": lambda json: json["email"],
        },
        "private_key_jwt": {
            "key": os.getenv("LOGINGOV_PRIVATE_KEY"),
            "alg": "RS256"
        },
        "acr_values": "http://idmanagement.gov/ns/assurance/ial/1",
        "scopes": ["openid", "email", "profile"],
        "nonce": lambda: secrets.token_urlsafe(64),
    }
}
