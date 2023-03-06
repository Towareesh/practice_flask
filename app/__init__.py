import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import BaseConfig

# from app.main import main_bp
# from app.auth import auth_bp
# from app.errors import errors_bp


# declaration of global variables
db        = SQLAlchemy()
migrate   = Migrate()
login     = LoginManager()
mail      = Mail()
bootstrap = Bootstrap()
moment    = Moment()
babel     = Babel()

login.login_view    = 'auth.login'
login.login_message = _l('Please login to access this page.')

def get_locale():
    return request.accept_languages.best_match('ru', 'en')

def create_app(config_class=BaseConfig, *blueprints):

    # creating an application instance
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # registers blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


from app import models