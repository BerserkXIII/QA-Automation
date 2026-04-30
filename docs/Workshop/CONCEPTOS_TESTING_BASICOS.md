# 📖 CONCEPTOS DE TESTING BÁSICOS

*Guía para entender qué hace cada línea de un test*

**Nivel:** Principiante (Python básico)  
**Tiempo:** 30-45 minutos  
**Meta:** Entender `test_reactive.py` y poder escribir tests desde cero

---

## 1. ¿QUÉ ES UN TEST?

### Definición Simple

Un **test** es un programa que verifica si otra parte del código funciona correctamente.

```python
# CÓDIGO NORMAL (lo que quieres probar)
def sumar(a, b):
    return a + b

# TEST (verifica que sumar() funciona bien)
def test_sumar():
    resultado = sumar(2, 3)
    print(resultado)  # Debería imprimir: 5
```

### Diferencia Importante

```python
# ❌ MAL: No es un test, solo ejecuta código
sumar(2, 3)

# ✅ BIEN: Es un test, verifica el resultado
resultado = sumar(2, 3)
assert resultado == 5  # "Verifica que el resultado sea 5"
```

**¿La diferencia?** El test **verifica** que el resultado es correcto.

---

## 2. `ASSERT` — LA HERRAMIENTA MÁS IMPORTANTE

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
assert 5 == 3          # ❌ ERROR: 5 no es igual a 3
assert "hola" == "adiós"  # ❌ ERROR: No son iguales
```

### Operadores Útiles para Assert

```python
# Igualdad
assert personaje["vida"] == 10        # ¿Es igual a 10?

# Desigualdad
assert personaje["vida"] != 0         # ¿No es igual a 0?

# Mayor/Menor
assert personaje["vida"] > 5          # ¿Es mayor que 5?
assert personaje["vida"] < 20         # ¿Es menor que 20?

# Pertenencia (¿está dentro?)
assert "vida" in personaje            # ¿"vida" existe en el dict?
assert "vida" not in personaje        # ¿"vida" NO existe?

# Tipo
assert isinstance(personaje, dict)    # ¿Es un diccionario?
assert isinstance(personaje, str)     # ¿Es un string? (falso)

# Longitud
assert len(personaje) == 5            # ¿Tiene 5 elementos?
```

### Assert con Funciones (Muy Importante)

```python
# Mock es una "función simulada" que registra si fue llamada
callback = Mock()

# Verificar que fue llamado
assert callback.called              # ¿Fue ejecutado alguna vez?

# Verificar que fue llamado UNA SOLA VEZ
callback.assert_called_once()       # Debe ejecutarse exactamente 1 vez

# Verificar que fue llamado CON UN PARÁMETRO
callback.assert_called_with(15)     # ¿Se ejecutó con parámetro 15?

# Verificar que NUNCA fue llamado
callback.assert_not_called()        # ¿NO se ejecutó nunca?
```

**Esto es crucial para entender `test_reactive.py`.**

---

## 3. AAA PATTERN — CÓMO ESTRUCTURAR UN TEST

### ¿Qué Es?

AAA = **Arrange, Act, Assert**

Es la estructura estándar de TODOS los tests profesionales.

```
┌─────────────────────────────────────┐
│  ARRANGE: Preparar datos            │ (Setup)
├─────────────────────────────────────┤
│  ACT: Ejecutar lo que se prueba     │ (Execute)
├─────────────────────────────────────┤
│  ASSERT: Verificar resultado        │ (Verify)
└─────────────────────────────────────┘
```

### Ejemplo Real: Sumar Números

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

### Ejemplo Real: Personaje con Vida

```python
def test_personaje_tiene_vida_inicial():
    # ARRANGE: Crear un personaje
    p = {"nombre": "Hero", "vida": 10}
    
    # ACT: Obtener la vida
    vida = p["vida"]
    
    # ASSERT: Verificar que es 10
    assert vida == 10
```

### Ejemplo Real: Cambiar Vida (Más Complejo)

```python
def test_personaje_recibe_danio():
    # ARRANGE: Crear personaje y función para aplicar daño
    personaje = {"nombre": "Hero", "vida": 10}
    
    def aplicar_danio(p, danio):
        p["vida"] -= danio
    
    # ACT: Aplicar daño
    aplicar_danio(personaje, 3)
    
    # ASSERT: Verificar que la vida bajó
    assert personaje["vida"] == 7
