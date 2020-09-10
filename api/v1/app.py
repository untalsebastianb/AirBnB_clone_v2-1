#!/usr/bin/python3
""" Status of our API """
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(error):
    """ Close db session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handler error 404 """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default=5000),
        debug=True, threaded=True,
    )
