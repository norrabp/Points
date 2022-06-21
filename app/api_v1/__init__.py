""" Module containing REST API endpoints """
from flask import Blueprint

api = Blueprint('api', __name__)

from . import points, errors
