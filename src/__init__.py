from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_view.login'
login_manager.login_message_category = 'info'


def create_app():
	app = Flask(__name__)
	app.config.from_object("src.default_settings.app_config")

	db.init_app(app)
	ma.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)
	login_manager.init_app(app)
	migrate.init_app(app, db)

	from src.commands import db_commands
	app.register_blueprint(db_commands)

	from src.controllers import registerable_controllers

	for controller in registerable_controllers:
		app.register_blueprint(controller)

	from src.views import registerable_views

	for view in registerable_views:
		app.register_blueprint(view)

	@app.errorhandler(ValidationError)
	def handle_bad_request(error):
		return (jsonify(error.messages), 400)

	return app