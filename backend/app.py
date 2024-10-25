from flask import Flask, redirect, url_for
from flask_login import current_user, login_required
from flask_cors import CORS

from config import init_app
from register_bp import register_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize configurations, extensions, and create database tables
init_app(app)

# Register blueprints
register_bp(app)

# Driver code
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
