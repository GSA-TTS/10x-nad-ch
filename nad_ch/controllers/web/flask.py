import os
from flask import Flask
from nad_ch.application.interfaces import ApplicationContext
from nad_ch.controllers.web.routes import home_bp


def create_flask_application(ctx: ApplicationContext):
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

    app = Flask(__name__, template_folder=template_folder, static_folder="dist")

    app.extensions["ctx"] = ctx

    app.register_blueprint(home_bp)

    return app
