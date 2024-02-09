from typing import Optional, Protocol
from nad_ch.application.dtos import DownloadResult
from nad_ch.domain.repositories import DataProviderRepository, DataSubmissionRepository


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
    def run_load_and_validate(
        self, submissions: DataSubmissionRepository, submission_id: int, path: str
    ):
        ...


class ApplicationContext:
    @property
    def providers(self) -> DataProviderRepository:
        return self._providers

    @property
    def submissions(self) -> DataSubmissionRepository:
        return self._submissions

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def task_queue(self) -> TaskQueue:
        return self._task_queue
