# Especificación de Tests — UI & THREADING (_Bridge, polling)

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

Sistema de **sincronización de hilos** para Tkinter + juego:
1. **_Bridge** — Objeto que sincroniza entrada/salida entre hilo juego y hilo UI
2. **polling()** — Procesa cola de mensajes del juego en el main thread de Tkinter

**CRÍTICO**: Sin esto, UI se congela durante narración

---

## CLASE: `_Bridge`

**¿Qué hace?**
- Encapsula `threading.Event` para sincronización
- Métodos:
  - `esperar()` — Bloquea hilo juego hasta recibir input
  - `recibir(texto)` — Envía input desde UI, desbloquea juego

### Función: `_Bridge.esperar()`

**¿Qué hace?**
- Llama `self.event.wait()`
- Bloquea hilo trabajador hasta que Event sea set
- Retorna el valor almacenado en `self.valor`

#### Test T1.1: Bloquea hasta recibir()
```
ARRANGE:
  - bridge = _Bridge()
  - Timer en thread separado llamará recibir() tras 100ms
ACT:
  - resultado = bridge.esperar()
ASSERT:
  - Esperó bloqueado (tiempo ≥ 100ms)
  - resultado == "input_enviado"
```

#### Test T1.2: Event.wait() es llamado
```
ARRANGE:
  - bridge = _Bridge()
  - Mock Event.wait()
ACT:
  - bridge.esperar()
ASSERT:
  - Event.wait.assert_called_once()
```

#### Test T1.3: Retorna valor almacenado
```
ARRANGE:
  - bridge = _Bridge()
  - bridge.valor = "test_value"
  - bridge.event.set()
ACT:
  - resultado = bridge.esperar()
ASSERT:
  - resultado == "test_value"
```

---

### Función: `_Bridge.recibir(texto)`

**¿Qué hace?**
- Almacena `texto` en `self.valor`
- Llama `self.event.set()` para desbloquear esperar()

#### Test T1.4: Almacena valor
```
ARRANGE: bridge = _Bridge()
ACT: bridge.recibir("hello")
ASSERT: bridge.valor == "hello"
```

#### Test T1.5: Set event
```
ARRANGE:
  - bridge = _Bridge()
  - Mock Event.set()
ACT:
  - bridge.recibir("test")
ASSERT:
  - Event.set.assert_called_once()
```

#### Test T1.6: Desbloquea esperar()
```
ARRANGE:
  - bridge = _Bridge()
  - Thread 1: llama esperar()
  - Thread 2: espera 50ms, luego recibir("x")
ACT:
  - Ejecutar threads simultáneamente
ASSERT:
  - esperar() retorna tras ~50ms (sin timeout)
  - resultado == "x"
```

---

## FUNCIÓN: `polling()`

**¿Qué hace?**
- Lee mensaje de `cola_mensajes` (deque thread-safe)
- Si hay mensaje Y `_ocupado == False`:
  - Llama `typewriter()` para emitir (con efecto visual)
- Reschedule `self.root.after(50, polling)` para siguiente iteración
- Si `_ocupado == True`: salta este ciclo

**Context**: `Vista` class (Tkinter)

#### Test T2.1: Procesa mensaje de la cola
```
ARRANGE:
  - vista = Vista()
  - cola_mensajes contiene ("info", "Hola")
  - _ocupado = False
ACT:
  - polling()
ASSERT:
  - typewriter() fue llamado con ("info", "Hola")
  - Mensaje removido de cola
```

#### Test T2.2: No procesa si _ocupado=True
```
ARRANGE:
  - vista.cola_mensajes = [("info", "Mensaje")]
  - vista._ocupado = True
ACT:
  - polling()
ASSERT:
  - typewriter() NO fue llamado
  - Mensaje aún en cola (será procesado cuando _ocupado=False)
```

#### Test T2.3: Procesa un mensaje por ciclo
```
ARRANGE:
  - cola_mensajes = [("info", "M1"), ("info", "M2"), ("info", "M3")]
ACT:
  - polling()  (solo una llamada)
ASSERT:
  - typewriter() llamado 1 sola vez
  - 2 mensajes quedan en cola
```

