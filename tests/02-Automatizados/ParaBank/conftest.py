
import uuid
import pytest
import requests
import constants
import time
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


#Este fixture bloquea la carga de imágenes y fuentes para mejorar el rendimiento de las pruebas
# y asi evitar exceder el limite peticiones a ParaBank.
@pytest.fixture(autouse=True)
def bloquear_recursos(page):
    def manejar(route):
        if route.request.resource_type in ("image", "font"):
            route.abort()
        else:
            route.continue_()
    page.route("**/*", manejar)

@pytest.fixture(autouse=True)
def pausa_entre_tests():
    yield
    time.sleep(constants.PAUSA_ENTRE_TESTS)