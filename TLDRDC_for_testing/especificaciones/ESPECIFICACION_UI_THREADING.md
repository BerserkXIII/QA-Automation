# Especificación de Tests — UI & THREADING (_Bridge, _iniciar_polling, pedir_input)

*Versión: 0.3 (Test Spec — Revisado contra código real)*

---

## RESUMEN EJECUTIVO

Sistema de **sincronización de hilos** para Tkinter + juego:
1. **_Bridge** — Objeto global que sincroniza entrada/salida entre hilo juego y hilo UI
2. **pedir_input()** — Función que reemplaza input() builtin; bloquea thread juego sin freezear UI
3. **_iniciar_polling()** — Método Vista que procesa cola_mensajes cada 50ms en main thread

**CRÍTICO**: Sin esto, UI se congela durante narración o lectura de input. Implementación real en TLDRDC_Prueba1.py líneas ~150-220 y ~5657

---

## MATRIZ DE PRUEBAS

| Test ID | Componente | Validación |
|---------|-----------|------------|
| T1.1 | _Bridge.__init__ | Inicialización de _evento y _valor |
| T1.2 | _Bridge.esperar | Event.wait() + clear() + retorna _valor |
| T1.3 | _Bridge.recibir | Asigna _valor y set() event |
| T1.4 | _Bridge - 2do esperar | Clear() resetea para siguiente ciclo |
| T2.1 | pedir_input - emite prompt | Llama emitir("preguntar", prompt) |
| T2.2 | pedir_input - habilita input | Llama emitir("habilitar_input") |
| T2.3 | pedir_input - bloquea en bridge | Llama bridge.esperar() y retorna |
| T3.1 | _iniciar_polling - primer tick | Procesa 1 mensaje si _ocupado=False |
| T3.2 | _iniciar_polling - reschedule | Llama root.after(50, ...) siempre |
| T3.3 | _iniciar_polling - cola vacía | Sin error si cola_mensajes vacía |
| T3.4 | _iniciar_polling - espera busy | No procesa si _ocupado=True |
| T3.5 | procesar_mensaje - router | Mapea tipo → método Vista correcto |
| T3.6 | Thread-safe | Cola deque sin race conditions |

---

## CLASE: `_Bridge`

**¿Qué hace?**
- Encapsula `threading.Event` para sincronización thread-safe
- Instancia global: `_bridge = _Bridge()` (línea ~201)
- Métodos:
  - `esperar()` — Bloquea hilo juego hasta recibir input
  - `recibir(texto)` — Envía input desde UI, desbloquea juego

**Atributos privados** (línea ~153-154):
```python
self._evento = threading.Event()    # Sincronización
self._valor = ""                    # String vacío inicial
```

### Función: `_Bridge.esperar()`

**¿Qué hace?** (línea ~159-166)
1. Llama `self._evento.wait()` → Bloquea thread trabajador
2. Cuando `recibir()` es llamado, set() desbloquea
3. Llama `self._evento.clear()` para resetear el Event
4. Retorna el valor almacenado en `self._valor`

**CRÍTICO**: `event.clear()` es esencial; sin él, siguiente esperar() retorna inmediatamente

#### Test T1.1: Inicialización
```
ARRANGE: bridge = _Bridge()
ACT: (inspect attributes)
ASSERT:
  - bridge._evento es threading.Event()
  - bridge._valor == ""  (string vacío inicial)
```

#### Test T1.2: Bloquea hasta recibir()
```
ARRANGE:
  - bridge = _Bridge()
  - Timer thread: sleep(0.1); bridge.recibir("test")
ACT:
  - t_start = time.time()
  - resultado = bridge.esperar()
  - t_elapsed = time.time() - t_start
ASSERT:
  - t_elapsed ≥ 0.095 (esperó bloqueado min)
  - resultado == "test"
```

