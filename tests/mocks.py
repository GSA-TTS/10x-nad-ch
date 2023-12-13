from nad_ch.domain.entities import DataProvider
from nad_ch.domain.repositories import DataProviderRepository


class MockDataProviderRepository(DataProviderRepository):
    def __init__(self) -> None:
        self._providers = set()
        self._next_id = 1

    def add(self, provider: DataProvider) -> None:
        provider.id = self._next_id
        self._providers.add(provider)
        self._next_id += 1

    def get_by_name(self, name: str) -> DataProvider:
        return next(p for p in self._providers if p.name == name)

    def get_all(self):
        return sorted(list(self._providers), key=lambda provider: provider.id)
