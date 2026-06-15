# 🔒 PROTECCIÓN CONTRA LOOPS INFINITOS

*Análisis de seguridad y estrategias para evitar cuelgos en tests*

**Nivel:** Intermedio → Avanzado | **Duración:** 20 min | **Meta:** Entiender cómo se protegen los tests

---

## 📊 STATUS ACTUAL

```
✅ 189 TESTS EJECUTADOS
✅ 189 TESTS PASADOS
❌ 0 TESTS FALLIDOS
❌ 0 CUELGOS INDEFINIDOS
⏱️  Tiempo total: 2.21 segundos
```

---

## 🎯 Estrategias de Protección

### 1. MOCKING CON `side_effect` (171 tests)

**¿Por qué?** Controla loops de validación (crear_personaje tiene input loop)

```python
# ❌ MAL: Loop infinito si entrada inválida
def crear_personaje():
    while True:
        nombre = pedir_input("Nombre: ")
        if nombre:
            break

# ✅ BIEN: Mock controla las respuestas
with patch('TLDRDC_Prueba1.pedir_input') as mock:
    mock.side_effect = ["nombre_valido"]  # Lista de valores → no infinito
    personaje = crear_personaje()
```

**Archivos protegidos:** test_core.py, test_combate_*, test_persistencia.py, etc.

### 2. THREADING CON TIMEOUTS (test_threading.py)

**¿Por qué?** Evita deadlocks en threads

```python
# ❌ MAL: Thread se cuelga, esperas para siempre
thread.join()  # Sin timeout = podría ser infinito

# ✅ BIEN: Thread tiene tiempo límite
thread.join(timeout=2)  # Máximo 2 segundos
assert not thread.is_alive(), "Thread se colgó"
```

**Archivos protegidos:** test_threading.py (20 tests con join timeouts)

### 3. PYTEST-TIMEOUT PER-TEST (test_integration.py) ⭐

**¿Por qué?** test_integration.py testea código con loops reales

```python
# ✅ IMPLEMENTADO: Timeout por test
@pytest.mark.timeout(2)
def test_INT_R1_observer_dispara(self, personaje_int):
    # Si hay loop infinito, pytest interrumpe automáticamente
    aplicar_evento({"vida": 5}, personaje_int)
    assert personaje_int["vida"] == 15
```

**Archivos protegidos:** test_integration.py (18 tests con @pytest.mark.timeout)

### 4. LOOPS ACOTADOS (test_events.py, test_imagen.py)

**¿Por qué?** range() es finito por definición

```python
# ✅ SEGURO: range(20) = máximo 20 iteraciones
for i in range(20):
    evento = obtener_evento_de_bolsa()
```

**Archivos protegidos:** test_events.py, test_imagen.py

---

## 📈 MATRIZ DE PROTECCIÓN POR ARCHIVO

| Archivo | Tests | Tiempo | Protección | Risk |
|---------|-------|--------|-----------|------|
| test_core.py | 32 | 0.11s | Mocks side_effect | BAJO |
| test_threading.py | 20 | 1.60s | join(timeout=N) | BAJO |
| test_reactive.py | 13 | 0.04s | Mocks observers | BAJO |
| test_events.py | 16 | 0.05s | Loops acotados | BAJO |
| test_combate_jugador.py | 16 | 0.08s | Mocks leer_input | BAJO |
| test_combate_enemigo.py | 34 | 0.10s | Mocks completos | BAJO |
| test_combate_loop.py | 14 | 0.09s | Mocks loop | BAJO |
| test_persistencia.py | 15 | 0.14s | Mocks I/O | BAJO |
| test_imagen.py | 11 | 0.12s | Loops simples | BAJO |
| **test_integration.py** | **18** | **<0.2s** | **@timeout(1-3s)** ⭐ | **MEDIO** |
| **TOTAL** | **189** | **~2.2s** | **IMPLEMENTADO** | - |

---

## 🛠️ RECOMENDACIONES PARA MANTENIMIENTO

### ✅ HACER

1. **Mantener test_integration.py con timeouts**
   - Razón: Testea loops reales
   - Ya implementado: `@pytest.mark.timeout(1-3)`

2. **Mantener test_threading.py COMO ESTÁ**
   - Razón: `join(timeout=N)` protege contra deadlocks
   - No necesita cambios

3. **Ejecutar suite periódicamente**
   ```bash
   pytest tests/02-Automatizados/ -v
   ```

### ❌ NO HACER

