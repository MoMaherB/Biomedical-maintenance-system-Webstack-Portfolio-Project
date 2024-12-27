from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from maintenance_system.models import User, Department, Device, Model, Machine, Hospital

#=========================================User Forms====================================================

class UserForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email(message='Please Enter valid email address!')])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],)
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data.strip()).first()
		if user:
			raise ValidationError('This username already taken. Please choose another one.')
		
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data.strip()).first()
		if user:
			raise ValidationError('This email already taken. Please choose another one.')
		
#=========================================Department Forms====================================================


class DepartmentForm(FlaskForm):
	name = StringField('Department Name', validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Add')

	def validate_name(self, name):
		department = Department.query.filter_by(name=name.data.strip()).first()
		if department:
			raise ValidationError('This department name already exists. Please choose another one.')
		
#=========================================Device Forms====================================================

class DeviceForm(FlaskForm):
	name = StringField('Device Name', validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Add')
	
	def validate_name(self, name):
		device = Device.query.filter_by(name=name.data.strip()).first()
		if device:
			raise ValidationError('This device name already exists. Please choose another one.')
		
#=========================================Model Forms====================================================

class ModelForm(FlaskForm):
	name = StringField('Model Name', validators=[DataRequired(), Length(min=2, max=20)])
	manufacturer = StringField('Manufacturer', validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Add')
	
	def validate_name(self, name):
		model = Model.query.filter_by(name=name.data.strip()).first()
		if model:
			raise ValidationError('This model name already exists. Please choose another one.')

#==========================================Machine Forms====================================================
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
	submit = SubmitField('Add')

	def validate_serial_number(self, serial_number):
		machine = Machine.query.filter_by(serial_number=serial_number.data.strip()).first()
		if machine:
			raise ValidationError('This serial number already exists. Please choose another one.')


#=========================================Hospital Forms====================================================
class HospitalForm(FlaskForm):
	name = StringField('Hospital Name', validators=[DataRequired(), Length(min=2, max=50)])
	governorate = StringField('Governorate', validators=[DataRequired(), Length(min=5, max=50)])
	submit = SubmitField('Add')

	def validate_name(self, name):
		hospital = Hospital.query.filter_by(name=name.data.strip()).first()
		if hospital:
			raise ValidationError('This hospital name already exists. Please choose another one.')			