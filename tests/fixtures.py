import os
import pytest
import yaml
import glob
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nad_ch.core.entities import (
    DataProducer,
    DataSubmissionStatus,
    DataSubmission,
    ColumnMap,
    User,
)
from nad_ch.infrastructure.database import (
    ModelBase,
    SqlAlchemyDataProducerRepository,
    SqlAlchemyDataSubmissionRepository,
    SqlAlchemyColumnMapRepository,
    SqlAlchemyUserRepository,
)
from nad_ch.config import DATABASE_URL

BASE_PATH = pathlib.Path(__file__).parent.resolve()
TEST_COLUMN_MAPS_PATH = os.path.join(BASE_PATH, "test_data/column_maps")


@pytest.fixture(scope="function")
def test_database():
    engine = create_engine(DATABASE_URL, echo=True)
    ModelBase.metadata.create_all(engine)
    yield engine
    ModelBase.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def column_maps(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyColumnMapRepository(Session)


@pytest.fixture(scope="function")
def producer_column_maps(repositories):
    producers, _, column_maps, _ = repositories
    new_producer = DataProducer("Producer A")
    saved_producer = producers.add(new_producer)

    for test_column_map_path in sorted(glob.glob(f"{TEST_COLUMN_MAPS_PATH}/*.yaml")):
        column_map_name = os.path.splitext(os.path.basename(test_column_map_path))[0]
        with open(test_column_map_path, "r") as file:
            mapping = yaml.safe_load(file)
            new_column_map = ColumnMap(column_map_name, saved_producer, mapping, 1)
        _ = column_maps.add(new_column_map)

    return column_maps


@pytest.fixture(scope="function")
def producer_column_maps_and_submissions(repositories):
    producers, submissions, column_maps, _ = repositories

    column_map_entities, producer_entities = [], []
    for i, test_column_map_path in enumerate(
        sorted(glob.glob(f"{TEST_COLUMN_MAPS_PATH}/*.yaml"))
    ):
        new_producer = DataProducer(f"Producer {i + 1}")
        producer_entities.append(producers.add(new_producer))

        column_map_name = os.path.splitext(os.path.basename(test_column_map_path))[0]
        with open(test_column_map_path, "r") as file:
            mapping = yaml.safe_load(file)
            new_column_map = ColumnMap(
                column_map_name, producer_entities[i], mapping, 1
            )
        column_map_entities.append(column_maps.add(new_column_map))

    new_submission1 = DataSubmission(
        "testproducer1-submission",
        DataSubmissionStatus.VALIDATED,
        producer_entities[0],
        column_map_entities[0],
    )
    new_submission2 = DataSubmission(
        "testproducer2-submission",
        DataSubmissionStatus.VALIDATED,
        producer_entities[1],
        column_map_entities[1],
    )
    _ = submissions.add(new_submission1)
    _ = submissions.add(new_submission2)
    return column_maps, submissions


@pytest.fixture(scope="function")
def users(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyUserRepository(Session)


@pytest.fixture(scope="function")
def users_xyz(users):
    user_names = ("X", "Y", "Z")
    for name in user_names:
        new_user = User(
            email=f"user{name}@gmail.com",
            login_provider=f"{name}.com",
            logout_url=f"dummy logout value for {name}",
        )
        users.add(new_user)
    return users


@pytest.fixture(scope="function")
def submissions(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataSubmissionRepository(Session)


@pytest.fixture(scope="function")
def producers(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataProducerRepository(Session)


@pytest.fixture(scope="function")
def producers_xyz(producers):
    producer_names = ("State X", "State Y", "State Z")
    for producer_name in producer_names:
        new_producer = DataProducer(producer_name)
        producers.add(new_producer)
    return producers


@pytest.fixture(scope="function")
def repositories(test_database):
    Session = sessionmaker(bind=test_database)
    return (
        SqlAlchemyDataProducerRepository(Session),
        SqlAlchemyDataSubmissionRepository(Session),
        SqlAlchemyColumnMapRepository(Session),
        SqlAlchemyUserRepository(Session),
    )
