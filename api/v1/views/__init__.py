#!/usr/bin/python3
""" intializes blueprints for app_views """
from flask import Blueprint
app_views = Blueprint('my_view', __name__)
from .states import *
from .index import *
