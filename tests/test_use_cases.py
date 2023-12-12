import pytest
from nad_ch.application_context import create_app_context
from nad_ch.entities import DataProvider
from nad_ch.use_cases import add_data_provider, ingest_data_submission


@pytest.fixture(scope='function')
def app_context():
    context = create_app_context()
    yield context


def test_add_data_provider(app_context):
    name = 'State X'
    add_data_provider(app_context, name)

    provider = app_context.providers.get_by_name(name)
    assert provider.name == name
    assert isinstance(provider, DataProvider) is True


# def test_ingest_data_submission(app_context):
#     # Arrange
#     provider = DataProvider('State X')
#     app_context.providers.add(provider)

#     # Act
#     ingest_data_submission(app_context, 'some_file_path', provider.name)

#     # Assert
#     submission = app_context.submissions.get_by_file_path('some_file_path')
#     assert submission.file_path == 'some_file_path'
#     assert submission.provider.name == provider.name
