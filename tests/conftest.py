import pytest

from interfaces.alpha_vantage import AlphaVantageAPIClient
from tests.stubs.alpha_vantage import mocked_response as alphavantage_mocked_response


@pytest.fixture
def mock_alphavantage_api_client():
	with AlphaVantageAPIClient() as client:
		yield client


@pytest.fixture
def mock_symbol():
	return 'AAPL'


@pytest.fixture
def alphavantage_mocked_responses():
	return alphavantage_mocked_response()
