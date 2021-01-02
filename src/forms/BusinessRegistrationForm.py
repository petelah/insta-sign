from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from src.models import User


class BusinessRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    business_name = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Business name"})
    state = StringField('State', validators=[DataRequired()], render_kw={"placeholder": "State"})
    post_code = StringField('Post code', validators=[DataRequired()], render_kw={"placeholder": "Post code"})
    country = StringField('Country', validators=[DataRequired()], render_kw={"placeholder": "Country"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != current_user.email:
            raise ValidationError('Email in use, please choose a different one.')
