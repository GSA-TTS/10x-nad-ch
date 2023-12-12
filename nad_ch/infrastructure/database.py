from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from ..entities import DataProvider
from ..repositories import DataProviderRepository


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


class SqlAlchemyDataProviderRepostiory(DataProviderRepository):
    def __init__(self, session):
        self.session = session

    def add(self, provider: DataProvider):
        provider_model = DataProviderModel.from_entity(provider)
        self.session.add(provider_model)
        self.session.commit()
        return provider_model.to_entity()

    def get_by_name(self, name: str) -> DataProvider:
        provider_model = (
            self.session.query(DataProviderModel)
            .filter(DataProviderModel.name == name)
            .first()
        )
        return provider_model.to_entity()
