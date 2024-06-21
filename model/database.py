#ini sqlalchemy in database.py then import it in main.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



#user class TODO Password hashing
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

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
  popularity = db.Column(db.Integer)
  contact_info = db.Column(db.String(100))
  availability = db.Column(db.String(500))  # Storing as JSON string
  
  def set_availability(self, availability_dict):
    self.availability = json.dumps(availability_dict)

  def get_availability(self):
    return json.loads(self.availability)
  
  def __repr__(self):
    return f'<Vet {self.name}>'