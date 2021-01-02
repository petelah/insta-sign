from src import db
from src.models import Comments, Posts, User


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    business_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    post_code = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    sign_in_enabled = db.Column(db.Boolean, nullable=False, default=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sign_ins = db.relationship('SignIn', backref='sign_in_id')

    def __repr__(self):
        return f"<User {self.business_name}>"
