

import pytest
import constants
from pages.products_page import ProductsPage
from playwright.sync_api import expect

class CartPage:
    def __init__(self, page):
        self.page = page

    def verificar_cartpage(self):
        expect(self.page).to_have_url(constants.CART_URL)

        def vaciar_carrito(self):
        self.page.get_by_role("link", name="View Cart").click()
        self.page.get_by_role("button", name="X").click()