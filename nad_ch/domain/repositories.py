from typing import Optional, Protocol
from collections.abc import Iterable
from nad_ch.domain.entities import DataProducer, DataSubmission, User


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
