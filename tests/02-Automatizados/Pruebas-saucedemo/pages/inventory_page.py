

import re
from playwright.sync_api import expect
from pages.cart_page import CartPage

class InventoryPage:
    def __init__(self, page):
        self.page = page
    
    def agregar_producto_al_carrito(self, producto_id):
        self.page.locator(f"[data-test='add-to-cart-{producto_id}']").click()
    
    def ir_al_carrito(self):
        self.page.locator("[data-test='shopping-cart-link']").click()
        return CartPage(self.page)

    def sidebar_buttons(self, button_id):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator(f"#{button_id}_sidebar_link").click()

    def comprobar_producto_en_carrito(self, numero_productos):
        self.cart_badge = self.page.locator("[data-test='shopping-cart-badge']")
        expect(self.cart_badge).to_have_text(str(numero_productos))

    def filtro_precios(self, filtro):
        self.page.locator("[data-test='product-sort-container']").select_option(filtro)
        elementos = self.page.locator(".inventory_item_price")
        textos = elementos.all_text_contents()
        precios = [float(re.sub(r'[^\d.]', '', t)) for t in textos if t]        
        orden = {
            "lohi": sorted(precios),
            "hilo": sorted(precios, reverse=True)}        
        assert precios == orden[filtro]

    def filtro_nombre(self, filtro):
        self.page.locator("[data-test='product-sort-container']").select_option(filtro)
        elementos = self.page.locator(".inventory_item_name")
        textos = elementos.all_text_contents()        
        orden = {
            "az": sorted(textos),
            "za": sorted(textos, reverse=True)}        
        assert textos == orden[filtro]