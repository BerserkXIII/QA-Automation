
import requests
from pages.open_account_page import OpenAccountPage
from constants import API_BASE_URL
from api_helpers import get_user_data, get_accounts



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




