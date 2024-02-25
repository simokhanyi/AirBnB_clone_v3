#!/usr/bin/python3
"""
Initializes the views module
"""

from flask import Blueprint

# Create the blueprint object
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import the views to register the routes
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
