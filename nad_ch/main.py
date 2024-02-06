from nad_ch.application_context import create_app_context
from nad_ch.config import PORT
from nad_ch.controllers.cli import cli
from nad_ch.controllers.web.flask import create_flask_application


ctx = create_app_context()


def run_cli():
    cli(obj=ctx)


def serve_flask_app():
    flask_app = create_flask_application(ctx)
    flask_app.run(host="0.0.0.0", port=PORT)
