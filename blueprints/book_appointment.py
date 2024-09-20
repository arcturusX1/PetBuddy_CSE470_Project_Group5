import json
import logging
from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from model.database import Appointment, Vet, VetAvailability, db

from .forms import AppointmentForm

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

@book_appointment_bp.route('/create_appointment/<int:vet_id>', methods=['GET', 'POST'])
@login_required
def create_appointment(vet_id): #need to hide this ^ vet_id in the url
    vet = Vet.query.filter_by(id=vet_id).first()
    day = get_days(vet_id)
    form = AppointmentForm(obj=vet) #sends default data to the formx
    form.vet_name.data = f'{vet.first_name} {vet.last_name}'#fetching first_name, last_name and concatting them. 
    form.vet_id.data = vet_id
    

    if form.validate_on_submit():
        try:
            user_id = current_user.id
            start_time, end_time = make_datetime(form.time.data)
            appointment = Appointment(
                start_time = datetime.combine(form.date.data, start_time),
                end_time = datetime.combine(form.date.data, end_time),
                vet_id=vet_id,
                user_id=current_user.id
            )
            db.session.add(appointment)
            db.session.commit()
            print(f'Appointment {appointment.id} for user {current_user.id} for vet {vet.id}')
            return redirect(url_for('meet_event_bp.confirm_event', appt_id = appointment.id))
        except Exception as e:
            print(f'{e}')
    else:
        print(form.errors)
    
    return render_template('appointment_form.html', form=form, day=day, vet_id=vet_id)

def get_days(vet_id):
    days = VetAvailability.query.with_entities(
        VetAvailability.day
    ).filter_by(vet_id=vet_id).all()
    days = [day[0] for day in days]
    return days

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
        ).filter_by(vet_id = vet_id, day = day_name)

        time_slot_strings = [f"{slot.time_start.strftime('%H:%M')} - {slot.time_end.strftime('%H:%M')}" for slot in time_slots]
        print(time_slot_strings)

        return jsonify({'time_slots': time_slot_strings})
    
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500