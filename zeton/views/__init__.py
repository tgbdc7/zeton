from flask import Blueprint

bp = Blueprint('views', __name__)

from . import index, settings, details
