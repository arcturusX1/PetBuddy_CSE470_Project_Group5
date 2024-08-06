import os

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from blueprints.auth import login_manager
from blueprints.mail import mail
from model.database import db


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['PG_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

def init_app(app):
    # Apply configurations
    app.config.from_object(Config)

    # Initialize extensions 
    migrate = Migrate() #db migration
    csrf = CSRFProtect() #csrf protection
    login_manager.login_view = 'blueprints.auth.login'
    login_manager.init_app(app) #loging_manager inti
    db.init_app(app) #db init
    migrate.init_app(app, db) #db migrate init
    csrf.init_app(app) #csrf init
    mail.init_app(app) #mail init

    #create db. is this required? 
    with app.app_context():
        db.create_all()

    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    return app