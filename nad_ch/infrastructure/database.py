import contextlib
from typing import List, Optional
from flask_login import UserMixin
from nad_ch.core.entities import (
    DataProducer,
    DataSubmission,
    DataSubmissionStatus,
    User,
    ColumnMap,
    Role,
)
from nad_ch.core.repositories import (
    DataProducerRepository,
    DataSubmissionRepository,
    UserRepository,
    ColumnMapRepository,
    RoleRepository,
)
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Integer,
    String,
    create_engine,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Table,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON


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

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    name = Column(String, nullable=False, unique=True)

    data_submissions = relationship(
        "DataSubmissionModel", back_populates="data_producer"
    )

    column_maps = relationship("ColumnMapModel", back_populates="data_producer")
    users = relationship("UserModel", back_populates="data_producer")

    @staticmethod
    def from_entity(producer: DataProducer):
        model = DataProducerModel(name=producer.name)
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

    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(
        Enum(DataSubmissionStatus), default=DataSubmissionStatus.PENDING_SUBMISSION
    )
    data_producer_id = Column(Integer, ForeignKey("data_producers.id"), nullable=False)
    column_map_id = Column(Integer, ForeignKey("column_maps.id"), nullable=False)
    report = Column(JSON)

    data_producer = relationship("DataProducerModel", back_populates="data_submissions")
    column_map = relationship("ColumnMapModel", back_populates="data_submissions")

    @staticmethod
    def from_entity(submission: DataSubmission, producer_id: int, column_map_id: int):
        model = DataSubmissionModel(
            name=submission.name,
            file_path=submission.file_path,
            status=submission.status,
            report=submission.report,
            data_producer_id=producer_id,
            column_map_id=column_map_id,
        )
        return model

    def to_entity(self):
        producer = self.data_producer.to_entity()
        column_map = self.column_map.to_entity()
        entity = DataSubmission(
            id=self.id,
            name=self.name,
            file_path=self.file_path,
            status=self.status,
            report=self.report,
            producer=producer,
            column_map=column_map,
        )

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


user_role_association = Table(
    "user_role",
    ModelBase.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class RoleModel(CommonBase):
    __tablename__ = "roles"

    name = Column(String, nullable=False, unique=True)
    permissions = Column(JSON, nullable=False)
    users = relationship(
        "UserModel", secondary=user_role_association, back_populates="roles"
    )

    @staticmethod
    def from_entity(role: Role, session):
        existing_role = session.query(RoleModel).filter_by(name=role.name).one_or_none()
        if existing_role:
            return existing_role
        return RoleModel(id=role.id, name=role.name, permissions=role.permissions)

    def to_entity(self):
        entity = Role(id=self.id, name=self.name, permissions=self.permissions)

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
    data_producer_id = Column(Integer, ForeignKey("data_producers.id"), nullable=True)
    activated = Column(Boolean, nullable=False, default=False)

    data_producer = relationship("DataProducerModel", back_populates="users")
    roles = relationship(
        "RoleModel", secondary=user_role_association, back_populates="users"
    )

    @staticmethod
    def from_entity(user, session):
        model = UserModel(
            id=user.id,
            email=user.email,
            login_provider=user.login_provider,
            logout_url=user.logout_url,
            data_producer_id=user.producer.id if user.producer else None,
            activated=user.activated,
        )

        if hasattr(user, 'roles') and user.roles:
            model.roles = [RoleModel.from_entity(role, session) for role in user.roles]

        return model

    def to_entity(self):
        producer = self.data_producer.to_entity() if self.data_producer else None

        entity = User(
            id=self.id,
            email=self.email,
            login_provider=self.login_provider,
            logout_url=self.logout_url,
            producer=producer,
            activated=self.activated,
        )

        if self.roles:
            entity.roles = [Role(id=role.id, name=role.name, permissions=role.permissions) for role in self.roles]

        if self.created_at is not None:
            entity.set_created_at(self.created_at)

        if self.updated_at is not None:
            entity.set_updated_at(self.updated_at)

        return entity


class ColumnMapModel(CommonBase):
    __tablename__ = "column_maps"

    data_producer_id = Column(Integer, ForeignKey("data_producers.id"), nullable=False)
    name = Column(String, nullable=False)
    mapping = Column(JSON, nullable=False)
    version_id = Column(Integer, nullable=False)

    data_producer = relationship("DataProducerModel", back_populates="column_maps")
    data_submissions = relationship("DataSubmissionModel", back_populates="column_map")

    __table_args__ = (
        UniqueConstraint(
            "data_producer_id", "name", "version_id", name="column_map_unique_contraint"
        ),
    )

    @staticmethod
    def from_entity(column_map: ColumnMap, producer_id: int):
        model = ColumnMapModel(
            name=column_map.name,
            data_producer_id=producer_id,
            mapping=column_map.mapping,
            version_id=column_map.version_id,
        )
        return model

    def to_entity(self):
        producer_entity = self.data_producer.to_entity()
        entity = ColumnMap(
            id=self.id,
            name=self.name,
            version_id=self.version_id,
            mapping=self.mapping,
            producer=producer_entity,
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
            producer_model = (
                session.query(DataProducerModel)
                .filter(DataProducerModel.name == submission.producer.name)
                .first()
            )
            column_map_model = (
                session.query(ColumnMapModel)
                .filter(
                    ColumnMapModel.name == submission.column_map.name,
                    ColumnMapModel.version_id == submission.column_map.version_id,
                )
                .first()
            )
            submission_model = DataSubmissionModel.from_entity(
                submission, producer_model.id, column_map_model.id
            )
            session.add(submission_model)
            session.commit()
            session.refresh(submission_model)
            return submission_model.to_entity()

    def get_by_id(self, id: int) -> Optional[DataSubmission]:
        with session_scope(self.session_factory) as session:
            submission_model = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.id == id)
                .first()
            )

            if submission_model:
                return submission_model.to_entity()
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
                submission.to_entity() for submission in submission_models
            ]
            return submission_entities

    def get_by_file_path(self, file_path: str) -> Optional[DataSubmission]:
        with session_scope(self.session_factory) as session:
            submission_model = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.file_path == file_path)
                .first()
            )

            if submission_model:
                return submission_model.to_entity()
            else:
                return None

    def update_report(self, id: int, report) -> None:
        with session_scope(self.session_factory) as session:
            submission_model = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.id == id)
                .first()
            )

            if submission_model:
                submission_model.report = report
                session.commit()
                session.refresh(submission_model)
                return submission_model.to_entity()
            else:
                return None


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, user: User) -> User:
        with session_scope(self.session_factory) as session:
            user_model = UserModel.from_entity(user, session)
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

    def get_all(self) -> List[User]:
        with session_scope(self.session_factory) as session:
            user_models = session.query(UserModel).all()
            user_entities = [user.to_entity() for user in user_models]
            return user_entities


