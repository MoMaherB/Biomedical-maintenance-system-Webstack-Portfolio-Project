from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from maintenance_system.models import Device


class DeviceForm(FlaskForm):
    name = StringField('Device Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        device = Device.query.filter_by(name=name.data.strip()).first()
        if device:
            raise ValidationError('This device name already exists. Please choose another one.')
