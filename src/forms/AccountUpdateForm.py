from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models import User
from flask_login import current_user


class AccountUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    first_name = StringField('First Name',
                                validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name',
                                validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Last Name"})
    bio = TextAreaField('Bio',
                            validators=[DataRequired()], render_kw={"placeholder": "User Bio"})
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != current_user.username:
            raise ValidationError('Username in use, please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != current_user.email:
            raise ValidationError('Email in use, please choose a different one.')
