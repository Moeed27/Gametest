from dotenv import load_dotenv
from database.dbconfig import Database
from flask import Flask
from argon2 import PasswordHasher
from logconfig import logger
import os, atexit
from flask_qrcode import QRcode

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
logger.debug("app starting")

# QR Code Setup
qr = QRcode(app)

# RECAPTCHA CONFIG
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# Database Setup
tunnel = Database.start_tunnel()
atexit.register(Database.stop_tunnel,tunnel)
db = Database.setup(app, tunnel)
ph = PasswordHasher()

app.config['EMAIL_SENDER']          = os.getenv('EMAIL_SENDER')
app.config['EMAIL_DEBUG']           = os.getenv('EMAIL_DEBUG', 'False').lower() == 'true'
app.config['SENDGRID_API_KEY']      = os.getenv('SENDGRID_API_KEY')
app.config['SMTP_SERVER']           = os.getenv('SMTP_SERVER')
app.config['SMTP_PORT']             = int(os.getenv('SMTP_PORT', 587))
app.config['SMTP_USERNAME']         = os.getenv('SMTP_USERNAME')
app.config['SMTP_PASSWORD']         = os.getenv('SMTP_PASSWORD')
app.config['SMTP_USE_TLS']          = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
app.config['EMAIL_CONFIRM_EXPIRES'] = int(os.getenv('EMAIL_CONFIRM_EXPIRES', 86400))
app.config['RESET_TOKEN_EXPIRES']   = int(os.getenv('RESET_TOKEN_EXPIRES', 7200))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY']  = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')


#from app_email import init_app as init_email_module
#init_email_module(app)

