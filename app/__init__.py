import os, config

from flask import Flask


# creating an application instance
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')

from app import views