

import pytest
import requests
import constants

def get_user_data(username, password):
    response = requests.get(f"{constants.API_BASE_URL}/login/{username}/{password}",
                            headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Login falló: {response.status_code} — {response.text}"
    return response.json()

def get_accounts(customer_id):
    response = requests.get(f"{constants.API_BASE_URL}/customers/{customer_id}/accounts",
                            headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Consulta de cuentas falló: {response.status_code} — {response.text}"
    return response.json()

def create_bank_account(customer_id, newAccountType="SAVINGS", fromAccountId=None):
    payload = {"customerId": customer_id, "accountType": newAccountType, "fromAccountId": fromAccountId}
    response = requests.post(f"{constants.API_BASE_URL}/createAccount", params=payload,
                             headers={"Accept": "application/json"})
    assert response.status_code == 200, f"Creación de cuenta falló: {response.status_code} — {response.text}"
    return response.json()["id"]

def saldos_por_id(cuentas):
    return {c["id"]: c["balance"] for c in cuentas}