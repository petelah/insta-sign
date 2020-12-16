from run import db
from datetime import datetime
from src.models import User, Posts

# likes = db.Table('likes'
#                  db.Column('like_id', db.Integer, db.ForeignKey('like.id'), primary_key=True),
#                  db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
# )


class Likes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
