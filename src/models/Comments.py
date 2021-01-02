from src import db
from datetime import datetime
from src.models import User, Posts


class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.now)
	content = db.Column(db.String, nullable=False)
	username = db.Column(db.String, db.ForeignKey("user.username"), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
