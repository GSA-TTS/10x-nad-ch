from nad_ch.domain.entities import DataProducer, DataSubmission, ColumnMap
from tests.fixtures import *


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


def test_add_data_producer_and_then_data_submission(repositories):
    producers, submissions, column_maps, users = repositories
    producer_name = "State X"
    new_producer = DataProducer(producer_name)
    saved_producer = producers.add(new_producer)
    new_column_map = ColumnMap("TestMap", saved_producer, version_id=1)
    saved_column_map = column_maps.add(new_column_map)
    new_submission = DataSubmission("some-file-name", saved_producer, saved_column_map)

    result = submissions.add(new_submission)

    assert result.id == 1
    assert result.created_at is not None
    assert result.updated_at is not None
    assert result.producer.id == saved_producer.id
    assert result.filename == "some-file-name"


def test_retrieve_a_list_of_submissions_by_producer(repositories):
    producers, submissions, column_maps, users = repositories
    producer_name = "State X"
    new_producer = DataProducer(producer_name)
    saved_producer = producers.add(new_producer)
    new_column_map = ColumnMap("TestMap", saved_producer, version_id=1)
    saved_column_map = column_maps.add(new_column_map)
    new_submission = DataSubmission("some-file-name", saved_producer, saved_column_map)
    submissions.add(new_submission)
    another_new_submission = DataSubmission(
        "some-other-file-name", saved_producer, saved_column_map
    )
    submissions.add(another_new_submission)

    submissions = submissions.get_by_producer(saved_producer)

    assert len(submissions) == 2
