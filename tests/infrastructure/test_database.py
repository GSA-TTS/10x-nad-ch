import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nad_ch.domain.entities import DataProducer, DataSubmission
from nad_ch.infrastructure.database import (
    ModelBase,
    SqlAlchemyDataProducerRepository,
    SqlAlchemyDataSubmissionRepository,
)


@pytest.fixture(scope="function")
def test_database():
    engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
    ModelBase.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def producers(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataProducerRepository(Session)


@pytest.fixture(scope="function")
def submissions(test_database):
    Session = sessionmaker(bind=test_database)
    return SqlAlchemyDataSubmissionRepository(Session)


def test_add_data_producer_to_repository_and_get_by_name(producers):
    producer_name = "State X"
    new_producer = DataProducer(producer_name)

    producers.add(new_producer)

    retrieved_producer = producers.get_by_name(producer_name)
    assert retrieved_producer.id == 1
    assert retrieved_producer.created_at is not None
    assert retrieved_producer.updated_at is not None
    assert retrieved_producer.name == producer_name
    assert isinstance(retrieved_producer, DataProducer) is True


def test_add_data_producer_and_then_data_submission(producers, submissions):
    producer_name = "State X"
    new_producer = DataProducer(producer_name)
    saved_producer = producers.add(new_producer)
    new_submission = DataSubmission("some-file-name", saved_producer)

    result = submissions.add(new_submission)

    assert result.id == 1
    assert result.created_at is not None
    assert result.updated_at is not None
    assert result.producer.id == saved_producer.id
    assert result.filename == "some-file-name"


def test_retrieve_a_list_of_submissions_by_producer(producers, submissions):
    producer_name = "State X"
    new_producer = DataProducer(producer_name)
    saved_producer = producers.add(new_producer)
    new_submission = DataSubmission("some-file-name", saved_producer)
    submissions.add(new_submission)
    another_new_submission = DataSubmission("some-other-file-name", saved_producer)
    submissions.add(another_new_submission)

    submissions = submissions.get_by_producer(saved_producer)

    assert len(submissions) == 2
