from typing import Protocol
from .entities import DataProvider


def DataProviderRepository(Protocol):
    def save(self, provider: DataProvider) -> None:
        ...