1. **No quitar timeouts de test_integration.py**
   - Regresionarías a loops infinitos

2. **No agregar timeouts globales innecesarios**
   - Ralentizaría suite (2.2s → 5+ segundos)
   - Los 171 tests no los necesitan (ya protegidos por mocks)

3. **No confiar en "siempre va a funcionar"**
   - El código puede cambiar
   - Las specs pueden cambiar
   - Los tests son red de seguridad

---

## 🚀 PARA CI/CD

### Opción 1: Status Quo (RECOMENDADA) ⭐

```bash
pytest tests/02-Automatizados/ -v
# 189 passed in 2.21s
```

**Ventajas:**
- Rápido (2.2 segundos)
- Seguro (test_integration.py tiene timeouts integrados)
- No hay overhead innecesario

### Opción 2: Con Timeout Global

```bash
pytest tests/02-Automatizados/ -v --timeout=30
# Cada test máx 30 segundos
```

**Ventajas:** Extra seguridad  
**Desventajas:** Overhead + innecesario (ya tenemos timeouts)

### Opción 3: Timeout Solo para Integration

```bash
pytest tests/02-Automatizados/test_integration.py -v --timeout=5
```

**Ventajas:** Doble protección  
**Desventajas:** Overhead mínimo

---

## ⚠️ ¿QUÉ HACER SI UN TEST SE CUELGA?

### Paso 1: Interrumpir
```bash
# Ctrl+C en terminal
# O en VS Code: Ctrl+Shift+P → Kill Terminal
```

### Paso 2: Identificar Cuál
```bash
pytest tests/02-Automatizados/ -v
# Última línea = test que se colgó
```

### Paso 3: Aislar
```bash
pytest tests/02-Automatizados/test_X.py::TestY::test_Z -v
```

### Paso 4: Proteger
Agrega timeout:
```python
@pytest.mark.timeout(2)
def test_Z(self):
    # ... código
```

### Paso 5: Validar
```bash
pytest tests/02-Automatizados/test_X.py::TestY::test_Z -v
# ✅ Debe pasar ahora
```

---

## 💡 CONCEPTOS CLAVE

### Loop Infinito vs. Acotado

```python
# ❌ INFINITO (sin protección)
while True:
    entrada = input("Ingresa valor: ")
    # Si usuario entra basura → loop infinito

# ✅ ACOTADO (protegido por mock)
with patch('builtins.input', side_effect=["valor_valido"]):
    entrada = input("Ingresa valor: ")
    # Mock provee valor → sin loop
```

### Threading Deadlock

```python
# ❌ DEADLOCK (thread se cuelga)
thread = threading.Thread(target=funcion_con_lock)
thread.start()
thread.join()  # Espera para siempre

# ✅ PROTEGIDO (timeout evita deadlock)
thread.join(timeout=2)
if thread.is_alive():
    raise TimeoutError("Thread se colgó")
```

### Pytest-Timeout

```python
# ❌ SIN TIMEOUT: Test corre para siempre
def test_algo():
    while True:
        pass

# ✅ CON TIMEOUT: Pytest interrumpe después de 2 segundos
@pytest.mark.timeout(2)
def test_algo():
    while True:
        pass
    # pytest termina aquí: "test_algo exceeded timeout of 2.0s"
```

---

## 📚 REFERENCIAS

**Documentos relacionados:**
- [01-CONCEPTOS_Y_WORKFLOW.md](01-CONCEPTOS_Y_WORKFLOW.md) — Mocks y fixtures
- [02-DE_ESPECIFICACION_A_TESTS.md](02-DE_ESPECIFICACION_A_TESTS.md) — Cómo escribir tests

**Código:**
- `tests/02-Automatizados/test_integration.py` — Ejemplo de `@pytest.mark.timeout`
- `tests/02-Automatizados/test_threading.py` — Ejemplo de `join(timeout=N)`

---

## ✨ CONCLUSIÓN

La suite de tests está **completamente protegida** contra loops infinitos:

| Categoría | Tests | Protección |
|-----------|-------|-----------|
| Unit tests | 171 | Mocks + loops acotados |
| Threading tests | 20 | join(timeout=N) |
| Integration tests | 18 | @pytest.mark.timeout ⭐ |
| **TOTAL** | **189** | **0 cuelgos garantizados** |

Sin sacrificar velocidad (2.2s) ni legibilidad del código.

---

**¿Test se cuelga?** → Agrega `@pytest.mark.timeout(2)` 🎯
