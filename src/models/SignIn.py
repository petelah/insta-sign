from datetime import datetime
from src import db
from src.models import Comments, Posts, Business, User


class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=False)
    name = db.Column(db.String(), nullable=False)
    signup = db.Column(db.Boolean, nullable=True, default=True)
    follow = db.Column(db.Boolean, nullable=True, default=True)
    symptoms = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))

    def __repr__(self):
        return f"<Sign In {self.name}>"