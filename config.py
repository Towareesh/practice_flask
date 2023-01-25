import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY                     = os.environ.get('SECRET_KEY') or 'is_admin'

    #### set config Flask-Mail ####
    # MAIL_USE_TLS  = True
    MAIL_SERVER   = 'localhost'
    MAIL_PORT     = 5050 or 8080

    #### define your data ####
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'app.db')


class TestingConfig(DevelopmentConfig):
    """
    Inheritance Map.

    Root-inheritance:
        BaseConfig (None): configuration constants
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'app.db')


class ProductionConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'app.db')