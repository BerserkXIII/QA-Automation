# Especificación de Tests — INTEGRATION TESTS

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

Tests de **integración entre módulos** — validan que cambios en un módulo funcionan correctamente con otros

**Scope**: Flujos reales de juego, no E2E completo (eso es manual en QA_project/tests/01-Manual/)

---

## TEST: `reactive.py + aplicar_evento()`

### Test INT1: Observer se dispara cuando evento aplica stats

**Escenario**: 
1. Personaje reactivo observa "vida"
2. Evento suma vida
3. Callback debe ejecutarse

```
ARRANGE:
  - p = Personaje({"vida": 10})
  - callback = Mock()
  - p.observe("vida", callback)
  - p.activo = True
  - evento = {"vida": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - callback.assert_called_with(15)
  - p["vida"] == 15
```

### Test INT2: Múltiples observadores en evento

**Escenario**: Varios callbacks por diferentes stats

```
ARRANGE:
  - p = Personaje({"vida": 10, "fuerza": 5})
  - callback_vida = Mock()
  - callback_fuerza = Mock()
  - p.observe("vida", callback_vida)
  - p.observe("fuerza", callback_fuerza)
  - p.activo = True
  - evento = {"vida": 3, "fuerza": 2}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - callback_vida.assert_called_with(13)
  - callback_fuerza.assert_called_with(7)
```

---

## TEST: `_Bridge + polling()`

### Test INT3: Hilo juego y UI sincronizados

**Escenario**: 
1. Juego en thread separado espera input
2. UI procesa mensajes y envía input
3. Juego continúa sin deadlock

```
ARRANGE:
  - bridge = _Bridge()
  - vista = VistaMock(bridge)
  - cola_mensajes = [("narration", "Test narration")]
ACT:
  - Thread1: bridge.esperar()
  - Thread2: sleep(50ms), vista.polling(), bridge.recibir("s")
  - Esperar a ambos threads
ASSERT:
  - bridge.esperar() retorna "s"  (sin timeout)
  - Vista procesó mensaje antes de recibir input
  - Sin deadlock/hanging
```

### Test INT4: Polling respeta _ocupado durante typewriter

**Escenario**:
1. Mensaje entra a cola
2. Se inicia typewriter (efecto visual)
3. Durante typewriter, _ocupado = True
4. Polling espera

```
ARRANGE:
  - vista.cola_mensajes = [("info", "Mensaje")]
  - vista._ocupado = True
ACT:
  - vista.polling()
ASSERT:
  - typewriter() NO fue llamado
  - Mensaje sigue en cola
  - Siguiente ciclo (cuando _ocupado=False) procesa
```

---

## TEST: `eventos + aplicar_evento + reactive`

### Test INT5: Evento modifica stats, UI se actualiza

**Escenario**:
1. _evento_1 retorna {"pociones": 1}
2. aplicar_evento lo aplica
3. Observer en personaje se dispara
4. UI callback (mock) ejecuta

```
ARRANGE:
  - p = Personaje({"pociones": 5, "pociones_max": 10})
  - ui_callback = Mock()
  - p.observe("pociones", ui_callback)
  - p.activo = True
  - evento = _evento_1(p)  (retorna {"pociones": 1})
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == 6
  - ui_callback.assert_called_with(6)
```

---

## TEST: `guardar_partida + cargar_partida`

### Test INT6: Guardar y cargar mantienen integridad

**Escenario**:
1. Personaje con state específico
2. Guardar
3. Cargar en nueva instancia
4. Verificar datos idénticos

```
ARRANGE:
  - personaje = {
      "nombre": "Test",
      "vida": 8,
      "fuerza": 6,
      "destreza": 4,
      "armas": {"daga": {"daño": 2}},
    }
  - estado = {"_c01": 42, "eventos_superados": 15}
ACT:
  - guardar_partida(personaje)
  - personaje2 = cargar_partida()
ASSERT:
  - personaje2["nombre"] == "Test"
  - personaje2["vida"] == 8
  - personaje2["fuerza"] == 6
  - personaje2["armas"]["daga"]["daño"] == 2
  - estado["_c01"] == 42  (restaurado)
```

