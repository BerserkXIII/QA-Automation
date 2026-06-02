
import pytest
import constants
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.register_page import RegisterPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "es-ES"
    }

@pytest.fixture
def home_page(page):
    home = HomePage(page)
    home.ir_a_home()
    home.cerrar_pop_up()
    home.verificar_home()
    return home

@pytest.fixture
def login_page(page):
    login = LoginPage(page)
    login.verificar_login()
    return login

@pytest.fixture
def cart_page(page):
    cart = CartPage(page)
    cart.verificar_cartpage()
    return cart

@pytest.fixture
def new_user():
    return constants.crear_usuario_nuevo()

@pytest.fixture
def register_page(page):
    register = RegisterPage(page)
    register.verificar_registro()
    return register

@pytest.fixture
def logged_user(home_page):
    home_page.ir_a_login()
    login = LoginPage(home_page.page)
    login.login_correcto()
    return home_page

@pytest.fixture
def carrito_lleno(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    prods_agregados = [2, 3, 5, 7, 12, 15]
    products_page.agregar_producto_al_carrito(prods_agregados)
    cart_page = products_page.boton_cart()
    return cart_page, prods_agregados
