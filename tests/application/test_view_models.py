from datetime import datetime
from nad_ch.application.view_models import (
    get_view_model,
    DataProducerViewModel,
    DataSubmissionViewModel,
)
from nad_ch.domain.entities import DataProducer, DataSubmission, ColumnMap


def test_get_a_single_data_producer_view_model():
    producer = DataProducer("State X")
    date = datetime(2024, 2, 29, 20, 48, 58, 205608)
    producer.set_created_at(date)

    result = get_view_model(producer)

    assert isinstance(result, DataProducerViewModel)
    assert result.date_created == "February 29, 2024"


def test_get_a_list_of_data_producer_view_models():
    producer_a = DataProducer("State A")
    date_a = datetime(2024, 2, 29, 20, 48, 58, 205608)
    producer_a.set_created_at(date_a)

    producer_b = DataProducer("State B")
    date_b = datetime(2024, 5, 1, 20, 48, 58, 205608)
    producer_b.set_created_at(date_b)

    result = get_view_model([producer_a, producer_b])

    assert len(result) == 2
    assert result[0].date_created == "February 29, 2024"
    assert result[1].date_created == "May 01, 2024"


def test_get_a_single_data_submisson_view_model():
    producer = DataProducer("State X")
    column_map_a = ColumnMap("MapA", producer, 1)
    submission = DataSubmission("some_file_name", producer, column_map_a)
    date = datetime(2024, 2, 29, 20, 48, 58, 205608)
    submission.set_created_at(date)

    result = get_view_model(submission)

    assert isinstance(result, DataSubmissionViewModel)
    assert result.date_created == "February 29, 2024"
    assert result.producer_name == "State X"


def test_get_a_list_of_data_submisson_view_models():
    producer_a = DataProducer("State A")
    column_map_a = ColumnMap("MapA", producer_a, 1)
    submission_a = DataSubmission("some_file_name", producer_a, column_map_a)
    date_a = datetime(2024, 2, 29, 20, 48, 58, 205608)
    submission_a.set_created_at(date_a)

    producer_b = DataProducer("State B")
    column_map_b = ColumnMap("MapB", producer_b, 1)
    submission_b = DataSubmission("some_other_file_name", producer_b, column_map_b)
    date_b = datetime(2024, 5, 1, 20, 48, 58, 205608)
    submission_b.set_created_at(date_b)

    result = get_view_model([submission_a, submission_b])

    assert len(result) == 2
    assert result[0].date_created == "February 29, 2024"
    assert result[0].producer_name == "State A"
    assert result[1].date_created == "May 01, 2024"
    assert result[1].producer_name == "State B"
