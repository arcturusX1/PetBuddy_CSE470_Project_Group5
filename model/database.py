#ini sqlalchemy in database.py then import it in main.py
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



#user class TODO Password hashing
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  prescription = db.relationship('Prescription', 
                                 back_populates='user', 
                                 cascade="all, delete-orphan")

  def __repr__(self):
    return f'id:{self.id}, username:{self.username}, email:{self.email}'

class Vet(db.Model):
  __tablename__ = 'vets'  # Adding __tablename__ for consistency
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  speciality = db.Column(db.String(100))
  workplace = db.Column(db.String(100))
  experience = db.Column(db.Integer)
  fees = db.Column(db.Float)
  rating = db.Column(db.Float)
  # popularity = db.Column(db.Integer)
  contact_info = db.Column(db.String(100))
  availability = db.Column(db.String(500))

  reviews = db.relationship('VetReview', 
                            back_populates='vet', 
                            cascade="all, delete-orphan")
  
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

class Prescription(db.Model):
  __tablename__ = 'prescription'
  user_id = db.Column(db.Integer, 
                      db.ForeignKey('users.id'), 
                      primary_key=True) 
  #user_id from User table is primary key
  med_1 = db.Column(db.Integer, primary_key=True)
  med_2 = db.Column(db.String(100), nullable=False)
  test_1 = db.Column(db.String(50), nullable=False)
  test_2 = db.Column(db.String(50), nullable=False)
  
  user = db.relationship('User', back_populates='prescriptions')
