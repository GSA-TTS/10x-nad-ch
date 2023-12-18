from typing import Protocol
from collections.abc import Iterable
from nad_ch.domain.entities import DataProvider


class DataProviderRepository(Protocol):
    def add(self, provider: DataProvider) -> None:
        ...

    def get_by_name(self, name: str) -> DataProvider:
        ...

    def get_all(self) -> Iterable[DataProvider]:
        ...
