
"""
Test de cantidad en carrito → añadir dos productos distintos y verificar que el contador muestra 2"""

"""import pytest, re
from playwright.sync_api import Page, expect


def test_login_correcto(logged_page: Page):
    expect(logged_page.get_by_text("Swag Labs")).to_be_visible()
    expect(logged_page.get_by_text("Products")).to_be_visible()


def test_login_incorrecto(page: Page):
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_text("Swag Labs")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("admin")
    page.locator("[data-test=\"password\"]").fill("admin")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test='error']")).to_have_text(
    "Epic sadface: Username and password do not match any user in this service")    


def test_item_en_carrito(logged_page: Page):
    expect(logged_page.get_by_text("Swag Labs")).to_be_visible()
    expect(logged_page.get_by_text("Products")).to_be_visible()
    logged_page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    logged_page.locator("[data-test=\"shopping-cart-link\"]").click()
    expect(logged_page.locator("[data-test=\"title\"]")).to_be_visible()
    expect(logged_page.get_by_text("Sauce Labs Backpack")).to_be_visible()


def test_logout(logged_page: Page):
    expect(logged_page.get_by_text("Swag Labs")).to_be_visible()
    expect(logged_page.get_by_text("Products")).to_be_visible()
    logged_page.locator("#react-burger-menu-btn").click()
    logged_page.locator("#logout_sidebar_link").click()
    expect(logged_page).to_have_url("https://www.saucedemo.com/")
    expect(logged_page.locator("[data-test='login-button']")).to_be_visible()


def test_checkout_completo(logged_page: Page):
    logged_page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(logged_page.locator("[data-test=\"shopping-cart-link\"]")).to_be_visible()
    logged_page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()
    expect(logged_page.locator("[data-test=\"shopping-cart-link\"]")).to_be_visible()
    logged_page.locator("[data-test=\"shopping-cart-link\"]").click()
    logged_page.locator("[data-test=\"remove-sauce-labs-bike-light\"]").click()
    expect(logged_page.get_by_text("Sauce Labs Bike Light")).not_to_be_visible()
    logged_page.locator("[data-test=\"checkout\"]").click()
    logged_page.locator("[data-test=\"firstName\"]").fill("standard")
    logged_page.locator("[data-test=\"lastName\"]").fill("user")
    logged_page.locator("[data-test=\"postalCode\"]").fill("12345")
    expect(logged_page.locator("[data-test=\"continue\"]")).to_be_visible()
    logged_page.locator("[data-test=\"continue\"]").click()
    expect(logged_page.locator("[data-test=\"finish\"]")).to_be_visible()
    logged_page.locator("[data-test=\"finish\"]").click()
    expect(logged_page.locator("[data-test=\"back-to-products\"]")).to_be_visible()
    logged_page.locator("[data-test=\"back-to-products\"]").click()
    expect(logged_page.locator("[data-test=\"title\"]")).to_be_visible()

def test_filtro_precio(logged_page: Page):
    logged_page.locator("[data-test=\"product-sort-container\"]").select_option("lohi")
    # 1. Localiza los elementos de precio 
    precios_elementos = logged_page.locator(".inventory_item_price") 
    
    # 2. Extrae el texto y limpia los caracteres extra (como el símbolo de moneda)
    # y convierte el texto a tipo float
    textos_precios = precios_elementos.all_text_contents()
    precios_numericos = []
    for texto in textos_precios:
        # Extrae solo los dígitos y el punto decimal
        numero_limpio = re.sub(r'[^\d.]', '', texto)
        if numero_limpio:
            precios_numericos.append(float(numero_limpio))
            
    # 3. Crea una copia ordenada de la lista de precios
    precios_ordenados = sorted(precios_numericos)

    # 4. Verifica si la lista original es idéntica a la ordenada
    assert precios_numericos == precios_ordenados


def test_usuario_bloqueado(page: Page):
    page.goto("https://www.saucedemo.com/")
    expect(page.get_by_text("Swag Labs")).to_be_visible()
    page.locator("[data-test=\"username\"]").fill("locked_out_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test='error']")).to_have_text(
    "Epic sadface: Sorry, this user has been locked out.")


def test_numero_de_productos_distintos(logged_page: Page):
    # Verifica que dos productos distintos suman 2 en el badge
    logged_page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    logged_page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]").click()
    expect(logged_page.locator("[data-test='shopping-cart-badge']")).to_have_text("2")"""