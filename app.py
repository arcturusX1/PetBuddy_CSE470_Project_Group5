from flask import Flask, redirect, url_for
from flask_login import login_required, current_user
from config import init_app
from register_bp import register_bp

# Initialize Flask app
app = Flask(__name__)

# Initialize configurations, extensions, and create database tables
init_app(app)

# Register blueprints
register_bp(app)

@app.route('/profile')
@login_required
def profile():
    if current_user.is_vet:
        return redirect(url_for('vet_profile_bp.vet_profile'))
    elif current_user.is_user:
        return redirect(url_for('patient_profile_bp.patient_profile'))
    else:
        return "User type not recognized", 403

# Driver code
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