#### Test T1.3: Clear event para siguiente ciclo
```
ARRANGE:
  - bridge = _Bridge()
  - bridge._evento.set()  (pre-set el event)
ACT:
  - resultado1 = bridge.esperar()  (retorna, hace clear())
ASSERT:
  - resultado1 retorna sin esperar
  - bridge._evento.is_set() == False (clear() funcionó)
```

---

### Función: `_Bridge.recibir(texto)`

**¿Qué hace?** (línea ~168-174)
1. Asigna `self._valor = texto`
2. Llama `self._evento.set()` para desbloquear esperar()

**Orden es importante**: Primero asignar valor, luego set() event

#### Test T1.4: Almacena valor
```
ARRANGE: bridge = _Bridge()
ACT: bridge.recibir("hello")
ASSERT: bridge._valor == "hello"
```

#### Test T1.5: Set event para desbloquear
```
ARRANGE:
  - bridge = _Bridge()
  - Thread 1: esperar() (bloqueado)
  - Timer: espera 100ms, recibir("x")
ACT:
  - Ejecutar threads
ASSERT:
  - esperar() retorna tras ~100ms
  - Evento fue set (sin timeout)
  - Resultado == "x"
```

#### Test T1.6: Sin race condition (multiples ciclos)
```
ARRANGE:
  - bridge = _Bridge()
ACT:
  - For i in range(10):
      - Thread 1: esperar()
      - Timer(100ms): recibir(f"input_{i}")
ASSERT:
  - Todos los ciclos retornan valor correcto
  - Sin AttributeError o race condition
  - Sin deadlock
```

---

## FUNCIÓN: `pedir_input(prompt="")`

**¿Qué hace?** (Reemplaza builtin input(); línea ~198-207)
1. Si `prompt` no vacío: Llama `emitir("preguntar", prompt)` → muestra en UI
2. Llama `emitir("habilitar_input")` → habilita input field en Vista
3. Llama `_bridge.esperar()` → **BLOQUEA thread juego**
4. Vista procesa con _iniciar_polling(), usuario envía input
5. Vista llama `_bridge.recibir(text)` → desbloquea esperar()
6. pedir_input() retorna al juego con el input

**CRÍTICO**: pedir_input() bloquea el thread TRABAJADOR, no el main thread Tkinter

#### Test T2.1: Emite prompt si no vacío
```
ARRANGE:
  - Mock emitir()
  - Timer thread para unbloquear bridge
ACT:
  - pedir_input("¿Qué haces?")
ASSERT:
  - emitir.assert_any_call("preguntar", "¿Qué haces?")
```

#### Test T2.2: Omite prompt si vacío
```
ARRANGE: Mock emitir()
ACT: pedir_input("")
ASSERT:
  - emitir.assert_not_called("preguntar")
  - emitir.assert_called_with("habilitar_input")  (solo este)
```

#### Test T2.3: Habilita input field
```
ARRANGE: Mock emitir()
ACT: pedir_input("test")
ASSERT:
  - emitir.assert_any_call("habilitar_input")
```

#### Test T2.4: Bloquea en bridge
```
ARRANGE:
  - Mock bridge.esperar() para retornar "respuesta"
ACT:
  - resultado = pedir_input("Prompt")
ASSERT:
  - resultado == "respuesta"
  - bridge.esperar() fue llamado exactamente 1 vez
```

---

## MÉTODO: `Vista._iniciar_polling()`

**¿Qué hace?** (Método privado de Vista; línea ~5657-5664; main thread Tkinter)
1. Si `not self._ocupado` Y `cola_mensajes` no vacía:
   - Extrae 1 mensaje: `msg = cola_mensajes.popleft()`
   - Llama `self.procesar_mensaje(msg)` para renderizar
2. **Siempre** reschedule: `self.root.after(50, self._iniciar_polling)`
3. Si `_ocupado == True`: salta procesamiento este ciclo (espera a terminar typewriter)

**CRÍTICO**: Procesa 1 mensaje por ciclo para mantener UI responsiva

