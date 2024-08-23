from flask import Blueprint, redirect, request, session, url_for, render_template
from google_auth_oauthlib.flow import Flow
import os

google_meet_bp = Blueprint('google_meet_bp', __name__)

SCOPES = ['https://www.googleapis.com/auth/calendar.events', 
          'https://www.googleapis.com/auth/userinfo.profile', 
          'https://www.googleapis.com/auth/userinfo.email',
         'openid'
         ]

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secrets.json")

@google_meet_bp.route('/login_google')
def login():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, 
                                         scopes=SCOPES
                                        )
    flow.redirect_uri = url_for('google_meet_bp.oauth2callback', 
                                _external=True)
    
    authorization_url, state = flow.authorization_url(access_type='offline',
                                                      include_granted_scopes='true'
                                                     )
    session['state'] = state
    return redirect(authorization_url)

@google_meet_bp.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_meet_bp.oauth2callback', _external=True)
    
    authorization_response = request.url
    
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    
    #store credentials in db later. check how to handle token refresh as well
    session['credentials'] = {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes}
    
    print(credentials)
    
    return render_template('meet_redirect_dummy.html', credentials = credentials)