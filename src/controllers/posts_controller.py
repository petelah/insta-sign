from src.schemas import comments_schema, comment_schema, users_schema, logged_in_user_schema, posts_schema, post_schema
from src.models import User, Posts, Comments
from src import db
from flask import Blueprint, request, jsonify, redirect, url_for, abort, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services import single_post_svc, edit_post_svc, delete_post_svc, new_post_svc, add_comment_svc
from pathlib import Path
import os

posts = Blueprint('posts', __name__, url_prefix="/api/posts")


@posts.route("/<int:id>", methods=["GET", "POST"])
def single_post(id):
	# Retrieve a post by id
	# Added POST method as flask won't redirect as GET from a post route
	post = single_post_svc(id)
	if post is None:
		return jsonify({"msg": "Post does not exist"}), 404
	return jsonify([post_schema.dump(post), comments_schema.dump(post.comments)]), 200


@posts.route("/<int:id>/edit", methods=["GET"])
@jwt_required
def edit_post(id):
	post = single_post_svc(id)
	if post is None:
		return jsonify({"msg": "Post does not exist"}), 404
	current_user = get_jwt_identity()
	if post.user_id == current_user:
		return jsonify(post_schema.dump(post)), 200
	return jsonify({"msg": "Authorization required"}), 401


@posts.route("/<int:id>/edit", methods=["PUT"])
@jwt_required
def send_edit_post(id):
	current_user = get_jwt_identity()
	post_fields = post_schema.load(request.json, partial=True)
	if not edit_post_svc(current_user, id, post_fields["content"]):
		return jsonify({"msg": "Post does not exist"}), 404
	return redirect(url_for('single_post', id=id)), 200


@posts.route("/<int:id>/delete_post", methods=["DELETE"])
@jwt_required
def delete_post(id):
	current_user = get_jwt_identity()
	if not delete_post_svc(current_user, id):
		return jsonify({"msg": "Post does not exist"}), 404
	return jsonify({"msg": "Post deleted"}), 200


@posts.route("/new_post", methods=["POST"])
@jwt_required
def new_post():
	current_user = get_jwt_identity()
	if current_user:
		post_fields = post_schema.load(dict(request.form), partial=True)
		image = request.files["image"]
		if Path(image.filename).suffix not in [".png", ".jpeg", ".jpg", ".gif"]:
			return abort(400, description="Invalid file type")
		ret_id = new_post_svc(current_user, post_fields["content"], image)
		return redirect(url_for('posts.single_post', id=ret_id), code=303)
	return jsonify({"msg": "Authorization required"}), 401


@posts.route("/<int:id>/comment", methods=["POST"])
@jwt_required
def add_comment(id):
	current_user = get_jwt_identity()
	if Posts.query.get(id):
		if current_user:
			content = comment_schema.load(request.json, partial=True)
			add_comment_svc(current_user, id, content["content"])
			return redirect(url_for('posts.single_post', id=id))
		return jsonify({"msg": "Authorization required"}), 401
	return jsonify({"msg": "Post does not exist"}), 404


@posts.route("/<int:id>/like", methods=["PUT"])
@jwt_required
def add_remove_like(id):
	pass
