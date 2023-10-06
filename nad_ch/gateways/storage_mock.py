from ..entities import File, FileMetadata
from ..interfaces.storage import StorageGateway

class StorageGatewayMock(StorageGateway):
    def __init__(self):
        self.files = []

    def save(self, file: File) -> None:
        self.files.append(file)

    def list_all(self) -> list[File]:
        return self.files

    def get_file(self, file_name: str) -> File:
        file = next((f for f in self.files if f.name == file_name), None)
        if not file:
            raise ValueError(f"No file named {file_name} found!")
        return file

    def get_metadata(self, file_name: str) -> FileMetadata:
        file = next((f for f in self.files if f.name == file_name), None)
        if not file:
            raise ValueError(f"No file named {file_name} found!")
        return FileMetadata(name=file.name, size=len(file.content))
