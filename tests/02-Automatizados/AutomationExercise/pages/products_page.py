

import pytest
import constants
from pages.cart_page import CartPage
from playwright.sync_api import expect

class ProductsPage:
    def __init__(self, page):
        self.page = page

    def verificar_productpage(self):
        expect(self.page).to_have_url(constants.PRODUCTS_URL)

    def agregar_producto_al_carrito(self, productos_agregados):
        for numero_prod in productos_agregados:
            self.page.locator(f".productinfo [data-product-id='{numero_prod}']").click()
            self.page.get_by_role("button", name="Continue Shopping").click()

    def boton_cart(self):
        self.page.get_by_role("link", name=" Cart").click()
        return CartPage(self.page)
    
