
import pytest
import constants
import allure
import requests
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.register_page import RegisterPage


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "es-ES"
    }

@pytest.fixture()
def attach_screenshot(page, request):
    yield
    if request.node.rep_call.failed:
        print(">>> INTENTANDO SCREENSHOT")
        try:
            allure.attach(
                page.screenshot(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print(">>> SCREENSHOT OK")
        except Exception as e:
            print(f">>> SCREENSHOT FALLÓ: {e}")


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

@pytest.fixture(autouse=True)
def setup_ads(page):
    ad_patterns = [
        "**/*googlesyndication*",
        "**/*doubleclick*",
        "**/*googleadservices*",
        "**/*googletagservices*",
        "**/*adtrafficquality*",
        "**/pagead/**",
        "**/*google_vignette*",
    ]
    for pattern in ad_patterns:
        page.route(pattern, lambda route: route.abort())

    page.on("request", lambda req: print(f"[REQ] {req.url}") if "google" in req.url or "doubleclick" in req.url or "ad" in req.url.lower() else None)


@pytest.fixture
def api_headers():
    return {"Content-Type": "application/x-www-form-urlencoded"}


@pytest.fixture
def usuario_temporal(api_headers):
    payload = {"name": "Test User", "email":f"{constants.crear_usuario_nuevo()['email']}", "password": "password", 
               "title": "Mr", "birth_date": "1", "birth_month": "1", "birth_year": "1990", 
               "firstname": "Test", "lastname": "User", "company": "Test Company", "address1": "123 Test St", "address2": "",
                "country": "United States", "zipcode": "12345", "state": "CA", "city": "Test City", "mobile_number": "1234567890"}
    response = requests.post(f"{constants.API_BASE_URL}/createAccount", data=payload, timeout=10)
    yield payload
    requests.delete(f"{constants.API_BASE_URL}/deleteAccount", data={"email": payload["email"], "password": payload["password"]}, headers=api_headers, timeout=10)