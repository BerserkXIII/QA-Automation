

import pytest
import constants
import requests
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

class OpenAccountPage:
    def __init__(self, page):
        self.page = page

    def ir_a_open_account(self):
        self.page.goto(constants.OPEN_ACCOUNT_URL)

    def crear_cuenta_bancaria_nueva(self, page, crear_usuario_nuevo, indice_cuenta=0):
        self.page.get_by_role("link", name="Open New Account").click()
        self.page.wait_for_url(f"{constants.HOME_URL}/openaccount.htm")
        try:
            self.page.locator("#fromAccountId option").first.wait_for(state="attached", timeout=5000)
        except PlaywrightTimeoutError:
            if self.page.locator("p.error").is_visible():
                pytest.fail("ParaBank: error interno (500) al abrir 'Open New Account'")
            raise
        self.page.locator("#fromAccountId option").first.wait_for(state="attached")
        self.page.locator("[id='fromAccountId']").select_option(index=indice_cuenta)
        bankID_inicial = self.page.locator("#fromAccountId").input_value()
        self.page.locator("#fromAccountId option").first.wait_for(state="attached")
        self.page.get_by_role("button", name="Open New Account").click()
        self.page.locator("#openAccountResult").wait_for(state="visible")
        nuevo_bankID = self.page.locator("#newAccountId").inner_text()
        return bankID_inicial, nuevo_bankID

