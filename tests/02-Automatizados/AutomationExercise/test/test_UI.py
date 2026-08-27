

import constants
import pytest
import allure
from playwright.sync_api import expect



@allure.feature("Registro y Login")
@allure.story("Registro de usuario")
def test_registrar_usuario(home_page, new_user):
    login = home_page.boton_login()
    register_page = login.registro(new_user)
    register_page.completar_formulario_registro(new_user)
    register_page.cerrar_pop_up1()
    home_page.verificar_home()

@allure.feature("Registro y Login")
@allure.story("Registro de usuario existente")
def test_registrar_usuario_existente(home_page):
    login = home_page.boton_login()
    login.registro_usuario_existente()
    expect(login.page.locator("#form")).to_contain_text("Email Address already exist!")


@allure.feature("Registro y Login")
@allure.story("Login correcto de usuario")
def test_login_correcto(home_page):
    login = home_page.boton_login()
    login.login_correcto()
    home_page.verificar_home()
    home_page.verificar_usuario_logueado()
    
@allure.feature("Registro y Login")
@allure.story("Login incorrecto de usuario")
def test_login_incorrecto(home_page):
    login = home_page.boton_login()
    login.login_incorrecto()
    expect(login.page.locator("#form")).to_be_visible()


@allure.feature("Registro y Login")
@allure.story("Logout de usuario")
def test_logout(home_page, logged_user):
    expect(logged_user.page.get_by_role("link", name="Logout")).to_be_visible()
    logged_user.page.get_by_role("link", name="Logout").click()
    expect(logged_user.page).to_have_url("https://automationexercise.com/login")

 
@allure.feature("Carrito de compras")
@allure.story("Agregar producto al carrito")
def test_agregar_producto_carrito(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    prods_agregados = [1, 6]
    products_page.agregar_producto_al_carrito(prods_agregados)
    cart_page = products_page.boton_cart()
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)

@allure.feature("Carrito de compras")
@allure.story("Agregar producto al carrito con hover")
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

@allure.feature("Carrito de compras")
@allure.story("Borrar producto del carrito")
def test_borrar_producto_del_carrito(carrito_lleno):
    cart_page, prods_agregados = carrito_lleno
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)
    cart_page.borrar_producto(prods_agregados)
    expect(cart_page.page.locator("#empty_cart")).to_contain_text("Cart is empty!")

@allure.feature("Carrito de compras")
@allure.story("Realizar checkout completo")
def test_checkout_completo(carrito_lleno):
    cart_page, prods_agregados = carrito_lleno
    cart_page.verificar_cartpage()
    cart_page.verificar_producto_en_carrito(prods_agregados)
    checkout_page = cart_page.boton_checkout()
    checkout_page.verificar_checkoutpage()
    checkout_page.boton_place_order()
    checkout_page.completar_formulario_checkout()
    checkout_page.verificar_orden_completada()

@allure.feature("Productos")
@allure.story("Verificar categorías y marcas")
def test_verificar_categorias(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    products_page.verificar_categorias()
    products_page.verificar_brands()


# NOTA: Test marcado como flaky de forma consciente.
# Causa raíz: Google sirve el popup "google_vignette" en un iframe (aswift_*)
# con contenido/timing no determinista — varía entre ejecuciones y no se puede
# interceptar de forma 100% fiable (bloqueo de red parcial, add_locator_handler
# no se dispara sin acciones, timing random). Se documenta y mitiga con reruns
# en vez de perseguir un fix imposible contra un sistema de terceros.
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@allure.feature("Productos")
@allure.story("Escribir review de producto")
def test_escribir_review_producto(logged_user):
    logged_user.verificar_usuario_logueado()
    products_page = logged_user.boton_productos()
    products_page.verificar_productpage()
    numero_prod = [1, 6, 15]
    for numero in numero_prod:
        products_page.view_product(numero)
        products_page.escribir_review()


@allure.feature("Funciones extra")
@allure.story("Suscripción a newsletter")
def test_suscripcion(home_page):
    home_page.suscribirse()
    expect(home_page.page.locator("#success-subscribe")).to_be_visible()


@allure.feature("Funciones extra")
@allure.story("Boton scroll to top")
def test_scroll_button(home_page):
    home_page.scroll_button()
    posicion = home_page.page.evaluate("window.scrollY")
    assert posicion == 0