from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import contextlib
from config import DATABASE_URL
from entities import DataProvider
from repositories import DataProviderRepository


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextlib.contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


ModelBase = declarative_base()


class DataProviderModel(ModelBase):
    __tablename__ = 'data_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @staticmethod
    def from_entity(provider):
        return DataProviderModel(name=provider.name)

    def to_entity(self):
        return DataProvider(name=self.name)


class SqlAlchemyDataProviderRepository(DataProviderRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, provider: DataProvider):
        with self.session_factory() as session:
            provider_model = DataProviderModel.from_entity(provider)
            session.add(provider_model)
            # session.commit()
            return provider_model.to_entity()

    def get_by_name(self, name: str) -> DataProvider:
        with self.session_factory() as session:
            provider_model = (
                session.query(DataProviderModel)
                .filter(DataProviderModel.name == name)
                .first()
            )
            return provider_model.to_entity()

    def get_all(self):
        with self.session_factory() as session:
            provider_models = session.query(DataProviderModel).all()
            providers_entities = [provider.to_entity() for provider in provider_models]
            return providers_entities
