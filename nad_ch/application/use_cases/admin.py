from nad_ch.application.interfaces import ApplicationContext


def activate_user(ctx: ApplicationContext, user_id: int, producer_name: str):
    user = ctx.users.get_by_id(user_id)
    user.activated = True
    user.producer = ctx.producers.get_by_name(producer_name)
    user.roles = [ctx.roles.get_by_name("producer")]
    saved_user = ctx.users.update(user)
    return saved_user
