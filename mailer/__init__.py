from flask import Blueprint

# Define the Flask Blueprint for this module
email_bp = Blueprint("email_bp", __name__, url_prefix="/email")

def init_app(app):
    """Initialize the email module with the Flask app."""
    # Register the email blueprint with the application
    app.register_blueprint(email_bp)
    # Schedule the weekly report emails job (if scheduler is used)
    try:
        from .tasks import schedule_jobs
        schedule_jobs(app)
    except ImportError:
        # In case tasks module is not present or APScheduler not configured
        pass
