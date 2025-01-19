from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from maintenance_system.models import Machine


class OptionalDateField(DateField):
    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '':
                self.data = None
            else:
                super().process_formdata(valuelist)

class MachineForm(FlaskForm):
    serial_number = StringField('Serial Number', validators=[DataRequired(), Length(min=4, max=20)])
    installation_date = DateField('Installation Date', format='%Y-%m-%d', validators=[DataRequired()])
    contract_type = SelectField('Contract Type', choices=[(0, 'Warranty'), (1, 'Maintenance'), (2, 'None')], validators=[DataRequired()])
    contract_name = StringField('Contract Name', validators=[Length(min=2, max=20)])
    contract_start_date = DateField('Contract Start Date', format='%Y-%m-%d', validators=[Optional()])
    contract_end_date = DateField('Contract End Date', format='%Y-%m-%d', validators=[Optional()])
    hospital = SelectField('Hospital', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_serial_number(self, serial_number):
        machine = Machine.query.filter_by(serial_number=serial_number.data.strip()).first()
        if machine:
            raise ValidationError('This serial number already exists. Please choose another one.')
