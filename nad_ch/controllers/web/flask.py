import os
from flask import Flask
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.controllers.web.routes.auth import setup_auth, user_loader, auth_bp
from nad_ch.controllers.web.routes.home import home_bp


def create_flask_application(ctx: ApplicationContext):
    template_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"
    )

    app = Flask(__name__, template_folder=template_folder, static_folder="dist")

    app.secret_key = "this-is-my-super-secret-key"

    app.extensions["ctx"] = ctx

    setup_auth(app, user_loader)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(home_bp)

    return app
