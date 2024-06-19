from datetime import datetime
from typing import Any, Dict, List
from api.v1.models import SuccessResponseModel, TickerCreatePayload, WatchlistResponseModel
from api.v1.services.constants import (
	OPEN_KEY,
	CLOSE_KEY,
	HIGH_KEY,
	LOW_KEY,
	VOLUME_KEY,
	DIVIDEND_AMOUNT_KEY,
	SPLIT_RATIO_KEY,
)
from database.db_setup import use_db
from interfaces.alpha_vantage import AlphaVantageAPIClient, AlphaVantageAPIClientError
from interfaces.constants import AlphaVantageResources, EODHDResources

from interfaces.eohd import EODHDAPIClient


@use_db('stock_data')
def get_stock_data_from_db(collections, stock_symbol: str):
	adjusted_data = collections['stock_data'].find_one({'ticker': stock_symbol})
	return SuccessResponseModel(message='Ticker added successfully', adjusted_data=adjusted_data['data'])


@use_db('watchlist')
def upsert_ticker_to_watchlist(collections, stock_symbol: str, close_price: float):
	collections['watchlist'].update_one(
		{'ticker': stock_symbol},
		{'$set': {'ticker': stock_symbol, 'close_price': close_price}},  # This ensures upsert works correctly
		upsert=True,
	)


@use_db('watchlist')
def get_watchlist_data(collections):
	watchlist_cursor = collections['watchlist'].find()
	watchlist = []
	for doc in watchlist_cursor:
		doc.pop('_id', None)
		watchlist.append(doc)
	return WatchlistResponseModel(message='successful', data=list(watchlist))


@use_db('stock_data')
def store_adjusted_close_data(collections, stock_symbol: str, adjusted_data: List[Dict[str, Any]]):
	collections['stock_data'].update_one(
		{'ticker': stock_symbol},
		{'$set': {'ticker': stock_symbol, 'data': adjusted_data}},
		upsert=True,
	)


def apply_splits(date: datetime, price: float, splits: Dict[datetime, float]) -> float:
	for split_date, ratio in sorted(splits.items()):
		if date >= split_date:
			price /= ratio
	return price


def apply_dividends(date: datetime, price: float, dividends: Dict[datetime, float]) -> float:
	if date in dividends:
		price -= dividends[date]
	return price


def adjust_prices(
	time_series: Dict[str, Any], dividends: List[Dict[str, Any]], splits: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
	processed_splits = {
		datetime.strptime(split['effective_date'], '%Y-%m-%d'): float(split[SPLIT_RATIO_KEY]) for split in splits
	}
	processed_dividends = {
		datetime.strptime(dividend['ex_dividend_date'], '%Y-%m-%d'): float(dividend[DIVIDEND_AMOUNT_KEY])
		for dividend in dividends
	}

	adjusted_data = []
	for date_str, daily_data in sorted(time_series.items()):
		date = datetime.strptime(date_str, '%Y-%m-%d')
		formatted_date = date.strftime('%Y-%m-%d')
		close_price = float(daily_data[CLOSE_KEY])
		adjusted_close = close_price

		# Apply splits first, then dividends
		adjusted_close = apply_splits(date, adjusted_close, processed_splits)
		adjusted_close = apply_dividends(date, adjusted_close, processed_dividends)

		adjusted_data.append(
			{
				'date': formatted_date,
				'open': float(daily_data[OPEN_KEY]),
				'high': float(daily_data[HIGH_KEY]),
				'low': float(daily_data[LOW_KEY]),
				'close': close_price,
				'adjusted_close': adjusted_close,
				'volume': int(daily_data[VOLUME_KEY]),
			}
		)
	return adjusted_data


def calculate_adjusted_close_dataa(body: TickerCreatePayload):
	def fetch_and_adjust_prices(symbol: str):
		with AlphaVantageAPIClient() as client:
			try:
				daily_data = client.fetch_data(
					AlphaVantageResources.TIME_SERIES_DAILY, symbol=symbol, outputsize='compact'
				)
				dividends_data = client.fetch_data(AlphaVantageResources.DIVIDENDS, symbol=symbol)
				splits_data = client.fetch_data(AlphaVantageResources.SPLITS, symbol=symbol)

				daily_data = daily_data.get('Time Series (Daily)', {})
				dividends_data = dividends_data.get('data', {})
				splits_data = splits_data.get('data', {})

				return adjust_prices(daily_data, dividends_data, splits_data)
			except AlphaVantageAPIClientError as e:
				print(f'An error occurred: {e}')

	adjusted_data = fetch_and_adjust_prices(body.stock_symbol)
	upsert_ticker_to_watchlist(body.stock_symbol, adjusted_data[-1]['close'])

	store_adjusted_close_data(body.stock_symbol, adjusted_data)
	return SuccessResponseModel(message='Ticker added successfully', adjusted_data=adjusted_data[:5])


def calculate_adjusted_close_data(body: TickerCreatePayload):
	with EODHDAPIClient() as client:
		adjusted_data = client.fetch_data(
			EODHDResources.EOD, symbol=body.stock_symbol, _from='2023-12-01', to='2024-06-14'
		)
		upsert_ticker_to_watchlist(body.stock_symbol, adjusted_data[-1]['close'])
		store_adjusted_close_data(body.stock_symbol, adjusted_data)
	return SuccessResponseModel(message='Ticker added successfully', adjusted_data=adjusted_data)
