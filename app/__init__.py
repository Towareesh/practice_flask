import os, config

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l


# creating an application instance
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')
db        = SQLAlchemy(app)
migrate   = Migrate(app, db)
login     = LoginManager(app)
mail      = Mail(app)
bootstrap = Bootstrap(app)
moment    = Moment(app)
babel     = Babel(app)

login.login_view    = 'login'
login.login_message = _l('Please login to access this page.')

# babel selector langs
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'en'

babel.init_app(app, locale_selector=get_locale)

from app import views, models, errors