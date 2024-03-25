#!/usr/bin/env python3

import argparse
from nad_ch.config import create_app_context
from nad_ch.config import PORT
from nad_ch.controllers.cli import cli
from nad_ch.controllers.web.flask import create_flask_application


ctx = create_app_context()


def run_cli(args):
    cli.main(args=args, obj=ctx)


def serve_flask_app():
    flask_app = create_flask_application(ctx)
    flask_app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Call a specific function.")
    subparsers = parser.add_subparsers(dest="function", required=True)

    parser_run_cli = subparsers.add_parser("run_cli", help="Run the CLI application")
    parser_run_cli.add_argument(
        "cli_args", nargs=argparse.REMAINDER, help="Arguments for the CLI application"
    )

    parser_serve_flask_app = subparsers.add_parser(
        "serve_flask_app", help="Serve the Flask application"
    )

    args = parser.parse_args()

    if args.function == "run_cli":
        run_cli(args.cli_args)
    elif args.function == "serve_flask_app":
        serve_flask_app()
