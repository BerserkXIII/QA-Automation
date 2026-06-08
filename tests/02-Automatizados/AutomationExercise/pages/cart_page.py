

import pytest
import constants
from pages.checkout_page import CheckoutPage
from playwright.sync_api import expect

class CartPage:
    def __init__(self, page):
        self.page = page

    def verificar_cartpage(self):
        expect(self.page).to_have_url(constants.CART_URL)

    def verificar_producto_en_carrito(self, prods_agregados):
        for numero_prod in prods_agregados:
            expect(self.page.locator(f"#product-{numero_prod}")).to_be_visible()

    def borrar_producto(self, prods_agregados):
        for numero_prod in prods_agregados:
            self.page.locator(f"a.cart_quantity_delete[data-product-id='{numero_prod}']").click()

    def boton_checkout(self):
        self.page.get_by_text("Proceed To Checkout").click()
        return CheckoutPage(self.page)
    
    def comparar_precios(self, precios):
        for numero_prod, precio in precios.items():
            precio_carrito = self.page.locator(f"#product-{numero_prod} .cart_price p").inner_text()
            assert precio == precio_carrito, f"Producto {numero_prod}: esperado {precio}, encontrado {precio_carrito}"