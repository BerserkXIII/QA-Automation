

import pytest
import constants
import conftest as ct
from pages.cart_page import CartPage
from playwright.sync_api import expect
from urllib.parse import unquote

class ProductsPage:
    def __init__(self, page):
        self.page = page

    def verificar_productpage(self):
        expect(self.page).to_have_url(constants.PRODUCTS_URL)

    def agregar_producto_al_carrito(self, productos_agregados):
        for numero_prod in productos_agregados:
            self.page.locator(f".productinfo [data-product-id='{numero_prod}']").click()
            self.page.get_by_role("button", name="Continue Shopping").click()

    def hover_producto(self, productos_agregados):
        for numero_prod in productos_agregados:
            self.page.locator(f".productinfo [data-product-id='{numero_prod}']").first.hover()
            self.page.locator(f".product-overlay [data-product-id='{numero_prod}']").click()
            self.page.get_by_role("button", name="Continue Shopping").click()

    def boton_cart(self):
        self.page.get_by_role("link", name=" Cart").click()
        return CartPage(self.page)
    
    def precio_producto(self, productos_agregados):
        precios = {}
        for numero_prod in productos_agregados:
            precio = self.page.locator(f".overlay-content:has(a[data-product-id='{numero_prod}']) h2").inner_text()
            precios[numero_prod] = precio
        return precios
    
    def verificar_categorias(self):
        paneles = ["Women", "Men", "Kids"]
        for panel in paneles:
            self.page.locator(f"a[href='#{panel}']").click()
            links = self.page.locator(f"#{panel} .panel-body a").all()
            for link in links:
                url_relativa = link.get_attribute("href")
                link.click()
                expect(self.page).to_have_url(f"{constants.HOME_URL.rstrip('/')}{url_relativa}")
                self.page.go_back()
                self.page.locator(f"a[href='#{panel}']").click()


    def verificar_brands(self):
        links = self.page.locator(".brands-name a").all()
        for link in links:
            url_relativa = link.get_attribute("href")
            link.click()
            url_actual = unquote(self.page.url)
            url_esperada = f"{constants.HOME_URL.rstrip('/')}{url_relativa}"
            assert url_actual == url_esperada, f"URL incorrecta: {url_actual}"
            self.page.go_back()
    
    def view_product(self, numero_prod):
        self.page.locator(f"a[href='/product_details/{numero_prod}']").click()
        expect(self.page).to_have_url(f"{constants.HOME_URL}product_details/{numero_prod}")
        try:
            self.page.locator("#dismiss-button-element").click(timeout=2000)
        except:
            pass
        
    def escribir_review(self):
        self.page.get_by_role("textbox", name="Your Name").fill(constants.VALID_USER["first_name"])
        self.page.get_by_role("textbox", name="Email Address", exact=True).fill(constants.VALID_USER["email"])
        self.page.get_by_role("textbox", name="Add Review Here!").fill("Excelente producto, muy recomendable!")
        self.page.get_by_role("button", name="submit").click()
        expect(self.page.locator(".alert-success").first).to_be_visible()
        expect(self.page.get_by_text("Thank you for your review.")).to_be_visible()
        self.page.go_back()
        try:
            self.page.locator("#dismiss-button-element").click(timeout=2000)
        except:
            pass
