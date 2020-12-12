from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.Book import Book
    from models.User import User
    from main import bcrypt
    from faker import Faker
    import random

    faker = Faker()
    users = []

    for i in range(5):
        user = User()
        user.email =  f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)
    
    db.session.commit()

    for i in range(20):
        book = Book()
        book.title = faker.catch_phrase()
        book.user_id = random.choice(users).id
        db.session.add(book)
    
    db.session.commit()
    print("Tables seeded")