
import pytest
import constants
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from playwright.sync_api import expect

class HomePage:
    def __init__(self, page):
        self.page = page

    def ir_a_home(self):
        self.page.goto(constants.HOME_URL) 

    def ir_a_login(self):
        self.page.goto(constants.LOGIN_URL)       
        
    def verificar_home(self):
        expect(self.page).to_have_url(constants.HOME_URL)

    def verificar_usuario_logueado(self):
        expect(self.page.get_by_text(f"Logged in as {constants.VALID_USER['first_name']} {constants.VALID_USER['last_name']}")).to_be_visible()

    def cerrar_pop_up(self):
        for name in ["Consentir"]:
            boton = self.page.get_by_role("button", name=name)
            try:
                boton.wait_for(state="visible", timeout=3000)
                boton.click()
                return
            except:
                continue

    def boton_login(self):
        self.page.get_by_role("link", name="Signup / Login").click()
        return LoginPage(self.page)
    
    def boton_productos(self):
        self.page.get_by_role("link", name="Products").click()
        return ProductsPage(self.page)
    
