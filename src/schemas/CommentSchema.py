from src import ma
from src.models.Comments import Comments
from marshmallow.validate import Length


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments

    username = ma.String()
    post_id = ma.Integer()
    content = ma.String(required=True, validate=[Length(min=2, max=600)])


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
