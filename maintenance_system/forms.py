from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from maintenance_system.models import User, Department, Device, Model

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

class MachineForm(FlaskForm):
	pass