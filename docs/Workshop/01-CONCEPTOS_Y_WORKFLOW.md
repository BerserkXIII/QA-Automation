# 📖 CONCEPTOS Y WORKFLOW — Testing Profesional

*Guía para entender qué hace cada línea de un test + AAA pattern + fixtures + comandos*

**Nivel:** Principiante → Intermedio | **Tiempo:** 45-60 minutos | **Meta:** Leer y escribir tests sin miedo

---

## 1️⃣ ¿QUÉ ES UN TEST?

### Definición Simple

Un **test** es un programa que verifica si otra parte del código funciona correctamente.

```python
# CÓDIGO NORMAL (lo que quieres probar)
def sumar(a, b):
    return a + b

# TEST (verifica que sumar() funciona bien)
def test_sumar():
    resultado = sumar(2, 3)
    assert resultado == 5  # "Verifica que el resultado sea 5"
```

**¿La diferencia?** El test **verifica** que el resultado es correcto.

---

## 2️⃣ `ASSERT` — LA HERRAMIENTA MÁS IMPORTANTE

### ¿Qué Hace?

`assert` es una palabra clave que verifica si algo es verdadero.

```python
# Sintaxis básica:
assert <algo_que_debería_ser_verdadero>
```

### Ejemplos Simples

```python
# ✅ Verdadero → No pasa nada
assert 5 == 5          # Correcto
assert "hola" == "hola"  # Correcto

# ❌ Falso → El test FALLA
assert 5 == 3          # ❌ ERROR
assert "hola" == "adiós"  # ❌ ERROR
```

### Operadores Útiles

```python
assert personaje["vida"] == 10        # ¿Es igual a 10?
assert personaje["vida"] != 0         # ¿No es igual a 0?
assert personaje["vida"] > 5          # ¿Mayor que 5?
assert personaje["vida"] < 20         # ¿Menor que 20?
assert "vida" in personaje            # ¿"vida" existe?
assert isinstance(personaje, dict)    # ¿Es un diccionario?
assert len(personaje) == 5            # ¿Tiene 5 elementos?
```

### Assert con Funciones (Mocks)

```python
from unittest.mock import Mock

callback = Mock()
callback(5)  # Ejecutar

# Verificar si fue llamado
assert callback.called              # ¿Fue ejecutado?
callback.assert_called_once()       # ¿Exactamente 1 vez?
callback.assert_called_with(5)      # ¿Con parámetro 5?
callback.assert_not_called()        # ¿NUNCA se ejecutó?
```

---

## 3️⃣ AAA PATTERN — ESTRUCTURA ESTÁNDAR

### ¿Qué Es?

AAA = **Arrange, Act, Assert** (Preparar, Ejecutar, Verificar)

```
┌─────────────────────────────────┐
│ ARRANGE: Preparar datos         │
├─────────────────────────────────┤
│ ACT: Ejecutar función           │
├─────────────────────────────────┤
│ ASSERT: Verificar resultado     │
└─────────────────────────────────┘
```

### Ejemplo Real 1: Sumar

```python
def test_sumar_dos_numeros():
    # ARRANGE: Preparar datos
    a = 2
    b = 3
    
    # ACT: Ejecutar lo que queremos probar
    resultado = sumar(a, b)
    
    # ASSERT: Verificar que funcionó
    assert resultado == 5
```

### Ejemplo Real 2: Personaje Recibe Daño

```python
def test_personaje_recibe_danio():
    # ARRANGE: Crear personaje
    personaje = {"nombre": "Hero", "vida": 10}
    
    def aplicar_danio(p, danio):
        p["vida"] -= danio
    
    # ACT: Aplicar daño
    aplicar_danio(personaje, 3)
    
    # ASSERT: Verificar que la vida bajó
    assert personaje["vida"] == 7
```

---

## 4️⃣ FIXTURES — REUTILIZAR DATOS

### ¿Qué Es Un Fixture?

Un **fixture** es **datos preparados** que usas en múltiples tests.

**Sin fixtures (malo):**
```python
def test_1():
    personaje = {"nombre": "Hero", "vida": 10, "fuerza": 5}
    # ... código

def test_2():
    personaje = {"nombre": "Hero", "vida": 10, "fuerza": 5}
    # ... código

# Repetido 50 veces... 😞
```

