from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model.database import db, Pet
from blueprints.forms import AddPetForm

patient_profile_bp = Blueprint('patient_profile', __name__)

@patient_profile_bp.route('/profile')
@login_required
def patient_profile():
    # Redirect vets to their profile page
    if current_user.is_vet:
        return redirect(url_for('vet_profile_bp.vet_profile'))

    form = AddPetForm()
    return render_template("patient_profile.html", user=current_user, form=form)

@patient_profile_bp.route('/patient/add_pet', methods=['POST'])
@login_required
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        pet_name = form.pet_name.data
        animal_type = form.animal_type.data
        breed = form.breed.data
        age = form.age.data

        new_pet = Pet(name=pet_name, animal_type=animal_type, breed=breed, age=age, user_id=current_user.id)
        db.session.add(new_pet)
        db.session.commit()

        flash(f'Added {pet_name} ({animal_type}) successfully!', 'success')
    else:
        flash('Failed to add pet. Please check the form and try again.', 'danger')

    return redirect(url_for('patient_profile.patient_profile'))
