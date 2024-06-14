from flask import Blueprint

from api.v1.decorators import serialize_response, validate
from api.v1.models import SuccessResponseModel, TickerCreatePayload
from api.v1.services.calc_adjusted_close_data import calculate_adjusted_close_data

v1 = Blueprint('v1', __name__)


@v1.route('/stock/adjusted_close_data', methods=['POST'])
@validate
@serialize_response(SuccessResponseModel)
def pull_adjusted_close_data(body: TickerCreatePayload):
	return calculate_adjusted_close_data(body)
