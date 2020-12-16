from run import db
from datetime import datetime


class Followers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.now)
	target_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
