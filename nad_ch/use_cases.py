from .application_context import ApplicationContext
from .interfaces.storage import StorageGateway


def ingest_data_submission(ctx: ApplicationContext, file_path: str) -> None:
    storage: StorageGateway = ctx.storage
    storage.save(file_path)
