import pytest
from nad_ch.application_context import create_app_context
from nad_ch.entities import DataProvider
from nad_ch.use_cases import (
    add_data_provider,
    list_data_providers,
    InvalidProviderNameException
)


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


def test_add_data_provider_throws_error_if_no_provider_name_given(app_context):
    with pytest.raises(InvalidProviderNameException):
        add_data_provider(app_context, '')


def test_list_data_providers(app_context):
    name = 'State X'
    add_data_provider(app_context, name)

    providers = list_data_providers(app_context)

    assert len(providers) == 1
    assert providers[0].name == name
