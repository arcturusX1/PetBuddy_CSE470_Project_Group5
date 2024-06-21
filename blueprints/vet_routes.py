
import logging

from flask import Blueprint, abort, jsonify, render_template, request

from model.database import Vet

vet_bp = Blueprint('vet_bp', __name__)


@vet_bp.route('/vets_list')
def show_vets():
    vets = Vet.query.all()
    return render_template('vet_list.html', vets=vets)


@vet_bp.route('/vet/<int:vet_id>')
def vet_profile(vet_id):
    vet = Vet.query.get_or_404(vet_id)
    return render_template('vet_profile.html', vet=vet)


@vet_bp.route('/create_appointment/<int:vet_id>', methods=['POST'])
def create_appointment(vet_id):
    vet = Vet.query.get(vet_id)

    if vet is None:
        logging.error(f'Vet with ID {vet_id} not found.')
        abort(404, description=f'Vet with ID {vet_id} not found.')

    # Parse data sent from client
    data = request.json
    dayOfWeek = data.get('dayOfWeek')
    timeOfDay = data.get('timeOfDay')

    # Example of matching user time with vet availability (replace with your logic)
    if dayOfWeek in vet.availability and timeOfDay in vet.availability[dayOfWeek]:
        # Here you would typically create an Appointment object and save it to the database
        # For simplicity, this example just returns a success message
        return jsonify({'message': 'Appointment created successfully'}), 200
    else:
        return jsonify({'error': 'Vet is not available at this time'}), 400
