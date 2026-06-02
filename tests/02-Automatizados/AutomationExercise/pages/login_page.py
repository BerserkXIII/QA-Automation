

import pytest
import constants
from pages.register_page import RegisterPage
from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page

    def registro(self, new_user):
        self.page.locator("[data-qa='signup-name']").fill(new_user["first_name"])
        self.page.locator("[data-qa='signup-email']").fill(new_user["email"])
        self.page.locator("[data-qa='signup-button']").click()
        return RegisterPage(self.page)
    
    def registro_usuario_existente(self):
        self.page.locator("[data-qa='signup-name']").fill(constants.VALID_USER["first_name"])
        self.page.locator("[data-qa='signup-email']").fill(constants.VALID_USER["email"])
        self.page.locator("[data-qa='signup-button']").click()

    def verificar_login(self):
        expect(self.page).to_have_url(constants.LOGIN_URL)
    
    def login_correcto(self):
        expect(self.page).to_have_url(constants.LOGIN_URL)
        self.page.locator("[data-qa='login-email']").fill(constants.VALID_USER["email"])
        self.page.locator("[data-qa='login-password']").fill(constants.VALID_USER["password"])
        self.page.locator("[data-qa='login-button']").click()

    def login_incorrecto(self):
        expect(self.page).to_have_url(constants.LOGIN_URL)
        self.page.locator("[data-qa='login-email']").fill(constants.INVALID_USER["email"])
        self.page.locator("[data-qa='login-password']").fill(constants.INVALID_USER["password"])
        self.page.locator("[data-qa='login-button']").click()

    