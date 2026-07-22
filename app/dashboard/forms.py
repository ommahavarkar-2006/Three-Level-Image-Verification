from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    """Form for updating user profile information."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField('Update Profile')


class SearchForm(FlaskForm):
    """Form for dashboard search functionality."""
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
