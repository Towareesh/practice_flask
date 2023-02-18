import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #### set config Flask-Mail ####
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True
    SECRET_KEY    = 'is_admin'
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465

    ADMINS = os.environ.get('ADMINS')

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    POSTS_PER_PAGE = 3


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