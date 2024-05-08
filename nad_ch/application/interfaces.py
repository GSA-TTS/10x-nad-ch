from typing import Optional, Protocol, Dict
from nad_ch.application.dtos import DownloadResult
from nad_ch.core.repositories import (
    DataProducerRepository,
    DataSubmissionRepository,
    UserRepository,
    ColumnMapRepository,
    RoleRepository,
)


class Logger(Protocol):
    def info(self, message): ...

    def error(self, message): ...

    def warning(self, message): ...


class Storage(Protocol):
    def upload(self, source: str, destination: str) -> bool: ...

    def delete(self, key: str) -> bool: ...

    def download_temp(self, key: str) -> Optional[DownloadResult]: ...

    def cleanup_temp_dir(self, temp_dir: str) -> bool: ...


class TaskQueue(Protocol):
    def run_load_and_validate(
        self,
        submissions: DataSubmissionRepository,
        submission_id: int,
        path: str,
        column_map: Dict[str, str],
    ): ...


class Authentication(Protocol):
    def fetch_oauth2_token(self, provider_name: str, code: str) -> str | None: ...

    def fetch_user_email_from_login_provider(
        self, provider_name: str, oauth2_token: str
    ) -> str | list[str] | None: ...

    def get_logout_url(self, provider_name: str) -> str: ...

    def make_login_url(self, provider_name: str, state_token: str) -> str | None: ...

    def make_logout_url(self, provider_name: str) -> str | None: ...

    def user_email_address_has_permitted_domain(
        self, email: str | list[str]
    ) -> bool: ...


class ApplicationContext:
    @property
    def producers(self) -> DataProducerRepository:
        return self._producers

    @property
    def submissions(self) -> DataSubmissionRepository:
        return self._submissions

    @property
    def users(self) -> UserRepository:
        return self._users

    @property
    def column_maps(self) -> ColumnMapRepository:
        return self._column_maps

    @property
    def roles(self) -> RoleRepository:
        return self._roles

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def task_queue(self) -> TaskQueue:
        return self._task_queue

    @property
    def auth(self) -> Authentication:
        return self._auth

    def __getitem__(self, key: str):
        if key == "producers":
            return self.producers
        elif key == "submissions":
            return self.submissions
        elif key == "users":
            return self.users
        elif key == "column_maps":
            return self.column_maps
        elif key == "roles":
            return self.roles
        elif key == "logger":
            return self.logger
        elif key == "storage":
            return self.storage
        elif key == "task_queue":
            return self.task_queue
        elif key == "auth":
            return self.auth
        else:
            raise KeyError(f"Invalid key: {key}")
