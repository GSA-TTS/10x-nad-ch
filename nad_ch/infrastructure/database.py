from typing import List, Optional
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
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


class CommonBase(ModelBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class DataProviderModel(CommonBase):
    __tablename__ = 'data_providers'

    name = Column(String)

    data_submissions = relationship(
        'DataSubmissionModel',
        back_populates='data_provider'
    )

    @staticmethod
    def from_entity(provider):
        model = DataProviderModel(id=provider.id, name=provider.name)
        return model

    def to_entity(self):
        entity = DataProvider(id=self.id, name=self.name)

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


class DataSubmissionModel(CommonBase):
    __tablename__ = 'data_submissions'

    file_name = Column(String)
    url = Column(String)
    data_provider_id = Column(Integer, ForeignKey('data_providers.id'))

    data_provider = relationship('DataProviderModel', back_populates='data_submissions')

    @staticmethod
    def from_entity(submission):
        model = DataSubmissionModel(
            id=submission.id,
            file_name=submission.file_name,
            url=submission.url,
            data_provider_id=submission.provider.id
        )
        return model

    def to_entity(self, provider: DataProvider):
        entity = DataSubmission(
            id=self.id,
            file_name=self.file_name,
            url=self.url,
            provider=provider
        )

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


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
            result = (
                session.query(DataSubmissionModel, DataProviderModel)
                .join(
                    DataProviderModel, DataProviderModel.id ==
                    DataSubmissionModel.data_provider_id
                )
                .filter(DataSubmissionModel.file_name == file_name)
                .first()
            )

            if result:
                submission_model, provider_model = result
                return submission_model.to_entity(provider_model.to_entity())
            else:
                return None

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
