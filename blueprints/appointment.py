from flask import Blueprint, render_template
from flask_login.utils import login_required

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
appointment_bp = Blueprint('appointment', __name__) 


@appointment_bp.route('/appointment_form') #route assign
def list():
  return render_template("appointment_form.html")

