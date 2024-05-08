import os
import zipfile
from nad_ch.config import create_app_context, OAUTH2_CONFIG
from nad_ch.core.entities import (
    User,
)


def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file), os.path.join(folder_path, "..")
                    ),
                )


def main():
    if os.getenv("APP_ENV") != "dev_local":
        raise Exception("This script can only be run in a local dev environment.")

    ctx = create_app_context()

    admin_role = ctx.roles.get_by_name("admin")

    admin_user = User(
        email="admin@test.org",
        login_provider="cloudgov",
        logout_url=OAUTH2_CONFIG["cloudgov"]["logout_url"],
        roles=[admin_role],
        activated=True,
    )

    ctx.users.add(admin_user)


if __name__ == "__main__":
    main()
