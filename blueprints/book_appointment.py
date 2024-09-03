from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, jsonify
from flask_login import current_user

from model.database import Appointment, VetAvailability, Vet, db

from .forms import AppointmentForm

import logging
import json

book_appointment_bp = Blueprint('book_appointment_bp', __name__)

def is_time_in_slot(time, slots):
    """Check if the given time is within any of the provided slots."""
    try:
        return any(start <= time <= end for start, end in slots)
    except Exception:
        return False

@book_appointment_bp.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        data = request.json
        selected_date = data.get('date')
        selected_time = data.get('time')
        action = data.get('action') #differentiate between filter and booking 

        if not selected_date or not selected_time:
            return jsonify({'error': 'Date and time are required'}), 400

        selected_day = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%A').lower()
        
        
        
        if action == 'filter':
            vets = Vet.query.all()
            available_vets = []
            for vet in vets:
                
                # there's a null value in one of the vet.avaliabilty rows.
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

    # For GET requests, render the HTML template
    return render_template('book_appointment.html', vets=[])

@book_appointment_bp.route('/create_appointment<int:vet_id>', methods=['GET', 'POST'])
def create_appointment(vet_id): #need to hide this ^ vet_id in the url
    vet = Vet.query.filter_by(id=vet_id).first()
    days = get_days(vet_id)
    time = get_time_slots(vet_id)
    form = AppointmentForm(obj=vet) #sends default data to the formx
    form.vet_name.data = f'{vet.first_name} {vet.last_name}'#fetching first_name, last_name and concatting them. 

    
    if form.validate_on_submit():
        
        vet_id = vet_id
        user_id = current_user.id
        date_time = datetime.combine(form.date.data, form.time.data)
        appointment = Appointment(
            date_time=date_time,
            vet_id=vet_id,
            user_id=current_user.id
        )
        db.session.add(appointment)
        db.session.commit()
        print(f'Appointment for user {current_user.id} at  for {vet.id}')
    
    return render_template('appointment_form.html', form=form, days=days)

def get_days(vet_id):
    days = VetAvailability.query.with_entities(
        VetAvailability.day
    ).filter_by(vet_id=vet_id).all()
    days = [day[0] for day in days]
    return days

@book_appointment_bp.route('/get_time_slots', methods=[])
def get_time_slots():
    date = request.args.get('date')
    day_index = request.args.get('day_index')
    vet_id = request.args.get('vet_id')
    if not date or day_index is None:
        return jsonify({'error': 'Date and day_index parameters are required'}), 400
    
    day_index = int(day_index)
    
    # Query the database for time slots on the given date and day index
    time_slots =VetAvailability.query.with_entities(
        VetAvailability.time_start,
        VetAvailability.time_end
    ).filter_by(vet_id=vet_id).all()
    
    # Convert the time slots to a list of formatted strings
    time_slot_strings = [f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}" for slot in time_slots]
    
    return jsonify({'time_slots': time_slot_strings})