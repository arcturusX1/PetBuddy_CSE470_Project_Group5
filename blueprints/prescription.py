from flask import Blueprint, render_template
from flask_login.utils import login_required

from model.database import Prescription

#arguments are name of the blueprint, optional - url_prefix = '/some_url'
prescription_bp = Blueprint('prescription', __name__) 


@prescription_bp.route('/prescription') #route assign
# @login_required
def list():
  prescription = Prescription.query.first()
  
  if prescription:
    # Get the patient associated with the prescription
    patient = prescription.patient

    # Get the user associated with the patient
    user = patient.user

    # Create the prescription data dictionary
    prescription_data = {
      'name': f"{user.first_name} {user.last_name}",
      'prescription_no':prescription.id,
      'med_1': prescription.med_1,
      'test_1': prescription.test_1,
      'test_2': prescription.test_2, 
    }
    print(prescription_data)
  else:
    prescription_data = None
  return render_template('prescriptions.html', prescription_data=prescription_data)

# def add_prescription():
#   new_prescription = Prescription(user_id=User.id, med_1='example med')
#   db.session.add(new_prescription)
#   db.session.commit()


