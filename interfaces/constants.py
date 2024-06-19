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


class EODHDResources(Enum):
	EOD = (
		Template(
			'${base_url}/api/eod/${symbol}?from=${_from}&to=${to}&period=${period}&api_token=${api_token}&fmt=${fmt}'
		),
		(('period', 'd'), ('fmt', 'json')),
	)
	DIVIDENDS = (
		Template('${base_url}/api/div/${symbol}?from=${from}&to=${to}&api_token=${api_token}&fmt=${fmt}'),
		(('fmt', 'json'),),
	)
	SPLITS = (
		Template('${base_url}/api/splits/${symbol}?from=${from}&to=${to}&api_token=${api_token}&fmt=${fmt}'),
		(('fmt', 'json'),),
	)
	FUNDAMENTALS = (
		Template('${base_url}/api/fundamentals/${symbol}?api_token=${api_token}&fmt=${fmt}'),
		(('fmt', 'json'),),
	)
