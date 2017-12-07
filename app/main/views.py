from flask import render_template, jsonify, make_response

from . import main


@main.route('/')
def index():
    return make_response(jsonify({"message":"connection OK"})), 200