class SqlAlchemyRoleRepository(RoleRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, role):
        with session_scope(self.session_factory) as session:
            role_model = RoleModel(name=role.name, permissions=role.permissions)
            session.add(role_model)
            session.commit()
            session.refresh(role_model)
            return role_model.to_entity()

    def get_by_name(self, name: str) -> Optional[Role]:
        with session_scope(self.session_factory) as session:
            role_model = session.query(RoleModel).filter(RoleModel.name == name).first()
            return role_model.to_entity() if role_model else None


class SqlAlchemyColumnMapRepository(ColumnMapRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, column_map: ColumnMap) -> ColumnMap:
        with session_scope(self.session_factory) as session:
            producer_model = (
                session.query(DataProducerModel)
                .filter(DataProducerModel.name == column_map.producer.name)
                .first()
            )
            column_map_model = ColumnMapModel.from_entity(column_map, producer_model.id)
            session.add(column_map_model)
            session.commit()
            session.refresh(column_map_model)
            return column_map_model.to_entity()

    def get_all(self) -> List[ColumnMap]:
        with session_scope(self.session_factory) as session:
            column_map_models = session.query(ColumnMapModel).all()
            column_map_entities = [
                column_map.to_entity() for column_map in column_map_models
            ]
            return column_map_entities

    def get_by_data_submission(
        self, data_submission: DataSubmission
    ) -> Optional[ColumnMap]:
        with session_scope(self.session_factory) as session:
            submission_model = (
                session.query(DataSubmissionModel)
                .filter(DataSubmissionModel.id == data_submission.id)
                .first()
            )
            if submission_model:
                column_map_entity = submission_model.column_map.to_entity()
                return column_map_entity
            else:
                return None

    def get_by_id(self, id: int) -> Optional[ColumnMap]:
        with session_scope(self.session_factory) as session:
            column_map_model = (
                session.query(ColumnMapModel).filter(ColumnMapModel.id == id).first()
            )
            if column_map_model:
                return column_map_model.to_entity()
            else:
                return None

    def get_by_name_and_version(
        self, name: str, version: int = 1
    ) -> Optional[ColumnMap]:
        with session_scope(self.session_factory) as session:
            column_map_model = (
                session.query(ColumnMapModel)
                .filter(
                    ColumnMapModel.name == name, ColumnMapModel.version_id == version
                )
                .first()
            )
            if column_map_model:
                return column_map_model.to_entity()
            else:
                return None

    def get_by_producer(self, producer: DataProducer) -> List[ColumnMap]:
        with session_scope(self.session_factory) as session:
            column_map_models = (
                session.query(ColumnMapModel)
                .filter(ColumnMapModel.data_producer_id == producer.id)
                .all()
            )
            column_map_entities = [
                column_map.to_entity() for column_map in column_map_models
            ]
            return column_map_entities

    def update(self, column_map: ColumnMap) -> ColumnMap:
        with session_scope(self.session_factory) as session:
            existing_column_map = (
                session.query(ColumnMapModel)
                .filter(ColumnMapModel.id == column_map.id)
                .first()
            )

            existing_column_map.name = column_map.name
            existing_column_map.mapping = column_map.mapping
            existing_column_map.version_id += 1
            session.commit()
            session.refresh(existing_column_map)
            return existing_column_map.to_entity()