```

---

## 4. FIXTURES — REUTILIZAR DATOS

### ¿Qué Es Un Fixture?

Un **fixture** es **datos preparados** que usas en múltiples tests.

Sin fixtures:
```python
def test_1():
    personaje = {"nombre": "Hero", "vida": 10, "fuerza": 5}
    # ... código del test

def test_2():
    personaje = {"nombre": "Hero", "vida": 10, "fuerza": 5}
    # ... código del test

# Repetido 50 veces... 😞
```

Con fixtures:
```python
# Define UNA VEZ
@pytest.fixture
def personaje():
    return {"nombre": "Hero", "vida": 10, "fuerza": 5}

# Usa en todos lados
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

# 1. Definir fixture (con @pytest.fixture)
@pytest.fixture
def personaje_base():
    """Este fixture crea un personaje listo para usar."""
    return {
        "nombre": "TestPlayer",
        "vida": 10,
        "fuerza": 5,
    }

# 2. Usar en test (parámetro automático)
def test_personaje_existe(personaje_base):
    # personaje_base se inyecta automáticamente
    assert personaje_base["vida"] == 10
    assert personaje_base["fuerza"] == 5

# 3. Pytest automáticamente:
# - Crea personaje_base antes de ejecutar el test
# - Lo pasa al test
# - Lo limpia después
```

### Ventajas

```python
# SIN fixture: Código repetido, difícil de cambiar
def test_1():
    p = {"vida": 10}; assert ...
def test_2():
    p = {"vida": 10}; assert ...
def test_3():
    p = {"vida": 10}; assert ...

# CON fixture: Código DRY (Don't Repeat Yourself)
@pytest.fixture
def p():
    return {"vida": 10}

def test_1(p): assert ...
def test_2(p): assert ...
def test_3(p): assert ...
# Si cambias el fixture, todos los tests se actualizan automáticamente
```

---

## 5. MOCKS — SIMULAR FUNCIONES

### ¿Por Qué Existen?

A veces necesitas simular funciones que:
- Hace cosas complejas
- Están en otra parte del código
- Tienes que verificar si fue llamada

```python
# Función real (complicada)
def enviar_email(destinatario, asunto):
    # Conectar a servidor
    # Validar email
    # Enviar
    # Registrar
    pass

# En un test, NO quieres enviar emails de verdad
# Quieres simular que se envió, verificar que se llamó correctamente
```

### Mock Simple

```python
from unittest.mock import Mock

# Crear un mock (función falsa)
mock_callback = Mock()

# Es una función que registra si fue llamada
mock_callback()              # Ejecutar
print(mock_callback.called)  # True (fue ejecutado)

# Crear con valor de retorno
mock_greeting = Mock(return_value="Hola")
resultado = mock_greeting()
assert resultado == "Hola"
```

### Verificar Si Fue Llamado

```python
from unittest.mock import Mock

callback = Mock()

# ❌ No fue llamado aún
assert not callback.called

# Llamar al callback
callback(5)

# ✅ Ahora fue llamado
assert callback.called
assert callback.call_count == 1  # Llamado 1 vez

# Verificar con QUÉ parámetro fue llamado
callback.assert_called_with(5)   # ¿Se ejecutó con 5?
callback.assert_called_with(3)   # ❌ Error: Se ejecutó con 5, no 3
```

### Ejemplo Real: Verificar Que UI Se Actualiza

```python
from unittest.mock import Mock

# ARRANGE: Crear mock que simula actualización de UI
actualizar_barra_vida = Mock()

# Crear personaje que "sabe" que debe actualizar UI
class Personaje(dict):
    def __init__(self, datos):
        super().__init__(datos)
        self.actualizar = actualizar_barra_vida
    
    def recibir_danio(self, danio):
        self["vida"] -= danio
        self.actualizar(self["vida"])  # Llamar actualización

# ACT
p = Personaje({"vida": 10})
p.recibir_danio(3)

# ASSERT
actualizar_barra_vida.assert_called_once_with(7)  # ¿Se llamó con 7?
```

---

## 6. CLASES EN TESTS

### ¿Por Qué Clases?

Tests están organizados en **clases** para agrupar tests relacionados.

```python
# ❌ SIN clases (desorganizado)
def test_init_1(): pass
def test_init_2(): pass
def test_init_3(): pass
def test_observe_1(): pass
def test_observe_2(): pass
def test_setitem_1(): pass
# 50 funciones sueltas... confuso

