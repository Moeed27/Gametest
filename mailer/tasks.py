# email/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .utils import send_email

def send_weekly_reports():
    """
    Fetch or compute weekly carbon usage for all users and send emails.
    This function simulates data if real data access is not available.
    """
    # Integration point: fetch users from the database who opted in for weekly reports
    users = []
    try:
        from app.models import User
        users = User.query.filter_by(weekly_report=True).all()
    except ImportError:
        # Simulate a list of user objects for demonstration purposes (name and email needed)
        class DummyUser:
            def __init__(self, name, email):
                self.name = name
                self.email = email
        users = [
            DummyUser("Alice", "[email protected]"),
            DummyUser("Bob", "[email protected]")
        ]

    # Determine the date range for the last week (for reporting purposes)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    # For each user, prepare and send a weekly report email
    for user in users:
        # Skip users who have not opted in (assuming 'weekly_report' attribute on User model)
        if hasattr(user, "weekly_report") and not getattr(user, "weekly_report"):
            continue

        # Generate placeholder data for weekly usage (or fetch real data if available)
        try:
            from database.models import CarbonLog
            # Example: sum up energy and carbon for the past week from CarbonLog table
            logs = CarbonLog.query.filter(
                CarbonLog.user_id == getattr(user, 'id', None),
                CarbonLog.date >= start_date,
                CarbonLog.date < end_date
            ).all()
            total_energy = sum(log.energy_used for log in logs)
            total_carbon = sum(log.carbon_emitted for log in logs)
        except Exception:
            # If actual data not accessible, use dummy values as placeholders
            total_energy = 100  # e.g., 100 kWh used in the week
            total_carbon = 50   # e.g., 50 kg CO2 emitted

        # Compose the email content for the weekly report
        subject = "Your Weekly Carbon Usage Report"
        content = f"""
        <p>Hello {getattr(user, 'name', 'User')},</p>
        <p>Here is your carbon usage report for the week {start_date.date()} to {end_date.date()}:</p>
        <ul>
          <li>Total Energy Used: {total_energy} kWh</li>
          <li>Total Carbon Emitted: {total_carbon} kg CO2</li>
        </ul>
        <p>Keep up the efforts to reduce your carbon footprint!</p>
        """
        # Send the email to the user
        send_email(user.email, subject, content)

def schedule_jobs(app):
    """
    Configure and start the APScheduler to send weekly reports.
    """
    scheduler = BackgroundScheduler()
    # Define a job to run send_weekly_reports() within application context, every week
    def weekly_job():
        with app.app_context():
            send_weekly_reports()
    # Schedule the job to run every week (e.g., every Monday at 8:00 AM)
    scheduler.add_job(weekly_job, trigger="cron", day_of_week="mon", hour=8, minute=0, id="weekly_report")
    scheduler.start()
