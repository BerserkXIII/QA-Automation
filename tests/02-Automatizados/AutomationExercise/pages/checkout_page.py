
import pytest
import constants
from playwright.sync_api import expect


class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def verificar_checkoutpage(self):
        expect(self.page).to_have_url(constants.CHECKOUT_URL)

    def boton_place_order(self):
        self.page.get_by_role("link", name="Place Order").click()
        expect(self.page).to_have_url("https://automationexercise.com/payment")

    def completar_formulario_checkout(self):
        self.page.locator("[data-qa='name-on-card']").fill(f"{constants.VALID_USER['first_name']} {constants.VALID_USER['last_name']}")
        self.page.locator("[data-qa='card-number']").fill(f"9012 3456")
        self.page.locator("[data-qa='cvc']").fill("123")
        self.page.locator("[data-qa='expiry-month']").fill("12")
        self.page.locator("[data-qa='expiry-year']").fill("2027")
        self.page.get_by_role("button", name="Pay and Confirm Order").click()

    def verificar_orden_completada(self):
        expect(self.page.get_by_text("Congratulations! Your order")).to_be_visible()
        self.page.get_by_role("link", name="Continue").click()
