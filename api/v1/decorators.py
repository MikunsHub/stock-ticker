from functools import wraps
from flask import jsonify, request
from pydantic import ValidationError


def serialize_response(model):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			response = f(*args, **kwargs)
			return jsonify(model.from_orm(response).dict())

		return decorated_function

	return decorator


def validate(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		model = func.__annotations__.get('body')
		if not model:
			raise ValueError("No Pydantic model specified in the 'body' argument type annotation")

		try:
			body = model(**request.get_json())
			kwargs['body'] = body
		except ValidationError as ve:
			errors = [f"{err['loc'][0]}: {err['msg']}" for err in ve.errors()]
			response = jsonify({'errors': errors})
			response.status_code = 400
			return response

		return func(*args, **kwargs)

	return wrapper
