from run import db
from datetime import datetime
from src.models import Likes, Comments


class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(), nullable=False)
	content = db.Column(db.String(), nullable=False)
	timestamp = db.Column(db.DateTime(), default=datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	comments = db.relationship("Comments", backref="comment", lazy="lazy")
	likes = db.relationship("Likes", backref='post', lazy="lazy")

	def __repr__(self):
		return f"<Post {self.title}>"