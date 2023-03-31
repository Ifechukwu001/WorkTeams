"""Blueprint for the Webpages"""
from flask import Blueprint

page_views = Blueprint("page_views", __name__)

from flask_app.pages.home import *
from flask_app.pages.login import *
from flask_app.pages.logout import *
from flask_app.pages.register import *