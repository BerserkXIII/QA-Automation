

from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page
        
    def ir_a_login(self):
        self.page.goto("https://www.saucedemo.com/")
    
    def hacer_login(self, usuario, contraseña):
        self.page.locator("[data-test='username']").fill(usuario)
        self.page.locator("[data-test='password']").fill(contraseña)
        self.page.locator("[data-test='login-button']").click()
    
    def verificar_login_exitoso(self):
        expect(self.page.get_by_text("Products")).to_be_visible()

    def verificar_login_fallido(self, mensaje_esperado):
        expect(self.page.locator("[data-test='error']")).to_have_text(mensaje_esperado)