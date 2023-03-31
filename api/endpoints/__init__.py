from flask import Blueprint

api_views = Blueprint("api_views", __name__)

from api.endpoints.users import *
from api.endpoints.reports import *
from api.endpoints.steps import *
from api.endpoints.tasks import *
from api.endpoints.auth import *
