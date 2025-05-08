import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

try:
    # Import SendGrid client if available
    import sendgrid
    from sendgrid.helpers.mail import Mail
except ImportError:
    sendgrid = None
import logging

def generate_token(data, salt):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data, salt=salt)

def confirm_token(token, salt, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    data = serializer.loads(token, salt=salt, max_age=expiration)
    return data

def send_async_email(app, to_email, subject, html_content):
    with app.app_context():
        send_email(to_email, subject, html_content)

def send_email(to_email, subject, html_content):
    sender = current_app.config.get('EMAIL_SENDER', 'no-reply@example.com')
    debug_mode = current_app.config.get('EMAIL_DEBUG', False)
    sendgrid_api_key = current_app.config.get('SENDGRID_API_KEY')
    smtp_server = current_app.config.get('SMTP_SERVER')
    smtp_port = current_app.config.get('SMTP_PORT', 587)
    smtp_username = current_app.config.get('SMTP_USERNAME')
    smtp_password = current_app.config.get('SMTP_PASSWORD')
    smtp_use_tls = current_app.config.get('SMTP_USE_TLS', True)

    # Choose sending method
    if sendgrid_api_key and not debug_mode:
        # Use SendGrid's API to send email
        if sendgrid:
            try:
                sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
                email = Mail(from_email=sender, to_emails=to_email, subject=subject, html_content=html_content)
                response = sg.send(email)
                # (Optional) log success or response status
                current_app.logger.info(f"Sent email to {to_email} via SendGrid. Status code: {response.status_code}")
            except Exception as e:
                # Log any error in sending
                current_app.logger.error(f"Failed to send email via SendGrid: {e}")
        else:
            # If sendgrid library is not installed
            current_app.logger.error("SendGrid API key provided, but sendgrid library is not installed.")
    elif smtp_server:
        # Use SMTP server to send email
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to_email
            # Attach the HTML content (could also add a text version if needed)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            # Connect to SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            # Secure the connection with TLS if enabled
            if smtp_use_tls:
                server.starttls()
            if smtp_username:
                server.login(smtp_username, smtp_password)
            server.sendmail(sender, [to_email], msg.as_string())
            server.quit()
            current_app.logger.info(f"Sent email to {to_email} via SMTP ({smtp_server}:{smtp_port}).")
        except Exception as e:
            current_app.logger.error(f"Failed to send email via SMTP: {e}")
    else:
        # No email service configured or in debug mode without SMTP server: just log the email content
        print(f"[DEBUG] Email to {to_email} with subject '{subject}':\n{html_content}\n")
        current_app.logger.info(f"[DEBUG] Email content (to {to_email}) not sent (debug mode).")