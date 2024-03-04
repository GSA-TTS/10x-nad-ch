import pytest
from nad_ch.application.use_cases.data_producers import (
    add_data_producer,
    list_data_producers,
)
from nad_ch.application.view_models import DataProducerViewModel
from nad_ch.config import create_app_context
from tests.application.use_cases import is_valid_date_format


@pytest.fixture(scope="function")
def app_context():
    context = create_app_context()
    yield context


def test_add_data_producer(app_context):
    name = "State X"

    result = add_data_producer(app_context, name)

    assert isinstance(result, DataProducerViewModel)
    assert is_valid_date_format(result.date_created)


def test_add_data_producer_logs_error_if_no_producer_name_given(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    add_data_producer(mock_context, "")
    mock_context.logger.error.assert_called_once_with("Producer name required")


def test_add_data_producer_logs_error_if_producer_name_not_unique(mocker):
    mock_context = mocker.patch("nad_ch.config.create_app_context")
    mock_context.producer.get_by_name.return_value("State X")
    add_data_producer(mock_context, "State X")

    mock_context.logger.error.assert_called_once_with("Producer name must be unique")


def test_list_a_single_data_producer(app_context):
    name = "State X"
    add_data_producer(app_context, name)

    result = list_data_producers(app_context)

    assert len(result) == 1
    assert isinstance(result[0], DataProducerViewModel)
    assert result[0].name == name


def test_list_multiple_data_producers(app_context):
    first_name = "State X"
    add_data_producer(app_context, first_name)

    second_name = "State Y"
    add_data_producer(app_context, second_name)

    result = list_data_producers(app_context)
    assert len(result) == 2
    assert isinstance(result[0], DataProducerViewModel)
    assert result[0].name == first_name
    assert isinstance(result[1], DataProducerViewModel)
    assert result[1].name == second_name
