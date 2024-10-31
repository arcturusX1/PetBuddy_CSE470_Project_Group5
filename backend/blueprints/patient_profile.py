from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from model.database import db, Pet
from blueprints.forms import AddPetForm

# Define the blueprint
patient_profile_bp = Blueprint('patient_profile', __name__)

@patient_profile_bp.route('/patient_profile')
@login_required
def patient_profile():
    # Redirect vets to their profile page
    if current_user.is_vet:
        return redirect(url_for('vet_profile_bp.vet_profile'))

    form = AddPetForm()
    return render_template("patient_profile.html", user=current_user, form=form)

# Updated: Allow both GET and POST methods for the add_pet route
@patient_profile_bp.route('/patient/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    form = AddPetForm()

    # Handle POST request (form submission)
    if request.method == 'POST' and form.validate_on_submit():
        pet_name = form.pet_name.data
        animal_type = form.animal_type.data
        breed = form.breed.data
        age = form.age.data

        new_pet = Pet(name=pet_name, animal_type=animal_type, breed=breed, age=age, user_id=current_user.id)
        db.session.add(new_pet)
        db.session.commit()

        flash(f'Added {pet_name} ({animal_type}) successfully!', 'success')
        return redirect(url_for('patient_profile.pet_list'))

    # Handle GET request (render the form)
    return render_template('add_pet.html', form=form)

# Route to display the list of pets
@patient_profile_bp.route('/pet_list')
@login_required
def pet_list():
    # Fetch the current user's pets and pass them to the template
    return render_template("pet_list.html", pets=current_user.pets)

# Route to display an individual pet's profile
@patient_profile_bp.route('/pet_profile/<int:pet_id>')
@login_required
def pet_profile(pet_id):
    # Fetch the pet by ID and ensure it belongs to the current user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user.id).first_or_404()

    # Render the pet profile page
    return render_template('pet_profile.html', pet=pet)