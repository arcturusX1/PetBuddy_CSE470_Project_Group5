from datetime import datetime
from flask import Blueprint, jsonify, render_template, request
from model.database import Vet

book_appointment_bp = Blueprint('book_appointment_bp', __name__)

def is_time_in_slot(time, slots):
    """Check if the given time is within any of the provided slots."""
    try:
        return any(start <= time <= end for start, end in slots)
    except Exception:
        return False

@book_appointment_bp.route('/book_appointment/', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        data = request.json
        selected_date = data.get('date')
        selected_time = data.get('time')

        if not selected_date or not selected_time:
            return jsonify({'error': 'Date and time are required'}), 400

        selected_day = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%A').lower()

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
