from http.client import responses

import pytest
from app import app
from data_entry.forms import TypeForm, TransportForm, ApplianceForm

@pytest.fixture()

def client():
    with app.test_client() as client:
        yield client

def test_type_form_load(client):
    response = client.get('/form')
    assert response.status_code == 200

def test_appliance_form(client):
    response = client.get('/appliance')
    assert response.status_code == 200

def test_transport_form(client):
    response = client.get('/transport')
    assert response.status_code == 200

def test_type_form_valid(client):
    form=TypeForm(
        data={'type': 'Appliance'},
        meta={'csrf': False}
    )
    assert form.validate() is True
