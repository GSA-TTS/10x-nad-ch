from datetime import datetime
from nad_ch.application.view_models import (
    get_view_model,
    DataProviderViewModel,
    DataSubmissionViewModel,
)
from nad_ch.domain.entities import DataProvider, DataSubmission


def test_get_a_single_data_provider_view_model():
    provider = DataProvider("State X")
    date = datetime(2024, 2, 29, 20, 48, 58, 205608)
    provider.set_created_at(date)

    result = get_view_model(provider)

    assert isinstance(result, DataProviderViewModel)
    assert result.date_created == "February 29, 2024"


def test_get_a_list_of_data_provider_view_models():
    provider_a = DataProvider("State A")
    date_a = datetime(2024, 2, 29, 20, 48, 58, 205608)
    provider_a.set_created_at(date_a)

    provider_b = DataProvider("State B")
    date_b = datetime(2024, 5, 1, 20, 48, 58, 205608)
    provider_b.set_created_at(date_b)

    result = get_view_model([provider_a, provider_b])

    assert len(result) == 2
    assert result[0].date_created == "February 29, 2024"
    assert result[1].date_created == "May 01, 2024"


def test_get_a_single_data_submisson_view_model():
    provider = DataProvider("State X")
    submission = DataSubmission("some_file_name", provider)
    date = datetime(2024, 2, 29, 20, 48, 58, 205608)
    submission.set_created_at(date)

    result = get_view_model(submission)

    assert isinstance(result, DataSubmissionViewModel)
    assert result.date_created == "February 29, 2024"
    assert result.provider_name == "State X"


def test_get_a_list_of_data_submisson_view_models():
    provider_a = DataProvider("State A")
    submission_a = DataSubmission("some_file_name", provider_a)
    date_a = datetime(2024, 2, 29, 20, 48, 58, 205608)
    submission_a.set_created_at(date_a)

    provider_b = DataProvider("State B")
    submission_b = DataSubmission("some_other_file_name", provider_b)
    date_b = datetime(2024, 5, 1, 20, 48, 58, 205608)
    submission_b.set_created_at(date_b)

    result = get_view_model([submission_a, submission_b])

    assert len(result) == 2
    assert result[0].date_created == "February 29, 2024"
    assert result[0].provider_name == "State A"
    assert result[1].date_created == "May 01, 2024"
    assert result[1].provider_name == "State B"
