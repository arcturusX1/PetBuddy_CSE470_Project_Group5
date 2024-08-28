from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

from model.database import Vet

from .forms import AppointmentForm

appointment_bp = Blueprint('appointment', __name__)

# Helper function to convert string time to datetime object
def time_string_to_datetime(time_string):
    return datetime.strptime(time_string, "%H:%M").time()

@appointment_bp.route('/appointment_form', methods=['GET', 'POST'])
def appointment_form():
    vet_id = request.args.get('vet_id')
    date = request.args.get('date')
    time = request.args.get('time')
    vet = Vet.query.get(vet_id)

    # Determine the day of the week
    appointment_date = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = appointment_date.strftime('%A').lower()

    # Extract available time slots for the given day
    available_slots = vet.availability.get(day_of_week, [])

    # Convert available_slots to datetime objects for comparison
    available_times = []
    for slot in available_slots:
        start_time = time_string_to_datetime(slot[0])
        end_time = time_string_to_datetime(slot[1])
        current_time = start_time
        while current_time < end_time:
            available_times.append(current_time.strftime("%H:%M"))
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()

    form = AppointmentForm()

    # Pre-fill form with vet information
    form.vet_name.data = f"{vet.first_name} {vet.last_name}"
    form.speciality.data = vet.speciality
    form.workplace.data = vet.workplace
    form.fees.data = vet.fees

    # Set the date field in the form
    form.date.data = appointment_date

    # Filter available times to populate the time choices in the form
    form.time.choices = [(t, t) for t in available_times]

    if form.validate_on_submit():
        # Implement form submission logic here (e.g., save the appointment)
        flash('Appointment successfully booked!', 'success')
        return redirect(url_for('some_page'))  # Redirect to some page after booking

    return render_template("appointment_form.html", form=form, available_times=available_times)
