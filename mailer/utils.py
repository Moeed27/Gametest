import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app, url_for
# If using SendGrid's official library:
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except ImportError:
    SendGridAPIClient = None
    Mail = None
import logging

def generate_confirmation_token(email):
    """
    Generate a timed confirmation token for the given email.
    Uses application's secret key and a salt for security.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    """
    Attempt to decode and verify a confirmation token.
    Returns the email if token is valid and not expired, otherwise None.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except SignatureExpired:
        # Token is valid but expired
        return None
    except BadSignature:
        # Token is invalid (tampered or wrong secret)
        return None
    return email

def send_email(to_email, subject, content):
    """
    Send an email using SendGrid. Requires SENDGRID_API_KEY and FROM_EMAIL (or SENDGRID_FROM_EMAIL) in env.
    """
    api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('FROM_EMAIL') or os.environ.get('SENDGRID_FROM_EMAIL')
    if not api_key or not from_email:
        logging.error("SendGrid API key or sender email not configured.")
        return False

    if SendGridAPIClient and Mail:
        # Using SendGrid official client if available
        try:
            sg = SendGridAPIClient(api_key)
            email = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
            sg.send(email)  # send the email (response status can be checked if needed)
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False
    else:
        # Fallback: send via HTTP POST to SendGrid API (if official client is not installed)
        import requests
        try:
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                json={
                    "personalizations": [{"to": [{"email": to_email}]}],
                    "from": {"email": from_email},
                    "subject": subject,
                    "content": [{"type": "text/html", "value": content}]
                },
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            )
            if 200 <= response.status_code < 300:
                return True  # Accepted by SendGrid
            else:
                logging.error(f"SendGrid API error {response.status_code}: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Exception during SendGrid API call: {e}")
            return False

def send_verification_email(user):
    """
    Generate a verification token for the user and send a confirmation email.
    """
    token = generate_confirmation_token(user.email)
    # Construct verification URL (external absolute URL for the link)
    verify_url = url_for('email_bp.verify_email', token=token, _external=True)
    subject = "Carbon Cruncher - Verify Your Email"
    content = f"""
    <p>Hello {user.name},</p>
    <p>Thank you for registering on Carbon Cruncher. Please click the link below to verify your email address:</p>
    <p><a href="{verify_url}">Verify Email</a></p>
    <p>If you did not sign up for Carbon Cruncher, please ignore this email.</p>
    """
    # Send the email (you could also log the verify_url for debugging)
    return send_email(user.email, subject, content)
##TODO: Register sendgird and use the API
