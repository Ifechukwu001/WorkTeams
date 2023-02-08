"""Blueprint for the Webpages"""
from flask import Blueprint

page_views = Blueprint("page_views", __name__)

from app.pages.home import *
from app.pages.login import *
from app.pages.logout import *
from app.pages.register import *