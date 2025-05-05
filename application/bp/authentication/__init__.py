from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user

from application.database.models import User
from application.bp.authentication.forms import RegisterForm, LoginForm

authentication = Blueprint('authentication', __name__, template_folder='templates')


@authentication.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        existing_user = User.find_user_by_email(email)
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('authentication.registration'))

        new_user = User.create(email, password)
        new_user.save()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('authentication.login'))

    return render_template('registration.html', form=form)


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User Not Found', 'danger')
            return redirect(url_for('authentication.login'))

        if not user.check_password(password):
            flash('Password Incorrect', 'danger')
            return redirect(url_for('authentication.login'))

        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('authentication.dashboard'))

    return render_template('login.html', form=form)


@authentication.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email, user_id=current_user.id)


@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('homepage.homepage'))


@authentication.route('/users')
def users():
    return render_template('users.html', users=User.all())


@authentication.route('/user/<int:user_id>')
def user_by_id(user_id):
    user = User.find_user_by_id(user_id)
    return render_template('user.html', user=user)
