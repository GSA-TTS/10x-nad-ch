from typing import Protocol
from .entities import DataProvider


class DataProviderRepository(Protocol):
    def add(self, provider: DataProvider) -> None:
        ...
