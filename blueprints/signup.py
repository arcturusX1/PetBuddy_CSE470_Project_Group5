from flask import Blueprint, flash, render_template

from blueprints.forms import UserForm

signup_bp = Blueprint('signup_bp', __name__)

# @signup_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = UserForm() #using flask_wtforms form object from UserForm
#     print(form) 
#     if form.validate_on_submit():
#         username = form.username.data
#         email = form.email.data
#         account_type = form.account_type.data
#         flash('User successfully created!', 'success')
#     return render_template('signup.html', form=form)


#debug 
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()  # using flask_wtforms form object from UserForm
    print("Form object:", form)  # Debugging statement

    if form.validate_on_submit():
        print("Form validated")  # Debugging statement
        username = form.username.data
        email = form.email.data
        account_type = form.account_type.data
        # Save user to the database (if required)
        flash('User successfully created!', 'success')
    else:
        print("Form errors:", form.errors)  # Debugging statement

    return render_template('signup.html', form=form)