#### Test T3.1: Procesa 1 mensaje
```
ARRANGE:
  - Mock procesar_mensaje()
  - cola_mensajes = [{"tipo": "narrar", "contenido": "Hola"}]
  - vista._ocupado = False
ACT:
  - vista._iniciar_polling()
ASSERT:
  - procesar_mensaje() llamado exactamente 1 vez
  - Cola vacía después
```

#### Test T3.2: Reschedule siempre
```
ARRANGE:
  - Mock root.after()
  - cola_mensajes vacía
ACT:
  - vista._iniciar_polling()
ASSERT:
  - root.after(50, vista._iniciar_polling) llamado
  - Ocurre incluso con cola vacía
```

#### Test T3.3: Cola vacía sin error
```
ARRANGE: cola_mensajes = []
ACT: vista._iniciar_polling()
ASSERT:
  - Sin IndexError o KeyError
  - Reschedule ocurre normalmente
```

#### Test T3.4: No procesa si _ocupado=True
```
ARRANGE:
  - Mock procesar_mensaje()
  - cola_mensajes = [{"tipo": "narrar", "contenido": "Test"}]
  - vista._ocupado = True
ACT:
  - vista._iniciar_polling()
ASSERT:
  - procesar_mensaje() NO fue llamado
  - Cola tiene 1 mensaje aún (no fue removido)
  - Reschedule ocurre (intentará siguiente ciclo)
```

#### Test T3.5: Solo 1 mensaje por ciclo
```
ARRANGE:
  - Mock procesar_mensaje()
  - cola_mensajes = [msg1, msg2, msg3]
  - vista._ocupado = False
ACT:
  - vista._iniciar_polling()
ASSERT:
  - procesar_mensaje() llamado 1 sola vez (no 3)
  - Cola tiene 2 mensajes aún
```

---

## FUNCIÓN: `procesar_mensaje(msg)`

**¿Qué hace?** (Método de Vista; línea ~5546; main thread)
- Router que mapea `msg["tipo"]` a método Vista específico
- Tipos soportados: "narrar", "alerta", "exito", "sistema", "dialogo", "preguntar", "susurros", "separador", "titulo", "panel", "stats", "hud", "opciones_combate", "terminar_combate", "menu_principal", "titulo_juego", "habilitar_input"
- Cada tipo tiene su handler (agregar_texto, actualizar_hud, etc.)

#### Test T3.6: Router funciona
```
ARRANGE:
  - Mock self.agregar_texto()
ACT:
  - msg = {"tipo": "narrar", "contenido": "Hola"}
  - vista.procesar_mensaje(msg)
ASSERT:
  - agregar_texto.assert_called_with("Hola", "narrar")
```

#### Test T3.7: Tipos desconocidos se ignoran
```
ARRANGE: msg = {"tipo": "tipo_desconocido", "contenido": "test"}
ACT: vista.procesar_mensaje(msg)
ASSERT:
  - Sin KeyError o excepción
  - Mensaje simplemente ignorado
```

---

## INTEGRACIÓN: Thread Juego + Thread UI (_Bridge + _iniciar_polling)

#### Test T4.1: Full sync cycle
```
ARRANGE:
  - Thread Juego: llama pedir_input()  (bloqueado en bridge.esperar())
  - Main thread: _iniciar_polling() activo
  - cola_mensajes: [{"tipo": "preguntar", "contenido": "¿Opción?"}]
ACT:
  - polling() procesa y renderiza pregunta
  - Usuario simula input: bridge.recibir("1")
ASSERT:
  - pedir_input() retorna "1"
  - Juego continúa sin freezeo UI
  - Sin deadlock
```

#### Test T4.2: Múltiples inputs consecutivos
```
ARRANGE:
  - Thread Juego: loop de 5 pedir_input() 
  - Main thread: _iniciar_polling()
ACT:
  - Simular 5 inputs con delays aleatorios
ASSERT:
  - Todos los inputs procesados correctamente
  - Sin race conditions
  - Orden FIFO respetado
```

