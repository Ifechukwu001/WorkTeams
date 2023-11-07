#!/usr/bin/python3
"""The API App module"""
from flask import Flask
from flask_cors import CORS
import models
from models import storage
from api.endpoints import api_views
from flask_apispec import FlaskApiSpec
from flask_apispec.extension import APISpec, MarshmallowPlugin

app = Flask(__name__)
app.register_blueprint(api_views, url_prefix="/api")
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='WorkTeams',
        version='v1',
        openapi_version="2.0",
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger-json/',
    'APISPEC_SWAGGER_UI_URL': '/swagger/',
})

docs = FlaskApiSpec(app, document_options=False)

for name, view in docs.app.view_functions.items():
    if name.startswith("api_views"):
        docs.register(view, blueprint="api_views")


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    print(docs.app.config)
    app.run(host="0.0.0.0", port="5001")
