from src.models.User import User
from src import db, bcrypt
from src.services.helpers import get_user_by_email


def register_user_svc(**kwargs):
	"""
	Register new user service
	:param kwargs:
	:return: user query object
	"""
	user = get_user_by_email(kwargs["email"])

	if user:
		return None

	user = User()
	user.email = kwargs["email"]
	user.username = kwargs["username"]
	user.f_name = kwargs["f_name"]
	user.l_name = kwargs["l_name"]
	user.bio = kwargs["bio"]
	user.password = bcrypt.generate_password_hash(kwargs["password"]).decode("utf-8")
	db.session.add(user)
	db.session.commit()
	return user


def login_user_svc(**kwargs):
	"""
	User authentication service.
	Checks the given password against the stored hash.
	:param kwargs:
	:return: user query object
	"""
	user = get_user_by_email(kwargs["email"])
	if not user or not bcrypt.check_password_hash(user.password, kwargs["password"]):
		return None
	return user
