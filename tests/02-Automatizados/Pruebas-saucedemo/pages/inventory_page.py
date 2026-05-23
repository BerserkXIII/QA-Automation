

class InventoryPage:
    def __init__(self, page):
        self.page = page
    
    def agregar_producto_al_carrito(self, producto_id):
        self.page.locator(f"[data-test='add-to-cart-{producto_id}']").click()
    
    def ir_al_carrito(self):
        self.page.locator("[data-test='shopping-cart-link']").click()