def register_bp(app):
  from blueprints.appointment import appointment_bp
  from blueprints.appointment_showcase import appointment_showcase_bp
  from blueprints.home import home_bp
  from blueprints.login import login_bp
  from blueprints.mail import mail_bp
  from blueprints.patient_profile import patient_profile_bp
  from blueprints.prescription import prescription_bp
  from blueprints.signup import signup_bp
  from blueprints.users import user_bp
  from blueprints.vet_routes import vet_bp

  app.register_blueprint(home_bp)
  app.register_blueprint(vet_bp)
  app.register_blueprint(user_bp)
  app.register_blueprint(login_bp)
  app.register_blueprint(signup_bp)
  app.register_blueprint(patient_profile_bp)
  app.register_blueprint(prescription_bp)
  app.register_blueprint(appointment_bp)
  app.register_blueprint(appointment_showcase_bp)
  app.register_blueprint(mail_bp)