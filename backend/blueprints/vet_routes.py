from flask import Blueprint, abort, jsonify, render_template, request
from flask_wtf.csrf import validate_csrf

from model.database import Vet, VetReview, db

from .forms import VetFilterForm

vet_bp = Blueprint('vet_bp', __name__)

@vet_bp.route('/api/vets', methods=['GET'])
def show_vets():
    vets = Vet.query.all()
    vets_data = [
        {
            'id': vet.id,
            'first_name': vet.first_name,
            'last_name': vet.last_name,
            'speciality': vet.speciality,
            'workplace': vet.workplace
        }
        for vet in vets
    ]
    return jsonify(vets_data), 200


@vet_bp.route('/vet/<int:vet_id>')
def vet_profile(vet_id):
    vet = Vet.query.get_or_404(vet_id)
    reviews = VetReview.query.filter_by(vet_id=vet_id).all()  # gets vet.id and checks with vet.id in VetReview
    return render_template('vet_profile.html', vet=vet)

# Vet Search
@vet_bp.route('/search_vets', methods=['GET'])
def search_vets():
    query = request.args.get('query', '').strip()
    if query:
        vets = Vet.query.filter(
            db.or_(
                Vet.name.ilike(f'%{query}%'),
                Vet.speciality.ilike(f'%{query}%'),
                Vet.workplace.ilike(f'%{query}%'),
                Vet.contact_info.ilike(f'%{query}%')
            )
        ).all()
    else:
        vets = Vet.query.all()
    return render_template('vet_list.html', vets=vets)

# @vet_bp.route('/create_appointment/<int:vet_id>', methods=['POST'])
# def create_appointment(vet_id):
#     vet = Vet.query.get(vet_id)
#     if vet is None:
#         logging.error(f'Vet with ID {vet_id} not found.')
#         abort(404, description=f'Vet with ID {vet_id} not found.')

#     # Parse data sent from client
#     data = request.json
#     dayOfWeek = data.get('dayOfWeek')
#     timeOfDay = data.get('timeOfDay')

#     availability = vet.get_availability()
#     if dayOfWeek in availability and timeOfDay in availability[dayOfWeek]:
#         # Space to create an Appointment object and save it to the database
#         # For simplicity, this example just returns a success message
#         return jsonify({'message': 'Appointment created successfully'}), 200
#     else:
#         return jsonify({'error': 'Vet is not available at this time'}), 400

@vet_bp.route('/filter_vets', methods=['GET', 'POST'])
def filter_vets():
    specialities = db.session.query(Vet.speciality.distinct()).all()
    workplaces = db.session.query(Vet.workplace.distinct()).all()

    form = VetFilterForm()
    form.update_choices(specialities, workplaces)

    if form.validate_on_submit():
        print(form.speciality.data, form.workplace.data)
        query = Vet.query
        if form.speciality.data:
            query = query.filter(Vet.speciality == form.speciality.data)
        if form.workplace.data:
            query = query.filter(Vet.workplace == form.workplace.data)
        if form.experience.data:
            if form.experience.data == '0-2':
                query = query.filter(Vet.experience.between(0, 2))
            elif form.experience.data == '3-5':
                query = query.filter(Vet.experience.between(3, 5))
            elif form.experience.data == '6-10':
                query = query.filter(Vet.experience.between(6, 10))
            elif form.experience.data == '10+':
                query = query.filter(Vet.experience >= 10)
        vets = query.all()
    else:
        vets = Vet.query.all()

    return render_template('vet_list.html', form=form, vets=vets)