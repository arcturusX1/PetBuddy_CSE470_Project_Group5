import os

from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

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

# Initialize extensions
migrate = Migrate()
csrf = CSRFProtect()

def init_app(app):
    # Apply configurations
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)

    return app