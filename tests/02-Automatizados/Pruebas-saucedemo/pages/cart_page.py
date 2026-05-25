

from playwright.sync_api import expect

class CartPage:
    def __init__(self, page):
        self.page = page

    def verificar_producto_en_carrito(self, nombre_producto):
        expect(self.page.get_by_text(nombre_producto)).to_be_visible()

    def eliminar_producto_del_carrito(self, nombre_producto):
        self.page.locator(f"[data-test='remove-{nombre_producto}']").click()
        expect(self.page.get_by_text(nombre_producto)).not_to_be_visible()

    def boton_checkout(self):
        self.page.locator("[data-test='checkout']").click()
        expect(self.page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    def info_checkout(self, nombre, apellido, codigo_postal):
        self.page.locator("[data-test='firstName']").fill(nombre)
        self.page.locator("[data-test='lastName']").fill(apellido)
        self.page.locator("[data-test='postalCode']").fill(codigo_postal)
        self.page.locator("[data-test='continue']").click()
        expect(self.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    
    def finalizar_checkout(self):
        self.page.locator("[data-test='finish']").click()
        expect(self.page.get_by_text("THANK YOU FOR YOUR ORDER")).to_be_visible()
        self.page.locator("[data-test='back-to-products']").click()
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
    
    def continuar_comprando(self):
        self.page.locator("[data-test='continue-shopping']").click()
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")