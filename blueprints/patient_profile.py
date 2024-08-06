from flask import Blueprint, render_template

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
patient_profile_bp = Blueprint('patient_profile', __name__) 


@patient_profile_bp.route('/patient') #route assign
def patient_profile():
  return render_template("patient_profile.html")


