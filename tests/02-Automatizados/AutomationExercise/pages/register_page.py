
import pytest
import constants
from playwright.sync_api import expect


class RegisterPage:
    def __init__(self, page):
        self.page = page

    def verificar_registro(self):
        expect(self.page).to_have_url(constants.REGISTER_URL)

    def completar_formulario_registro(self, user):
        self.page.get_by_role("radio", name="Mr.").check()
        self.page.get_by_role("textbox", name="Password *").fill(user["password"])
        self.page.locator("#days").select_option(user["day"])
        self.page.locator("#months").select_option(user["month"])
        self.page.locator("#years").select_option(user["year"])
        self.page.get_by_role("textbox", name="First name *").fill(user["first_name"])
        self.page.get_by_role("textbox", name="Last name *").fill(user["last_name"])
        self.page.get_by_role("textbox", name="Address * (Street address, P.").fill(user["address"])
        self.page.get_by_label("Country *").select_option(user["country"])
        self.page.get_by_role("textbox", name="State *").fill(user["state"])
        self.page.get_by_role("textbox", name="City * Zipcode *").fill(user["city"])
        self.page.locator("#zipcode").fill(user["zipcode"])
        self.page.get_by_role("textbox", name="Mobile Number *").fill(user["phone"])
        self.page.get_by_role("button", name="Create Account").click()
        expect(self.page).to_have_url("https://automationexercise.com/account_created")
        self.page.locator("[data-qa='continue-button']").click()

    def cerrar_pop_up1(self):
        try:
            iframe = self.page.frame_locator("iframe[name^='aswift_']")
            boton = iframe.get_by_role("button", name="Close ad")
            boton.wait_for(state="visible", timeout=5000)
            boton.click()
        except:
            pass
    