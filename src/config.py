"""
Configuration classes for app
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base Config class
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development Config class
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' +
                                        os.path.join(basedir, 'flask_finances_api_development.db'))
    JWT_SECRET_TOKEN=os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Testing Config class
    """
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TST', 'sqlite:///' +
                                        os.path.join(basedir, 'flask_finances_api_testing.db'))
    JWT_SECRET_TOKEN=os.environ.get('JWT_SECRET_KEY')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production Config class
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '').replace("postgres://",
                                                                    "postgresql://", 1)


config_by_name = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig
}

key = Config.SECRET_KEY
