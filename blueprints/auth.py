from flask import Blueprint, flash, redirect, render_template, url_for, abort, current_app, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from urllib.parse import urlparse, urljoin
from blueprints.forms import LoginForm, UserForm
from model.database import User, Vet, db

auth_bp = Blueprint('auth_bp', __name__)

# Initialize the login manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return (
#         test_url.scheme in ('http', 'https') and
#         ref_url.netloc == test_url.netloc
#     )

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# Route for the login page
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                flash('Login Successful!', 'success')
                return(redirect(next_page))
            else:
                flash('Login Successful!', 'success')
                return redirect(url_for('home_bp.index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/add_user_form', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.pass1.data
        phone = form.phone.data
        email = form.email.data

        # Check if the phone number or email already exists
        existing_user = User.query.filter((User.phone == phone) | (User.email == email)).first()
        if existing_user:
            flash('A user with this phone number or email already exists.', 'danger')
            return render_template('signup.html', form=form)

        is_user = form.account_type.data == 'user'
        is_vet = form.account_type.data == 'vet'

        # Create a new user
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password_hash=generate_password_hash(password),
            is_user=is_user,
            is_vet=is_vet
        )
        db.session.add(user)
        db.session.commit()

        # If the user is a vet, create a corresponding vet entry
        if is_vet:
            vet = Vet(
                user_id=user.id,  # Using the same ID as the User to link them together
                first_name=first_name,
                last_name=last_name,
                # Add other vet-specific fields here as needed
            )
            db.session.add(vet)
            db.session.commit()

        flash('User successfully created!', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))

def access_required(user_type):  # Custom decorator to check user type
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if user_type == 'user' and not current_user.is_user:
                abort(403)
            if user_type == 'vet' and not current_user.is_vet:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/profile')
@login_required
def profile():
    if current_user.is_vet:
        return redirect(url_for('vet_profile_bp.vet_profile'))
    elif current_user.is_user:
        return redirect(url_for('patient_profile_bp.patient_profile'))
    else:
        return "User type not recognized", 403