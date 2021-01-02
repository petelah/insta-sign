from flask_login import UserMixin
from src import db, login_manager
from src.models import Comments, Posts, Business
from src.models.Followers import followers


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    profile_picture = db.Column(db.String(), nullable=True, default='default_pic.jpg')
    bio = db.Column(db.String(400), nullable=True)
    f_name = db.Column(db.String(), nullable=False)
    l_name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    posts = db.relationship("Posts", backref="user", lazy=True)
    comments = db.relationship("Comments", backref="comment_id", lazy=True)
    business = db.relationship("Business", backref="user", uselist=False, lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followers_count(self):
        return self.followed.count()

    def following_count(self):
        return self.followers.count()

