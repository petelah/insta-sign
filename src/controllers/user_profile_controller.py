from src.schemas.UserSchema import user_schema, logged_in_user_schema
from src.schemas.PostSchema import posts_schema
from src.schemas.SignInSchema import SignIn_schema
from src.models.User import User
from src.models.Posts import Posts
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services import get_profile_svc, sign_in_svc, save_profile_settings_svc, follow_svc, get_user_by_username

user_profile = Blueprint('user_profile', __name__, url_prefix="/api/profile")


@user_profile.route("/<string:username>", methods=["GET"])
def profile_page(username):
	# Retrieve user profile
	user, posts = get_profile_svc(username)
	return jsonify([user_schema.dump(user), posts_schema.dump(posts), {"followers": user.followers_count()}])


@user_profile.route("/<string:username>/posts", methods=["GET"])
def profile_posts(username):
	# Get users posts - probably redundant
	user = User.query.filter_by(username=username).first_or_404()
	posts = Posts.query.filter_by(user_id=user.id).all()
	return jsonify(posts_schema.dump(posts))


@user_profile.route("/<string:username>/sign_in", methods=["POST"])
def profile_sign_in(username):
	# Outside user signs into venue
	sign_in_fields = SignIn_schema.load(request.json)
	new_sign_in = sign_in_svc(
		username,
		name=sign_in_fields["name"],
		email=sign_in_fields["email"],
		signup=sign_in_fields["signup"],
		symptoms=sign_in_fields["symptoms"],
		follow=sign_in_fields["follow"]
	)
	if new_sign_in is not None:
		return jsonify(SignIn_schema.dump(new_sign_in)), 200
	return 400


@user_profile.route("/<string:username>/settings", methods=["GET"])
@jwt_required
def get_profile_settings(username):
	# Get user profile settings
	current_user = get_jwt_identity()
	user = User.query.get(current_user)
	return jsonify(logged_in_user_schema.dump(user)), 200


@user_profile.route("/<string:username>/settings", methods=["PUT"])
@jwt_required
def set_profile_settings(username):
	# Set user settings
	current_user = get_jwt_identity()
	user = get_user_by_username(username)
	if user.id == current_user:
		user_fields = logged_in_user_schema.load(request.json, partial=True)
		if save_profile_settings_svc(
			user,
			email=user_fields["email"],
			f_name=user_fields["f_name"],
			l_name=user_fields["l_name"],
			address=user_fields["address"],
			state=user_fields["state"],
			post_code=user_fields["post_code"],
			country=user_fields["country"]


		) is not None:
			return redirect(url_for('user_profile.get_profile_settings', username=user.username)), 200
	return jsonify({"msg": "Not authorized"}), 401


@user_profile.route("/<string:username>/follow", methods=["PATCH"])
@jwt_required
def follow(username):
	# follow a user
	current_user = get_jwt_identity()
	logged_user, follow_user = follow_svc(current_user)
	return jsonify(following=logged_user.is_following(follow_user)), 200


@user_profile.route("/<string:username>/unfollow", methods=["PATCH"])
@jwt_required
def unfollow(username):
	# unfollow a user
	current_user = get_jwt_identity()
	logged_user, follow_user = follow_svc(current_user)
	return jsonify(following=logged_user.is_following(follow_user)), 200
