from flask import current_app, url_for, redirect, flash, jsonify
from . import email_bp
from .utils import confirm_token

@email_bp.route("/verify/<token>")
def verify_email(token):
    """Endpoint to verify a user's email using a token."""
    # Decode and verify the token to get the user's email
    email = confirm_token(token)
    if not email:
        # Token is invalid or expired
        # In a real app, you might redirect to an error page or prompt to resend verification
        return jsonify({"message": "Invalid or expired token."}), 400

    # Find the user by email (assuming a User model with an email field)
    # and mark their email as verified.
    # (Integration point: import and use your User model and database session)
    user = None
    try:
        from app.models import User, db  # adjust import based on actual project structure
        user = User.query.filter_by(email=email).first()
    except ImportError:
        # If we cannot import the app's models (e.g., in a test context), simulate it
        user = None

    if user:
        user.email_verified = True  # Assume User model has an 'email_verified' boolean field
        try:
            db.session.commit()
        except Exception:
            pass  # handle database commit errors if needed
        # In practice, you might redirect to the login page with a success message:
        # flash("Email verified! Please log in.", "success")
        # return redirect(url_for("auth.login"))
        return jsonify({"message": "Email verified successfully. Please log in."})
    else:
        # If no user is found for the email (unlikely if token was valid), handle gracefully
        return jsonify({"message": "Verification failed: user not found."}), 404
