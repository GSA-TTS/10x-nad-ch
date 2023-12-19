from typing import Optional
from nad_ch.domain.entities import DataProvider, DataSubmission
from nad_ch.domain.repositories import DataProviderRepository, DataSubmissionRepository


class MockDataProviderRepository(DataProviderRepository):
    def __init__(self) -> None:
        self._providers = set()
        self._next_id = 1

    def add(self, provider: DataProvider) -> DataProvider:
        provider.id = self._next_id
        self._providers.add(provider)
        self._next_id += 1
        return provider

    def get_by_name(self, name: str) -> Optional[DataProvider]:
        return next((p for p in self._providers if p.name == name), None)

    def get_all(self):
        return sorted(list(self._providers), key=lambda provider: provider.id)


class MockDataSubmissionRepository(DataSubmissionRepository):
    def __init__(self) -> None:
        self._submissions = set()
        self._next_id = 1

    def add(self, submission: DataSubmission) -> DataSubmission:
        submission.id = self._next_id
        self._submissions.add(submission)
        self._next_id += 1
        return submission

    def get_by_provider(self, provider: DataProvider) -> Optional[DataSubmission]:
        return next(
            (s for s in self._submissions if s.provider.name == provider.name), None
        )
