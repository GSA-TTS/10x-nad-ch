from .controllers.cli import cli
from .application_context import create_app_context


def main():
    context = create_app_context()
    cli(obj=context)


if __name__ == '__main__':
    main()
