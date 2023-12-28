import pytest
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nad_ch.config import DATABASE_URL
from nad_ch.domain.entities import DataProvider, DataSubmission
from nad_ch.infrastructure.database import (
    ModelBase,
    SqlAlchemyDataProviderRepository,
    SqlAlchemyDataSubmissionRepository,
)


@pytest.fixture(scope="function")
def test_session():
    engine = create_engine(DATABASE_URL)
    ModelBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    @contextlib.contextmanager
    def test_session_scope():
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return test_session_scope


@pytest.fixture(scope="function")
def providers(test_session):
    return SqlAlchemyDataProviderRepository(test_session)


@pytest.fixture(scope="function")
def submissions(test_session):
    return SqlAlchemyDataSubmissionRepository(test_session)


def test_add_data_provider_to_repository_and_get_by_name(providers):
    provider_name = "State X"
    new_provider = DataProvider(provider_name)

    providers.add(new_provider)

    retrieved_provider = providers.get_by_name(provider_name)
    assert retrieved_provider.id == 1
    assert retrieved_provider.created_at is not None
    assert retrieved_provider.updated_at is not None
    assert retrieved_provider.name == provider_name
    assert isinstance(retrieved_provider, DataProvider) is True


def test_add_data_provider_and_then_data_submission(providers, submissions):
    provider_name = "State X"
    new_provider = DataProvider(provider_name)
    saved_provider = providers.add(new_provider)
    new_submission = DataSubmission("some-file-name", "some-url", saved_provider)

    result = submissions.add(new_submission)

    assert result.id == 1
    assert result.created_at is not None
    assert result.updated_at is not None
    assert result.provider.id == saved_provider.id
    assert result.file_name == "some-file-name"
    assert result.url == "some-url"


def test_retrieve_a_list_of_submissions_by_provider(providers, submissions):
    provider_name = "State X"
    new_provider = DataProvider(provider_name)
    saved_provider = providers.add(new_provider)
    new_submission = DataSubmission("some-file-name", "some-url", saved_provider)
    submissions.add(new_submission)
    another_new_submission = DataSubmission(
        "some-other-file-name", "some-other-url", saved_provider
    )
    submissions.add(another_new_submission)

    submissions = submissions.get_by_provider(saved_provider)

    assert len(submissions) == 2
