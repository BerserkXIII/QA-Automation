# 📚 TALLER DE TESTS — TLDRDC

*Guía para implementar tests unitarios siguiendo ISTQB-CTFL y AAA pattern*

---

## 📋 ¿Qué es este taller?

Este es tu espacio para **aprender y practicar** cómo escribir tests profesionales basados en las especificaciones. Aquí encontrarás:

1. **Fixtures compartidas** (`conftest.py`) — Personajes, estado, mocks listos para usar
2. **Ejemplos resueltos** — Cómo implementar un test basado en la spec
3. **Templates vacíos** — Donde tú escribirás los tests

---

## 🎯 Flujo de Trabajo

### 1️⃣ Lee la Especificación
Antes de escribir un test, **lee la especificación** correspondiente:
- `docs/especificaciones/ESPECIFICACION_REACTIVE.md` → tests para reactive.py
- `docs/especificaciones/ESPECIFICACION_EVENTS.md` → tests para events.py
- `docs/especificaciones/ESPECIFICACION_TLDRDC_CORE.md` → tests para calcular_daño, crear_personaje, aplicar_evento

### 2️⃣ Abre el Template
Copia `test_reactive_TEMPLATE.py` como `test_reactive.py` y rellenalo.

### 3️⃣ Sigue AAA Pattern
Cada test tiene 3 secciones:

```python
def test_ejemplo(personaje_base):
    # ═══════════════════════════════════════════════════════
    # ARRANGE: Preparar datos y mocks
    # ═══════════════════════════════════════════════════════
    p = personaje_base.copy()
    p["vida"] = 5
    mock_alerta = Mock()
    
    # ═══════════════════════════════════════════════════════
    # ACT: Ejecutar la función bajo test
    # ═══════════════════════════════════════════════════════
    resultado = mi_funcion(p, mock_alerta)
    
    # ═══════════════════════════════════════════════════════
    # ASSERT: Verificar que el resultado es correcto
    # ═══════════════════════════════════════════════════════
    assert resultado == {"vida": 4}
    assert p["vida"] == 4
    mock_alerta.assert_called_once()
```

---

## 📦 Fixtures Disponibles

### Personajes
```python
def test_ejemplo(personaje_base):
    # Personaje estándar con todos los campos
    p = personaje_base  # vida=10, fuerza=5, destreza=5, etc.

def test_ejemplo_vivo(personaje_vivo):
    # Personaje con vida máxima
    p = personaje_vivo  # vida=25 (vida_max)

def test_ejemplo_critico(personaje_bajo_vida):
    # Personaje con vida crítica (2)
    p = personaje_bajo_vida

def test_ejemplo_ko(personaje_muerto):
    # Personaje KO (vida=0)
    p = personaje_muerto
```

### Estado Global
```python
def test_ejemplo(estado_test, estado_con_armas):
    # estado_test: Estado limpio
    # estado_con_armas: Con daga + espada ya equipadas
    pass
```

### Mocks
```python
def test_ejemplo(mock_alerta, mock_leer_input):
    # Mocks disponibles:
    # - mock_narrar
    # - mock_alerta
    # - mock_exito
    # - mock_sistema
    # - mock_preguntar
    # - mock_leer_input
    # - mock_combate
    # - mock_enemigo_aleatorio
    # - mock_fin_derrota
    
    # Usar con:
    mock_alerta("Prueba")
    mock_alerta.assert_called_once_with("Prueba")
```

### Composite (Todo junto)
```python
def test_ejemplo(game_context):
    # game_context = {
    #     "personaje": personaje_base,
    #     "estado": estado_test,
    #     "armas": armas_global,
    #     "mocks": {
    #         "narrar": mock_narrar,
    #         "alerta": mock_alerta,
    #         ...
    #     }
    # }
    p = game_context["personaje"]
    estado = game_context["estado"]
```

---

## ✍️ Ejemplo Completo: Test de calcular_daño()

Basado en `ESPECIFICACION_TLDRDC_CORE.md` → Test C1.2

```python
def test_calcular_daño_sutil_destreza_baja(armas_global):
    """
    Test C1.2: Tipo sutil + destreza baja
    
    Spec: arma = {"daño": 2, "tipo": "sutil"}, destreza=4
    Resultado esperado: 2 + (4//2) = 4
    """
    # ═══════════════════════════════════════════════════════
    # ARRANGE
    # ═══════════════════════════════════════════════════════
    arma = armas_global["daga"]  # daño=2, tipo="sutil"
    personaje = {
        "destreza": 4,
        "fuerza": 5,
    }
    
    # ═══════════════════════════════════════════════════════
    # ACT
    # ═══════════════════════════════════════════════════════
    from TLDRDC_Prueba1 import calcular_daño
    resultado = calcular_daño(arma, personaje)
    
    # ═══════════════════════════════════════════════════════
    # ASSERT
    # ═══════════════════════════════════════════════════════
    assert resultado == 4, f"Esperado 4, obtenido {resultado}"
```

