from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

# User class for general user information
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
    no_of_pets = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    pets = db.relationship('Pet', back_populates='user', cascade="all, delete-orphan")
    prescriptions = db.relationship('Prescription', back_populates='user', cascade="all, delete-orphan")
    appointments = db.relationship('Appointment', back_populates='user')
    vet = db.relationship('Vet', back_populates='user', uselist=False)  # One-to-one relationship with Vet

    def __repr__(self):
        return f'id:{self.id}, username:{self.username}, email:{self.email}'


# Pet class for storing pets details
class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', back_populates='pets')

    def __repr__(self):
        return f'<Pet {self.name}, Type {self.animal_type}, Breed {self.breed}, Age {self.age}>'


# Vet class for veterinarian details
class Vet(db.Model):
    __tablename__ = 'vets'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey linking to User
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    speciality = db.Column(db.String(100))
    workplace = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    fees = db.Column(db.Float)
    rating = db.Column(db.Float)
    contact_info = db.Column(db.String(100))
    availability_json = db.Column(JSONB)

    user = db.relationship('User', back_populates='vet')  # Backref to the User model
    reviews = db.relationship('VetReview', back_populates='vet', cascade="all, delete-orphan")
    appointments = db.relationship('Appointment', back_populates='vet')
    availability = db.relationship('VetAvailability', back_populates='vet', cascade='all, delete-orphan')

    def set_availability(self, availability_dict):
        self.availability = availability_dict

    def get_availability(self):
        return self.availability

    def __repr__(self):
        return f'<Vet: ID:{self.id} {self.first_name} {self.last_name}>'

class VetAvailability(db.Model):
    """Stores Vet Availability in days and timeslots. Shows if a slot is booked or not."""
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'), nullable=False)
    day=db.Column(db.Text, nullable=False)
    time_start=db.Column(db.Time, nullable=False)
    time_end=db.Column(db.Time, nullable=False) 
    booked=db.Column(db.Boolean, nullable=False, default=False)

    vet = db.relationship('Vet', back_populates='availability')

# VetReview class for veterinarian reviews
class VetReview(db.Model):
    __tablename__ = 'vet_reviews'
    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review_date = db.Column(db.Date, default=db.func.current_date(), nullable=False)

    vet = db.relationship('Vet', back_populates='reviews')

    def __repr__(self):
        return f'<VetReview {self.id} for Vet {self.vet_id}>'


# Appointment class for scheduling appointments
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    start_time = db.Column(db.DateTime, default = func.now(), nullable=False)
    end_time = db.Column(db.DateTime, default = func.now(), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    vet = db.relationship('Vet', back_populates='appointments')
    user = db.relationship('User', back_populates='appointments')

    def __repr__(self):
        return f'<Appointment {self.id} for User {self.user_id} at {self.date} {self.time}>'


# Prescription class for patient prescriptions
class Prescription(db.Model):
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    med_1 = db.Column(db.String(100), nullable=False)
    med_2 = db.Column(db.String(100), nullable=True)
    test_1 = db.Column(db.String(50), nullable=True)
    test_2 = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', back_populates='prescriptions')

    __table_args__ = (db.UniqueConstraint('id', name='uix_id'),)

    def __repr__(self):
        return f'<Prescription {self.id} for User {self.user_id}>'