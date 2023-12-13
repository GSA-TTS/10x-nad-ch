import pytest
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nad_ch.config import DATABASE_URL
from nad_ch.domain.entities import DataProvider
from nad_ch.infrastructure.database import ModelBase, SqlAlchemyDataProviderRepository


@pytest.fixture(scope='function')
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


@pytest.fixture(scope='function')
def providers(test_session):
    return SqlAlchemyDataProviderRepository(test_session)


def test_add_data_provider_to_repository_and_get_by_name(providers):
    provider_name = 'State X'
    new_provider = DataProvider(provider_name)

    providers.add(new_provider)

    retreived_provider = providers.get_by_name(provider_name)
    assert retreived_provider.name == provider_name
    assert isinstance(retreived_provider, DataProvider) is True
