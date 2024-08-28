import datetime
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

    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    

def init_app(app):
    
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # Apply configurations
    app.config.from_object(Config)
    app.config['USE_SESSION_FOR_NEXT'] = True
    app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"
    # Initialize extensions 
    migrate = Migrate() #db migration
    csrf = CSRFProtect() #csrf protection
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "You need to be logged in"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app) #loging_manager inti
    db.init_app(app) #db init
    migrate.init_app(app, db) #db migrate init
    csrf.init_app(app) #csrf init
    mail.init_app(app) #mail init

    @app.template_filter('to_12_hour')
    def to_12_hour(time_str):
        try:
            time_obj = datetime.datetime.strptime(time_str, '%H:%M')
            return time_obj.strftime('%I:%M %p')
        except ValueError:
            return time_str

    #create db. is this required? 
    with app.app_context():
        db.create_all()

    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    return app

