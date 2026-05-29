

import pytest
import constants
from pages.register_page import RegisterPage
from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page

    def ir_a_login(self):
        self.page.goto(constants.LOGIN_URL)

    def ir_a_registro(self, user):
        print(f"\n=== URL al registrar: {self.page.url} ===\n")
        self.page.locator("[data-qa='signup-name']").fill(user["first_name"])
        self.page.locator("[data-qa='signup-email']").fill(user["email"])
        self.page.locator("[data-qa='signup-button']").click()
        return RegisterPage(self.page)

    def verificar_login(self):
        expect(self.page).to_have_url(constants.LOGIN_URL)
    
    def login_correcto(self):
        expect(self.page).to_have_url(constants.LOGIN_URL)
        self.page.locator("[data-qa='login-email']").fill(constants.VALID_USER["email"])
        self.page.locator("[data-qa='login-password']").fill(constants.VALID_USER["password"])
        self.page.locator("[data-qa='login-button']").click()