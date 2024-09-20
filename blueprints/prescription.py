from flask import Blueprint, render_template
from flask_login import login_required
from model.database import Prescription

# Create the Blueprint
prescriptions_bp = Blueprint('prescriptions_bp', __name__)

@prescriptions_bp.route('/prescriptions')
@login_required
def view_prescriptions():
    prescription = Prescription.query.first()

    if prescription:
        patient = prescription.patient
        user = patient.user

        prescription_data = {
            'name': f"{user.first_name} {user.last_name}",
            'prescription_no': prescription.id,
            'med_1': prescription.med_1,
            'test_1': prescription.test_1,
            'test_2': prescription.test_2, 
        }
        print(prescription_data)
    else:
        prescription_data = None
    return render_template('prescriptions.html', prescription_data=prescription_data)
