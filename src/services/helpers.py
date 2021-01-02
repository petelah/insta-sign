from src.models import User, Posts, Comments, Business, SignIn


def get_user_by_username(username):
	user = User.query.filter_by(username=username).first()
	return user


def get_user_by_id(id):
	user = User.query.get(id)
	return user


def get_user_by_email(email):
	user = User.query.filter_by(email=email).first()
	return user


def save_image():
	pass