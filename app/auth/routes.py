from . import auth
from flask_login import login_required
from ..models import User, AnonymousUser
from flask import render_template


@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/reset-password')
def reset_password():
    return render_template('auth/reset_password.html')