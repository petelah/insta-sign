from src.forms import NewPostForm, CommentForm, AccountUpdateForm, SignInForm, BusinessRegistrationForm
from flask import Blueprint, request, abort, render_template, redirect, url_for
from flask_login import current_user, login_required
from src.services import new_post_svc, single_post_svc, get_user_by_username, add_comment_svc, save_profile_settings_svc, sign_in_svc, delete_post_svc, business_register_svc

profile_view = Blueprint('profile_view', __name__, url_prefix="/")


@profile_view.route('/<string:username>/new_post', methods=['GET', "POST"])
@login_required
def new_post(username):
	"""
	Route to create a new post for the front end.
	:param username:
	:return: render_template object
	"""
	form = NewPostForm()
	if form.validate_on_submit():
		post_id = new_post_svc(
			current_user.id,
			form.content.data,
			form.image.data
		)
		return redirect(url_for('profile_view.single_post', username=current_user.username, id=post_id))
	return render_template('new_post.jinja2', form=form)


@profile_view.route('/<string:username>/post/<int:id>/delete', methods=['GET', "POST"])
@login_required
def delete_post(username, id):
	"""
	Route to delete a post from the db for the front end.
	:param username:
	:param id:
	:return: redirect object
	"""
	del_post = delete_post_svc(current_user.id, id)
	if not del_post:
		return abort(404)
	return redirect(url_for('main_view.profile', username=username))


@profile_view.route('/<string:username>/post/<int:id>', methods=['GET', "POST"])
def single_post(username, id):
	"""
	Returns a view of a single post for a user to read comments and comment on when logged in.
	:param username:
	:param id:
	:return: render_tempalte object
	"""
	logged_user = False
	form = CommentForm()
	post = single_post_svc(id)
	user = get_user_by_username(username)
	if current_user.is_authenticated and current_user.id == user.id:
		logged_user = True
	if current_user.is_authenticated:
		if form.validate_on_submit():
			add_comment_svc(
				current_user.id,
				id,
				form.content.data
			)
			return redirect(url_for('profile_view.single_post', username=username, id=id))

	return render_template('post.html', post=post, form=form, logged_user=logged_user, username=username)


@profile_view.route('/<string:username>/update', methods=["GET", "POST"])
@login_required
def update_account(username):
	"""
	Forms to update user account on front end.
	:param username:
	:return: render_template object
	"""
	user = get_user_by_username(username)
	form = AccountUpdateForm()
	if request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.first_name.data = current_user.f_name
		form.last_name.data = current_user.l_name
		form.bio.data = current_user.bio

	if current_user.id == user.id:
		if form.validate_on_submit():
			save_profile_settings_svc(
				current_user.id,
				profile_picture=form.profile_picture.data,
				email=form.email.data,
				username=form.username.data,
				f_name=form.first_name.data,
				l_name=form.last_name.data,
				bio=form.bio.data,
			)
			return redirect(url_for('main_view.profile', username=current_user.username))
	return render_template('update_account.jinja2', form=form)


@profile_view.route('/<string:username>/business_register', methods=["GET", "POST"])
@login_required
def business_register(username):
	"""
	If a user wishes to register a business with instagram from their account update page.
	Used for the front end.
	:param username:
	:return: render_template object
	"""
	form = BusinessRegistrationForm()
	if request.method == "GET":
		form.email.data = current_user.email
		form.business_name.data = current_user.username
	if form.validate_on_submit():
		business_register_svc(
			current_user.id,
			email=form.email.data,
			business_name=form.business_name.data,
			address=form.address.data,
			state=form.state.data,
			post_code=form.post_code.data,
			country=form.country.data
		)
		return redirect(url_for('main_view.profile', username=username))
	return render_template('business_register.jinja2', form=form)


@profile_view.route('/<string:username>/sign_in', methods=["GET", "POST"])
def sign_in(username):
	"""
	Allows users and anonymous users to sign into a business or venue if
	it is verified.
	:param username:
	:return:
	"""
	form = SignInForm()
	if request.method == "GET" and current_user.is_authenticated:
		form.email.data = current_user.email
		form.name.data = current_user.f_name + ' ' + current_user.l_name
		if current_user.is_authenticated:
			if current_user.is_following(get_user_by_username(username)):
				form.follow.data = True

	if form.validate_on_submit():
		sign_in_svc(
			username,
			name=form.name.data,
			email=form.email.data,
			signup=form.sign_up.data,
			follow=form.follow.data,
			symptoms=form.symptoms.data
		)
		return redirect(url_for('main_view.profile', username=username))
	return render_template('sign_in.jinja2', form=form)


