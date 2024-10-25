from flask import Blueprint, redirect, request, session, url_for, render_template, Response
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import uuid
from model.database import Appointment, User, Vet


meet_event_bp = Blueprint('meet_event_bp', __name__)

def check_google_login():
    # Check if 'credentials' exist in the session
    if 'credentials' not in session:
        # Redirect to your Google login route if not logged in
        return redirect(url_for('google_oauth_bp.login'))
    
    # Check if the credentials are valid
    credentials = Credentials(**session['credentials'])
    if not credentials or not credentials.valid:
        # If credentials are invalid, redirect to Google login
        return redirect(url_for('google_oauth_bp.login'))

    # If the user is signed in, return True
    return True

@meet_event_bp.route('/confirm_event', methods=['GET', 'POST'])
def confirm_event():
    redirect_response = check_google_login()
    if isinstance(redirect_response, Response):  # If redirected
        return redirect_response

    # If the user is signed in, create the Calendar service
    credentials = Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=credentials)

    appt_id = request.args.get('appt_id')
    appointment = Appointment.query.filter_by(id = appt_id).first()
    vet = Vet.query.filter_by(id = appointment.vet_id).first()
    user = User.query.filter_by(id = appointment.user_id).first()
    
    event = {
        'summary': f'VET: {vet.first_name} {vet.last_name} USER: {user.first_name} {user.last_name}',
        'location': 'Online',
        'description': 'A meeting to discuss pet health.', #replace with actual details
        'start': {
            'dateTime': appointment.start_time.isoformat(), #replace with time 
            'timeZone': 'Asia/Dhaka',
        },
        'end': {
            'dateTime': appointment.end_time.isoformat(),
            'timeZone': 'Asia/Dhaka',
        },
        'attendees': [
            {'email': user.email},
            {'email': vet.user.email},
        ],
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4),
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

        print('Event created: %s' % (event.get('htmlLink')))

        return render_template('event_confirmation.html', event=event)

    except Exception as e:

        print('Error creating event:', e)

        return 'Error creating event', 500
  