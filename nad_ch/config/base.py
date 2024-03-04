import os
from dotenv import load_dotenv


load_dotenv()


APP_ENV = os.getenv("APP_ENV")
PORT = os.getenv("PORT", 5000)
ALLOWED_LOGIN_DOMAINS = ["dot.gov", "gsa.gov"]
if os.environ.get("LOCAL_ALLOWED_DOMAIN"):
    ALLOWED_LOGIN_DOMAINS.append(os.environ.get("LOCAL_ALLOWED_DOMAIN"))
CALLBACK_URL_SCHEME = os.getenv("CALLBACK_URL_SCHEME", "http")
OAUTH2_CONFIG = {
    "cloudgov": {
        "client_id": os.environ.get("CLOUDGOV_CLIENT_ID"),
        "client_secret": os.environ.get("CLOUDGOV_CLIENT_SECRET"),
        "authorize_url": "https://login.fr.cloud.gov/oauth/authorize",
        "token_url": "https://uaa.fr.cloud.gov/oauth/token",
        "logout_url": "https://login.fr.cloud.gov/logout.do",
        "userinfo": {
            "url": "access_token",
            "email": lambda json: json["email"],
        },
        "scopes": ["openid"],
    },
    "logingov": {
        # login.gov configuration details go here
    },
}