**Con fixtures (bien):**
```python
@pytest.fixture
def personaje():
    return {"nombre": "Hero", "vida": 10, "fuerza": 5}

def test_1(personaje):
    # personaje ya está listo
    pass

def test_2(personaje):
    # personaje ya está listo
    pass
```

### Cómo Funciona

```python
import pytest

# 1. Definir fixture
@pytest.fixture
def personaje_base():
    return {
        "nombre": "TestPlayer",
        "vida": 10,
        "fuerza": 5,
    }

# 2. Usar en test
def test_personaje_existe(personaje_base):
    # personaje_base se inyecta automáticamente
    assert personaje_base["vida"] == 10

# 3. Pytest automáticamente:
# - Crea personaje_base
# - Lo pasa al test
# - Lo limpia después
```

### Fixtures Disponibles (en conftest.py)

```python
# PERSONAJES
def test_ejemplo(personaje_base, personaje_vivo, personaje_bajo_vida, personaje_muerto):
    pass

# ESTADO
def test_ejemplo(estado_test, estado_con_armas, estado_bolsa_vacia):
    pass

# ARMAS
def test_ejemplo(armas_global):
    pass

# MOCKS
def test_ejemplo(mock_narrar, mock_alerta, mock_exito, mock_sistema):
    pass

# COMPLETO
def test_ejemplo(game_context):
    p = game_context["personaje"]
    estado = game_context["estado"]
    mocks = game_context["mocks"]
```

---

## 5️⃣ MOCKS — SIMULAR FUNCIONES

### ¿Por Qué Existen?

A veces necesitas simular funciones para verificar si fueron llamadas o controlar su comportamiento.

```python
from unittest.mock import Mock

# Crear mock (función falsa)
mock_callback = Mock()

# Ejecutar
mock_callback()

# Verificar si fue llamado
assert mock_callback.called  # True
```

### Ejemplo Real: Verificar Notificación

```python
from unittest.mock import Mock

# ARRANGE: Crear mock que simula función de UI
actualizar_vida = Mock()

class Personaje(dict):
    def __init__(self, datos):
        super().__init__(datos)
        self.actualizar = actualizar_vida
    
    def recibir_danio(self, danio):
        self["vida"] -= danio
        self.actualizar(self["vida"])  # Llamar actualización

# ACT
p = Personaje({"vida": 10})
p.recibir_danio(3)

# ASSERT
actualizar_vida.assert_called_once_with(7)  # ¿Se ejecutó con 7?
```

---

## 6️⃣ CLASES EN TESTS

### ¿Por Qué?

Tests están organizados en **clases** para agrupar tests relacionados.

**Sin clases (desorganizado):**
```python
def test_init_1(): pass
def test_init_2(): pass
def test_observe_1(): pass
def test_observe_2(): pass
# 50 funciones sueltas... confuso
```

**Con clases (organizado):**
```python
class TestInit:
    def test_1(self): pass
    def test_2(self): pass

class TestObserve:
    def test_1(self): pass
    def test_2(self): pass
```

### Estructura

```python
import pytest

class TestReactiveInit:
    """Agrupa tests de inicialización"""
    
    def test_init_vacio(self):
        # ... código
        assert ...
    
    def test_init_con_datos(self):
        # ... código
        assert ...

class TestObserve:
    """Agrupa tests de observadores"""
    
    def test_observe_registro(self):
        # ... código
        assert ...
```

### Fixtures en Clases

```python
@pytest.fixture
def personaje():
    return {"vida": 10}

class TestPersonaje:
    def test_1(self, personaje):  # ← se inyecta
        assert personaje["vida"] == 10
    
    def test_2(self, personaje):  # ← nuevo para cada test
        personaje["vida"] = 5
        assert personaje["vida"] == 5
    
    def test_3(self, personaje):  # ← vuelve a vida=10
        assert personaje["vida"] == 10
```

---

## 7️⃣ EJEMPLO COMPLETO COMENTADO

### Código Que Vamos a Testear

