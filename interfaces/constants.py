from enum import Enum
from string import Template


AUTHORIZATION = 'authorization'
BEARER = 'Bearer'
API_KEY = 'apikey'
GET = 'GET'
POST = 'POST'
BASE_URL = 'base_url'


class AlphaVantageResources(Enum):
	TIME_SERIES_DAILY = (
		Template(
			'${base_url}/query?function=TIME_SERIES_DAILY&symbol=${symbol}&outputsize=${outputsize}&apikey=${apikey}'
		),
		(('outputsize', 'compact'),),
	)
	DIVIDENDS = (
		Template('${base_url}/query?function=DIVIDENDS&symbol=${symbol}&apikey=${apikey}'),
		(),
	)
	SPLITS = (
		Template('${base_url}/query?function=SPLITS&symbol=${symbol}&apikey=${apikey}'),
		(),
	)
	SYMBOL_SEARCH = (
		Template('${base_url}/query?function=SYMBOL_SEARCH&keywords=${keywords}&datatype=${datatype}&apikey=${apikey}'),
		(('datatype', 'json'),),
	)
	TOP_GAINERS_LOSERS = (
		Template('${base_url}/query?function=TOP_GAINERS_LOSERS&apikey=${apikey}'),
		(),
	)
