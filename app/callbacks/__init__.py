from flask import Blueprint

callback = Blueprint('callback', __name__)

from . import errors, views, tasks
