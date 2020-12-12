from models.Book import Book
from models.User import User
from main import db
from schemas.BookSchema import book_schema, books_schema
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import verify_user
from sqlalchemy.orm import joinedload

books = Blueprint('books', __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def book_index():
    #Retrieve all books
    books = Book.query.options(joinedload("user")).all()
    return jsonify(books_schema.dump(books))

@books.route("/", methods=["POST"])
@jwt_required
@verify_user
def book_create(user):
    #Create a new book
    book_fields = book_schema.load(request.json)

    new_book = Book()
    new_book.title = book_fields["title"]

    user.books.append(new_book)

    db.session.commit()
    
    return jsonify(book_schema.dump(new_book))

@books.route("/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    book = Book.query.get(id)
    return jsonify(book_schema.dump(book))

@books.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def book_update(user, id):
    #Update a book
    book_fields = book_schema.load(request.json)

    books = Book.query.filter_by(id=id, user_id=user.id)

    if books.count() != 1:
        return abort(401,  description="Unauthorized to update this book")    
    
    books.update(book_fields)
    db.session.commit()

    return jsonify(book_schema.dump(books[0]))

@books.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def book_delete(user, id):
    #Delete a book
    book = Book.query.filter_by(id=id, user_id=user.id).first()

    if not book:
        return abort(400)
    
    db.session.delete(book)
    db.session.commit()

    return jsonify(book_schema.dump(book))