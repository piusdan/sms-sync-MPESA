from flask import render_template, jsonify, make_response

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



