from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from blueprints.forms import LoginForm, UserForm
from model.database import User, db

auth_bp = Blueprint('auth_bp', __name__)

#init login manager here even though ugly
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for the login page
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user, remember=True)
                print(f'login:{user.id}, {user,email}')
                flash('Login Sucess!', 'success')
                return redirect(url_for('home_bp.index'))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('User does not exist', 'danger')
        
    return render_template('login.html', form = form)

@auth_bp.route('/add_user_form', methods=['GET', 'POST'])
def signup():
    form = UserForm()  # using flask_wtforms form object from UserForm
    print("Form object:", form)  # Debugging statement

    if form.validate_on_submit():
        print("Form validated")  # Debugging statement
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.pass1.data
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
                            password_hash=generate_password_hash(password),
                            is_user=is_user,
                            is_vet=is_vet
                           ))
        db.session.commit()

        # Save user to the database (if required)
        flash('User successfully created!', 'success')
    else:
        print("Form errors:", form.errors)  # Debugging statement

    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))