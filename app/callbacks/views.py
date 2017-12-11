from flask import jsonify, request
from flask import current_app
from ..models import Message
from . import callback


@callback.route('/sms-sync', methods=['get', 'post'])
def sms_callback():
    api_payload = request.get_json()

    current_app.logger.warn("received: {}".format(api_payload))

    return jsonify({"payload": {"success": True, "error": None}}), 200
