from flask import Blueprint, request, jsonify, abort, current_app, Response
from flask_jwt_extended import jwt_required
from services.auth_service import verify_user
from models.BookImage import BookImage
from models.Book import Book
from schemas.BookImageSchema import book_image_schema
import boto3
from main import db
from pathlib import Path

book_images = Blueprint("book_images",  __name__, url_prefix="/books/<int:book_id>/image")

@book_images.route("/", methods=["POST"])
@jwt_required
@verify_user
def book_image_create(user, book_id):
    book = Book.query.filter_by(id=book_id, user_id=user.id).first()

    if not book:
        return abort(401, description="Invalid book")
    
    if "image" not in request.files:
        return  abort(400, description="No Image")
    
    image = request.files["image"]

    if Path(image.filename).suffix not in [".png", ".jpeg", ".jpg", ".gif"]:
        return abort(400, description="Invalid file type")

    filename = f"{book_id}{Path(image.filename).suffix}"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"book_images/{filename}"

    bucket.upload_fileobj(image, key)

    if not book.book_image:
        new_image = BookImage()
        new_image.filename = filename
        book.book_image = new_image
        db.session.commit()
    
    return ("", 201)

@book_images.route("/<int:id>", methods=["GET"])
def book_image_show(book_id, id):
    book_image = BookImage.query.filter_by(id=id).first()

    if not book_image:
        return abort(401, description="Invalid book")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = book_image.filename
    file_obj = bucket.Object(f"book_images/{filename}").get()

    print(file_obj)

    return Response(
        file_obj["Body"].read(),
        mimetype="image/*",
        headers={"Content-Disposition": "attachment;filename=image"}
    )

@book_images.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def book_image_delete(user, book_id, id):
    book = Book.query.filter_by(id=book_id, user_id=user.id).first()

    if not book:
        return abort(401, description="Invalid book")
    
    if book.book_image:
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        filename = book.book_image.filename

        bucket.Object(f"book_images/{filename}").delete()

        db.session.delete(book.book_image)
        db.session.commit()

    return ("", 204)