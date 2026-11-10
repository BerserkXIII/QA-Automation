
import requests
import constants
import pytest
from pages.home_page import HomePage
from pages.open_account_page import OpenAccountPage
from pages.transfer_funds_page import TransferFundsPage
from pages.account_overview_page import AccountOverviewPage
from playwright.sync_api import expect
from api_helpers import *



def test_accounts_UI_checking_API(crear_usuario_nuevo, datos_usuario_nuevo, page):
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

def test_transfer_funds_UI_checking_API(crear_usuario_nuevo, datos_usuario_nuevo, page):
    Open = OpenAccountPage(page)
    bank_id_origen, bank_id_nuevo = Open.crear_cuenta_bancaria_nueva(page, crear_usuario_nuevo, indice_cuenta=0)
    user = get_user_data(datos_usuario_nuevo["username"], datos_usuario_nuevo["password"])
    userID = user["id"]
    user_accounts = get_accounts(userID)
    saldos_pre_transfer = saldos_por_id(user_accounts)
    Transfer = TransferFundsPage(page)
    Transfer.ir_a_transfer_funds()
    amount_transfer = "150"
    origen, destino = Transfer.transferir_fondos(amount = amount_transfer, from_account_id = bank_id_origen , to_account_id = bank_id_nuevo)
    assert origen == bank_id_origen
    assert destino == bank_id_nuevo
    expect(page.get_by_role("heading", name="Transfer Complete!")).to_be_visible()
    user_accounts = get_accounts(userID)
    saldos_post_transfer = saldos_por_id(user_accounts)
    origen_int = int(origen)
    destino_int = int(destino)
    assert saldos_post_transfer[origen_int] == pytest.approx(saldos_pre_transfer[origen_int] - float(amount_transfer))
    assert saldos_post_transfer[destino_int] == pytest.approx(saldos_pre_transfer[destino_int] + float(amount_transfer))