from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from model.database import Vet

vet_profile_bp = Blueprint('vet_profile_bp', __name__)

@vet_profile_bp.route('/vet_profile')
@login_required
def vet_profile():
    if not current_user.is_vet:
        # Redirect to a suitable page if the user is not a vet
        return redirect(url_for('home_bp.index'))

    print(f'Current User ID: {current_user.id}')  # Debugging statement
    vet = Vet.query.filter_by(user_id=current_user.id).first()
    if not vet:
        print(f'Vet profile not found for User ID: {current_user.id}')  # Debugging statement
        return "Vet profile not found", 404

    print(f'Vet profile found: {vet}')  # Debugging statement
    return render_template('vet_profile.html', vet=vet)

@vet_profile_bp.route('/vet_profile/attend_appointments/<int:vet_id>')
@login_required
def attend_appointments(vet_id):
    if not current_user.is_vet or current_user.id != vet_id:
        return "Access Denied", 403

    # Logic for attending appointments
    return render_template('attend_appointments.html', vet_id=vet_id)
