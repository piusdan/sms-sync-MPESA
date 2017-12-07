#!/usr/bin/env bash
export FLASK_APP=manage.py
export FLASK_DEBUG=1
gunicorn manage:app --reload