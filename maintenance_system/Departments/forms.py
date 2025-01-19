from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from maintenance_system.models import Department


class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        department = Department.query.filter_by(name=name.data.strip()).first()
        if department:
            raise ValidationError('This department name already exists. Please choose another one.')
