from . import auth
from flask_login import login_required
from ..models import User, AnonymousUser, Auth
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user
from .forms import LoginForm
from flask import flash
from ..utils import is_safe_url


@auth.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_auth = Auth.query.filter_by(email=form.email.data).first()
        user = user_auth.user
        if user_auth is not None and user_auth.verify_password(form.password.data) and user is not None:
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if not is_safe_url(next):
                abort(404)
            flash(message='Logged In Successfuly', category="success")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid Username or Password', category='warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category="warning")
    return redirect(url_for('.login'))


@auth.route('/reset-password', methods=['post', 'get'])
def reset_password():
    return render_template('auth/reset_password.html')