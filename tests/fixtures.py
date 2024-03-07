import os
import pytest
import yaml
import glob
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nad_ch.domain.entities import DataProducer, DataSubmission, ColumnMap
from nad_ch.infrastructure.database import (
    ModelBase,
    SqlAlchemyDataProducerRepository,
    SqlAlchemyDataSubmissionRepository,
    SqlAlchemyColumnMapRepository,
    SqlAlchemyUserRepository,
)
from nad_ch.config import DATABASE_URL

BASE_PATH = pathlib.Path(__file__).parent.resolve()


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
def test_provider_column_maps(repositories):
    producers, _, column_maps, _ = repositories
    new_producer = DataProducer("Producer A")
    saved_producer = producers.add(new_producer)
    test_column_maps_path = os.path.join(BASE_PATH, "test_data/column_maps")
    for test_column_map_path in glob.glob(f"{test_column_maps_path}/*.yaml"):
        column_map_name = os.path.splitext(os.path.basename(test_column_map_path))[0]
        with open(test_column_map_path, "r") as file:
            mapping = yaml.safe_load(file)
            new_column_map = ColumnMap(column_map_name, saved_producer, mapping, 1)
        _ = column_maps.add(new_column_map)

    return column_maps


@pytest.fixture(scope="function")
def users(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyUserRepository(Session)


@pytest.fixture(scope="function")
def submissions(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataSubmissionRepository(Session)


@pytest.fixture(scope="function")
def producers(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataProducerRepository(Session)


@pytest.fixture(scope="function")
def repositories(test_database):
    Session = sessionmaker(bind=test_database)
    return (
        SqlAlchemyDataProducerRepository(Session),
        SqlAlchemyDataSubmissionRepository(Session),
        SqlAlchemyColumnMapRepository(Session),
        SqlAlchemyUserRepository(Session),
    )
