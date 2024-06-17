from flask import Blueprint

from api.v1.decorators import serialize_response, validate
from api.v1.models import (
	ErrorResponseModel,
	StockSearchQueryParams,
	StockSearchResponseModel,
	SuccessResponseModel,
	TickerCreatePayload,
)
from api.v1.services.calc_adjusted_close_data import calculate_adjusted_close_data
from api.v1.services.search_for_ticker import search_alpha_vantage_for_ticker

v1 = Blueprint('v1', __name__)
# In-memory cache(upgrade to Redis)
cache: dict = {}


@v1.route('/stock/adjusted_close_data', methods=['POST'])
@validate
@serialize_response(SuccessResponseModel, ErrorResponseModel)
def pull_adjusted_close_data(body: TickerCreatePayload):
	return calculate_adjusted_close_data(body)


@v1.route('/stock/search', methods=['GET'])
@validate
@serialize_response(StockSearchResponseModel, ErrorResponseModel)
def search_for_stock_ticker(query: StockSearchQueryParams):
	return search_alpha_vantage_for_ticker(query.keyword, cache)
