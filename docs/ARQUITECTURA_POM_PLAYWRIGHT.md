# Arquitectura POM (Page Object Model) con Playwright

## El modelo de Lego

Imagina que construyes con piezas de Lego:

```
┌─────────────────────────────────────────────┐
│ TEST: Verificador del comportamiento        │
│ "¿Se comporta el sistema como esperamos?"   │
└──────────────┬──────────────────────────────┘
               │ usa
               ▼
┌─────────────────────────────────────────────┐
│ CONFTEST: El ensamblador                    │
│ "Prepara las piezas en el estado correcto"  │
└──────────────┬──────────────────────────────┘
               │ instancia y prepara
               ▼
┌─────────────────────────────────────────────┐
│ PAGES: Piezas especializadas                │
│ "Cada página encapsula su propia lógica"    │
└─────────────────────────────────────────────┘
```

**Cada capa tiene una responsabilidad clara. Si algo cambia en la UI, solo tocas la capa de Pages. Los tests no se enteran.**

---

## Los 3 componentes

### 1. PAGES — Las piezas especializadas

Cada clase representa una página de la aplicación y sabe todo sobre ella: dónde están los elementos y cómo interactuar con ellos. Los tests no necesitan conocer ningún selector.

```python
# pages/login_page.py
from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page

    def ir_a_login(self):
        self.page.goto("https://www.saucedemo.com/")

    def hacer_login(self, usuario, contraseña):
        self.page.locator("[data-test='username']").fill(usuario)
        self.page.locator("[data-test='password']").fill(contraseña)
        self.page.locator("[data-test='login-button']").click()

    def verificar_login_exitoso(self):
        expect(self.page.get_by_text("Products")).to_be_visible()

    def verificar_login_fallido(self, mensaje_esperado):
        expect(self.page.locator("[data-test='error']")).to_have_text(mensaje_esperado)
```

**Ventaja:** si cambia un selector, lo cambias aquí y todos los tests siguen funcionando sin tocarlos.

---

### 2. CONFTEST — El ensamblador

Prepara el estado que necesita cada test antes de ejecutarse. Usa las Pages para hacer ese trabajo.

```python
# conftest.py
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.fixture
def ini_page(page):
    """Estado: navegador abierto en la página de login."""
    login = LoginPage(page)
    login.ir_a_login()
    return login

@pytest.fixture
def logged_page(page):
    """Estado: usuario ya logueado, listo para operar en el inventario."""
    login = LoginPage(page)
    login.ir_a_login()
    login.hacer_login("standard_user", "secret_sauce")
    login.verificar_login_exitoso()  # Sanity check: confirma que el estado es correcto
    return InventoryPage(page)
```

La fixture `page` que reciben como parámetro la proporciona pytest-playwright automáticamente. No hace falta crearla.

---

### 3. TESTS — El verificador

Solo describe qué se verifica. Sin locators, sin clicks directos, sin lógica de navegación.

```python
def test_login_correcto(logged_page):
    expect(logged_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_agregar_al_carrito(logged_page):
    logged_page.agregar_producto("sauce-labs-backpack")
    expect(logged_page.page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")
```

**El test no sabe cómo funciona el login ni qué selectores usa. Solo asume que el estado está preparado y verifica lo que le importa.**

---

## ✚ El sanity check

### Un sanity check es una verificación dentro de la fixture que confirma que el estado se preparó correctamente antes de que empiece el test.

```python
@pytest.fixture
def logged_page(page):
    login = LoginPage(page)
    login.ir_a_login()
    login.hacer_login("standard_user", "secret_sauce")
    login.verificar_login_exitoso()  # ← Sanity check
    return InventoryPage(page)
```

**Por qué es útil:** cuando un test falla, necesitas saber dónde. Sin sanity check, si el login falla silenciosamente, el test posterior falla con un error confuso que no apunta al problema real. Con sanity check, si el login falla, la fixture falla inmediatamente y el mensaje es claro: el problema está en la preparación, no en el test.

```
# Sin sanity check, el error es confuso:
FAILED test_carrito — AssertionError: expected 1, got 0
→ ¿Falló el login? ¿El selector del carrito? ¿La función agregar?

# Con sanity check, el error es claro:
FAILED logged_page — "Products" not visible
→ El login no funcionó. Busca ahí.
```

El sanity check tarda un segundo en escribir y puede ahorrarte media hora de debugging.

---

## Fixtures en capas

