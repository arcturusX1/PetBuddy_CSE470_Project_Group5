from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Optional


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    account_type = SelectField('Account Type', choices=[('user', 'User'), ('vet', 'Vet')], validators=[DataRequired()])
    submit = SubmitField('Add User')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember= BooleanField('Remember Me')

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

    remember= BooleanField('Remember Me')
