from functools import wraps
from pymongo import MongoClient

from env import MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT

client: MongoClient = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/')

db = client.stock_ticker

ALLOWED_COLLECTIONS = ['watchlist', 'stock_data']


def use_db(*collection_names):
	# Check if all provided collection names are in the allowed list
	for collection_name in collection_names:
		if collection_name not in ALLOWED_COLLECTIONS:
			raise ValueError(
				f"Collection '{collection_name}' is not allowed. Allowed collections are: {ALLOWED_COLLECTIONS}"
			)

	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			# Create a dictionary with collection name keys and collection objects as values
			collections = {name: db[name] for name in collection_names}
			return func(collections, *args, **kwargs)

		return wrapper

	return decorator
