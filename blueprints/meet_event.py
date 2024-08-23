from flask import Blueprint, redirect, request, session, url_for, render_template
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import uuid


meet_event_bp = Blueprint('meet_event_bp', __name__)

@meet_event_bp.route('/confirm_event')
def confirm_event():
  # Assuming the user is already authenticated
  credentials = Credentials(**session['credentials'])
  service = build('calendar', 'v3', credentials=credentials)
  
  # Gather event data from the form or database
  user_email = session['user_email']
  vet_email = 'vet@example.com'  # Replace with actual vet email
  
  event = {
      'summary': f'Vet Appointment with {Vet.first_name} {Vet.last_name}',
      'location': 'Online',
      'description': 'A meeting to discuss pet health.', #replace with actual details
      'start': {
          'dateTime': f'{appointment.time}', #replace with time 
          'timeZone': '',
      },
      'end': {
          'dateTime': '2024-08-18T10:00:00-07:00',
          'timeZone': '',
      },
      'attendees': [
          {'email': User.email},
          {'email': Vet.email},
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
  
  event = service.events().insert(calendarId='primary', 
                                  body=event, 
                                  conferenceDataVersion=1).execute()
  
  print('Event created: %s' % (event.get('htmlLink')))
  return render_template('event_confirmation.html', event=event)
  