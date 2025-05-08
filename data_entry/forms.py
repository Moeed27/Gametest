from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, TimeField, DateTimeField
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
    transport = SelectField('Transport Options', validators=[DataRequired()],
                       choices=[('Car (Petrol)', 'Car (Petrol)'), ('Car (Diesel)', 'Car (Diesel)'), ('Train', 'Train'), ('Bus', 'Bus'), ('Bicycle', 'Bicycle'), ('Plane', 'Plane'), ('Motorbike', 'Motorbike')])
    start_time = DateTimeField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    distance_unit = SelectField('Distance Unit', validators=[DataRequired()],
                       choices=[('Km', 'Km'), ('Miles', 'Miles')])
    distance = FloatField('Distance', validators=[DataRequired(), NumberRange(min=0, message="Number can't be lower than 0")])
    is_public = SelectField('Post visibility', validators=[DataRequired()],
                         choices=[(True, 'Public'), (False, 'Private')])
    submit = SubmitField('Submit')

class UserCar(FlaskForm):
    fuel_consumption = DecimalField('Fuel Consumption', validators=[DataRequired(), NumberRange(min=0, message="Number can't be lower than 0")])
    type = SelectField('Fuel type', validators=[DataRequired()],
                       choices=[('petrol', 'Petrol'), ('diesel', 'Diesel')])
    submit = SubmitField('Submit')