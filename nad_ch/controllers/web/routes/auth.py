from flask import (
    abort,
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    g,
    url_for,
)
from flask_login import LoginManager, login_user, logout_user, current_user
import secrets
from typing import Optional
from nad_ch.application.exceptions import (
    InvalidEmailDomainError,
    InvalidEmailError,
    OAuth2TokenError,
)
from nad_ch.application.use_cases.auth import (
    get_or_create_user,
    get_logged_in_user_redirect_url,
    get_logged_out_user_redirect_url,
    get_oauth2_token,
    get_user_email,
    get_user_email_domain_status,
)
from nad_ch.core.entities import User


login_view = "index"
login_manager = LoginManager()
login_manager.login_view = login_view


def setup_auth(app, user_loader):
    login_manager.init_app(app)
    login_manager.user_loader(user_loader)

    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template("401.html"), 401

    return app


def user_loader(user_id: int) -> Optional[User]:
    users = current_app.extensions["ctx"]["users"]
    return users.get_by_id(user_id)


auth_bp = Blueprint("auth", __name__)


@auth_bp.before_request
def before_request():
    g.ctx = current_app.extensions["ctx"]


@auth_bp.route("/logout/<provider>")
def logout_provider(provider: str):
    logout_user()

    redirect_url = get_logged_out_user_redirect_url(g.ctx, provider)
    if not redirect_url:
        abort(404)

    return redirect(redirect_url)


@auth_bp.route("/authorize/<provider>")
def oauth2_authorize(provider: str):
    if not current_user.is_anonymous:
        return redirect(url_for(login_view))

    state_token = secrets.token_urlsafe(16)

    redirect_url = get_logged_in_user_redirect_url(g.ctx, provider, state_token)
    if not redirect_url:
        abort(404)

    session["oauth2_state"] = state_token

    return redirect(redirect_url)


@auth_bp.route("/callback/<provider>")
def oauth2_callback(provider: str):
    if not current_user.is_anonymous or "error" in request.args:
        return redirect(url_for(login_view))

    try:
        login_request_is_valid = (
            request.args["state"] == session.get("oauth2_state")
            and "code" in request.args
        )
        if not login_request_is_valid:
            error_message = "Request state and/or code invalid."
            g.ctx.logger.error(f"OAUTH2 error: {error_message}")
            abort(401, description=error_message)

        oauth2_token = get_oauth2_token(g.ctx, provider, request.args["code"])

        email = get_user_email(g.ctx, provider, oauth2_token)

        get_user_email_domain_status(g.ctx, email)

        session["oauth2_token"] = oauth2_token

        user = get_or_create_user(g.ctx, provider, email)

        login_user(user)

        return redirect(url_for(login_view))
    except InvalidEmailDomainError:
        logout_user()
        return redirect(url_for("logout_provider", provider=provider))
    except InvalidEmailError as e:
        abort(400, description=e.message)
    except OAuth2TokenError as e:
        abort(401, description=e.message)
