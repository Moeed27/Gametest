from flask import Blueprint

# Define the Flask Blueprint for this module
email_bp = Blueprint("email_bp", __name__, url_prefix="/email")

def init_app(app):
    # Register the email blueprint with the application
    app.register_blueprint(email_bp)
    # Set up weekly report email scheduler (if not in debug mode or as configured)
    # Only start the scheduler if the app is not in testing mode, etc.
    # (Assume EMAIL_DEBUG config controls whether to actually send emails or not)
    from . import tasks
    # Start background scheduler for weekly emails (avoid running twice in debug reload scenarios)
    if not app.debug:
        tasks.start_scheduler(app)


# Import routes and tasks so that they register with the blueprint and scheduler
from . import routes, tasks
