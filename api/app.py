#!/usr/bin/python3
"""The API App module"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.endpoints import api_views

app = Flask(__name__)
app.register_blueprint(api_views, url_prefix="/api")
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")