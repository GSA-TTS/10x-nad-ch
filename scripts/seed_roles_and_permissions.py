import os
from nad_ch.config import create_app_context
from nad_ch.core.entities import Role, ROLE_PERMISSIONS_MAP


def main():
    if os.getenv("APP_ENV") != "dev_local":
        raise Exception("This script can only be run in a local dev environment.")

    ctx = create_app_context()

    for role, permissions in ROLE_PERMISSIONS_MAP.items():
        role = Role(name=role, permissions=permissions)
        ctx.roles.add(role)
