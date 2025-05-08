import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app
from user.forms import RegistrationForm, LoginForm

"""Webpage Tests"""

@pytest.fixture()
def client():
    """A Test client for the app"""
    with app.test_client() as client:
        yield client

def test_login_load(client):
    """Test the login route loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_register_load(client):
    """Test the register route loads"""
    response = client.get('/register')
    assert response.status_code == 200

def test_logout_load(client):
    """Test the logout route loads, when user logged out"""
    response = client.get('/logout')
    assert response.status_code == 302

def test_profile_load(client):
    """Test the profile route loads, when user logged out"""
    response = client.get('/profile')
    assert response.status_code == 302

"""Form Tests"""

def test_register_form_valid():
    """Test the register form with valid data"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is True

def test_register_form_invalid_username():
    """Test the register form with invalid username"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test123!',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'username' in form.errors

def test_register_form_empty_username():
    """Test the register form with empty username"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': '',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'username' in form.errors

def test_register_form_short_username():
    """Test the register form with short username"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 't',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'username' in form.errors

def test_register_form_long_username():
    """Test the register form with long username"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'testtesttesttesttesttest',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'username' in form.errors

def test_register_form_invalid_email():
    """Test the register form with invalid email"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'email' in form.errors

def test_register_form_empty_email():
    """Test the register form with empty email"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': '',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'email' in form.errors

def test_register_form_invalid_firstname():
    """Test the register form with invalid firstname"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Te_st',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'firstname' in form.errors

def test_register_form_empty_firstname():
    """Test the register form with empty firstname"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': '',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'firstname' in form.errors

def test_register_form_invalid_lastname():
    """Test the register form with invalid lastname"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Te_st',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'lastname' in form.errors

def test_register_form_empty_lastname():
    """Test the register form with empty lastname"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': '',
                'password': 'Test123!',
                'confirm_password': 'Test123!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'lastname' in form.errors

def test_register_form_empty_password():
    """Test the register form with empty password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': '',
                'confirm_password': ''
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_short_password():
    """Test the register form with short password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Te1!',
                'confirm_password': 'Te1!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_long_password():
    """Test the register form with long password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'TestTestTestTest1!',
                'confirm_password': 'TestTestTestTest1!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_uppercase_password():
    """Test the register form with uppercase password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'TESTTEST1!',
                'confirm_password': 'TESTTEST1!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_lowercase_password():
    """Test the register form with lowercase password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'testtest1!',
                'confirm_password': 'testtest1!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_no_numbers_password():
    """Test the register form with no numbers password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Testtest!',
                'confirm_password': 'Testtest!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_no_spec_char_password():
    """Test the register form with no special character password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Testtest1',
                'confirm_password': 'Testtest1'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'password' in form.errors

def test_register_form_invalid_confirm_password():
    """Test the register form with invalid confirm_password"""
    with app.app_context():
        form = RegistrationForm(
            data={
                'username': 'test',
                'email': 'test@test.com',
                'firstname': 'Test',
                'lastname': 'Test',
                'password': 'Test123!',
                'confirm_password': 'Test123!!'
            },
            meta={'csrf': False}
        )
        assert form.validate() is False
        assert 'confirm_password' in form.errors

""" Login Form Test """

def test_login_valid():
    """Test the login form with valid data"""
    with app.app_context():
        with app.test_request_context():
            form = LoginForm(
                data={
                    'email': 'test@test.com',
                    'password': 'Test123!',
                    'recaptcha': "PASSED"
                },
                meta={'csrf': False}
            )
            form._fields.pop('recaptcha', None)
            assert form.validate() is True

def test_login_invalid():
    """Test the login form with invalid data"""
    with app.app_context():
        with app.test_request_context():
            form = LoginForm(
                data={
                    'email': 'test',
                    'password': 'Test123!',
                    'recaptcha': "PASSED"
                },
                meta={'csrf': False}
            )
            form._fields.pop('recaptcha', None)
            assert form.validate() is False
            assert 'email' in form.errors
