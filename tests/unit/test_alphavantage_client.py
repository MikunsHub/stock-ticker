from env import ALPHA_VANTAGE_BASE_URL, ALPHA_VANTAGE_API_KEY
from interfaces.constants import API_KEY, BASE_URL, AlphaVantageResources


def test_fetch_data_success(requests_mock, mock_alphavantage_api_client, mock_symbol, alphavantage_mocked_responses):
	resource = AlphaVantageResources.TIME_SERIES_DAILY
	template, default_params = resource.value
	params = {key: value for key, value in default_params}
	params.update()
	params[API_KEY] = ALPHA_VANTAGE_API_KEY
	params[BASE_URL] = ALPHA_VANTAGE_BASE_URL
	params['symbol'] = mock_symbol
	url = template.substitute(params)
	requests_mock.get(url, json=alphavantage_mocked_responses['TIME_SERIES_DAILY'])

	data = mock_alphavantage_api_client.fetch_data(
		AlphaVantageResources.TIME_SERIES_DAILY, symbol=mock_symbol, outputsize='compact'
	)
	assert isinstance(data, dict)
