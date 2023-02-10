#!/usr/bin/python3
"""The API App module"""
from flask import Flask
from api.endpoints import api_views

app = Flask(__name__)
app.register_blueprint(api_views, url_prefix="/api")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")