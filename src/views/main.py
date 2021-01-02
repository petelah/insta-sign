from flask import Blueprint, request, abort, render_template, send_from_directory, current_app, redirect, url_for
from flask_login import current_user
from src.services import get_profile_svc

main_view = Blueprint('main_view', __name__, url_prefix="/")


@main_view.route("/", methods=["GET"])
def root():
	"""
	The root directory of the front end.
	Will redirect to users page if they are logged in or redirect to
	the login page if they are not.
	:return: render_template object
	"""
	if current_user.is_authenticated:
		return redirect(url_for('main_view.profile', username=current_user.username))
	return redirect(url_for('auth_view.login'))


@main_view.route("/<string:username>", methods=["GET"])
def profile(username):
	"""
	Shows a users profile.
	If the user is logged in and the same as the profile they can change settings or
	create new posts.
	:param username:
	:return: render_template object
	"""
	user, posts = get_profile_svc(username)
	if not user or not posts:
		return abort(404)
	logged_user = False
	if current_user.is_authenticated:
		logged_user = True
	return render_template(
		'index.html',
		user=user,
		posts=posts,
		followers=user.followers_count(),
		logged_user=logged_user
	)

