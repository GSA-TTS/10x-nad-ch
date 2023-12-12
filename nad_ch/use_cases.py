from nad_ch.application_context import ApplicationContext
from nad_ch.entities import DataProvider


def add_data_provider(
      ctx: ApplicationContext, provider_name: str
) -> None:
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
