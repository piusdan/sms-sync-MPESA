from flask import jsonify, request
from flask import current_app
from ..models import Message
from . import callback
from ..utils import parse_message, ParseError
import uuid


@callback.route('/sms-sync', methods=['get', 'post'])
def sms_callback():
    api_payload = request.get_json()
    from_ = api_payload.get("from")
    message_id = api_payload.get("message_id") or str(uuid.uuid1())
    message = api_payload.get("message")
    if Message.by_code(message_id) is None:
        try:
            parse_message(message)
        except ParseError as exec:
            return jsonify({"payload": {"success": False, "error": "".format(exec)}}), 300
        sms = Message.create(text=message, code=message_id, to_=api_payload.get("sent_to"), from_=from_)
        current_app.logger.warn("{}".format(sms.to_dict()))
    else:
        current_app.logger.warn("Not saved: {}".format(message))

    return jsonify({"payload": {"success": True, "error": None}}), 200
