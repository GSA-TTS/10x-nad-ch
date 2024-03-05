import os
from alembic.config import Config
from alembic import command


def main():
    if os.getenv("APP_ENV") != "dev_local":
        raise Exception("This script can only be run in a local dev environment.")

    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    alembic_cfg_path = os.path.join(project_root, "alembic.ini")

    alembic_cfg = Config(alembic_cfg_path)
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    main()