---

## TEST: `imagen_manager + ui_estructura`

### Test INT7: Sprites se cargan sin fallar

**Escenario**:
1. UI solicita cargar sprite
2. Si PNG falta: retorna None
3. UI usa fallback (texto) sin crash

```
ARRANGE:
  - manager = ImagenManager(ruta_assets)
  - Ruta contiene: daga.png (válido), espada.png (falta), martillo_corrupto.png
  - ui_button = UIButton(manager)
ACT:
  - daga_img = manager.cargar_imagen("daga.png", (50, 50))
  - espada_img = manager.cargar_imagen("espada.png", (50, 50))
  - martillo_img = manager.cargar_imagen("martillo_corrupto.png", (50, 50))
  - ui_button.render(daga_img, "Daga")
  - ui_button.render(espada_img, "Espada")  (None, fallback a texto)
ASSERT:
  - daga_img is not None
  - espada_img is None
  - martillo_img is None
  - UI renderiza sin excepción en ambos casos
```

---

## TEST: `calcular_daño + combate`

### Test INT8: Daño se calcula correctamente en combate

**Escenario**:
1. Combate ejecuta turno jugador
2. calcular_daño() con arma + stats
3. Daño infligido al enemigo

```
ARRANGE:
  - personaje = {"fuerza": 8, "destreza": 6, "armas": ["martillo"]}
  - enemigo = {"vida": 20}
  - arma = armas_global["martillo"]
ACT:
  - daño = calcular_daño(arma, personaje)
  - enemigo["vida"] -= daño
ASSERT:
  - daño == 5 + (8 // 2) == 9
  - enemigo["vida"] == 11
```

---

## MATRIZ DE PRUEBAS (Integration)

| Test ID | Módulos | Escenario |
|---------|---------|-----------|
| INT1 | reactive + aplicar_evento | Observer se dispara |
| INT2 | reactive + aplicar_evento | Múltiples observadores |
| INT3 | _Bridge + polling | Hilos sincronizados |
| INT4 | polling + _ocupado | Respeta flag |
| INT5 | eventos + aplicar + reactive | Stats → UI actualiza |
| INT6 | guardar + cargar | Integridad datos |
| INT7 | imagen_manager + UI | Sprites faltan, fallback OK |
| INT8 | calcular_daño + combate | Daño en contexto |

---

## FIXTURE COMPARTIDA: Personaje Reactivo Real

```python
@pytest.fixture
def personaje_reactivo():
    """Personaje real (no mock) con observer registrado"""
    from modules.reactive import Personaje
    
    p = Personaje({
        "nombre": "TestPlayer",
        "vida": 10,
        "fuerza": 5,
        "destreza": 5,
        "pociones": 6,
        "nivel": 1,
        "armas": {},
    })
    p.activo = True
    return p

@pytest.fixture
def estado_test():
    """Estado global mockado"""
    return {
        "armas_jugador": {},
        "ruta_jugador": [],
        "eventos_superados": 0,
        "bolsa_eventos": list(range(1, 21)),
        "bolsa_exploracion": list(range(1, 16)),
        "_c01": 0,
        "veces_guardado": 0,
    }

@pytest.fixture
def bridge_real():
    """_Bridge sin mocks"""
    from ui_estructura import _Bridge
    return _Bridge()
```

---

## NOTAS

- **INT3, INT4**: Tests con threads reales (no simple mock) — validan sincronización
- **INT6**: Test de persistencia requiere tmp_path fixture
- **INT7**: Test defensivo — sprites faltantes no rompen juego
- **INT8**: Valida que calcular_daño funciona en contexto de combate real
- **No testear**: Narrativa completa (manual en QA_project), UI visual exacta