```python
class Personaje(dict):
    """Un diccionario que puede notificar cambios"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._watchers = {}        # Observadores
        self.activo = False        # ¿Notifica cambios?
    
    def observe(self, field, callback):
        """Registrar función que se ejecuta cuando field cambia"""
        self._watchers[field] = callback
    
    def __setitem__(self, key, value):
        """Cuando asignas p[key] = value, notifica si hay observador"""
        if self.get(key) != value:
            super().__setitem__(key, value)
            if self.activo and key in self._watchers:
                self._watchers[key](value)
```

### Test 1: Inicialización Vacía

```python
class TestReactiveInit:
    
    def test_init_vacio(self):
        """Test U1.1: Crear personaje vacío"""
        
        # ARRANGE (no hay nada que preparar)
        
        # ACT: Crear personaje vacío
        p = Personaje()
        
        # ASSERT: Verificar que funciona
        assert isinstance(p, dict)     # ¿Es un dict?
        assert len(p) == 0             # ¿Vacío?
        assert len(p._watchers) == 0   # ¿Sin watchers?
        assert p.activo == False       # ¿Inactivo?
```

### Test 2: Con Datos

```python
    def test_init_con_datos(self):
        """Test U1.2: Crear personaje con datos"""
        
        # ARRANGE: Datos iniciales
        datos = {"vida": 10, "fuerza": 5}
        
        # ACT: Crear con esos datos
        p = Personaje(datos)
        
        # ASSERT: Verificar que los datos se guardaron
        assert p["vida"] == 10
        assert p["fuerza"] == 5
        assert len(p) == 2
        assert p._watchers == {}
        assert p.activo == False
```

### Test 3: Observer (Lo Complejo)

```python
    def test_observe_sobrescribe(self):
        """Test U2.3: Segundo observer sobrescribe el primero"""
        
        # ARRANGE: Dos mocks + personaje
        callback_1 = Mock()
        callback_2 = Mock()
        p = Personaje()
        
        # ACT: Registrar dos observadores + cambiar vida
        p.observe("vida", callback_1)
        p.observe("vida", callback_2)  # Sobrescribe
        p["vida"] = 15
        
        # ASSERT: Verificar que callback_2 se ejecutó, callback_1 no
        assert callback_2.called            # callback_2 SÍ
        callback_2.assert_called_with(15)   # Con 15
        callback_1.assert_not_called()      # callback_1 NO
```

---

## 8️⃣ COMANDOS PYTEST FRECUENTES

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/02-Automatizados/ -v

# Un archivo
pytest tests/02-Automatizados/test_reactive.py -v

# Una clase
pytest tests/02-Automatizados/test_reactive.py::TestReactiveInit -v

# Un test específico
pytest tests/02-Automatizados/test_reactive.py::TestReactiveInit::test_init_vacio -v

# Modo rápido (sin detalles)
pytest tests/02-Automatizados/ -q

# Con prints visibles
pytest tests/02-Automatizados/ -s
```

### Debugging

```bash
# Ver más detalles si algo falla
pytest tests/02-Automatizados/test_reactive.py -vv

# Traceback completo
pytest tests/02-Automatizados/test_reactive.py --tb=long

# Debugger interactivo (pausa en errores)
pytest tests/02-Automatizados/test_reactive.py --pdb
```

### Git Commits

```bash
# Cuando termines un módulo
git add tests/02-Automatizados/test_reactive.py
git commit -m "test: test_reactive implementado (13 tests)"

# Cuando termines TODO
git add tests/02-Automatizados/test_*.py
git commit -m "test: todos los 96 tests implementados"
```

---

## ✅ CHECKLIST ANTES DE ESCRIBIR TEST

- [ ] Leo la especificación completa
- [ ] Identifico los casos a testear (ARRANGE inputs)
- [ ] Preparo mocks necesarios
- [ ] Llamo la función (ACT)
- [ ] Verifico resultado (ASSERT)
- [ ] Ejecuto el test: `pytest -v`
- [ ] Test pasa ✅

---

## 🚀 Próximo Paso

Ahora que entiendes los conceptos:

1. **Lee:** [02-DE_ESPECIFICACION_A_TESTS.md](02-DE_ESPECIFICACION_A_TESTS.md)
2. **Ejecuta:**
   ```bash
   pytest tests/02-Automatizados/test_reactive.py -v
   ```
3. **Comienza:** Copia template y llena gaps

**¡Vamos!** 🎯
