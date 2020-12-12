from controllers.books_controller import books
from controllers.auth_controller  import auth
from controllers.book_images_controller import book_images

registerable_controllers = [
    auth,
    books,
    book_images
]