# ✅ CON clases (organizado)
class TestInit:
    def test_1(self): pass
    def test_2(self): pass
    def test_3(self): pass

class TestObserve:
    def test_1(self): pass
    def test_2(self): pass

class TestSetitem:
    def test_1(self): pass
```

### Estructura

```python
import pytest

class TestReactiveInit:
    """Agrupa tests de inicialización"""
    
    def test_init_vacio(self):
        """Test 1 de InitReactive"""
        # ... código
        assert ...
    
    def test_init_con_datos(self):
        """Test 2 de InitReactive"""
        # ... código
        assert ...

class TestObserve:
    """Agrupa tests de observadores"""
    
    def test_observe_registro(self):
        """Test 1 de Observe"""
        # ... código
        assert ...
```

### Fixtures en Clases

```python
@pytest.fixture
def personaje():
    return {"vida": 10}

class TestPersonaje:
    def test_1(self, personaje):  # ← personaje se inyecta
        assert personaje["vida"] == 10
    
    def test_2(self, personaje):  # ← Se crea nuevo para cada test
        personaje["vida"] = 5
        assert personaje["vida"] == 5
    
    # En test_3, personaje vuelve a tener vida=10 (fixture es fresco)
    def test_3(self, personaje):
        assert personaje["vida"] == 10
