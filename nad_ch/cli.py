from nad_ch.controllers.cli import cli
from nad_ch.config import create_app_context


def main():
    context = create_app_context()
    cli(obj=context)


if __name__ == "__main__":
    main()
