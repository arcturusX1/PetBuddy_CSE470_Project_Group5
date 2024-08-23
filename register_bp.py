def register_bp(app):
  from blueprints.appointment import appointment_bp
  from blueprints.appointment_showcase import appointment_showcase_bp
  from blueprints.auth import auth_bp
  from blueprints.book_appointment import book_appointment_bp
  from blueprints.google_oauth import google_meet_bp
  from blueprints.home import home_bp
  from blueprints.mail import mail_bp
  from blueprints.patient_profile import patient_profile_bp
  from blueprints.prescription import prescription_bp
  from blueprints.vet_routes import vet_bp
  from blueprints.vet_profile import vet_profile_bp  # Add vet profile blueprint

  app.register_blueprint(home_bp)
  app.register_blueprint(vet_bp)
  app.register_blueprint(auth_bp)
  app.register_blueprint(patient_profile_bp)
  app.register_blueprint(prescription_bp)
  app.register_blueprint(appointment_bp)
  app.register_blueprint(appointment_showcase_bp)
  app.register_blueprint(mail_bp)
  app.register_blueprint(book_appointment_bp)
  app.register_blueprint(google_meet_bp)
  app.register_blueprint(vet_profile_bp)  # Register vet profile blueprint
