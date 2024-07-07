from flask import Blueprint, render_template

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
prescription_bp = Blueprint('prescription', __name__) 


@prescription_bp.route('/prescription') #route assign
def list():
  return render_template("prescriptions.html")


