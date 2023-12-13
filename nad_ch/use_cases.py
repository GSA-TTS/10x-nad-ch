from nad_ch.application_context import ApplicationContext
from nad_ch.entities import DataProvider


def add_data_provider(
      ctx: ApplicationContext, provider_name: str
) -> None:
    if not provider_name:
        raise InvalidProviderNameException()

    provider = DataProvider(provider_name)
    ctx.providers.add(provider)


def list_data_providers(
    ctx: ApplicationContext
):
    list = ctx.providers.get_all()
    return list


def ingest_data_submission(
        ctx: ApplicationContext, file_path: str, provider_name: str
) -> None:
    pass


class InvalidProviderNameException(Exception):
    def __init__(self, message='Provider name is required'):
        self.message = message
        super().__init__(self.message)
