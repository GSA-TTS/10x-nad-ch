import contextlib
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from typing import List, Optional
from nad_ch.domain.entities import DataProducer, DataSubmission, User
from nad_ch.domain.repositories import (
    DataProducerRepository,
    DataSubmissionRepository,
    UserRepository,
)


def create_session_factory(connection_string: str):
    engine = create_engine(
        connection_string, connect_args={"options": "-c timezone=UTC"}
    )
    return sessionmaker(bind=engine)


@contextlib.contextmanager
def session_scope(session_factory):
    session = session_factory()
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
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class DataProducerModel(CommonBase):
    __tablename__ = "data_producers"

    name = Column(String)

    data_submissions = relationship(
        "DataSubmissionModel", back_populates="data_producer"
    )

    @staticmethod
    def from_entity(producer):
        model = DataProducerModel(id=producer.id, name=producer.name)
        return model

    def to_entity(self):
        entity = DataProducer(id=self.id, name=self.name)

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


class DataSubmissionModel(CommonBase):
    __tablename__ = "data_submissions"

    filename = Column(String)
    data_producer_id = Column(Integer, ForeignKey("data_producers.id"))
    report = Column(JSON)

    data_producer = relationship("DataProducerModel", back_populates="data_submissions")

    @staticmethod
    def from_entity(submission):
        model = DataSubmissionModel(
            id=submission.id,
            filename=submission.filename,
            report=submission.report,
            data_producer_id=submission.producer.id,
        )
        return model

    def to_entity(self, producer: DataProducer):
        entity = DataSubmission(
            id=self.id, filename=self.filename, report=self.report, producer=producer
        )

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


class UserModel(UserMixin, CommonBase):
    __tablename__ = "users"

    email = Column(String)
    login_provider = Column(String)
    logout_url = Column(String)

    @staticmethod
    def from_entity(user):
        model = UserModel(
            id=user.id,
            email=user.email,
            login_provider=user.login_provider,
            logout_url=user.logout_url,
        )
        return model

    def to_entity(self):
        entity = User(
            id=self.id,
            email=self.email,
            login_provider=self.login_provider,
            logout_url=self.logout_url,
        )

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


class SqlAlchemyDataProducerRepository(DataProducerRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, producer: DataProducer) -> DataProducer:
        with session_scope(self.session_factory) as session:
            producer_model = DataProducerModel.from_entity(producer)
            session.add(producer_model)
            session.commit()
            session.refresh(producer_model)
            return producer_model.to_entity()

    def get_by_name(self, name: str) -> Optional[DataProducer]:
        with session_scope(self.session_factory) as session:
            producer_model = (
                session.query(DataProducerModel)
                .filter(DataProducerModel.name == name)
                .first()
            )
            return producer_model.to_entity() if producer_model else None

    def get_all(self) -> List[DataProducer]:
        with session_scope(self.session_factory) as session:
            producer_models = session.query(DataProducerModel).all()
            producer_entities = [producer.to_entity() for producer in producer_models]
            return producer_entities


class SqlAlchemyDataSubmissionRepository(DataSubmissionRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, submission: DataSubmission) -> DataSubmission:
        with session_scope(self.session_factory) as session:
            submission_model = DataSubmissionModel.from_entity(submission)
            session.add(submission_model)
            session.commit()
            session.refresh(submission_model)
            producer_model = (
                session.query(DataProducerModel)
                .filter(DataProducerModel.id == submission_model.data_producer_id)
                .first()
            )
            return submission_model.to_entity(producer_model.to_entity())

    def get_by_id(self, id: int) -> Optional[DataSubmission]:
        with session_scope(self.session_factory) as session:
            result = (
                session.query(DataSubmissionModel, DataProducerModel)
                .join(
                    DataProducerModel,
                    DataProducerModel.id == DataSubmissionModel.data_producer_id,
                )
                .filter(DataSubmissionModel.id == id)
                .first()
            )

            if result:
                submission_model, producer_model = result
                return submission_model.to_entity(producer_model.to_entity())
            else:
                return None

    def get_by_producer(self, producer: DataProducer) -> List[DataSubmission]:
        with session_scope(self.session_factory) as session:
            submission_models = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.data_producer_id == producer.id)
                .all()
            )
            submission_entities = [
                submission.to_entity(producer) for submission in submission_models
            ]
            return submission_entities

    def get_by_filename(self, filename: str) -> Optional[DataSubmission]:
        with session_scope(self.session_factory) as session:
            result = (
                session.query(DataSubmissionModel, DataProducerModel)
                .join(
                    DataProducerModel,
                    DataProducerModel.id == DataSubmissionModel.data_producer_id,
                )
                .filter(DataSubmissionModel.filename == filename)
                .first()
            )

            if result:
                submission_model, producer_model = result
                return submission_model.to_entity(producer_model.to_entity())
            else:
                return None

    def update_report(self, id: int, report) -> None:
        with session_scope(self.session_factory) as session:
            model_instance = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.id == id)
                .first()
            )

            if model_instance:
                model_instance.report = report


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, user: User) -> User:
        with session_scope(self.session_factory) as session:
            user_model = UserModel.from_entity(user)
            session.add(user_model)
            session.commit()
            session.refresh(user_model)
            return user_model.to_entity()

    def get_by_email(self, email: str) -> Optional[User]:
        with session_scope(self.session_factory) as session:
            user_model = (
                session.query(UserModel).filter(UserModel.email == email).first()
            )

            if user_model:
                return user_model.to_entity()
            else:
                return None

    def get_by_id(self, id: int) -> Optional[User]:
        with session_scope(self.session_factory) as session:
            user_model = session.query(UserModel).filter(UserModel.id == id).first()

            if user_model:
                return user_model.to_entity()
            else:
                return None
