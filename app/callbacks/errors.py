from app.exceptions import InvalidUsage
from flask import jsonify

from . import callback

@callback.errorhandler(InvalidUsage)
def invalidUsage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
