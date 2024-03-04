from nad_ch.application.interfaces import ApplicationContext
from nad_ch.domain.entities import User


def get_or_create_user(
    ctx: ApplicationContext, provider_name: str, email: str
) -> User:
    """
    Using an email address, retrieve the entity of the user who has just logged in. If
    no such user exists, create a new one and return it.
    """
    user = ctx.users.get_by_email(email)

    if user:
        return user

    # TODO validate email address and throw invalid email error if necessary

    new_user = User(
        email=email,
        username=email.split("@")[0],
        login_provider=provider_name,
        logout_url=ctx.auth.get_logout_url(provider_name),
    )
    saved_user = ctx.users.add(new_user)
    return saved_user


def get_logged_in_user_redirect_url(
    ctx: ApplicationContext, provider_name: str, state_token: str
) -> str | None:
    return ctx.auth.make_login_url(provider_name, state_token)


def get_logged_out_user_redirect_url(
    ctx: ApplicationContext, provider_name: str
) -> str | None:
    return ctx.auth.make_logout_url(provider_name)


def get_oauth2_token(
    ctx: ApplicationContext, provider_name: str, code: str
) -> str | None:
    oauth2_token = ctx.auth.fetch_oauth2_token(provider_name, code)

    if not oauth2_token:
        ctx.logger.error("OAUTH2 error: Could not get access token.")
        return None

    return oauth2_token


def get_user_email(
    ctx: ApplicationContext, provder_name: str, oath2_token: str
) -> str | None:
    return ctx.auth.fetch_user_email_from_login_provider(provder_name, oath2_token)


def get_user_email_domain_status(
    ctx: ApplicationContext, email: str | list[str]
) -> bool:
    is_valid_domain = ctx.auth.user_email_address_has_permitted_domain(email)

    if not is_valid_domain:
        ctx.logger.info(
            "OAUTH2 error: Attempted login with non-permitted email domain."
        )

    return is_valid_domain
