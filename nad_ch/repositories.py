from typing import Protocol
from .entities import DataProvider


class DataProviderRepository(Protocol):
    def add(self, provider: DataProvider) -> None:
        ...

    def get_by_name(self, name: str) -> DataProvider:
        ...
