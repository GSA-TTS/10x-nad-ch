import os
import shutil


class LocalStorage:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def _full_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)

    def upload(self, source: str, destination: str) -> None:
        shutil.copy(source, self._full_path(destination))

    def delete(self, file_path: str) -> None:
        full_file_path = self._full_path(file_path)
        if os.path.exists(full_file_path):
            os.remove(full_file_path)

    def get_file_url(self, filename: str) -> str:
        return filename
