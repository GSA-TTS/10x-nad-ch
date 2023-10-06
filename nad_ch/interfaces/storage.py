from typing import Protocol
from ..entities import File, FileMetadata

class StorageGateway(Protocol):
    def save(self, file: File) -> None:
        ...

    def list_all(self) -> list[File]:
        ...

    def get_metadata(self, file_name: str) -> FileMetadata:
        ...
