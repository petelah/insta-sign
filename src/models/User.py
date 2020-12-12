from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"