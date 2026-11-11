
import pytest
import constants
from pages.home_page import *
from pages.register_page import *
from pages.open_account_page import *
from pages.account_overview_page import *
from pages.transfer_funds_page import *
from playwright.sync_api import expect



def test_create_user_account(crear_usuario_nuevo, page):
    expect(page.get_by_role("heading", name="Account Services")).to_be_visible()

def test_create_user_account_with_existing_username(page, datos_usuario_nuevo):
    home = HomePage(page)
    home.ir_a_home()
    home.ir_a_register()
    register = RegisterPage(page)
    register.rellenar_formulario_registro(datos_usuario_nuevo)
    page.get_by_role("link", name="Log Out").click()
    home.ir_a_register()
    register.rellenar_formulario_registro(datos_usuario_nuevo)
    expect(page.get_by_text("This username already exists.")).to_be_visible()
    
def test_create_user_account_required_fields(page, datos_usuario_nuevo):
    home = HomePage(page)
    register = RegisterPage(page)
    for clave_usuario, datos_error in constants.CAMPOS_OBLIGATORIOS.items():
        home.ir_a_home()
        home.ir_a_register()
        usuario_modificado = datos_usuario_nuevo.copy()
        usuario_modificado[clave_usuario] = ""
        register.rellenar_formulario_registro(usuario_modificado)
        id_html_error = datos_error["id_error"]
        mensaje_esperado = datos_error["mensaje"]        
        locator_error = page.locator(f"[id='{id_html_error}']")
        expect(locator_error).to_be_visible()
        expect(locator_error).to_have_text(mensaje_esperado)

def test_create_new_bank_account(page, crear_usuario_nuevo):
    Open = OpenAccountPage(page)
    bank_id_origen, bank_id_nuevo = Open.crear_cuenta_bancaria_nueva()
    expect(page.get_by_role("heading", name="Account Opened!")).to_be_visible()
    Home = HomePage(page)
    Home.ir_a_account_overview()
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()
    OverView = AccountOverviewPage(page)
    expect(OverView.localizar_cuenta(bank_id_origen)).to_be_visible()
    expect(OverView.localizar_cuenta(bank_id_nuevo)).to_be_visible()

def test_transfer_funds(crear_usuario_nuevo, page):
    Open = OpenAccountPage(page)
    bank_id_origen, bank_id_nuevo = Open.crear_cuenta_bancaria_nueva()
    AccountO = AccountOverviewPage(page)
    AccountO.ir_a_account_overview()
    saldos_pre_transfer = AccountO.obtener_saldos()
    Transfer = TransferFundsPage(page)
    Transfer.ir_a_transfer_funds()
    amount_transfer = "150"
    origen, destino = Transfer.transferir_fondos(amount = amount_transfer, from_account_id = bank_id_origen, to_account_id = bank_id_nuevo)
    assert origen == bank_id_origen
    assert destino == bank_id_nuevo
    expect(page.get_by_role("heading", name="Transfer Complete!")).to_be_visible()
    AccountO.ir_a_account_overview()
    saldos_post_transfer = AccountO.obtener_saldos()
    origen_int = int(origen)
    destino_int = int(destino)
    assert saldos_post_transfer[origen_int] == pytest.approx(saldos_pre_transfer[origen_int] - float(amount_transfer))
    assert saldos_post_transfer[destino_int] == pytest.approx(saldos_pre_transfer[destino_int] + float(amount_transfer))

def test_transfer_funds_sin_limite_saldo_negativo_confirmado(crear_usuario_nuevo, page):
    Open = OpenAccountPage(page)
    bank_id_origen, bank_id_nuevo = Open.crear_cuenta_bancaria_nueva()
    AccountO = AccountOverviewPage(page)
    AccountO.ir_a_account_overview()
    saldos_pre_transfer = AccountO.obtener_saldos()
    saldo_origen = saldos_pre_transfer[int(bank_id_origen)]
    Transfer = TransferFundsPage(page)
    Transfer.ir_a_transfer_funds()
    amount_transfer = str(int(saldo_origen) + 1000)
    origen, destino = Transfer.transferir_fondos(amount = amount_transfer, from_account_id = bank_id_origen, to_account_id = bank_id_nuevo)
    assert origen == bank_id_origen
    assert destino == bank_id_nuevo
    expect(page.get_by_role("heading", name="Transfer Complete!")).to_be_visible()
    AccountO.ir_a_account_overview()
    saldos_post_transfer = AccountO.obtener_saldos()
    origen_int = int(origen)
    destino_int = int(destino)
    assert saldos_post_transfer[origen_int] == pytest.approx(saldos_pre_transfer[origen_int] - float(amount_transfer))
    assert saldos_post_transfer[destino_int] == pytest.approx(saldos_pre_transfer[destino_int] + float(amount_transfer))
    assert saldos_post_transfer[origen_int] < 0

@pytest.mark.xfail(reason="BUG conocido: ParaBank permite abrir cuentas con saldo insuficiente en la cuenta de origen.", raises=AssertionError)
def test_create_bank_account_insufficient_funds(page, crear_usuario_nuevo):
    Open = OpenAccountPage(page)
    Open.crear_cuenta_bancaria_nueva()
    Open.crear_cuenta_bancaria_nueva(indice_cuenta=1)
    Open.crear_cuenta_bancaria_nueva(indice_cuenta=1)
    expect(page.get_by_text("You do not have sufficient funds in your account to complete this transaction.")).to_be_visible()
