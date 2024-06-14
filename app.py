from api.v1.endpoints import v1
from flask import Flask


app = Flask(__name__)


app.register_blueprint(v1, url_prefix='/api/v1')

if __name__ == '__main__':
	app.run(debug=True)
