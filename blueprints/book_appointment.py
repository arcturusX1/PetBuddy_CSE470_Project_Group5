import json
import logging
from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from model.database import Appointment, Vet, VetAvailability, db, Pet
from .forms import AppointmentForm

book_appointment_bp = Blueprint('book_appointment_bp', __name__)

def is_time_in_slot(time, slots):
    """Check if the given time is within any of the provided slots."""
    try:
        return any(start <= time <= end for start, end in slots)
    except Exception:
        return False

# Main booking route, now with optional pet_id
@book_appointment_bp.route('/book_appointment', defaults={'pet_id': None}, methods=['GET', 'POST'])
@book_appointment_bp.route('/book_appointment/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(pet_id):
    # Redirect if no pet is provided
    if pet_id is None:
        return redirect(url_for('patient_profile.pet_list'))

    # Retrieve the pet using pet_id to ensure the pet belongs to the current user
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        data = request.json
        selected_date = data.get('date')
        selected_time = data.get('time')
        action = data.get('action')

        if not selected_date or not selected_time:
            return jsonify({'error': 'Date and time are required'}), 400

        selected_day = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%A').lower()

        if action == 'filter':
            vets = Vet.query.all()
            available_vets = []
            for vet in vets:
                if vet.availability is None:
                    continue

                availability = vet.availability.get(selected_day, [])
                if is_time_in_slot(selected_time, availability):
                    available_vets.append({
                        'id': vet.id,
                        'first_name': vet.first_name,
                        'last_name': vet.last_name,
                        'speciality': vet.speciality,
                        'workplace': vet.workplace,
                        'experience': vet.experience,
                        'fees': vet.fees,
                        'availability': vet.availability,
                        'rating': vet.rating,
                        'contact_info': vet.contact_info
                    })

            return jsonify({'vets': available_vets})

    # Render the booking template and pass the pet object
    return render_template('book_appointment.html', pet=pet, vets=[])

# Route to create the appointment
@book_appointment_bp.route('/create_appointment/<int:vet_id>/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def create_appointment(vet_id, pet_id):
    vet = Vet.query.filter_by(id=vet_id).first()
    day = get_days(vet_id)
    pet = Pet.query.filter_by(id=pet_id, user_id=current_user.id).first_or_404()

    form = AppointmentForm(obj=vet)
    form.vet_name.data = f'{vet.first_name} {vet.last_name}'
    form.vet_id.data = vet_id

    if form.validate_on_submit():
        try:
            start_time, end_time = make_datetime(form.time.data)
            appointment = Appointment(
                start_time=datetime.combine(form.date.data, start_time),
                end_time=datetime.combine(form.date.data, end_time),
                vet_id=vet_id,
                user_id=current_user.id,
                pet_id=pet.id  # Associate the appointment with the pet
            )
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('meet_event_bp.confirm_event', appt_id=appointment.id))
        except Exception as e:
            logging.error(f'Error creating appointment: {e}')

    return render_template('appointment_form.html', form=form, day=day, vet_id=vet_id, pet=pet)

# Utility function to get available days for a vet
def get_days(vet_id):
    days = VetAvailability.query.with_entities(
        VetAvailability.day
    ).filter_by(vet_id=vet_id).all()
    return [day[0] for day in days]

# Utility function to create datetime objects
def make_datetime(string):
    start_time, end_time = string.split(' - ')
    start_time = datetime.strptime(start_time, "%I:%M:%S %p").time()
    end_time = datetime.strptime(end_time, "%I:%M:%S %p").time()
    return start_time, end_time

@book_appointment_bp.route('/get_time_slots', methods=['GET'])
def get_time_slots():
    date = request.args.get('date')
    day_name = request.args.get('dayName')
    vet_id = request.args.get('vetId')

    # Query the database for time slots on the given date and day index
    try:
        time_slots = VetAvailability.query.with_entities(
            VetAvailability.time_start,
            VetAvailability.time_end
        ).filter_by(vet_id=vet_id, day=day_name)

        time_slot_strings = [f"{slot.time_start.strftime('%H:%M')} - {slot.time_end.strftime('%H:%M')}" for slot in time_slots]
        print(time_slot_strings)

        return jsonify({'time_slots': time_slot_strings})

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
