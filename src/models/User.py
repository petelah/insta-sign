from src.run import db
from src.models import Comments, Posts, Business


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    f_name = db.Column(db.String(), nullable=False)
    l_name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    post_code = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    following = db.Column()
    posts = db.relationship("Posts", backref="user", lazy="lazy")
    comments = db.relationship("Comments", backref="user", lazy="lazy")
    business = db.relationship("Business", backref="user", uselist=False, lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
