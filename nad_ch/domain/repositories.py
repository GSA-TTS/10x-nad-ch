from typing import Optional, Protocol
from collections.abc import Iterable
from nad_ch.domain.entities import DataProvider, DataSubmission


class DataProviderRepository(Protocol):
    def add(self, provider: DataProvider) -> DataProvider:
        ...

    def get_by_name(self, name: str) -> Optional[DataProvider]:
        ...

    def get_all(self) -> Iterable[DataProvider]:
        ...


class DataSubmissionRepository(Protocol):
    def add(self, submission: DataSubmission) -> DataSubmission:
        ...

    def get_by_id() -> Optional[DataSubmission]:
        ...

    def get_by_provider(self, provider: DataProvider) -> Iterable[DataSubmission]:
        ...

    def get_by_filename() -> Optional[DataSubmission]:
        ...

    def update_report(self, submission_id: int, report) -> None:
        ...
