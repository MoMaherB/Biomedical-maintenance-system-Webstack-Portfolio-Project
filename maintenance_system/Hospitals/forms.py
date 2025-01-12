from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from maintenance_system.models import Hospital


class HospitalForm(FlaskForm):
	name = StringField('Hospital Name', validators=[DataRequired(), Length(min=2, max=50)])
	governorate = StringField('Governorate', validators=[DataRequired(), Length(min=5, max=50)])
	submit = SubmitField('Add')

	def validate_name(self, name):
		hospital = Hospital.query.filter_by(name=name.data.strip()).first()
		if hospital:
			raise ValidationError('This hospital name already exists. Please choose another one.')