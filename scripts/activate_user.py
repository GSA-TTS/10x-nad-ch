import sys
from nad_ch.config import create_app_context


ctx = create_app_context()


def activate_user():
    if len(sys.argv) != 2:
        print("Usage: python3 activate_user.py <exisiting user email>")
        sys.exit(1)

    email = sys.argv[1]

    user = ctx.users.get_by_email(email)

    # This assumes a seed script has been run so that there is at least one record in
    # the data_producers table
    user.associate_with_data_producer(ctx.producers.get_all()[0])

    user.activate()

    updated_user = ctx.users.update(user)

    print("User activated:", updated_user)


if __name__ == "__main__":
    activate_user()
