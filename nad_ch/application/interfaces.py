from typing import Optional, Protocol
from nad_ch.application.dtos import DownloadResult


class Logger(Protocol):
    def info(self, message):
        ...

    def error(self, message):
        ...

    def warning(self, message):
        ...


class Storage(Protocol):
    def upload(self, source: str, destination: str) -> bool:
        ...

    def delete(self, key: str) -> bool:
        ...

    def download_temp(self, key: str) -> Optional[DownloadResult]:
        ...

    def cleanup_temp_dir(self, temp_dir: str) -> bool:
        ...


class TaskQueue(Protocol):
    def run_load_and_validate(self, path: str):
        ...
