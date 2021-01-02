from src import ma
from src.models import Posts
from marshmallow.validate import Length


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Posts

    filename = ma.String(required=True, validate=[Length(min=5)])
    content = ma.String(required=True, validate=[Length(min=2, max=600)])


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
