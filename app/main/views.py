from flask import render_template, jsonify, make_response

from ..models import Message

from . import main


@main.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


@main.route('/dashboard')
def dashboard():
    return render_template('index.html')

