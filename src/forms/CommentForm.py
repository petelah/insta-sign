from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = StringField('Content',
                             validators=[DataRequired(), Length(min=2, max=600)], render_kw={"placeholder": "Comment"})
    submit = SubmitField('Submit')