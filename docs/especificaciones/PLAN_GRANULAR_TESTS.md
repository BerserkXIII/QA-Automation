# Plan Granular de Tests — TLDRDC

*Fecha: 27 de abril de 2026*  
*Versión: 0.1 (Design Phase)*

---

## 1. REACTIVE.PY — Sistema Reactivo

### Función: `Personaje.__init__()`
**Propósito**: Inicializar personaje con watchers vacío y `activo=False`

| Aspecto | Test | Validación | Mocks Necesarios |
|--------|------|-----------|---|
| **U1.1** | Inicialización básica | `_watchers` es dict vacío, `activo=False` | Ninguno |
| **U1.2** | Herencia de dict | Personaje es 100% compatible con dict | Ninguno |
| **U1.3** | Inicialización con datos | Personaje("vida": 10) crea dict con datos | Ninguno |

**Test File**: `tests/unit/test_reactive_init.py`

---

### Función: `Personaje.observe(field, callback)`
**Propósito**: Registrar callback para un campo

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U2.1** | Registrar único callback | `observe("vida", cb)` → `_watchers["vida"] = cb` | Mock callback |
| **U2.2** | Segundo observe sobrescribe | `observe("vida", cb1)` luego `observe("vida", cb2)` → cb2 activo, cb1 perdido | Mock callback |
| **U2.3** | Múltiples campos | `observe("vida", cb1)` + `observe("fuerza", cb2)` → ambos almacenados | Mock callback |

**Test File**: `tests/unit/test_reactive_observe.py`

---

### Función: `Personaje.__setitem__(key, value)`
**Propósito**: Asignar valor y disparar callback si cambió

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U3.1** | Valor idéntico no dispara callback | `p["vida"] = 10` dos veces → callback solo 1x | Mock callback spy |
| **U3.2** | Valor nuevo dispara callback | `p["vida"] = 5` → `p["vida"] = 10` → callback dispara con 10 | Mock callback spy |
| **U3.3** | Sin observador, no error | Asignar sin `observe()` previo → funciona sin error | Ninguno |
| **U3.4** | Con `activo=False`, no dispara | `p.activo = False` → asignación no dispara callback | Mock callback spy |
| **U3.5** | Con `activo=True`, dispara | `p.activo = True` → asignación dispara callback | Mock callback spy |

**Test File**: `tests/unit/test_reactive_setitem.py`

---

## 2. EVENTS.PY — Sistema de Eventos

### Función: `rellenar_bolsa_eventos()`
**Propósito**: Llenar bolsa con 20 eventos únicos (IDs 1-20)

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U4.1** | Bolsa llena con 20 eventos | Llamar función → len(bolsa) == 20 | Ninguno |
| **U4.2** | Eventos únicos | Todos IDs 1-20 presentes una vez | Ninguno |
| **U4.3** | Llamada múltiple idempotente | Llamar 2x → bolsa sigue teniendo 20 | Ninguno |

**Test File**: `tests/unit/test_events_bolsa.py`

---

### Función: `obtener_evento_de_bolsa()`
**Propósito**: Sacar evento de bolsa, rellenar si vacía

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U5.1** | Obtiene evento válido | Retorna ID 1-20 | Ninguno |
| **U5.2** | Decrementa bolsa | Bolsa pasa de 20 a 19 | Ninguno |
| **U5.3** | Rellenamiento automático | Sacar 20 eventos → bolsa rellenada → evento 21 es válido | Ninguno |
| **U5.4** | Sin repetición inmediata | Evento X no aparece 2 veces seguidas | Estadístico (50+ iteraciones) |

**Test File**: `tests/unit/test_events_bolsa.py`

---

### Función: `_evento_N(personaje)` (ej. `_evento_1`, `_evento_2`, ...)
**Propósito**: Procesar evento específico (narrativa + lógica)

**Ejemplo con `_evento_1`**:

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U6.1** | Retorna dict válido | `_evento_1(p)` retorna `{"vida": -1, ...}` | Personaje mock |
| **U6.2** | Lógica condicional | Si `fuerza >= 8` retorna X; si < 8 retorna Y | Personaje mock con stats |
| **U6.3** | Dependencias inyectadas | Si `narrar` no está inyectado, maneja gracefully | Mock narrar |
| **I6.4** | Con aplicar_evento() | `aplicar_evento(_evento_1(p), p)` aplica correctamente | Mock personaje reactivo |

**Test File**: `tests/unit/test_events_evento_<N>.py` (p.ej. `test_events_evento_1.py`)

---

## 3. TLDRDC_PRUEBA1.PY — Monolito Core

