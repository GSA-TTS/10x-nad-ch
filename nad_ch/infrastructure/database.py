from typing import List, Optional
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import contextlib
from nad_ch.config import DATABASE_URL
from nad_ch.domain.entities import DataProvider, DataSubmission
from nad_ch.domain.repositories import DataProviderRepository, DataSubmissionRepository


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

    data_submissions = relationship(
        'DataSubmissionModel',
        back_populates='data_provider'
    )

    @staticmethod
    def from_entity(provider):
        return DataProviderModel(id=provider.id, name=provider.name)

    def to_entity(self):
        return DataProvider(id=self.id, name=self.name)


class DataSubmissionModel(ModelBase):
    __tablename__ = 'data_submissions'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    url = Column(String)
    data_provider_id = Column(Integer, ForeignKey('data_providers.id'))

    data_provider = relationship('DataProviderModel', back_populates='data_submissions')

    @staticmethod
    def from_entity(submission):
        return DataSubmissionModel(
            id=submission.id,
            file_name=submission.file_name,
            url=submission.url,
            data_provider_id=submission.provider.id
        )

    def to_entity(self, provider: DataProvider):
        return DataSubmission(
            id=self.id,
            file_name=self.file_name,
            url=self.url,
            provider=provider
        )


class SqlAlchemyDataProviderRepository(DataProviderRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, provider: DataProvider) -> DataProvider:
        with self.session_factory() as session:
            provider_model = DataProviderModel.from_entity(provider)
            session.add(provider_model)
            session.commit()
            session.refresh(provider_model)
            return provider_model.to_entity()

    def get_by_name(self, name: str) -> Optional[DataProvider]:
        with self.session_factory() as session:
            provider_model = (
                session.query(DataProviderModel)
                .filter(DataProviderModel.name == name)
                .first()
            )
            return provider_model.to_entity() if provider_model else None

    def get_all(self) -> List[DataProvider]:
        with self.session_factory() as session:
            provider_models = session.query(DataProviderModel).all()
            providers_entities = [provider.to_entity() for provider in provider_models]
            return providers_entities


class SqlAlchemyDataSubmissionRepository(DataSubmissionRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, submission: DataSubmission) -> DataSubmission:
        with self.session_factory() as session:
            submission_model = DataSubmissionModel.from_entity(submission)
            session.add(submission_model)
            session.commit()
            session.refresh(submission_model)
            provider_model = (
                session.query(DataProviderModel)
                .filter(DataProviderModel.id == submission_model.data_provider_id)
                .first()
            )
            return submission_model.to_entity(provider_model.to_entity())

    def get_by_name(self, file_name: str) -> Optional[DataSubmission]:
        with self.session_factory() as session:
            submission_model = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.name == file_name)
                .first()
            )
            provider_model = (
                session.query(DataProviderModel)
                .filter(DataProviderModel.id == submission_model.data_provider_id)
                .first()
            )
            return submission_model.to_entity(provider_model.to_entity())

    def get_by_provider(self, provider: DataProvider) -> List[DataSubmission]:
        with self.session_factory() as session:
            submission_models = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.data_provider_id == provider.id)
                .all()
            )
            submission_entities = (
                [submission.to_entity(provider) for submission in submission_models]
            )
            return submission_entities
