from nad_ch.application_context import ApplicationContext
from nad_ch.domain.entities import DataProvider


def add_data_provider(
      ctx: ApplicationContext, provider_name: str
) -> None:
    if not provider_name:
        ctx.logger.error('Provider name required')
        return

    provider = DataProvider(provider_name)
    ctx.providers.add(provider)
    ctx.logger.info('Provider added')


def list_data_providers(ctx: ApplicationContext):
    providers = ctx.providers.get_all()
    ctx.logger.info('Data Provider Names:')
    for p in providers:
        ctx.logger.info(p.name)

    return providers


def ingest_data_submission(
        ctx: ApplicationContext, file_path: str, provider_name: str
) -> None:
    pass
