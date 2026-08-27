

import pytest
import requests
import constants
import allure
import time
from conftest import capturar_pantalla
from playwright.sync_api import expect



def test_API_account_UI_login(home_page, usuario_temporal):
    usuario = usuario_temporal
    login = home_page.boton_login()
    login.login_correcto(usuario["email"], usuario["password"])
    home_page.verificar_home()
    home_page.verificar_usuario_logueado(usuario["firstname"], usuario["lastname"])

def test_UI_account_API_check(home_page, new_user):
    login = home_page.boton_login()
    register_page = login.registro(new_user)
    register_page.completar_formulario_registro(new_user)
    register_page.cerrar_pop_up1()
    home_page.verificar_home()
    home_page.verificar_usuario_logueado(new_user["first_name"])
    response = requests.get(f"{constants.API_BASE_URL}/getUserDetailByEmail", params={"email": new_user["email"]})
    assert response.status_code == 200
    assert response.json()["responseCode"] == 200
    assert response.json()["user"]["email"] == new_user["email"]