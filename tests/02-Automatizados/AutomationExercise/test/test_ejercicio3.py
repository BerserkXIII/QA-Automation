

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
    
def test_agregar_producto_carrito(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    prods_agregados = [1, 6]
    products_page.agregar_producto_al_carrito(prods_agregados)
    cart_page = products_page.boton_cart()
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)

def test_agregar_producto_carrito_hover(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    prods_agregados = [1, 6]
    products_page.hover_producto(prods_agregados)
    precios = products_page.precio_producto(prods_agregados)
    cart_page = products_page.boton_cart()
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)
    cart_page.comparar_precios(precios)
    
def test_borrar_producto_del_carrito(carrito_lleno):
    cart_page, prods_agregados = carrito_lleno
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)
    cart_page.borrar_producto(prods_agregados)
    expect(cart_page.page.locator("#empty_cart")).to_contain_text("Cart is empty!")

def test_checkout_completo(carrito_lleno):
    cart_page, prods_agregados = carrito_lleno
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)
    checkout_page = cart_page.boton_checkout()
    checkout_page.verificar_checkoutpage()
    checkout_page.boton_place_order()
    checkout_page.completar_formulario_checkout()
    checkout_page.verificar_orden_completada()

def test_verificar_categorias(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    products_page.verificar_categorias()
    products_page.verificar_brands()