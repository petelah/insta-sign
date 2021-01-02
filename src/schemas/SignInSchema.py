from src import ma
from src.models.SignIn import SignIn
from marshmallow.validate import Length, Email


class SignInSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SignIn
    
    email = ma.String(required=True, validate=[Length(min=4), Email()])
    name = ma.String(required=True, validate=[Length(min=2)])
    #symptoms = ma.Boolean(required=True)


SignIn_schema = SignInSchema()
SignIns_schema = SignInSchema(many=True)
