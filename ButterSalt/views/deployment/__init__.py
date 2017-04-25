from flask import Blueprint

deployment = Blueprint('deployment', __name__, url_prefix='/deployment')

from .sytem import system
from .product import product
