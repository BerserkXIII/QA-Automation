

import pytest
import re
from playwright.sync_api import expect


def test_login_correcto(logged_page):
    expect(logged_page.page.get_by_text("Products")).to_be_visible()

def test_login_incorrecto(ini_page):
    expect(ini_page.page.get_by_text("Swag Labs")).to_be_visible()
    ini_page.hacer_login("admin", "admin")
    ini_page.verificar_login_fallido("Epic sadface: Username and password do not match any user in this service")


def test_usuario_bloqueado(ini_page):
    expect(ini_page.page.get_by_text("Swag Labs")).to_be_visible()
    ini_page.hacer_login("locked_out_user", "secret_sauce")
    ini_page.verificar_login_fallido("Epic sadface: Sorry, this user has been locked out.")