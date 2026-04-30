# Especificación de Tests — REACTIVE.PY

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

`reactive.py` implementa un **patrón Observer simplificado**. Es un diccionario (`Personaje`) que:
- Almacena datos (vida, fuerza, etc.)
- Permite registrar "escuchas" (callbacks) en campos específicos
- Dispara esos callbacks automáticamente cuando el campo cambia

**Tú necesitas testear:** ¿Funciona correctamente este patrón? ¿Se ejecutan callbacks en el momento correcto? ¿Hay casos donde falla?

---

## MATRIZ DE PRUEBAS

| Test ID | Descripción | Entrada | Salida Esperada | Mocks |
|---------|-------------|---------|-----------------|-------|
| U1.1 | Init vacío | `Personaje()` | `{}`, `_watchers={}`, `activo=False` | Ninguno |
| U1.2 | Init con datos | `Personaje({...})` | Datos presentes, dict válido | Ninguno |
| U1.3 | Compatible dict | Operaciones dict | `.get()`, `in`, `len()` funcionan | Ninguno |
| U2.1 | Registrar callback | `observe("vida", cb)` | `cb` almacenado | Mock callback |
| U2.2 | Múltiples callbacks | 2x `observe()` campos diferentes | Ambos almacenados | Mock callback |
| U2.3 | Sobrescribir callback | `observe(f, cb1)` → `observe(f, cb2)` | cb2 activo, cb1 ignorado | 2x Mock |
| U3.1 | Asignar sin observador | `p["x"] = v` | `p["x"] == v`, sin error | Ninguno |
| U3.2 | Valor idéntico | Asignar valor igual | Callback NO ejecutado | Mock callback |
| U3.3 | Valor diferente | Asignar valor nuevo | Callback ejecutado con nuevo valor | Mock callback |
| U3.4 | Inactivo | `activo=False` + asignación | Callback NO ejecutado | Mock callback |
| U3.5 | Activar | `activo=True` + asignación | Callback ejecutado | Mock callback |
| U3.6 | Múltiples cambios | Asignar 3 veces | Callback ejecutado 3 veces | Mock callback |
| U3.7 | Valor None | Asignar `None` | Callback ejecutado con `None` | Mock callback |

---

## MÓDULO: `Personaje` (clase)

### Función 1: `__init__(datos_iniciales)` — Inicialización

**¿Qué hace?**
- Crea un objeto Personaje (que es un diccionario)
- Prepara un sistema interno de watchers (observadores)
- Inicializa con estado "inactivo" (no dispara callbacks aún)

**Casos a testear (Arrange-Act-Assert):**

#### Test U1.1: Crear personaje vacío
```
ARRANGE: No hay datos iniciales
ACT: p = Personaje()
ASSERT: 
  - p es un dict vacío {}
  - p._watchers existe y es dict vacío
  - p.activo == False
```

#### Test U1.2: Crear personaje con datos
```
ARRANGE: Tengo dict {"vida": 10, "fuerza": 5}
ACT: p = Personaje({"vida": 10, "fuerza": 5})
ASSERT:
  - p["vida"] == 10
  - p["fuerza"] == 5
  - p["vida"] accesible como dict normal
  - p.activo == False
```

#### Test U1.3: Personaje es dict normal
```
ARRANGE: p = Personaje({"vida": 10})
ACT: Pruebo operaciones dict
ASSERT:
  - p.get("vida") == 10
  - p.get("inexistente") == None
  - len(p) == 1
  - "vida" in p
```

---

### Función 2: `observe(field, callback)` — Registrar observador

**¿Qué hace?**
- Registra una función callback para ser ejecutada cuando `field` cambia
- Guarda el callback internamente en `_watchers`
- Si llamas dos veces con el mismo `field`, la segunda sobrescribe la primera

**Casos a testear:**

#### Test U2.1: Registrar callback único
```
ARRANGE: 
  - p = Personaje()
  - callback_mock = Mock()  (función simulada que registra llamadas)
ACT:
  - p.observe("vida", callback_mock)
ASSERT:
  - callback_mock está almacenado internamente
  - No se ejecuta aún (personaje no activo)
```

#### Test U2.2: Múltiples callbacks en campos diferentes
```
ARRANGE:
  - p = Personaje()
  - callback_vida = Mock()
  - callback_fuerza = Mock()
ACT:
  - p.observe("vida", callback_vida)
  - p.observe("fuerza", callback_fuerza)
ASSERT:
  - Ambos callbacks almacenados
  - callback_vida asociado a "vida"
  - callback_fuerza asociado a "fuerza"
```

#### Test U2.3: Segundo observe del mismo field sobrescribe el primero
```
ARRANGE:
  - p = Personaje()
  - callback_1 = Mock()
  - callback_2 = Mock()
ACT:
  - p.observe("vida", callback_1)
  - p.observe("vida", callback_2)  ← Sobrescribe
  - p.activo = True
  - p["vida"] = 5
ASSERT:
  - callback_2 fue ejecutado
  - callback_1 NUNCA fue ejecutado (fue reemplazado)
```

---

### Función 3: `__setitem__(key, value)` — Asignar valor y disparar callback

