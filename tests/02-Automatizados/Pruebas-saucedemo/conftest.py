
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def ini_page(page):
    login = LoginPage(page)
    login.ir_a_login()
    return login

@pytest.fixture
def logged_page(page):
    login = LoginPage(page)
    login.ir_a_login()
    login.hacer_login("standard_user", "secret_sauce")
    login.verificar_login_exitoso()
    return InventoryPage(page)


    

