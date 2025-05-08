import datetime
from threading import Thread
from flask import current_app, render_template, url_for
from database.tables import db, User, CarbonLog
from itsdangerous import BadSignature, SignatureExpired
from . import utils  # Import the utils module for token generation and email sending

def send_verification_email(user):
    # Generate a unique token for email verification
    token = utils.generate_token(user.id, salt='email-confirm')
    # Construct verification URL (absolute URL)
    verify_url = url_for('email_bp.verify_email', token=token, _external=True)
    # Render the email template with the verification link
    subject = "Please Verify Your Account"
    html_content = render_template('email/verification.html', user=user, verify_url=verify_url)
    # Send the email asynchronously in a new thread
    app = current_app._get_current_object()  # get the real app instance for thread usage
    thr = Thread(target=utils.send_async_email, args=(app, user.email, subject, html_content))
    thr.daemon = True   #The daemon thread is automatically terminated when the main thread exits (to avoid the program not exiting properly)
    thr.start()
def send_weekly_reports(app):
    with app.app_context():
        # Calculate the date range for the past week (last 7 days)
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)
        # Query all users from the database
        users = User.query.all()
        for user in users:
            # If the user has an opt-out flag for weekly reports, skip them
            if hasattr(user, "weekly_report") and not getattr(user, "weekly_report"):
                continue
            # Compute total energy and carbon for the user in the past week from CarbonLog data
            try:
                logs = CarbonLog.query.filter(
                    CarbonLog.user_id == user.id,
                    CarbonLog.date >= start_date,
                    CarbonLog.date < end_date
                ).all()
                total_energy = sum(log.energy_used for log in logs)
                total_carbon = sum(log.carbon_emitted for log in logs)
            except Exception as e:
                # In case of any error (e.g., database issue), use placeholder values
                total_energy = 0
                total_carbon = 0
            # Render the weekly report email template with the aggregated data
            subject = "Your Weekly Carbon Emission Report"
            html_content = render_template('email/report.html', user=user,
                                           total_energy=total_energy,
                                           total_carbon=total_carbon,
                                           start_date=start_date.date(),
                                           end_date=end_date.date())
            # Send the email (synchronously, since this code itself runs in a background job)
            utils.send_email(user.email, subject, html_content)

def start_scheduler(app):
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    # Schedule the weekly report job to run once every week (e.g., every Monday at 00:00)
    scheduler.add_job(func=send_weekly_reports, trigger="cron", day_of_week="mon", hour=0, minute=0, args=[app])
    scheduler.start()