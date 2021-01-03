from src import db
from src.default_settings import Config
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)

TEST_PASSWORD = Config.TEST_PASSWORD


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("DB Created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from src.models.User import User
    from src.models.Posts import Posts
    from src.models.Business import Business
    from src.models.Comments import Comments
    from src.models.SignIn import SignIn
    from src import bcrypt
    from faker import Faker
    import random

    faker = Faker()
    users = []
    businesses = []
    posts = []

    if not TEST_PASSWORD:
        raise ValueError('TEST_PASSWORD not provided.')

    for i in range(5):

        # Add users
        user = User()
        user.email = f"test{i}@test.com"
        user.bio = faker.paragraph(nb_sentences=3)
        user.username = f"test{i}"
        user.f_name = faker.first_name()
        user.l_name = faker.last_name()
        user.password = bcrypt.generate_password_hash(f"{TEST_PASSWORD}").decode("utf-8")

        # Add businesses
        business = Business()
        business.email = user.email
        business.business_name = faker.bs()
        business.address = f"{i} test St"
        business.state = "NSW"
        business.post_code = f"123{i}"
        business.country = "Australia"
        business.sign_in_enabled = True
        business.verified = True
        business.user = user

        db.session.add(user)
        users.append(user)
        businesses.append(business)
        db.session.add(business)
    
    db.session.commit()
    print("Users Added")

    for i in range(20):
        post = Posts()
        post.filename = f"{random.randrange(1,15)}.jpg"
        post.content = faker.paragraph(nb_sentences=3)
        post.user_id = random.choice(users).id
        posts.append(post)
        db.session.add(post)
    
    db.session.commit()
    print("Posts added")

    for i in range(100):
        comment = Comments()
        comment.content = faker.paragraph(nb_sentences=2)
        comment.username = random.choice(users).username
        comment.post_id = random.choice(posts).id

        db.session.add(comment)

    db.session.commit()
    print("Posts added")

    for i in range(350):
        sign_in = SignIn()
        sign_in.email = f"test{i}@test.com"
        sign_in.name = f"test_name{i}"
        sign_in.symptoms = True
        sign_in.follow = True
        sign_in.signup = True
        sign_in.business_id = random.choice(businesses).id
        db.session.add(sign_in)

    db.session.commit()

    print("Sign in's added")
    print("Tables seeded")
