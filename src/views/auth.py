from src.forms import LoginForm, RegistrationForm
from flask import Blueprint, request, jsonify, abort, render_template, current_app, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional, create_access_token
from src.services import get_user_by_id, login_user_svc, register_user_svc
from datetime import timedelta

auth_view = Blueprint('auth_view', __name__, url_prefix="/")


@auth_view.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main_view.profile', username=current_user.username))
	form = LoginForm()
	if form.validate_on_submit():
		user = login_user_svc(
			email=form.email.data,
			password=form.password.data
		)
		if not user:
			return abort(401, description="Incorrect username and password")
		login_user(user)
		return redirect(url_for('main_view.profile', username=user.username))
	return render_template('login.html', title='login', form=form)


@auth_view.route("/register", methods=["GET", "POST"])
def register_page():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for('main_view.profile', username=current_user.username))
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = register_user_svc(email=form.email.data,
		            username=form.username.data,
		            f_name=form.first_name.data,
		            l_name=form.last_name.data,
		            password=hashed_password, )
		if user is not None:
			return redirect(url_for('auth_view.login'))
		return render_template('register.html', form=form)
	return render_template('register.html', form=form)


@auth_view.route("/logout", methods=["GET", "POST"])
def logout():
	logout_user()
	return redirect(url_for('auth_view.login'))
