from typing import Optional, Protocol
from collections.abc import Iterable
from nad_ch.core.entities import DataProducer, DataSubmission, User, ColumnMap


class DataProducerRepository(Protocol):
    def add(self, producer: DataProducer) -> DataProducer:
        ...

    def get_by_name(self, name: str) -> Optional[DataProducer]:
        ...

    def get_all(self) -> Iterable[DataProducer]:
        ...


class DataSubmissionRepository(Protocol):
    def add(self, submission: DataSubmission) -> DataSubmission:
        ...

    def get_by_filename(filename: str) -> Optional[DataSubmission]:
        ...

    def get_by_id(id: int) -> Optional[DataSubmission]:
        ...

    def get_by_producer(self, producer: DataProducer) -> Iterable[DataSubmission]:
        ...

    def update_report(self, submission_id: int, report) -> None:
        ...


class UserRepository(Protocol):
    def add(self, user: User) -> User:
        ...

    def get_by_email(self, email: str) -> Optional[User]:
        ...

    def get_by_id(self, id: int) -> Optional[User]:
        ...

    def get_all(self) -> Iterable[User]:
        ...


class ColumnMapRepository(Protocol):
    def add(self, column_map: ColumnMap) -> ColumnMap:
        ...

    def get_all(self) -> Iterable[ColumnMap]:
        ...

    def get_by_data_submission(
        self, data_submission: DataSubmission
    ) -> Optional[ColumnMap]:
        ...

    def get_by_id(self, id: int) -> Optional[ColumnMap]:
        ...

    def get_by_name_and_version(self, name: str, version: int) -> Optional[ColumnMap]:
        ...

    def get_by_producer(self, producer: DataProducer) -> Iterable[ColumnMap]:
        ...

    def update(self, column_map: ColumnMap) -> ColumnMap:
        ...
