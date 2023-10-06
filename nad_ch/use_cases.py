from .application_context import ApplicationContext
from .entities import File, FileMetadata
from .interfaces.storage import StorageGateway


def upload_file(ctx: ApplicationContext, file: File) -> None:
    storage: StorageGateway = ctx.storage
    storage.save(file)


def list_files(ctx: ApplicationContext) -> list[File]:
    storage: StorageGateway = ctx.storage
    return storage.list_all()


def get_file_metadata(ctx: ApplicationContext, file_name: str) -> FileMetadata:
    storage: StorageGateway = ctx.storage
    return storage.get_metadata(file_name)