### Función: `calcular_daño(arma, personaje)`
**Propósito**: Calcular daño según arma + stats

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U7.1** | Tipo `sutil` suma destreza//2 | `calcular_daño("daga", p)` con destreza=10 → daño base + 5 | Personaje mock |
| **U7.2** | Tipo `pesada` suma fuerza//2 | `calcular_daño("martillo", p)` con fuerza=8 → daño base + 4 | Personaje mock |
| **U7.3** | Tipo `mixta` suma (fuerza+destreza)//3 | `calcular_daño("cimitarra", p)` → fórmula correcta | Personaje mock |
| **U7.4** | Bonificación multiplicador | Arma con `multiplicador: 1.5` se aplica | Personaje mock |
| **U7.5** | Auto-daño | `"Hacha Maldita"` inflige 1 daño al personaje | Personaje mock reactivo |
| **U7.6** | Mínimo 1 daño | Nunca retorna < 1 | Personaje mock con stats bajos |

**Test File**: `tests/unit/test_calcular_daño.py`

---

### Función: `crear_personaje()`
**Propósito**: Crear personaje nuevo con stats iniciales

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U8.1** | Stats en rango válido | Fuerza [1-9], Destreza = 10-Fuerza | Mock input |
| **U8.2** | Armadura según destreza | Destreza ≥9 → 4; ≥6 → 2; ≥3 → 1; rest → 0 | Mock input |
| **U8.3** | Inventario vacío | `armas: {}` al inicio | Mock input |
| **U8.4** | Rechaza entrada inválida | Fuerza=0 o 10 → repregunta | Mock input |
| **U8.5** | Retorna Personaje reactivo | Objeto hereda de dict + tiene observe() | Mock input |

**Test File**: `tests/unit/test_crear_personaje.py`

---

### Función: `aplicar_evento(evento_dict, personaje)`
**Propósito**: Aplicar cambios de evento al personaje

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U9.1** | Vida no baja de 0 | Aplicar `{"vida": -100}` → vida = 0 (clamp) | Personaje mock |
| **U9.2** | Vida a 0 llama fin_derrota() | Vida llega 0 → `fin_derrota()` llamado, early return | Personaje mock, mock fin_derrota |
| **U9.3** | Pociones se clampean | Aplicar `{"pociones": +100}` → pociones = max | Personaje mock |
| **U9.4** | Armadura se clampea | Aplicar `{"armadura": -100}` → armadura = 0 | Personaje mock |
| **U9.5** | Stats no superan máximo | Aplicar `{"fuerza": +50}` → fuerza = 20 | Personaje mock |
| **U9.6** | Arma válida se añade | Aplicar `{"armas": {"daga": {}}}` → personaje.armas tiene daga | Personaje mock reactivo |
| **U9.7** | Arma desconocida genera alerta | Aplicar `{"armas": {"arma_fake": {}}}` → alerta emitida | Mock emitir |
| **I9.8** | Observer se dispara | Aplicar evento que sube vida → callback observer ejecutado | Personaje reactivo real |

**Test File**: `tests/unit/test_aplicar_evento.py` + `tests/integration/test_aplicar_evento_reactive.py`

---

### Función: `guardar_partida(personaje)`
**Propósito**: Guardar partida a JSON de forma atómica

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U10.1** | Archivo creado | Llamar → archivo existe en ruta correcta | Mock path |
| **U10.2** | JSON válido | Contenido es JSON parseable | Tmp file |
| **U10.3** | Integridad de datos | Todos los campos del personaje presentes | Tmp file + personaje mock |
| **I10.4** | Atomicidad | Escribir a temp, luego os.replace() | Tmp file |
| **I10.5** | No corrupción si falla | Simular error durante escritura → archivo original intacto | Tmp file con error mock |

**Test File**: `tests/unit/test_guardar_partida.py` + `tests/integration/test_guardar_atomico.py`

---

### Función: `cargar_partida()`
**Propósito**: Cargar partida guardada

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U11.1** | Retorna dict/personaje | Archivo existe → retorna Personaje válido | Tmp JSON file |
| **U11.2** | Migración antiguo save | `eventos_superados` (lista) → se convierte a int | Tmp JSON antiguo |
| **U11.3** | Stats restaurados | Todos los campos (vida, fuerza, armas) correctos | Tmp JSON file |
| **U11.4** | Archivo no existe | Sin archivo → retorna None o nuevo personaje | Mock path |

**Test File**: `tests/unit/test_cargar_partida.py`

---

## 4. UI_ESTRUCTURA.PY — Sistema de Threading

### Función: `_Bridge.esperar()`
**Propósito**: Bloquear hilo de juego hasta recibir input

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U12.1** | Event.wait() bloqueado | Antes de `recibir()` → espera | Mock threading.Event |
| **U12.2** | Event.set() desbloquea | Llamar `recibir()` → `esperar()` retorna | Mock threading.Event |
| **U12.3** | Timeout si implementado | Si timeout=5s → retorna tras 5s | Mock threading.Event |