```

---

## 7. EJEMPLO COMPLETO COMENTADO LÍNEA POR LÍNEA

### Código Que Vamos a Testear

```python
class Personaje(dict):
    """Un diccionario que puede notificar cambios"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._watchers = {}        # Diccionario de observadores
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
import pytest
from unittest.mock import Mock

class TestReactiveInit:
    
    def test_init_vacio(self):
        """
        Test U1.1: Crear personaje vacío
        
        ¿Qué verifica?
        - Que puedo crear un Personaje sin datos
        - Que no tiene watchers
        - Que está inactivo
        """
        
        # ─────────────────────────────────────
        # ARRANGE: Preparar (no hay nada que preparar aquí)
        # ─────────────────────────────────────
        # Solo vamos a crear un Personaje vacío
        
        # ─────────────────────────────────────
        # ACT: Ejecutar lo que queremos probar
        # ─────────────────────────────────────
        p = Personaje()
        # Ahora p es un Personaje vacío
        
        # ─────────────────────────────────────
        # ASSERT: Verificar que funciona correctamente
        # ─────────────────────────────────────
        
        # ¿p es un dict?
        assert isinstance(p, dict)
        
        # ¿p está vacío (0 elementos)?
        assert len(p) == 0
        
        # ¿p._watchers es un dict?
        assert isinstance(p._watchers, dict)
        
        # ¿p._watchers está vacío?
        assert len(p._watchers) == 0
        
        # ¿p.activo es False?
        assert p.activo == False
```

### Test 2: Con Datos

```python
    def test_init_con_datos(self):
        """
        Test U1.2: Crear personaje con datos
        
        ¿Qué verifica?
        - Que puedo pasar datos al crear
        - Que los datos se guardan correctamente
        - Que watchers sigue vacío
        - Que sigue inactivo
        """
        
        # ─────────────────────────────────────
        # ARRANGE: Preparar datos iniciales
        # ─────────────────────────────────────
        datos = {"vida": 10, "fuerza": 5}
        # datos es un dict normal con vida y fuerza
        
        # ─────────────────────────────────────
        # ACT: Crear Personaje con esos datos
        # ─────────────────────────────────────
        p = Personaje(datos)
        # Ahora p tiene los datos de vida y fuerza
        
        # ─────────────────────────────────────
        # ASSERT: Verificar que los datos se guardaron
        # ─────────────────────────────────────
        
        # ¿p["vida"] es 10?
        assert p["vida"] == 10
        
        # ¿p["fuerza"] es 5?
        assert p["fuerza"] == 5
        
        # ¿p tiene exactamente 2 elementos?
        assert len(p) == 2
        
        # ¿_watchers sigue vacío (no copió observadores)?
        assert p._watchers == {}
        
        # ¿Sigue inactivo?
        assert p.activo == False
```

### Test 3: Observer (Lo Complejo)

```python
    def test_observe_sobrescribe(self):
        """
        Test U2.3: Si registras dos observadores para el mismo field,
        el segundo SOBRESCRIBE al primero
        
        ¿Qué verifica?
        - Que registro callback_1 para "vida"
        - Que registro callback_2 para "vida" (sobrescribe)
        - Que cuando cambia vida, se ejecuta callback_2 (no callback_1)
        """
        
        # ─────────────────────────────────────
        # ARRANGE: Preparar
        # ─────────────────────────────────────
        
        # Crear dos mocks (funciones simuladas)
        callback_1 = Mock()  # Primera función simulada
        callback_2 = Mock()  # Segunda función simulada
        
        # Crear personaje
        p = Personaje()
        
        # ─────────────────────────────────────
        # ACT: Ejecutar lo que queremos probar
        # ─────────────────────────────────────
        
        # Registrar primer observador
        p.observe("vida", callback_1)
        # Ahora p._watchers = {"vida": callback_1}
        
        # Registrar segundo observador (sobrescribe)
        p.observe("vida", callback_2)
        # Ahora p._watchers = {"vida": callback_2}  (callback_1 desapareció)
        
        # Cambiar la vida
        p["vida"] = 15
        # Esto debe ejecutar callback_2 (con parámetro 15)
        # callback_1 no debe ejecutarse
        
        # ─────────────────────────────────────
        # ASSERT: Verificar que funcionó
        # ─────────────────────────────────────
        
        # ¿callback_2 fue ejecutado?
        assert callback_2.called  # True
        
        # ¿callback_2 fue ejecutado exactamente 1 vez?
        callback_2.assert_called_once()
        
        # ¿callback_2 se ejecutó con el parámetro 15?
        callback_2.assert_called_with(15)
        
        # ¿callback_1 NUNCA se ejecutó?
        callback_1.assert_not_called()
```

---

## 8. CÓMO LEER UN TEST

### Paso a Paso

Cuando veas un test, lee así:

```python
def test_sumar_positivos(self, personaje_base):  # ← Nombre del test (qué prueba)
    """Test X.Y: Descripción clara de qué verifica"""
    
    # ARRANGE: ¿Qué preparo? (responde: personaje_base viene del fixture)
    # → personaje_base es un dict {"vida": 10, ...}
    
    # ACT: ¿Qué ejecuto? (responde: lo que quiero probar)
    p = personaje_base
    p["vida"] = 15
    # → Cambié la vida a 15
    
    # ASSERT: ¿Qué verifica? (responde: el resultado es correcto)
    assert p["vida"] == 15
    # → Verifica que la vida sea 15
```

### Checklist para Leer Tests

```
□ ¿Cuál es el nombre del test? (test_*)
□ ¿Cuál es el docstring? ("""...""")
□ ¿Qué fixtures usa? (parámetros)
□ ¿Dónde empieza ARRANGE? (preparación)
□ ¿Dónde empieza ACT? (ejecución)
□ ¿Dónde empieza ASSERT? (verificación)
□ ¿Cuántos asserts hay? (mínimo 1, máximo 5-10)
```

---

## ✅ RESUMEN

| Concepto | Definición | Ejemplo |
|----------|-----------|---------|
| **Test** | Verifica si código funciona | `def test_sumar():` |
| **Assert** | Verifica si algo es verdadero | `assert 5 == 5` |
| **AAA** | Estructura: Arrange, Act, Assert | Prepare → Execute → Verify |
| **Fixture** | Datos reutilizables | `@pytest.fixture def p():` |
| **Mock** | Función simulada | `Mock()` |
| **Clase** | Agrupa tests relacionados | `class TestInit:` |

---

## 🎯 Próximo Paso

Ahora que entiendes los conceptos:

1. **Abre:** `test_reactive.py`
2. **Lee cada test** usando el checklist anterior
3. **Identifica:**
   - ¿Dónde está ARRANGE?
   - ¿Dónde está ACT?
   - ¿Dónde está ASSERT?
4. **Pregunta:** "¿Por qué este test verifica esto?"

---

**¿Preguntas? Relée este documento. Si algo no queda claro, eso significa que el documento necesita mejorar.** 🚀