Las fixtures se construyen unas sobre otras según el estado que necesita cada test:

```python
@pytest.fixture
def ini_page(page):
    """Nivel 1: Solo navega a la URL."""
    login = LoginPage(page)
    login.ir_a_login()
    return login

@pytest.fixture
def logged_page(page):
    """Nivel 2: Navega y hace login."""
    login = LoginPage(page)
    login.ir_a_login()
    login.hacer_login("standard_user", "secret_sauce")
    login.verificar_login_exitoso()
    return InventoryPage(page)
```

Los tests que necesitan login usan `logged_page`. Los tests de login fallido usan `ini_page`. Cada uno recibe exactamente el estado que necesita, sin más.

Las fixtures son "lazy": solo se ejecutan si un test las pide como parámetro. Si un test no necesita login, no gasta recursos en prepararlo.

---

## Parametrización

Cuando varios tests tienen la misma estructura pero con datos distintos, `@pytest.mark.parametrize` evita repetir código:

```python
# Sin parametrizar: 3 tests idénticos con datos distintos
def test_login_admin_incorrecto(ini_page): ...
def test_login_pass_incorrecta(ini_page): ...
def test_login_bloqueado(ini_page): ...

# Con parametrizar: 1 test, 3 casos
@pytest.mark.parametrize("username,password,error_message", [
    ("admin", "secret_sauce", "Epic sadface: Username and password do not match any user in this service"),
    ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
])
def test_login_fallido(ini_page, username, password, error_message):
    ini_page.hacer_login(username, password)
    ini_page.verificar_login_fallido(error_message)
```

Pytest genera un test por cada fila y les asigna nombres automáticamente. Si añades un caso nuevo, solo añades una línea.

**Cuándo usarlo:** cuando tienes 3 o más casos del mismo comportamiento con datos distintos.
**Cuándo no:** cuando los comportamientos son distintos entre sí (logout y agregar al carrito son tests separados, no parametrizables).

---

## Estructura de carpetas recomendada

```
Pruebas-saucedemo/
├── conftest.py
├── pages/
│   ├── __init__.py
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   └── test_checkout.py
├── utils/
│   └── constants.py       # URLs, credenciales de test
└── requirements.txt
```

Separar los tests por funcionalidad hace que cuando algo falla sea fácil saber en qué área buscar.

---

## Errores comunes

| Error | Causa probable | Solución |
|-------|---------------|----------|
| `ElementNotFound` en la fixture | El sanity check falta o falla | Añadir `verificar_*()` en la fixture |
| Test falla de repente sin cambios | Selector hard-coded que cambió en la UI | Usar `get_by_text()` o `get_by_role()` donde sea posible |
| Tests lentos | `time.sleep()` innecesarios | Playwright espera automáticamente, no hace falta |
| Código duplicado en tests | Lógica que debería estar en la Page | Mover acciones repetidas a métodos de la Page |
| `page` fixture sobreescrita | Definir `def page(browser)` en conftest | Borrarla, pytest-playwright ya la proporciona |

---

## Cuándo NO usar POM

POM añade capas de abstracción que tienen un coste: más archivos, más estructura, más cosas que mantener. No siempre merece la pena.

**No uses POM cuando:**
- Tienes 3-4 tests exploratorios o de un solo uso.
- Estás prototipando algo rápido para ver si funciona.
- El proyecto es tan pequeño que la estructura añade más complejidad de la que resuelve.

**Sí usa POM cuando:**
- El proyecto tiene más de 10-15 tests.
- Varios tests comparten las mismas páginas y acciones.
- El proyecto va a crecer o a ser mantenido por más de una persona.

La regla simple: si ves que estás copiando selectores entre tests, es momento de POM.

---

## Resumen

```python
# 1. La Page encapsula selectores y acciones
class LoginPage:
    def hacer_login(self, user, password): ...
    def verificar_login_exitoso(self): ...

# 2. El conftest prepara el estado con sanity check
@pytest.fixture
def logged_page(page):
    login = LoginPage(page)
    login.ir_a_login()
    login.hacer_login("standard_user", "secret_sauce")
    login.verificar_login_exitoso()  # Sanity check
    return InventoryPage(page)

# 3. El test solo verifica comportamiento nuevo
def test_carrito(logged_page):
    logged_page.agregar_producto("sauce-labs-backpack")
    expect(logged_page.page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")
```

Código limpio, mantenible, y que falla en el lugar correcto cuando algo rompe.
