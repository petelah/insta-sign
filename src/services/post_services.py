import os
from src.models import User, Posts, Comments
from src import db
from werkzeug.utils import secure_filename


def single_post_svc(id):
	"""
	Retrieves a single user post by id.
	:param id:
	:return:
	"""
	post = Posts.query.get(id)
	return post


def edit_post_svc(current_user, id, content):
	"""
	Updates post content.
	:param current_user:
	:param id:
	:param content:
	:return:
	"""
	post = single_post_svc(id)
	if post is None or post.user_id != current_user:
		return None
	post.content = content
	db.session.commit()
	return True


def delete_post_svc(current_user, id):
	"""
	Deletes a single post.
	:param current_user:
	:param id:
	:return:
	"""
	post = single_post_svc(id)
	if post is None or post.user_id != current_user:
		return None
	db.session.delete(post)
	db.session.commit()
	return True


def new_post_svc(current_user, content, image):
	"""
	Creates a new user post.
	:param current_user:
	:param content:
	:param image:
	:return:
	"""
	filename = secure_filename(image.filename)
	image.save(os.path.join('src/static/images/dummy/', filename))
	post = Posts()
	post.content = content
	post.filename = filename
	post.user_id = current_user
	db.session.add(post)
	db.session.commit()
	return post.id


def add_comment_svc(current_user, post_id, content):
	"""
	Add's a comment to an existing post
	:param current_user:
	:param post_id:
	:param content:
	:return:
	"""
	comment = Comments()
	comment.content = content
	comment.post_id = post_id
	comment.username = User.query.get(current_user).username
	db.session.add(comment)
	db.session.commit()