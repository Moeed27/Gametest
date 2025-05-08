from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TimeField, DateTimeField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import DataRequired, NumberRange


class TypeForm(FlaskForm):
    type = SelectField('Form Options', validators=[DataRequired()],
                       choices=[('Appliance','Appliance'),('Transport', 'Transport')])
    submit = SubmitField('Submit')

class ApplianceForm(FlaskForm):
    appliance = StringField('Appliance Name', validators=[DataRequired()])
    wattage = IntegerField('Wattage', validators=[DataRequired(), NumberRange(min=0, message="Number can't be lower than 0")])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    is_public = SelectField('Post visibility', validators=[DataRequired()],
                         choices=[(True, 'Public'), (False, 'Private')])
    submit = SubmitField('Submit')

class TransportForm(FlaskForm):
    transport = StringField('Transport Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    distance = IntegerField('Distance', validators=[DataRequired(), NumberRange(min=0, message="Number can't be lower than 0")])
    is_public = SelectField('Post visibility', validators=[DataRequired()],
                         choices=[(True, 'Public'), (False, 'Private')])
    submit = SubmitField('Submit')

class UserCar(FlaskForm):
    fuel_consumption = DecimalField('Fuel Consumption', validators=[DataRequired(), NumberRange(min=0, message="Number can't be lower than 0")])
    type = SelectField('Fuel type', validators=[DataRequired()],
                       choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')])
    submit = SubmitField('Submit')