from flask import Blueprint, render_template
from flask.helpers import redirect, url_for

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
home_bp = Blueprint('home_bp', __name__) 


@home_bp.route('/')
def index():
    return render_template('index.html')

@home_bp.route('/about')
def about():
    return render_template('about.html')

@home_bp.route('/contact')
def contact():
    return render_template('contact.html')

@home_bp.route('/service')
def service():
    return render_template('service.html')

@home_bp.route('/login')
def login():
    return render_template('login.html')

# @home_bp.route('/signup')
# def signup():
#     return redirect(url_for('signup_bp.signup'))


