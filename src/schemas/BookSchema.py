from main import ma
from models.Book import Book
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

    title = ma.String(required=True, validate=Length(min=1))
    author = ma.String()
    user =  ma.Nested(UserSchema)
    
book_schema = BookSchema()
books_schema = BookSchema(many=True)