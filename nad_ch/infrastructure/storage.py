import os
import shutil


class LocalStorage:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def _full_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)

    def upload(self, source: str, destination: str) -> None:
        shutil.copy(source, self._full_path(destination))

    def get_file_url(self, file_name: str) -> str:
        return file_name
