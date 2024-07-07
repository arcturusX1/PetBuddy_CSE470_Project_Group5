from flask import Blueprint
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '041ea147949443'
app.config['MAIL_PASSWORD'] = 'bb3bb09ede76ac'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

mail_bp = Blueprint('mail_bp', __name__) 

@mail_bp.route('/send')
def send():
  message = Message(
    subject = 'Your PetBuddy Appointment!',
    sender='md.yameem53@gmail.com',
    recipients=['yameemsecond@gmail.com.com'])


  message.body = 'Hello, this is a test email sent from a Flask application!'
  mail.send(message)
  
  return 'Email sent!'
