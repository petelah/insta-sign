from flask import Blueprint, abort, jsonify, request
from src.schemas.UserSchema import user_schema
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from src.services.auth_services import register_user_svc, login_user_svc
from datetime import timedelta

auth = Blueprint("auth",  __name__,  url_prefix="/api/auth")


@auth.route("/register", methods=["POST"])
@jwt_optional
def auth_register():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"msg": "Already logged in"}), 200
    user_fields = user_schema.load(request.json)

    user = register_user_svc(
        f_name=user_fields["f_name"],
        l_name=user_fields["l_name"],
        email=user_fields["email"],
        bio=user_fields["bio"],
        username=user_fields["username"],
        password=user_fields["password"]
    )
    if user is None:
        return abort(400, description="Email already registered")

    return jsonify(user_schema.dump(user))


@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json, partial=True)
    user = login_user_svc(
        email=user_fields["email"],
        password=user_fields["password"]
    )
    if not user:
        return abort(401, description="Incorrect username and password")
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=user.id, expires_delta=expiry)
    
    return jsonify({ "token": access_token })

