
import uuid
import pytest
import requests
import constants
from pages.home_page import *
from pages.register_page import *



@pytest.fixture
def home_page(page):
    home = HomePage(page)
    home.ir_a_home()
    return home

@pytest.fixture
def register_page(page):
    register = RegisterPage(page)
    register.ir_a_register()
    return register

@pytest.fixture
def datos_usuario_nuevo():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Test Street",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "phone": "1234567890",
        "ssn": "123-45-6789",
        "username": f"jdoe{uuid.uuid4().hex[:8]}",
        "password": "Password123",
        "repeated_password": "Password123"
    }

@pytest.fixture
def crear_usuario_nuevo(page, datos_usuario_nuevo):
    home = HomePage(page)
    home.ir_a_home()
    home.ir_a_register()
    register = RegisterPage(page)
    register.rellenar_formulario_registro(datos_usuario_nuevo)

@pytest.fixture
def GET_user_data(crear_usuario_nuevo, datos_usuario_nuevo):
    response = requests.get(f"{constants.API_BASE_URL}/login/{datos_usuario_nuevo['username']}/{datos_usuario_nuevo['password']}", 
                            headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Login falló: {response.status_code} — {response.text}"
    user_data = response.json()
    return user_data

@pytest.fixture
def GET_accountID(GET_user_data):
    response = requests.get(f"{constants.API_BASE_URL}/customers/{GET_user_data['id']}/accounts", 
                            headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Login falló: {response.status_code} — {response.text}"
    account_data = response.json()
    return account_data

