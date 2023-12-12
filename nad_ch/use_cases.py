from .application_context import ApplicationContext
from .entities import DataProvider

def add_data_provider(
      ctx: ApplicationContext, provider_name: str
) -> None:
    provider = DataProvider(provider_name)
    ctx.providers.add(provider)


def ingest_data_submission(
        ctx: ApplicationContext, file_path: str, provider_name: str
) -> None:
    pass
