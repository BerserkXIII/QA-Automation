

import pytest
import constants
from playwright.sync_api import expect

class RegisterPage:
    def __init__(self, page):
        self.page = page

    def ir_a_register(self):
        self.page.goto(constants.REGISTER_URL)

    def rellenar_formulario_registro(self, user_nuevo):
        self.page.locator("[id=\"customer.firstName\"]").fill(user_nuevo["first_name"])
        self.page.locator("[id=\"customer.lastName\"]").fill(user_nuevo["last_name"])
        self.page.locator("[id=\"customer.address.street\"]").fill(user_nuevo["address"])
        self.page.locator("[id=\"customer.address.city\"]").fill(user_nuevo["city"])
        self.page.locator("[id=\"customer.address.state\"]").fill(user_nuevo["state"])
        self.page.locator("[id=\"customer.address.zipCode\"]").fill(user_nuevo["zip_code"])
        self.page.locator("[id=\"customer.phoneNumber\"]").fill(user_nuevo["phone"])
        self.page.locator("[id=\"customer.ssn\"]").fill(user_nuevo["ssn"])
        self.page.locator("[id=\"customer.username\"]").fill(user_nuevo["username"])
        self.page.locator("[id=\"customer.password\"]").fill(user_nuevo["password"])
        self.page.locator("[id=\"repeatedPassword\"]").fill(user_nuevo["repeated_password"])
        self.page.get_by_role("button", name="Register").click()
