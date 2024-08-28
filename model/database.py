from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pass1 = PasswordField('Password', validators=[DataRequired(), 
                                                  Length(min=8, max=15,
                                                         message='Password must be between 8 and 15 characters long')])
    pass2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                          EqualTo('pass1',
                                                                message='Passwords do not match')])
    account_type = SelectField('Account Type', choices=[('user', 'User'), ('vet', 'Vet')], validators=[DataRequired()])

    # Vet-specific fields
    speciality = StringField('Specialty', validators=[Optional()])
    workplace = StringField('Workplace', validators=[Optional()])
    experience = IntegerField('Experience', validators=[Optional()])
    fees = FloatField('Fees', validators=[Optional()])
    contact_info = StringField('Contact Info', validators=[Optional()])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class VetFilterForm(FlaskForm):
    speciality = SelectField('Specialty', 
                             choices=[('', 'All Specialties')], 
                             validators=[Optional()],
                            )
    workplace = SelectField('Workplace', 
                            choices=[('', 'All Workplaces')], 
                            validators=[Optional()],
                           )
    experience = SelectField('Experience', 
                             choices=[
                                 ('', 'All Experience'),
                                 ('0-2', '0-2 years'),
                                 ('3-5', '3-5 years'),
                                 ('6-10', '6-10 years'),
                                 ('10+', '10+ years')
                             ], 
                             validators=[Optional()], 
                             )
    submit = SubmitField('Filter')

    def update_choices(self, specialities, workplaces):
        self.speciality.choices = [('', 'All Specialties')] + [(s[0], s[0]) for s in specialities]
        self.workplace.choices = [('', 'All Workplaces')] + [(w[0], w[0]) for w in workplaces]

class AddPrescriptionForm(FlaskForm):
    # Define fields for adding a prescription
    submit = SubmitField('Add Prescription')

class AppointmentForm(FlaskForm):
    vet_name = StringField('Veterinarian', validators=[DataRequired()])
    speciality = StringField('Specialty', validators=[DataRequired()])
    workplace = StringField('Workplace', validators=[DataRequired()])
    fees = StringField('Consultation Fees ($)',
                       validators=[DataRequired()])
    date = DateField('Appointment Date', validators=[DataRequired()])
    time = SelectField('Appointment Time', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddPetForm(FlaskForm):
    pet_name = StringField('Pet Name', validators=[DataRequired()])
    animal_type = SelectField('Animal Type', choices=[('Dog', 'Dog'), ('Cat', 'Cat')], validators=[DataRequired()])
    breed = StringField('Breed', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    submit = SubmitField('Add Pet')
