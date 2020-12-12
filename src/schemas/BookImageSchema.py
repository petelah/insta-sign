from main import ma
from models.BookImage import BookImage
from marshmallow.validate import Length

class BookImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookImage
    
    filename = ma.String(required=True, validate=Length(min=1))

book_image_schema = BookImageSchema()