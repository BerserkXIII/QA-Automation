

import pytest
import re
from playwright.sync_api import expect


def test_login_correcto(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html") 

@pytest.mark.parametrize("username,password,error_message", [
    ("admin", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out.")
])

def test_login_erroneo(ini_page, username, password, error_message):
    expect(ini_page.page).to_have_url("https://www.saucedemo.com/")
    ini_page.hacer_login(username, password)
    ini_page.verificar_login_fallido(error_message)

def test_sidebar_items(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.sidebar_buttons("inventory")
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_sidebar_about(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.sidebar_buttons("about")
    expect(logged_page.page).to_have_url("https://saucelabs.com/")

def test_sidebar_reset(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.sidebar_buttons("reset")
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_sidebar_logout(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.sidebar_buttons("logout")
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/")

def test_un_item_en_carrito(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.agregar_producto_al_carrito("sauce-labs-backpack")
    logged_page.comprobar_producto_en_carrito(1)

def test_todos_items_en_carrito(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.agregar_producto_al_carrito("sauce-labs-backpack")
    logged_page.agregar_producto_al_carrito("sauce-labs-bike-light")
    logged_page.agregar_producto_al_carrito("sauce-labs-bolt-t-shirt")
    logged_page.agregar_producto_al_carrito("sauce-labs-fleece-jacket")
    logged_page.agregar_producto_al_carrito("sauce-labs-onesie")
    logged_page.agregar_producto_al_carrito("test.allthethings()-t-shirt-(red)")
    logged_page.comprobar_producto_en_carrito(6)

@pytest.mark.parametrize("filtro", [
    "lohi", "hilo" ])

def test_filtrar_precios(logged_page, filtro):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.filtro_precios(filtro)
    
@pytest.mark.parametrize("filtro", [
    "az", "za" ])

def test_filtrar_nombre(logged_page, filtro):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.filtro_nombre(filtro)

def test_checkout_completo(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.agregar_producto_al_carrito("sauce-labs-backpack")
    logged_page.agregar_producto_al_carrito("sauce-labs-bike-light")
    cart = logged_page.ir_al_carrito()
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/cart.html")
    cart.verificar_producto_en_carrito("sauce-labs-backpack")
    cart.verificar_producto_en_carrito("sauce-labs-bike-light")
    cart.eliminar_producto_del_carrito("sauce-labs-backpack")
    cart.boton_checkout()
    cart.info_checkout("Juan", "Perez", "12345")
    cart.finalizar_checkout()
    expect(logged_page.page.get_by_text("Products")).to_be_visible()

def test_continuar_comprando(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")
    logged_page.agregar_producto_al_carrito("sauce-labs-backpack")
    cart = logged_page.ir_al_carrito()
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/cart.html")
    cart.continuar_comprando()
    expect(logged_page.page.get_by_text("Products")).to_be_visible()