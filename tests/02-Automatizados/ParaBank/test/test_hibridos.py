
import requests
import constants
import pytest
from pages.home_page import HomePage
from pages.open_account_page import OpenAccountPage
from pages.transfer_funds_page import TransferFundsPage
from pages.account_overview_page import AccountOverviewPage
from playwright.sync_api import expect
from api_helpers import get_user_data, get_accounts



def test_cuentas_creadas_UI_existen_en_API(crear_usuario_nuevo, datos_usuario_nuevo, page):
    user = get_user_data(datos_usuario_nuevo["username"], datos_usuario_nuevo["password"])
    Open = OpenAccountPage(page)
    bankID = []
    bankID.append(Open.crear_cuenta_bancaria_nueva(page, crear_usuario_nuevo, indice_cuenta=0))
    bankID.append(Open.crear_cuenta_bancaria_nueva(page, crear_usuario_nuevo, indice_cuenta=0))
    bankID.append(Open.crear_cuenta_bancaria_nueva(page, crear_usuario_nuevo, indice_cuenta=0))
    cuentas = get_accounts(user["id"])
    ids_api = [cuenta["id"] for cuenta in cuentas]
    for cuenta in cuentas:
        assert cuenta["customerId"] == user["id"]
    for id_creado in bankID:
        assert id_creado in ids_api, f"{id_creado} no está en la API: {ids_api}"