**Test File**: `tests/unit/test_bridge_esperar.py`

---

### Función: `_Bridge.recibir(texto)`
**Propósito**: Enviar input y desbloquear juego

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U13.1** | Almacena input | Llamar `recibir("test")` → `self.valor = "test"` | Ninguno |
| **U13.2** | Llama Event.set() | Tras `recibir()` → Event está set | Mock threading.Event |

**Test File**: `tests/unit/test_bridge_recibir.py`

---

### Función: `polling()` (en Vista)
**Propósito**: Procesar cola de mensajes del juego en main thread

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U14.1** | Procesa mensaje 1x | Mensaje en cola → se emite una sola vez | Mock cola, mock typewriter |
| **U14.2** | No procesa si `_ocupado=True` | Durante typewriter → no procesa | Mock cola, mock ocupado |
| **U14.3** | Reschedule después del mensaje | Tras procesar → `self.root.after(50, polling)` | Mock root |

**Test File**: `tests/unit/test_polling.py`

---

## 5. UI_IMAGEN_MANAGER.PY — Gestión de Imágenes

### Función: `ImagenManager.cargar_imagen(ruta, tamaño)`
**Propósito**: Cargar y cachear imagen con redimensión

| Aspecto | Test | Validación | Mocks |
|--------|------|-----------|---|
| **U15.1** | Imagen válida cargada | PNG existente → retorna PIL Image | Tmp PNG file |
| **U15.2** | Redimensión aplicada | Tamaño=50x50 → imagen es 50x50 | Tmp PNG file |
| **U15.3** | Caché funciona | Llamar 2x con misma ruta → retorna cached sin releer | Tmp PNG file |
| **U15.4** | Imagen inexistente retorna None | Ruta fake → retorna None sin excepción | Mock path |
| **U15.5** | PNG corrupto maneja gracefully | Archivo PNG inválido → None o excepción capturada | Tmp invalid PNG |

**Test File**: `tests/unit/test_imagen_manager.py`

---

## 6. TESTS DE INTEGRACIÓN (Ejemplos)

### Test: `reactive.py + aplicar_evento()`
**Scenario**: Evento sube vida → Observer se dispara → callback ejecuta

| Paso | Validación |
|------|-----------|
| 1. Crear Personaje reactivo | `p = Personaje({"vida": 10})` |
| 2. Registrar observer | `p.observe("vida", callback_mock)` |
| 3. Activar reactividad | `p.activo = True` |
| 4. Aplicar evento | `aplicar_evento({"vida": +5}, p)` |
| 5. Verificar callback | `callback_mock.assert_called_once_with(15)` |

**Test File**: `tests/integration/test_reactive_eventos.py`

---

### Test: `_Bridge + threading`
**Scenario**: Hilo juego espera input, hilo UI envía, se sincronizan

| Paso | Validación |
|------|-----------|
| 1. Crear _Bridge | `bridge = _Bridge()` |
| 2. Thread juego llama esperar() | En thread separado |
| 3. Thread UI llama recibir("s") | En main thread |
| 4. Juego continúa | `esperar()` retorna con valor |
| 5. Validar sincronización | Sin race conditions, timeout OK |

**Test File**: `tests/integration/test_threading_bridge.py`

---

## 7. RESUMEN POR TIPO

**Unit Tests necesarios (15 test files)**:
- `test_reactive_init.py`, `test_reactive_observe.py`, `test_reactive_setitem.py`
- `test_events_bolsa.py`
- `test_events_evento_1.py` ... `test_events_evento_20.py` (20 files, pero podemos agrupar en 3-4)
- `test_calcular_daño.py`
- `test_crear_personaje.py`
- `test_aplicar_evento.py`
- `test_guardar_partida.py`, `test_cargar_partida.py`
- `test_bridge_*.py`, `test_polling.py`
- `test_imagen_manager.py`

**Integration Tests necesarios (5-6 test files)**:
- `test_reactive_eventos.py` (observer + aplicar_evento)
- `test_threading_bridge.py` (sync)
- `test_ui_sprites.py` (imagen_manager + UI)
- `test_guardar_atomico.py` (guardar + thread-safety)
- `test_flujo_evento_completo.py` (evento → aplicar → UI)

**E2E Tests (2-3)**:
- `test_partida_corta.py` (create → evento → combate → save)

---

## 8. SIGUIENTE PASO

Con este plan granular, ahora redactaremos **ARQUITECTURA_TESTS.md**:
- Estructura común Arrange-Act-Assert
- Fixtures reutilizables (mock_personaje, mock_ui, etc.)
- Convenciones de inyección de dependencias
- Boilerplate conftest.py

¿Algún cambio en este plan antes de redactar ARQUITECTURA?