**¿Qué hace?**
- Asigna un valor a un campo (como dict normal)
- Si el valor es diferente del anterior, lo actualiza
- Si `activo=True` Y hay callback registrado para ese campo, ejecuta el callback
- Si `activo=False`, nunca ejecuta callback

**Casos a testear:**

#### Test U3.1: Asignar valor nuevo (sin observador) — No error
```
ARRANGE: p = Personaje()
ACT: p["vida"] = 10
ASSERT:
  - p["vida"] == 10
  - Sin error ni excepción
```

#### Test U3.2: Asignar valor idéntico — Callback NO dispara
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = True
ACT:
  - p["vida"] = 10  ← Mismo valor
ASSERT:
  - callback.assert_not_called()  (nunca ejecutado)
```

#### Test U3.3: Asignar valor diferente — Callback SÍ dispara
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = True
ACT:
  - p["vida"] = 15  ← Valor diferente
ASSERT:
  - p["vida"] == 15
  - callback.assert_called_once_with(15)  (ejecutado CON el nuevo valor)
```

#### Test U3.4: Con activo=False — Callback no dispara
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = False  ← Inactivo
ACT:
  - p["vida"] = 15
ASSERT:
  - p["vida"] == 15
  - callback.assert_not_called()  (no ejecutado porque activo=False)
```

#### Test U3.5: Activar reactividad — Callback dispara
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = False  (inicialmente inactivo)
ACT:
  - p.activo = True  ← Activamos
  - p["vida"] = 15
ASSERT:
  - callback.assert_called_once_with(15)
```

#### Test U3.6: Múltiples cambios — Callbacks se ejecutan cada vez
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = True
ACT:
  - p["vida"] = 15
  - p["vida"] = 20
  - p["vida"] = 25
ASSERT:
  - callback.assert_called_with(25)
  - callback.call_count == 3  (ejecutado 3 veces)
```

#### Test U3.7: Asignar None — Funciona como cualquier otro valor
```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = True
ACT:
  - p["vida"] = None
ASSERT:
  - p["vida"] == None
  - callback.assert_called_once_with(None)
```

---

## ESTRUCTURA DE CADA TEST

Todos los tests siguen el patrón **ARRANGE → ACT → ASSERT**:

```python
def test_ejemplo():
    # ARRANGE: Preparar el estado inicial
    personaje = Personaje({"vida": 10})
    callback = Mock()
    personaje.observe("vida", callback)
    personaje.activo = True
    
    # ACT: Ejecutar la acción a testear
    personaje["vida"] = 15
    
    # ASSERT: Verificar resultados
    assert personaje["vida"] == 15
    callback.assert_called_once_with(15)
```

**Nota importante**: Para tests de `observe()` y `__setitem__()`, necesitas:
- `Mock()` de `unittest.mock` para simular callbacks
- Verificar tanto llamadas como argumentos exactos
- Diferenciar entre callbacks ejecutados vs no ejecutados

---

## FIXTURES NECESARIAS

```python
import pytest
from unittest.mock import Mock

# Fixture: Personaje vacío
@pytest.fixture
def personaje_vacio():
    from modules.reactive import Personaje
    return Personaje()

# Fixture: Personaje con datos iniciales
@pytest.fixture
def personaje_base():
    from modules.reactive import Personaje
    return Personaje({"vida": 10, "fuerza": 5, "destreza": 3})

# Fixture: Mock callback reutilizable
@pytest.fixture
def mock_callback():
    return Mock()

# Fixture: Personaje con callback registrado y activo
@pytest.fixture
def personaje_con_observador(personaje_base, mock_callback):
    personaje_base.observe("vida", mock_callback)
    personaje_base.activo = True
    return personaje_base, mock_callback
```

---

## NOTAS

1. **Importación**: Los tests importan `Personaje` desde `modules.reactive`. Asegúrate de que el path 
   es accesible (puede requerir `sys.path.insert(0, path_to_modules)`).

2. **Mock vs Real**: Todos los callbacks en tests son Mocks. El patrón Observer en `reactive.py` es REAL 
   (no mockear la clase Personaje, solo los callbacks).

3. **Orden de ejecución**: Algunos tests dependen de que `activo` sea True/False. No asumir un estado 
   global — configurar explícitamente en ARRANGE.

4. **Valor vs Identidad**: El test U3.2 verifica que callback NO se ejecuta si el valor asignado es 
   idéntico al anterior. Esto requiere una comparación `==`, no solo `is`.

5. **None como valor válido**: El test U3.7 valida que `None` sea un valor válido. Algunos sistemas 
   interpretan `None` como "sin valor", pero aquí es un valor legítimo.

6. **Reproducibilidad**: Todos los 13 tests deben ser independientes. No compartir estado entre tests 
   (excepto vía fixtures, que se recrean cada test).

---

## SIGUIENTES PASOS

Una vez completados estos 13 tests de `reactive.py`:
- Generarás **COBERTURA REPORT**
- Pasarás a **EVENTOS.PY** (más complejo)
- Luego **TLDRDC_PRUEBA1.PY** funciones críticas
