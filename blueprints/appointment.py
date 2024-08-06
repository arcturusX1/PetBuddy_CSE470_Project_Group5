from flask import Blueprint, render_template

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
appointment_bp = Blueprint('appointment', __name__) 


@appointment_bp.route('/appointment') #route assign
def list():
  return render_template("appointment.html")

