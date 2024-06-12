from alpha_vantage.timeseries import TimeSeries
from constants import JSON
from env import ALPHA_VANTAGE_API_KEY, MONGO_USER, MONGO_PASSWORD, MONGO_HOST
from rich import print
from pymongo import MongoClient

MONGO_PORT = 27017
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format=JSON)
client: MongoClient = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/')

# db = client.stock_ticker
# people = db.people

# people.insert_one({'name': 'Ayomikun', 'age':'24'})

# for person in people.find():
#     print(person)

data = ts.get_daily('AAPL')

print(data)
