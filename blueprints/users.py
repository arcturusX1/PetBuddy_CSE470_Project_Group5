from flask import Blueprint, flash, redirect, render_template, request, url_for

from blueprints.forms import UserForm
from model.database import User, db

user_bp = Blueprint('users', __name__)

@user_bp.route('/add_user_form', methods=['GET', 'POST'])
def add_user_form():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('users.add_user_form'))

    # Fetch all users from the database
    users = User.query.all()
    return render_template('user.html', form=form, users=users)
