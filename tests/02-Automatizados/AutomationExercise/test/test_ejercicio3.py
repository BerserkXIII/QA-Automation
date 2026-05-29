

import pytest
from playwright.sync_api import expect



def test_registrar_usuario(home_page, new_user):
    login = home_page.boton_login()
    register_page = login.ir_a_registro(new_user)
    register_page.completar_formulario_registro(new_user)
    register_page.cerrar_pop_up1()
    home_page.verificar_home()


def test_login_correcto(home_page):
    login = home_page.boton_login()
    login.login_correcto()
    home_page.verificar_home()
    home_page.verificar_usuario_logueado()