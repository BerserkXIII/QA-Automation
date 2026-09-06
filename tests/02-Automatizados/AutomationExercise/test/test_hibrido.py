

import pytest
import requests
import constants
from conftest import capturar_pantalla
from pages.login_page import LoginPage
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

def test_API_account_UI_delete_API_check(home_page, usuario_temporal):
    usuario = usuario_temporal
    login = home_page.boton_login()
    login.login_correcto(usuario["email"], usuario["password"])
    home_page.verificar_usuario_logueado(usuario["firstname"], usuario["lastname"])
    home_page.boton_delete_account()
    response = requests.get(f"{constants.API_BASE_URL}/getUserDetailByEmail", params={"email": usuario["email"]})
    assert response.status_code == 200
    assert response.json()["responseCode"] == 404

def test_UI_account_API_delete_UI_check(home_page, new_user):
    login = home_page.boton_login()
    register_page = login.registro(new_user)
    register_page.completar_formulario_registro(new_user)
    register_page.cerrar_pop_up1()
    home_page.verificar_home()
    home_page.verificar_usuario_logueado(new_user["first_name"])
    response = requests.delete(f"{constants.API_BASE_URL}/deleteAccount", data={"email": new_user["email"], "password": new_user["password"]})
    assert response.status_code == 200
    assert response.json()["responseCode"] == 200
    home_page.ir_a_login()
    login_page = LoginPage(home_page.page)
    login_page.login_correcto(email=new_user["email"], password=new_user["password"])
    expect(login_page.page.get_by_text("Your email or password is incorrect!")).to_be_visible()