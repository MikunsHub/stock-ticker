from typing import Any
from pydantic import BaseModel, ConfigDict


class TickerCreatePayload(BaseModel):
	model_config = ConfigDict(extra='forbid')
	stock_symbol: str


class SuccessResponseModel(BaseModel):
	message: str
	adjusted_data: list[dict[str, Any]]

	class Config:
		from_attributes = True
