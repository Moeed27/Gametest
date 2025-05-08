from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20),
                                                   Regexp('^[a-zA-Z-]+$', message="Only letters and hyphens are allowed")])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired(),
                                                      Regexp('^[a-zA-Z-]+$', message="Only letters and hyphens are allowed")])
    lastname = StringField('Last Name', validators=[DataRequired(),
                                                    Regexp('^[a-zA-Z-]+$', message="Only letters and hyphens are allowed")])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(8, 15, message='Password must be 8 to 15 characters long'),
                                                     Regexp('.*[A-Z]', message='Password must contain at least one upper case letter'),
                                                     Regexp('.*[a-z]', message='Password must contain at least one lower case letter'),
                                                     Regexp('.*\d', message='Password must contain at least one number'),
                                                     Regexp('.*\W', message='Password must contain at least one special character')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    mfapin = StringField('MFA Pin')
    recaptcha = RecaptchaField()
    submit = SubmitField('Log In')