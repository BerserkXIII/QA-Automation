

import pytest
import constants
from playwright.sync_api import expect

class OpenAccountPage:
    def __init__(self, page):
        self.page = page

    def crear_cuenta_nueva(self, page, crear_usuario_nuevo, indice_cuenta=0):
        self.page.get_by_role("link", name="Open New Account").click()
        self.page.wait_for_url(f"{constants.HOME_URL}/openaccount.htm")
        self.page.locator("#fromAccountId option").first.wait_for(state="attached")
        self.page.locator("[id='fromAccountId']").select_option(index=indice_cuenta)
        self.page.locator("#fromAccountId option").first.wait_for(state="attached")
        self.page.get_by_role("button", name="Open New Account").click()
        self.page.locator("#openAccountResult").wait_for(state="visible")