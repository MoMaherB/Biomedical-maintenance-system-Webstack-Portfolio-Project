from flask_wtf import FlaskForm
from wtforms.fields import SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length 


class TaskForm(FlaskForm):
    task_type = SelectField('Task Type', choices=[('0', 'Preventive'), ('1', 'Corrective'), ('2', 'installation')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=100)])
    hospital = SelectField('Hospital', choices=[('', 'Choose a hospital')], validators=[DataRequired()])
    governorate = SelectField('Governorate', choices=[('', 'Choose a governorate')], validators=[DataRequired()])
    device = SelectField('Device', choices=[('', 'Choose a device')], validators=[DataRequired()])
    model = SelectField('Model',  choices=[('', 'Choose a device')], validators=[DataRequired()])
    machine = SelectMultipleField('Machine', validators=[DataRequired()])
    user = SelectMultipleField('Engineer(s) / Technichan(s)', validators=[DataRequired()])
