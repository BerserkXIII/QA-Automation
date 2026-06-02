

import pytest
import constants
from playwright.sync_api import expect

class ProductsPage:
    def __init__(self, page):
        self.page = page

    def verificar_productpage(self):
        expect(self.page).to_have_url(constants.PRODUCTS_URL)

    def agregar_producto_al_carrito(self, numero_prod):
        self.page.locator(f".productinfo [data-product-id='{numero_prod}']").click()
    
