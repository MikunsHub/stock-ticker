from api.v1.endpoints import v1
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})


app.register_blueprint(v1, url_prefix='/api/v1')

if __name__ == '__main__':
	app.run(port=5002, debug=True)
