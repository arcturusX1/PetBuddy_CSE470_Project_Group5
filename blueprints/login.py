from flask import Blueprint, flash, render_template

from blueprints.forms import LoginForm

login_bp = Blueprint('login_bp', __name__)

# Route for the login page

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit:
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
    flash('Login Sucess!', 'success')
    return render_template('login.html', form = form)
    