#### Test T4.3: Contención bajo carga
```
ARRANGE:
  - Thread Juego: emitir() rápidamente (100 msgs)
  - Main thread: _iniciar_polling() procesa (1 msg/50ms)
  - Simultáneamente: pedir_input() bloqueado
ACT:
  - Ejecutar 2 segundos
ASSERT:
  - Sin deadlock
  - Sin crash
  - Todos los mensajes procesados eventualmente
  - Sin datos corruptos
```
ASSERT:
  - Sin deadlock
  - Sin exception
  - Todos los mensajes procesados eventualmente
```

---

## FIXTURES NECESARIAS

```python
import threading
import time
from unittest.mock import Mock, patch, MagicMock
from collections import deque

# _Bridge: Implementación real (copiar desde TLDRDC_Prueba1.py línea ~151)
class _Bridge:
    def __init__(self):
        self._evento = threading.Event()
        self._valor = ""
    
    def esperar(self):
        self._evento.wait()
        self._evento.clear()
        return self._valor
    
    def recibir(self, texto):
        self._valor = texto
        self._evento.set()

# Global instance
_bridge = _Bridge()

# cola_mensajes global
cola_mensajes = deque()

# emitir function
def emitir(tipo, contenido=""):
    cola_mensajes.append({"tipo": tipo, "contenido": contenido})

# pedir_input function (copied from TLDRDC_Prueba1.py)
def pedir_input(prompt=""):
    if prompt:
        emitir("preguntar", prompt)
    emitir("habilitar_input")
    return _bridge.esperar()

# Vista mock para tests (simplificada)
class VistaMock:
    def __init__(self):
        self._ocupado = False
        self.root = Mock()
        self.procesar_mensaje = Mock()
    
    def _iniciar_polling(self):
        if not self._ocupado and cola_mensajes:
            msg = cola_mensajes.popleft()
            self.procesar_mensaje(msg)
        self.root.after(50, self._iniciar_polling)

# Fixture: Bridge con timer para unblock
@pytest.fixture
def bridge_with_timer():
    bridge = _Bridge()
    def delayed_recibir():
        time.sleep(0.1)
        bridge.recibir("test_input")
    
    thread = threading.Thread(target=delayed_recibir)
    thread.daemon = True
    thread.start()
    
    return bridge
```

---

## NOTAS

### Implementación Real
- **Ubicación**: TLDRDC_Prueba1.py línea ~140-220 (_Bridge, pedir_input, emitir)
- **Ubicación**: TLDRDC_Prueba1.py línea ~250-270 (cola_mensajes, emitir)
- **Ubicación**: TLDRDC_Prueba1.py línea ~5657 (Vista._iniciar_polling)
- **Ubicación**: TLDRDC_Prueba1.py línea ~5546 (Vista.procesar_mensaje)

### Decisiones de Diseño
1. **event.clear()**: CRÍTICO en esperar(). Sin clear(), segundo esperar() retorna inmediatamente
2. **1 mensaje por ciclo**: _iniciar_polling() procesa solo 1 msg cada 50ms para mantener UI responsiva
3. **_ocupado flag**: Evita procesar mensajes durante typewriter (evita intercalación de caracteres)
4. **Thread-safe deque**: cola_mensajes es deque (thread-safe en CPython); no requiere Lock
5. **Global _bridge**: Instancia global única; simplifica acceso desde múltiples funciones
6. **pedir_input() bloquea juego**: Permite que Tkinter main thread siga activo

### Validación en Tests
- **T1.6**: Test con threads reales valida sincronización sin mocking
- **T3.4**: Verificar que _ocupado=True pausa procesamiento
- **T4.3**: Test de carga para detectar deadlocks o race conditions
- **Timeouts**: Usar `pytest-timeout` para evitar tests colgados (max 2s per test)
- **time.sleep()**: Aceptable en threading tests (es pattern estándar)

### Precauciones
- No mockear Event.wait() / Event.set() (necesita real para bloqeo)
- No mockear deque (necesita real para thread-safety)
- Siempre usar thread real para bloqueo, no simular

