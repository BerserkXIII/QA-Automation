
import requests
from pages.open_account_page import OpenAccountPage
from constants import API_BASE_URL
from api_helpers import *


def test_get_userID(crear_usuario_nuevo, datos_usuario_nuevo):
    user = get_user_data(datos_usuario_nuevo["username"], datos_usuario_nuevo["password"])
    cuentas = get_accounts(user["id"])
    response = requests.get(f"{API_BASE_URL}/accounts/{cuentas[0]['id']}",
                            headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json()["id"] == cuentas[0]["id"]

def test_get_accountID(crear_usuario_nuevo, datos_usuario_nuevo):
    user = get_user_data(datos_usuario_nuevo["username"], datos_usuario_nuevo["password"])
    cuentas = get_accounts(user["id"])
    for cuenta in cuentas:
        assert cuenta["customerId"] == user["id"]

def test_transfer_funds_API(crear_usuario_nuevo, datos_usuario_nuevo):
    user = get_user_data(datos_usuario_nuevo["username"], datos_usuario_nuevo["password"])
    cuentas = get_accounts(user["id"])   
    origen_id = cuentas[0]["id"] 
    new_bank_account = create_bank_account(customer_id=cuentas[0]["customerId"], fromAccountId=cuentas[0]["id"])
    cuentas = get_accounts(user["id"])
    saldos_pre_transfer = saldos_por_id(cuentas)
    amount_transfer = 150
    payload = {
        "fromAccountId": origen_id,
        "toAccountId": new_bank_account,
        "amount": amount_transfer
    }
    response = requests.post(f"{API_BASE_URL}/transfer", params=payload,
                             headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Transferencia falló: {response.status_code} — {response.text}"
    saldos_post_transfer = saldos_por_id(get_accounts(user["id"]))
    assert saldos_post_transfer[origen_id] == pytest.approx(saldos_pre_transfer[origen_id] - amount_transfer)
    assert saldos_post_transfer[new_bank_account] == pytest.approx(saldos_pre_transfer[new_bank_account] + amount_transfer)

