#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint('my_view', __name__)
from .index import *
