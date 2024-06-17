from datetime import datetime
from typing import Any, Dict, List
from api.v1.models import SuccessResponseModel, TickerCreatePayload
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
from interfaces.constants import AlphaVantageResources
from rich import print


@use_db('watchlist')
def upsert_ticker_to_watchlist(collections, stock_symbol: str):
	collections['watchlist'].update_one(
		{'ticker': stock_symbol},
		{'$set': {'ticker': stock_symbol}},  # This ensures upsert works correctly
		upsert=True,
	)


@use_db('stock_data')
def store_adjusted_close_data(collections, stock_symbol: str, adjusted_data: List[Dict[str, Any]]):
	collections['stock_data'].update_one(
		{'ticker': stock_symbol},
		{'$set': {'ticker': stock_symbol, 'data': adjusted_data}},
		upsert=True,
	)
	print('DONE')


def apply_splits(date: datetime, adjusted_close: float, splits: Dict[datetime, float]) -> float:
	for split_date, split_ratio in splits.items():
		if date < split_date:
			adjusted_close /= split_ratio
	return adjusted_close


def apply_dividends(date: datetime, adjusted_close: float, dividends: Dict[datetime, float]) -> float:
	for dividend_date, dividend_amount in dividends.items():
		if date <= dividend_date:
			adjusted_close -= dividend_amount
	return adjusted_close


def adjust_prices(
	time_series: Dict[str, Any], dividends: Dict[str, Any], splits: Dict[str, Any]
) -> List[Dict[str, Any]]:
	processed_splits = {
		datetime.strptime(date, '%Y-%m-%d'): float(event[SPLIT_RATIO_KEY]) for date, event in splits.items()
	}
	processed_dividends = {
		datetime.strptime(date, '%Y-%m-%d'): float(event[DIVIDEND_AMOUNT_KEY]) for date, event in dividends.items()
	}

	adjusted_data = []
	for date_str, daily_data in sorted(time_series.items()):
		date = datetime.strptime(date_str, '%Y-%m-%d')
		formatted_date = date.strftime('%Y-%m-%d')
		close_price = float(daily_data[CLOSE_KEY])
		adjusted_close = close_price

		# Adjust for splits
		adjusted_close = apply_splits(date, adjusted_close, processed_splits)

		# Adjust for dividends
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


def calculate_adjusted_close_data(body: TickerCreatePayload):
	def fetch_and_adjust_prices(symbol: str):
		with AlphaVantageAPIClient() as client:
			try:
				daily_data = client.fetch_data(
					AlphaVantageResources.TIME_SERIES_DAILY, symbol=symbol, outputsize='compact'
				)
				dividends_data = client.fetch_data(AlphaVantageResources.DIVIDENDS, symbol=symbol)
				splits_data = client.fetch_data(AlphaVantageResources.SPLITS, symbol=symbol)

				daily_data = daily_data.get('Time Series (Daily)', {})
				dividends_data = dividends_data.get('Time Series (Dividends)', {})
				splits_data = splits_data.get('Time Series (Splits)', {})

				return adjust_prices(daily_data, dividends_data, splits_data)
			except AlphaVantageAPIClientError as e:
				print(f'An error occurred: {e}')

	upsert_ticker_to_watchlist(body.stock_symbol)
	adjusted_data = fetch_and_adjust_prices(body.stock_symbol)
	from rich import print
	print(adjusted_data)
	store_adjusted_close_data(body.stock_symbol, adjusted_data)
	return SuccessResponseModel(message='Ticker added successfully', adjusted_data=adjusted_data[:5])
