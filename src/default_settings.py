import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "duck"

    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DB_URI")

        if not value:
            raise ValueError("DB_URI is not set")

        return value

    @property
    def AWS_ACCESS_KEY_ID(self):
        value = os.environ.get("AWS_ACCESS_KEY_ID")

        if not value:
            raise ValueError("AWS_ACCESS_KEY_ID is not set")

        return value
    
    @property
    def AWS_SECRET_ACCESS_KEY(self):
        value = os.environ.get("AWS_SECRET_ACCESS_KEY")

        if not value:
            raise ValueError("AWS_SECRET_ACCESS_KEY is not set")

        return value
    
    @property
    def AWS_S3_BUCKET(self):
        value = os.environ.get("AWS_S3_BUCKET")

        if not value:
            raise ValueError("AWS_S3_BUCKET is not set")

        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        value = os.getenv("JWT_SECRET_KEY")

        if not value:
            raise ValueError("JWT_SECRET_KEY is not set")

        return value


class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()