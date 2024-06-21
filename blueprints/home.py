from flask import Blueprint, render_template

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
home_bp = Blueprint('home', __name__) 


@home_bp.route('/') #route assign
def home():
  return render_template("base.html")
  