

import pytest
from playwright.sync_api import expect



def test_registrar_usuario(home_page, new_user):
    login = home_page.boton_login()
    register_page = login.registro(new_user)
    register_page.completar_formulario_registro(new_user)
    register_page.cerrar_pop_up1()
    home_page.verificar_home()

def test_registrar_usuario_existente(home_page):
    login = home_page.boton_login()
    login.registro_usuario_existente()
    expect(login.page.locator("#form")).to_contain_text("Email Address already exist!")


def test_login_correcto(home_page):
    login = home_page.boton_login()
    login.login_correcto()
    home_page.verificar_home()
    home_page.verificar_usuario_logueado()

def test_login_incorrecto(home_page):
    login = home_page.boton_login()
    login.login_incorrecto()
    expect(login.page.locator("#form")).to_be_visible()

def test_logout(home_page, logged_user):
    expect(logged_user.page.get_by_role("link", name="Logout")).to_be_visible()
    logged_user.page.get_by_role("link", name="Logout").click()
    expect(logged_user.page).to_have_url("https://automationexercise.com/login")
    
def test_agregar_producto_al_carrito(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    products_page.agregar_producto_al_carrito(1)
    products_page.agregar_producto_al_carrito(6)


    