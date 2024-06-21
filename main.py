import logging
import os

#flask
from flask import Flask
from flask_wtf.csrf import CSRFProtect

#import blueprints
from blueprints.home import home_bp
from blueprints.users import user_bp
from blueprints.vet_routes import vet_bp

#import db
from model.database import db

# Initialize Flask app
app = Flask(__name__)

# Set up database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../model/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#secret key
app.secret_key = os.environ['SECRET_KEY']
#CSRF init
csrf = CSRFProtect(app)

# Initialize the database
db.init_app(app)

# Register blueprints from blueprints folder
app.register_blueprint(home_bp)
app.register_blueprint(vet_bp)
app.register_blueprint(user_bp)

# Set up logging
logging.basicConfig(level=logging.INFO)

#driver
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
