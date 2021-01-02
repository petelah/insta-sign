from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NewPostForm(FlaskForm):
    content = TextAreaField('Content',
                             validators=[DataRequired(), Length(min=2, max=600)], render_kw={"placeholder": "Post content"})
    image = FileField('Image',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Post')