---

## 🚀 Cómo Ejecutar Tests

### Ejecutar todos los tests
```bash
pytest tests/unit/
```

### Ejecutar tests específicos
```bash
pytest tests/unit/test_reactive.py
pytest tests/unit/test_reactive.py::test_observer_se_dispara
```

### Con verbosidad (ver outputs)
```bash
pytest -v tests/unit/
pytest -s tests/unit/  # Muestra prints
```

### Con cobertura
```bash
pytest --cov=tests/unit tests/unit/
```

---

## 📌 Checklist para escribir un test

- [ ] Leo la especificación completa
- [ ] Identifico los casos a testear (ARRANGE inputs)
- [ ] Preparo mocks necesarios
- [ ] Llamo la función (ACT)
- [ ] Verifico resultado (ASSERT)
- [ ] Verifico que los mocks fueron llamados correctamente
- [ ] Ejecuto el test: `pytest -v`
- [ ] Test pasa ✅

---

## 🐛 Debugging

### El test falla: ¿Qué hago?

1. **Lee el error** — pytest te dice exactamente qué falló
2. **Añade prints** — `print(resultado)` para ver qué pasó
3. **Usa `-s`** — `pytest -s tests/unit/test_*.py` para ver los prints
4. **Revisa la spec** — ¿Tu test está alineado con la especificación?
5. **Pregunta** — Si el código no hace lo que dice la spec, consulta

### Tip: Usar debugger de pytest
```bash
pytest --pdb tests/unit/test_ejemplo.py  # Abre debugger en error
```

---

## 📂 Estructura de Archivos

```
tests/unit/
├── conftest.py                 # ← Fixtures compartidas (NO EDITES)
├── TALLER_README.md            # ← Esta guía
├── test_ejemplo_evento1.py     # ← Ejemplo resuelto (referencia)
├── test_reactive_TEMPLATE.py   # ← Template vacío (copia y llena)
├── test_events_TEMPLATE.py     # ← Template vacío
├── test_core_TEMPLATE.py       # ← Template vacío
├── test_persistencia_TEMPLATE.py
├── test_threading_TEMPLATE.py
├── test_imagen_TEMPLATE.py
└── test_integration_TEMPLATE.py
```

---

## 💡 Tips Profesionales

### 1. Tests DRY (Don't Repeat Yourself)
Si repites código en 3+ tests, crea un helper en `conftest.py`:

```python
@pytest.fixture
def personaje_con_armas(personaje_base):
    """Personaje con 3 armas equipadas."""
    p = personaje_base.copy()
    p["armas"] = {"daga": {}, "espada": {}, "martillo": {}}
    return p
```

### 2. Parametrize para variaciones
```python
@pytest.mark.parametrize("daño,tipo,fuerza,destreza,esperado", [
    (2, "sutil", 5, 6, 5),    # 2 + 3 = 5
    (5, "pesada", 8, 2, 9),   # 5 + 4 = 9
    (5, "mixta", 6, 9, 10),   # 5 + 5 = 10
])
def test_calcular_daño_variaciones(daño, tipo, fuerza, destreza, esperado, armas_global):
    arma = {"daño": daño, "tipo": tipo}
    p = {"fuerza": fuerza, "destreza": destreza}
    from TLDRDC_Prueba1 import calcular_daño
    assert calcular_daño(arma, p) == esperado
```

### 3. Verify Mock Calls
```python
# ¿Fue llamado?
mock_alerta.assert_called()
mock_alerta.assert_called_once()
mock_alerta.assert_called_with("Mensaje")
mock_alerta.assert_not_called()

# ¿Cuántas veces?
assert mock_alerta.call_count == 3
```

### 4. Side Effects para lógica
```python
# Simular múltiples respuestas
mock_leer_input.side_effect = ["xyz", "s"]  # Primer intento falla, segundo pasa
```

---

## 🎓 Recuerda

**ISTQB Principios:**
1. ✅ **Temprano** — Encontrar bugs antes es más barato
2. ✅ **Exhaustivo** — Cubre casos normales, límites, errores
3. ✅ **Aislado** — Cada test prueba UNA cosa
4. ✅ **Reproducible** — El test siempre da el mismo resultado
5. ✅ **Útil** — El test ayuda a entender el código

**AAA Pattern:**
- **Arrange** — Prepara datos
- **Act** — Ejecuta función
- **Assert** — Verifica resultado

---

¿Dudas? Consulta con senior o revisa ejemplos resueltos.

**¡A codear! 🚀**
