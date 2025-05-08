from flask import current_app, render_template, request, redirect, url_for, flash
from itsdangerous import BadSignature, SignatureExpired
from database.tables import User  # Import the database and User model
from config import db
from app_email.utils import confirm_token
from app_email import email_bp

@email_bp.route("/verify/<token>")
def verify_email(token):
    try:
        # Confirm the token and get the user ID (assuming token contains user ID)
        user_id = confirm_token(token, salt='email-confirm', expiration=current_app.config.get('EMAIL_CONFIRM_EXPIRES', 3600*24))
    except SignatureExpired:
        # Token is valid but expired
        return "The confirmation link has expired.", 400
    except BadSignature:
        # Token is invalid
        return "The confirmation link is invalid.", 400
    # Token was valid, find the user by ID and activate them
    user = User.query.get(int(user_id))
    if not user:
        return "User not found.", 404
    # Mark the user as verified (assuming User model has an 'email_verified' or similar field)
    user.email_verified = True
    db.session.commit()
    # Optionally, flash a message or redirect to a login page
    # For simplicity, just return a confirmation message here
    return "Email verified successfully. You can now log in."
@email_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        # Verify the token validity
        user_id = confirm_token(token, salt='password-reset',
                                expiration=current_app.config.get('RESET_TOKEN_EXPIRES', 3600 * 2))
    except SignatureExpired:
        return "The password reset link has expired.", 400
    except BadSignature:
        return "The password reset link is invalid.", 400
        # Token is valid; fetch the user
    user = User.query.get(int(user_id))
    if not user:
        return "User not found.", 404
    if request.method == 'GET':
        # Render a template with a form for the user to enter a new password
        return render_template('email/reset_form.html', token=token)
    # If POST method:
    new_password = request.form.get('password')
    if not new_password:
        return "Password is required.", 400
    # Update the user's password (assuming User model has a password field and storing hashed password)
    from werkzeug.security import generate_password_hash
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return "Your password has been reset successfully. You can now log in with the new password."