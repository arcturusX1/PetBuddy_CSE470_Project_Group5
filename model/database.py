#ini sqlalchemy in database.py then import it in main.py
import json

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()



#user class TODO Password hashing
class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  first_name = db.Column(db.String(80), nullable=False)
  last_name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  phone = db.Column(db.String(80), unique=True, nullable=False)
  password_hash = db.Column(db.String(256), nullable=False) 
  is_user = db.Column(db.Boolean, nullable=False)
  is_vet = db.Column(db.Boolean, nullable=False)
  

  patient = db.relationship('Patient', back_populates='user') #New
  vet = db.relationship('Vet', back_populates='user') #New

  def __repr__(self):
    return f'id:{self.id}, username:{self.username}, email:{self.email}'

class Vet(db.Model):
  __tablename__ = 'vets'  # Adding __tablename__ for consistency
  id = db.Column(db.Integer, primary_key=True, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Foreign key to User table
  name = db.Column(db.String(100))
  speciality = db.Column(db.String(100))
  workplace = db.Column(db.String(100))
  experience = db.Column(db.Integer)
  fees = db.Column(db.Float)
  rating = db.Column(db.Float)
  contact_info = db.Column(db.String(100))
  availability = db.Column(db.String(500))

  reviews = db.relationship('VetReview', back_populates='vet', 
                            cascade="all, delete-orphan")

  user = db.relationship('User', back_populates='vet')
  
  def set_availability(self, availability_dict):
    self.availability = json.dumps(availability_dict)

  def get_availability(self):
    return json.loads(self.availability)
  
  def __repr__(self):
    return f'<Vet {self.name}>'

class VetReview(db.Model):
  __tablename__ = 'vet_reviews'
  id = db.Column(db.Integer, primary_key=True)
  vet_id = db.Column(db.Integer, 
                     db.ForeignKey('vets.id'), 
                     nullable=False)
  review = db.Column(db.Text, nullable=False)
  rating = db.Column(db.Float, nullable=False)
  review_date = db.Column(db.Date, 
                          default=db.func.current_date(), 
                          nullable=False)

  vet = db.relationship('Vet', back_populates='reviews')

  def __repr__(self):
      return f'<VetReview {self.id} for Vet {self.vet_id}>'


#New Patient class
class Patient(db.Model):
  __tablename__ = 'patients'
  id = db.Column(db.Integer, primary_key=True, nullable = False)  # Primary key for the Patient table
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to reference the Users table
  no_of_pets = db.Column(db.Integer, nullable=False)
  prescription = db.relationship('Prescription', 
     back_populates='patient', 
     cascade="all, delete-orphan")

  # Relationship to the User model
  user = db.relationship('User', back_populates='patient')

  def __repr__(self):
      return f'<Patient {self.id}>'



class Prescription(db.Model):
  __tablename__ = 'prescription'
  id = db.Column(db.Integer, 
                 primary_key=True, 
                 nullable=False,
                autoincrement=True)
  patient_id = db.Column(db.Integer, 
                      db.ForeignKey('patients.id'),
                     nullable=False) 

  med_1 = db.Column(db.String(100), nullable=False)
  med_2 = db.Column(db.String(100), nullable=True)
  test_1 = db.Column(db.String(50), nullable=True)
  test_2 = db.Column(db.String(50), nullable=True)
  
  patient = db.relationship('Patient', back_populates='prescription')

__table_args__ = (db.UniqueConstraint('id', 
                                      'user_id',   
                                      name='uix_id_user_id'),
                 )