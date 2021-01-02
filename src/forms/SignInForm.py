from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class SignInForm(FlaskForm):
    name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    symptoms = BooleanField('I am not experiencing any flu like symptoms:', validators=[DataRequired()])
    follow = BooleanField('Follow us!')
    sign_up = BooleanField('Want cool emails from this place?')
    submit = SubmitField('Sign In')
