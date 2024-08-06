from flask import Blueprint
from flask_mail import Mail, Message

mail = Mail()

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
