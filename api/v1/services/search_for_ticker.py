from typing import Any
from api.v1.models import StockSearchResponseModel, ErrorResponseModel
from interfaces.alpha_vantage import AlphaVantageAPIClient, AlphaVantageAPIClientError
from interfaces.constants import AlphaVantageResources
from api.v1.services.constants import key_mapping


def transform_match(key_mapping: dict[str, str], match: dict[str, Any]) -> dict[str, Any]:
	return {key_mapping[key]: value for key, value in match.items() if key in key_mapping}


def search_alpha_vantage_for_ticker(keyword: str, cache: dict):
	try:
		keyword = keyword.strip('"')
		if keyword in cache:
			return cache[keyword]

		with AlphaVantageAPIClient() as client:
			response = client.fetch_data(AlphaVantageResources.SYMBOL_SEARCH, keywords=keyword)

		matches = [transform_match(key_mapping, match) for match in response.get('bestMatches', [])]
		result = StockSearchResponseModel(message='Successful', data=matches)
		cache[keyword] = result
		return result

	except AlphaVantageAPIClientError as e:
		return ErrorResponseModel(message=str(e), data=[])

	except Exception:
		return ErrorResponseModel(message='An unexpected error occurred', data=[])
