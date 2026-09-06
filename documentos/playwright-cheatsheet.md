# Playwright (Python) — Cheat Sheet

## Navegación
```python
page.goto("https://example.com")
page.go_back()
page.go_forward()
page.reload()
```

## Localizadores (Locators)
```python
page.get_by_role("button", name="Continue")   # por rol de accesibilidad (preferido)
page.get_by_text("Delete Account")             # por texto visible
page.get_by_label("Email")                     # por label de un input
page.get_by_placeholder("Enter email")
page.get_by_test_id("submit-btn")              # por data-testid
page.locator("#id")                            # por CSS
page.locator("[data-qa='login-button']")       # por atributo
page.locator("iframe[name^='aswift_']")        # frame_locator, ver abajo

# Modificadores útiles
locator.first
locator.last
locator.nth(2)
locator.filter(has_text="algo")
```

## Acciones
```python
locator.click()
locator.click(force=True)          # salta comprobaciones de Playwright (ojo, no atraviesa overlays)
locator.dblclick()
locator.fill("texto")              # limpia y escribe
locator.type("texto")              # escribe letra a letra (simula teclado)
locator.check() / .uncheck()       # checkboxes
locator.select_option("valor")     # <select>
locator.hover()
locator.press("Enter")
locator.set_input_files("ruta.pdf")
```

## Esperas y aserciones (expect)
```python
from playwright.sync_api import expect

expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_be_enabled() / .to_be_disabled()
expect(locator).to_have_text("texto exacto")
expect(locator).to_contain_text("parte del texto")
expect(locator).to_have_value("valor de input")
expect(locator).to_have_count(3)
expect(page).to_have_url("https://...")
expect(page).to_have_title("Título")

# Con timeout custom
expect(locator).to_be_visible(timeout=5000)
```

## Esperas manuales (evitar si `expect` ya cubre el caso)
```python
page.wait_for_url("**/success")
page.wait_for_load_state("networkidle")
page.wait_for_timeout(1000)          # último recurso, evitar sleeps fijos
locator.wait_for(state="visible")
page.wait_for_function("window.scrollY === 0")
```

## Frames / iframes
```python
frame = page.frame_locator("iframe[name='miframe']")
frame.get_by_role("button", name="Close").click()
```

## Popups y nuevas pestañas
```python
with page.expect_popup() as popup_info:
    page.get_by_text("Abrir en nueva pestaña").click()
new_page = popup_info.value
```

## Interceptar peticiones de red
```python
# Bloquear
page.route("**/*ads*", lambda route: route.abort())

# Espiar
with page.expect_request("**/api/signup") as req_info:
    boton.click()
request = req_info.value
print(request.post_data)

# Escuchar todo (debug)
page.on("request", lambda req: print(req.url))

# Manejar popups que aparecen en cualquier momento
page.add_locator_handler(locator, handler_fn, no_wait_after=True)
```

## Screenshots y debug
```python
page.screenshot(path="captura.png")
page.pause()                          # abre el Inspector, pausa el test ahí
```
```powershell
$env:PWDEBUG=1                        # modo debug para toda la ejecución (PowerShell)
Remove-Item Env:\PWDEBUG              # desactivarlo
```

## Fixtures típicas de pytest-playwright
```python
def test_algo(page):        # ya viene inyectada, no hace falta crearla
    ...

@pytest.fixture
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "es-ES"}
```

## Comandos de terminal
```powershell
playwright install                    # instalar navegadores
playwright install --with-deps chromium
playwright codegen https://example.com   # graba acciones y genera código
pytest -v                             # verbose
pytest -v -s                          # + mostrar prints
pytest -k "nombre_test"               # correr solo un test
pytest --headed                       # ver el navegador mientras corre
pytest --alluredir=allure-results --clean-alluredir
allure serve allure-results
```
