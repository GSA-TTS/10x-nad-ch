from typing import Optional, Protocol
from collections.abc import Iterable
from nad_ch.domain.entities import DataProducer, DataSubmission


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

    def get_by_id() -> Optional[DataSubmission]:
        ...

    def get_by_producer(self, producer: DataProducer) -> Iterable[DataSubmission]:
        ...

    def get_by_filename() -> Optional[DataSubmission]:
        ...

    def update_report(self, submission_id: int, report) -> None:
        ...
