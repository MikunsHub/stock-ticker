from functools import wraps
from typing import Type
from flask import jsonify, request, make_response
from pydantic import BaseModel, ValidationError


def serialize_response(success_model: Type[BaseModel], error_model: Type[BaseModel]):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			response = f(*args, **kwargs)
			if isinstance(response, success_model):
				return make_response(jsonify(success_model.model_validate(response).model_dump()), 200)
			elif isinstance(response, error_model):
				return make_response(jsonify(error_model.model_validate(response).model_dump()), 500)
			return response  # In case neither model matches, return the raw response

		return decorated_function

	return decorator


def validate(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		# Validate body if specified
		model = func.__annotations__.get('body')
		if model:
			try:
				body = model(**request.get_json())
				kwargs['body'] = body
			except ValidationError as ve:
				errors = [f"{err['loc'][0]}: {err['msg']}" for err in ve.errors()]
				response = jsonify({'errors': errors})
				response.status_code = 400
				return response

		# Validate query parameters if specified
		query_model = func.__annotations__.get('query')
		if query_model:
			try:
				query_params = query_model(**request.args)
				if 'keyword' in query_params.__fields_set__:
					keyword = query_params.keyword.strip('"')
					if keyword == '':
						return jsonify({'data': [], 'message': 'Successful'}), 200
				kwargs['query'] = query_params
			except ValidationError as ve:
				errors = [f"{err['loc'][0]}: {err['msg']}" for err in ve.errors()]
				response = jsonify({'errors': errors})
				response.status_code = 400
				return response

		return func(*args, **kwargs)

	return wrapper
