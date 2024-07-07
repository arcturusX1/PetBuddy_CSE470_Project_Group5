import logging
import os

#flask
from flask import Flask
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

#import blueprints
from blueprints.appointment import appointment_bp
from blueprints.appointment_showcase import appointment_showcase_bp
from blueprints.home import home_bp
from blueprints.login import login_bp
from blueprints.patient_profile import patient_profile_bp
from blueprints.prescription import prescription_bp
from blueprints.signup import signup_bp
from blueprints.users import user_bp
from blueprints.vet_routes import vet_bp

#import db
from model.database import db

# Initialize Flask app
app = Flask(__name__)

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['PG_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#secret key
app.secret_key = os.environ['SECRET_KEY']
#CSRF init
csrf = CSRFProtect(app)

# Initialize the database
db.init_app(app)
#initialize migration
migrate = Migrate(app, db)

# Register blueprints from blueprints folder
app.register_blueprint(home_bp)
app.register_blueprint(vet_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(patient_profile_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(appointment_showcase_bp)

# Set up logging
logging.basicConfig(level=logging.INFO)


#-------Emailing------
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '041ea147949443'
app.config['MAIL_PASSWORD'] = 'bb3bb09ede76ac'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/send')
def send():
  message = Message(
    subject = 'Your PetBuddy Appointment!',
    sender='md.yameem53@gmail.com',
    recipients=['yameemsecond@gmail.com'])


  message.body = 'Hello, this is a test email sent from a Flask application!'
  mail.send(message)

  return 'Email sent!'
#------End emailing-----


#driver
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
