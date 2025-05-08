from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, current_user, login_required
import pyotp
from argon2 import PasswordHasher
from database.enums import Roles
from database.tables import User
#from app_email.tasks import send_verification_email
from user.forms import RegistrationForm, LoginForm
from config import db

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in.", "success")
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already in use.", "danger")
            return render_template("user/register.html", form=form)
        mfa_key = pyotp.random_base32()
        ph = PasswordHasher()
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=ph.hash(form.password.data),
                        role=Roles.user,
                        first_name=form.firstname.data,
                        last_name=form.lastname.data,
                        mfa_key=mfa_key,
                        mfa_enabled=False
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created', category='success')
        flash('MFA must be enabled before account use', category='warning')
        uri = str(pyotp.totp.TOTP(new_user.mfa_key).provisioning_uri(new_user.email, "Carbon Cruncher"))
        return render_template("user/mfasetup.html", secret=mfa_key, uri=uri)
    return render_template('user/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "success")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            if pyotp.TOTP(user.mfa_key).verify(form.mfapin.data):
                if not user.mfa_enabled:
                    user.update_mfa()
                flash('Login Successful', category='success')
                login_user(user)
                if not user.emailSent():
                    #send_verification_email(user)
                    pass
                return redirect(url_for('user.profile'))
            if not user.mfa_enabled():
                flash('MFA must be enabled before account use', category='warning')
                uri = str(pyotp.totp.TOTP(user.mfa_key).provisioning_uri(user.email, "Carbon Cruncher"))
                return render_template('user/mfasetup.html', secret=user.mfa_key, uri=uri)
        flash('Login Failed', category='danger')
        return redirect(url_for('user.login'))
    return render_template('user/login.html', form=form)

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
