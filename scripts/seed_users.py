import os
from nad_ch.config import create_app_context, OAUTH2_CONFIG
from nad_ch.core.entities import (
    DataProducer,
    User,
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


    new_producer = DataProducer(name="New Jersey")
    saved_producer = ctx.producers.add(new_producer)

    producer_role = ctx.roles.get_by_name("producer")

    new_activated_user = User(
        email="activated@test.org",
        login_provider="cloudgov",
        logout_url=OAUTH2_CONFIG["cloudgov"]["logout_url"],
        producer=saved_producer,
        roles=[producer_role],
        activated=True,
    )

    ctx.users.add(new_activated_user)

    new_unactivated_user = User(
        email="unactivated@test.org",
        login_provider="cloudgov",
        logout_url=OAUTH2_CONFIG["cloudgov"]["logout_url"],
        activated=False,
    )

    ctx.users.add(new_unactivated_user)


if __name__ == "__main__":
    main()
