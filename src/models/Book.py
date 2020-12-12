from main import db
from models.BookImage import BookImage

class Book(db.Model):
    __tablename__ = "books"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_image = db.relationship("BookImage", backref="book", uselist=False)

    def __repr__(self):
        return f"<Book {self.title}>"