from flask import Blueprint, render_template

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
appointment_showcase_bp = Blueprint('appointment_showcase', __name__) 


@appointment_showcase_bp.route('/appointment_showcase') #route assign
def list():
  return render_template("appointment_showcase.html")


