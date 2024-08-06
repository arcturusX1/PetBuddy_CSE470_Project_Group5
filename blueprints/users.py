from flask import Blueprint, flash, redirect, render_template, url_for

from .forms import UserForm
from model.database import User, db

user_bp = Blueprint('users', __name__)

@user_bp.route('/add_user_form', methods=['GET', 'POST'])
def add_user_form():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        
        if form.account_type.data =='patient':
            is_user = True
            is_vet = False
        else:
            is_user = False
            is_vet = True
            
        
        flash('User added successfully!', 'success')
        return redirect(url_for('users.add_user_form'))
   
    return render_template('user.html', form=form)
