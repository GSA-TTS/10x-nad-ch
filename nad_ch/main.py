#!/usr/bin/env python3

import argparse
from nad_ch.config import create_app_context
from nad_ch.config import PORT
from nad_ch.controllers.cli import cli
from nad_ch.controllers.web.flask import create_flask_application


ctx = create_app_context()


def run_cli():
    cli(obj=ctx)


def serve_flask_app():
    flask_app = create_flask_application(ctx)
    flask_app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Call a specific function.")
    parser.add_argument("function", choices=["run_cli", "serve_flask_app"])

    args = parser.parse_args()

    if args.function == "run_cli":
        run_cli()
    elif args.function == "serve_flask_app":
        serve_flask_app()
