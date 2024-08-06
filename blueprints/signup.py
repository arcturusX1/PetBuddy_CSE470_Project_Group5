from flask import Blueprint, flash, render_template

from blueprints.forms import UserForm
from model.database import User, db

signup_bp = Blueprint('signup_bp', __name__)

#debug 
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()  # using flask_wtforms form object from UserForm
    print("Form object:", form)  # Debugging statement

    if form.validate_on_submit():
        print("Form validated")  # Debugging statement
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data
        if form.account_type.data == 'user':
            is_user = True
            is_vet = False
        elif form.account_type.data == 'vet':
            is_user = False
            is_vet = True
            
        db.session.add(User(username=username, 
                            first_name=first_name, 
                            last_name=last_name,
                            phone =phone,
                            email=email,
                            is_user=is_user,
                            is_vet=is_vet
                           ))
        db.session.commit()
        
        # Save user to the database (if required)
        flash('User successfully created!', 'success')
    else:
        print("Form errors:", form.errors)  # Debugging statement

    return render_template('signup.html', form=form)