from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user, current_user
from . import db

# create a blueprint
bp = Blueprint('auth', __name__)


# https://stackoverflow.com/questions/13585663/flask-wtfform-flash-does-not-display-errors
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)

# login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # check login validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()
        # find user by email and password
        if user is None or not check_password_hash(user.password, request.form.get('password')):
            # not match
            flash('invalid email or password!')
        else:
            # match
            login_user(user)
            return redirect(url_for('main.homePage'))
    else:
        flash_errors(form)
    return render_template(
        'renderforms.html',
        form=form,
        formTitle='Login',
        user=current_user
    )


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    # check signup form validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user:
            # user already exist
            flash('Email is taken, pls try another')
        else:
            # create new user
            u = User(
                email=request.form.get('email'),
                password=generate_password_hash(request.form.get('password'), method='sha256'),
                name=request.form.get('name'),
                contact=request.form.get('contact'),
                address=request.form.get('address'),
            )

            db.session.add(u)
            db.session.commit()
            # login and redirect
            login_user(u)
            return redirect(url_for('main.homePage'))
    else:
        flash_errors(form)
    return render_template(
        'renderforms.html',
        form=form,
        formTitle='Signup',
        user=current_user
    )


@bp.route('/logout')
def logout():
    # logout user
    logout_user()
    return redirect(url_for('auth.login'))
