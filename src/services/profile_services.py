from src.models import Posts, Business, SignIn
from src import db
from src.services.helpers import get_user_by_id, get_user_by_username, get_user_by_email
from werkzeug.utils import secure_filename
import os


def get_profile_svc(username):
	user = get_user_by_username(username)
	if user is None:
		return False, False
	posts = Posts.query.filter_by(user_id=user.id).all()
	return user, posts


def sign_in_svc(username, **kwargs):
	user = get_user_by_username(username)
	if user is None:
		return None
	business = Business.query.filter_by(user_id=user.id).first()
	if business.verified:
		new_sign_in = SignIn(
			business_id=business.id,
			name=kwargs["name"],
			email=kwargs["email"],
			signup=kwargs["signup"],
			symptoms=kwargs["symptoms"],
			follow=kwargs["follow"]
		)
		sign_in_user = get_user_by_email(kwargs["email"])
		sign_in_user.follow(user)
		db.session.add(new_sign_in)
		db.session.commit()
		return new_sign_in
	return None


def save_profile_settings_svc(user_id, profile_picture=None, **kwargs):
	user = get_user_by_id(user_id)
	user.email = kwargs["email"]
	user.username = kwargs["username"]
	user.f_name = kwargs["f_name"]
	user.l_name = kwargs["l_name"]
	user.bio = kwargs["bio"]
	if profile_picture:
		image = profile_picture
		filename = secure_filename(image.filename)
		image.save(os.path.join('src/static/images/dummy/', filename))
		user.profile_picture = filename
	print(kwargs)
	db.session.commit()


def follow_svc(current_user, username):
	logged_user = get_user_by_id(current_user)
	follow_user = get_user_by_username(username)
	logged_user.follow(follow_user)
	return logged_user, follow_user


def unfollow_svc(current_user, username):
	logged_user = get_user_by_id(current_user)
	follow_user = get_user_by_username(username)
	logged_user.unfollow(follow_user)
	return logged_user, follow_user


def business_register_svc(user_id, **kwargs):
	business = Business()
	business.email = kwargs["email"]
	business.business_name = kwargs["business_name"]
	business.address = kwargs["address"]
	business.state = kwargs["state"]
	business.post_code = kwargs["post_code"]
	business.country = kwargs["country"]
	business.sign_in_enabled = True
	business.user = get_user_by_id(user_id)
