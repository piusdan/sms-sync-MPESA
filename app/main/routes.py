from flask import render_template, jsonify, make_response
from flask_login import login_required

from ..models import Message

from . import main


@main.route('/')
def index():
    messages = Message.query.all()
    new = Message.query.filter_by(seen=False)
    return render_template('index.html', messages=messages, new=new)


@main.route('/dashboard')
def dashboard():
    return render_template('index.html')


@main.route('/reset', methods=['DELETE'])
def reset():
    """Clears all messages"""
    for message in Message.query.all():
        message.delete()
    response = jsonify({"data": "App Reset"})
    return response, 200


@main.before_request
@login_required
def init_session():
    pass