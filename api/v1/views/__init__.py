""" views init """
from flask import Blueprint
from models.user import User
from models.city import City
from models.state import State
from models.review import Review


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

"""Wildcard import views"""
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.amenities import *
from api.v1.views.places_reviews import *
