
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def logged_page(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.get_by_text("Products")).to_be_visible()
    return page