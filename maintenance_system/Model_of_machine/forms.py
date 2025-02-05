from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from maintenance_system.models import Model
from flask_wtf.file import FileField, FileAllowed


class ModelForm(FlaskForm):
    name = StringField('Model Name', validators=[DataRequired(), Length(min=2, max=20)])
    manufacturer = StringField('Manufacturer', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Model Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

    def validate_name(self, name):
        model = Model.query.filter_by(name=name.data.strip()).first()
        if model:
            raise ValidationError('This model name already exists. Please choose another one.')