#### Test T2.4: Reschedule tras procesar
```
ARRANGE:
  - vista.root = Mock()
ACT:
  - polling()
ASSERT:
  - vista.root.after(50, polling).assert_called_once()
```

#### Test T2.5: Cola vacía no error
```
ARRANGE: cola_mensajes = []
ACT: polling()
ASSERT:
  - Sin error
  - typewriter() no llamado
  - root.after() aún reschedule
```

#### Test T2.6: Maneja deque thread-safe
```
ARRANGE:
  - Thread 1: produce mensajes continuamente
  - Thread 2: llama polling() múltiples veces
ACT:
  - Ejecutar 5 segundos
ASSERT:
  - Sin race conditions
  - Mensajes procesados en orden FIFO
```

---

## ESCENARIO INTEGRACIÓN: Hilo Juego + Hilo UI

#### Test T3.1: Full sync cycle
```
ARRANGE:
  - Thread Juego: llama bridge.esperar()  (bloqueado)
  - Thread UI: polling() activo
  - cola_mensajes: [("narration", "Te duele...")]
ACT:
  - polling() procesa mensajes
  - Usuario envía input: bridge.recibir("s")
ASSERT:
  - Juego desbloquea (bridge.esperar() retorna)
  - Input recibido correctamente ("s")
  - UI no froze
```

#### Test T3.2: Interrupción sin crash
```
ARRANGE:
  - Juego enviando mensajes rápidamente
  - UI procesando con polling()
  - Usuario envía input simultáneamente
ACT:
  - Simular condiciones de carrera
ASSERT:
  - Sin deadlock
  - Sin exception
  - Todos los mensajes procesados eventualmente
```

---

## MATRIZ DE PRUEBAS

| Test ID | Componente | Validación |
|---------|-----------|-----------|
| T1.1 | _Bridge.esperar | Bloquea hasta recibir() |
| T1.2 | _Bridge.esperar | Event.wait() llamado |
| T1.3 | _Bridge.esperar | Retorna valor |
| T1.4 | _Bridge.recibir | Almacena valor |
| T1.5 | _Bridge.recibir | Set event |
| T1.6 | _Bridge.recibir | Desbloquea esperar() |
| T2.1 | polling | Procesa mensaje de cola |
| T2.2 | polling | Respeta _ocupado flag |
| T2.3 | polling | Un mensaje por ciclo |
| T2.4 | polling | Reschedule root.after() |
| T2.5 | polling | Cola vacía sin error |
| T2.6 | polling | Thread-safe FIFO |
| T3.1 | Integración | Full sync cycle |
| T3.2 | Integración | Sin deadlock/crash |

---

## FIXTURES NECESARIAS

```python
import threading
import time
from unittest.mock import Mock, patch, MagicMock
from collections import deque

# _Bridge real
class _Bridge:
    def __init__(self):
        self.event = threading.Event()
        self.valor = None
    
    def esperar(self):
        self.event.wait()
        return self.valor
    
    def recibir(self, texto):
        self.valor = texto
        self.event.set()

# Vista mock para tests
class VistaMock:
    def __init__(self):
        self.cola_mensajes = deque()
        self._ocupado = False
        self.root = Mock()
        self.typewriter_mock = Mock()
    
    def typewriter(self, tipo, contenido):
        self.typewriter_mock(tipo, contenido)
    
    def polling(self):
        if not self._ocupado and self.cola_mensajes:
            tipo, contenido = self.cola_mensajes.popleft()
            self.typewriter(tipo, contenido)
        self.root.after(50, self.polling)

# Fixture: Bridge con timer
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

- **CRÍTICO T1.6**: Test con threads reales valida sincronización correcta
- **T2.2**: _ocupado flag evita que mensajes se procesen durante typewriter (UI bloqueado visualmente)
- **T2.6**: Deque es thread-safe en CPython; tests deben validar en múltiples iteraciones
- Tests pueden usar `time.sleep()` para simular delays (aceptable en unit tests de threading)
- Considerar `pytest-timeout` para evitar tests que cuelguen indefinidamente
