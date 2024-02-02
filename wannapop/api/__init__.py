from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import orders, statuses, users, errors, categories, orders, products