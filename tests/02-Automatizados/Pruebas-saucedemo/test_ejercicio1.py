
"""Test de filtro de productos → seleccionar "Price low to high" y verificar que el primer producto es el más barato
Test con usuario bloqueado → saucedemo tiene un user locked_out_user que no puede logear, verifica el mensaje de error
Test de cantidad en carrito → añadir dos productos distintos y verificar que el contador muestra 2"""

import pytest
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
    expect(page.locator(".error-message-container")).to_be_visible()    


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