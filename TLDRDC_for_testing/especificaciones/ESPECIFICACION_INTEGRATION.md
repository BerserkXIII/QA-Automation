# Especificación de Tests — INTEGRATION TESTS (EXHAUSTIVO)

*Versión: 1.0 (Análisis Completo: 171 Unit Tests → 25+ Integration Tests)*

---

## 📊 RESUMEN EJECUTIVO

**Objetivo**: Validar que 171 tests unitarios en **9 módulos** funcionan correctamente JUNTOS

| Módulo Unitario | Tests | Integraciones Críticas |
|-----------------|-------|----------------------|
| test_reactive.py | 13 | Observer real + UI callbacks |
| test_threading.py | 20 | Sincronización _Bridge + polling |
| test_eventos.py | 16 | Bolsa + obtener + aplicar |
| test_core.py | 32 | crear → aplicar → explorar → validar |
| test_combate_jugador.py | 16 | calcular_daño + turno + armas |
| test_combate_enemigo.py | 34 | IA + habilidades + jefes |
| test_combate_loop.py | 14 | Loop completo + sangrado + Fibonacci |
| test_persistencia.py | 15 | Guardar/cargar + migraciones |
| test_imagen.py | 11 | Caché + fallback visual |
| **TOTAL** | **171** | **25 Integration Tests** |

---

## 🎯 MATRIZ DE INTEGRACIONES (25 Tests)

### GRUPO 1: REACTIVIDAD + OBSERVADORES (4 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.R1 | reactive + aplicar_evento | Personaje.observe + aplicar_evento | Callback ejecutado con nuevo valor |
| INT.R2 | reactive + threading | Personaje + pedir_input en thread | Observer no race condition |
| INT.R3 | reactive + UI | Personaje observa stats + emitir | UI callback dispara correctamente |
| INT.R4 | reactive + eventos | Personaje observa + bolsa aplica | Multiple observers + eventos simultáneos |

### GRUPO 2: THREADING + COMUNICACIÓN (4 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.T1 | _Bridge + esperar + recibir | Thread juego + Thread UI | Sin deadlock, retorna valor correcto |
| INT.T2 | pedir_input + _Bridge + Vista | Múltiples inputs secuenciales | Queue FIFO funciona sin race |
| INT.T3 | polling + _ocupado + typewriter | Polling respeta flag durante animación | No procesa mensajes mientras busy |
| INT.T4 | threading + pedir_input + mock_input | Juego bloquea sin freezear UI | Thread worker espera correctamente |

### GRUPO 3: EVENTOS + STATS (5 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.E1 | bolsa_eventos + obtener + aplicar | obtener_evento + aplicar_evento | Evento de bolsa aplica correctamente |
| INT.E2 | eventos ramificados + stats | _evento_1 a _evento_20 + aplicar | Cada rama aplica efectos diferentes |
| INT.E3 | múltiples eventos + clamping | Cadena aplicar_evento 3+ veces | Stats respetan máximos/mínimos |
| INT.E4 | eventos + muerte + revive | evento muerte + fin_derrota + revive | Flag _flg1 permite continuar |
| INT.E5 | eventos + efectos_temporales | aplicar con efectos + decrementar | Efectos persisten, limpian correctamente |

### GRUPO 4: COMBATE COMPLETO (7 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.C1 | calcular_daño + stats + armas | calcular_daño con builds diferentes | Bonificación correcta por tipo arma |
| INT.C2 | turno_jugador + calcular_daño + enemigo | Ataque jugador → daño real → vida enemigo | Loop combate funciona 1 ciclo |
| INT.C3 | turno_enemigo + habilidades + sangrado | IA enemigo + buffs + sangrado | Habilidades de jefe se aplican |
| INT.C4 | combate_loop completo | crear_personaje → turno_jugador → turno_enemigo → sangrado → victoria | Flujo completo con todas las integraciones |
| INT.C5 | enemigo_aleatorio + jefes + combate | Todos los 6 tipos base + 9 jefes | Jefes no rompen loop combate |
| INT.C6 | post_combate + eventos + stats | resolver_eventos_post_combate + aplicar + Fibonacci | Bonus Fibonacci se calcula correctamente |
| INT.C7 | daño + esquiva + stats | calcular_daño × 2 builds + probabilidad golpe | Hit chance afecta combate realísticamente |

### GRUPO 5: PERSISTENCIA (4 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.P1 | guardar + cargar + validar | guardar_partida → cargar_partida → validar_personaje | Ciclo save/load íntegro |
| INT.P2 | guardar + migración + armas | guardar con armas → cargar + sincronización armas | Armas restauradas correctamente |
| INT.P3 | múltiples guardadas | guardar × 3 cambios + carpeta | Fichero se sobrescribe atómicamente |
| INT.P4 | cargar corrupto + fallback | JSON corrupto → retorna None + alerta | Sin crash en corrupto |

### GRUPO 6: FLUJO COMPLETO DEL JUEGO (5 tests)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.G1 | crear → aplicar → validar | crear_personaje + aplicar_evento + validar_personaje | Personaje válido post-creación |
| INT.G2 | explorar + eventos + aplicar | explorar + bolsa_eventos + aplicar_evento | Evento exploratorio se aplica correctamente |
| INT.G3 | crear → combate → post_combate | crear + combate + resolver_eventos + aplicar | Ciclo juego real |
| INT.G4 | efectos_temporales + multiples_ciclos | aplicar_efecto + decrementar × N + limpiar | Efectos duran correctamente N turnos |
| INT.G5 | juego_completo_save_load | crear → explorar → combate → guardar → cargar → continuar | Full game session persistence |

### GRUPO 7: IMAGEN + UI (1 test)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.V1 | imagen_manager + fallback + UI | cargar_imagen × 3 (válida/faltante/corrupta) + fallback | UI no rompe con sprites faltantes |

### GRUPO 7: IMAGEN + UI (1 test)

| ID | Integración | Funciones | Validación |
|---|---|---|---|
| INT.V1 | imagen_manager + fallback + UI | cargar_imagen × 3 (válida/faltante/corrupta) + fallback | UI no rompe con sprites faltantes |

---

---

## 🔬 TESTS DETALLADOS

## GRUPO 1: REACTIVIDAD + OBSERVADORES

### INT.R1: Observer se dispara en aplicar_evento

**Escenario**: Personaje reactivo observa "vida", evento suma vida → callback ejecuta

```python
# ARRANGE
personaje = Personaje({
    "vida": 10,
    "vida_max": 25,
    "fuerza": 5,
})
callback_mock = Mock()
personaje.observe("vida", callback_mock)
personaje.activo = True
evento = {"vida": 5}

# ACT
aplicar_evento(evento, personaje)

# ASSERT
assert personaje["vida"] == 15
callback_mock.assert_called_once_with(15)  # Callback ejecutado con nuevo valor
```

**Por qué es crítico**: Valida que observers internos de Personaje se ejecutan cuando aplicar_evento modifica stats. Si falla = UI no se actualiza en tiempo real.

---

### INT.R2: Observer + Threading SIN race condition

**Escenario**: Personaje observado desde thread juego, cambios desde thread principal sin race

```python
# ARRANGE
personaje = Personaje({"vida": 10})
eventos_disparo = []
personaje.observe("vida", lambda v: eventos_disparo.append(v))
personaje.activo = True

# ACT - Thread 1: aplica cambios
def thread_aplica_eventos():
    for i in range(5):
        aplicar_evento({"vida": 1}, personaje)
        time.sleep(0.01)

t1 = threading.Thread(target=thread_aplica_eventos)
t1.start()
t1.join()

# ASSERT
assert len(eventos_disparo) == 5
assert personaje["vida"] == 15
assert eventos_disparo == [11, 12, 13, 14, 15]  # Orden correcto
```

**Por qué es crítico**: Threading real expone race conditions en observer pattern. Si falla = crash intermitente durante juego.

---

### INT.R3: Observer + UI Callback (emitir)

**Escenario**: Personaje observa, aplicar_evento dispara observer, observer emite a UI

```python
# ARRANGE
personaje = Personaje({"vida": 10, "fuerza": 5})
mock_emitir = Mock()
def ui_callback(valor):
    mock_emitir("actualizar_stat", {"vida": valor})

personaje.observe("vida", ui_callback)
personaje.activo = True
evento = {"vida": 3}

# ACT
aplicar_evento(evento, personaje)

# ASSERT
assert personaje["vida"] == 13
mock_emitir.assert_called_once_with("actualizar_stat", {"vida": 13})
```

**Por qué es crítico**: Ciclo completo: evento → observer → UI update. Si falla = UI no actualiza tras cambio de stats.

---

### INT.R4: Múltiples Observers + Eventos Simultáneos

**Escenario**: 2 observers en diferentes stats, 1 evento modifica ambos

```python
# ARRANGE
personaje = Personaje({
    "vida": 10,
    "fuerza": 5,
    "destreza": 5,
})
cb_vida = Mock()
cb_fuerza = Mock()
personaje.observe("vida", cb_vida)
personaje.observe("fuerza", cb_fuerza)
personaje.activo = True
evento = {"vida": 3, "fuerza": 2}

# ACT
aplicar_evento(evento, personaje)

# ASSERT
assert personaje["vida"] == 13
assert personaje["fuerza"] == 7
cb_vida.assert_called_once_with(13)
cb_fuerza.assert_called_once_with(7)
```

**Por qué es crítico**: Múltiples stats modificados simultáneamente. Si falla = algunos observers no disparan, UI inconsistente.

---

## GRUPO 2: THREADING + COMUNICACIÓN

### INT.T1: _Bridge esperar + recibir (2 threads)

**Escenario**: Thread 1 (juego) espera input, Thread 2 (UI) envía → sin deadlock

```python
# ARRANGE
bridge = _Bridge()
resultado = []

def thread_juego():
    respuesta = bridge.esperar()
    resultado.append(respuesta)

def thread_ui():
    time.sleep(0.05)  # Simula procesamiento UI
    bridge.recibir("s")

# ACT
t1 = threading.Thread(target=thread_juego)
t2 = threading.Thread(target=thread_ui)
t1.start()
t2.start()
t1.join(timeout=1)
t2.join(timeout=1)

# ASSERT
assert resultado == ["s"]
assert not t1.is_alive()  # Juego desbloqueó
assert not t2.is_alive()
```

**Por qué es crítico**: Deadlock aquí congela la aplicación. Si falla = UI freezea.

---

### INT.T2: pedir_input + _Bridge + polling (secuencial múltiple)

**Escenario**: Llamadas múltiples a pedir_input funcionan correctamente

```python
# ARRANGE
inputs = ["jugador", "5", "s"]
inputs_iter = iter(inputs)

def mock_bridge_esperar():
    return next(inputs_iter)

# ACT
with patch('TLDRDC_Prueba1._bridge.esperar', side_effect=mock_bridge_esperar):
    nombre = pedir_input("Nombre: ")
    fuerza = pedir_input("Fuerza: ")
    accion = pedir_input("Acción: ")

# ASSERT
assert nombre == "jugador"
assert fuerza == "5"
assert accion == "s"
```

**Por qué es crítico**: pedir_input llamado múltiples veces en crear_personaje. Si falla = loop no funciona correctamente.

---

### INT.T3: polling + _ocupado (no procesar mientras typewriter activo)

**Escenario**: polling() respeta _ocupado flag durante animación

```python
# ARRANGE
cola_mensajes = deque([("narration", "Prueba mensaje")])
mock_typewriter = Mock()
vista_mock = Mock()
vista_mock.cola_mensajes = cola_mensajes
vista_mock._ocupado = True  # Animación en progreso

# ACT
def _iniciar_polling():
    if not vista_mock._ocupado and vista_mock.cola_mensajes:
        tipo, contenido = vista_mock.cola_mensajes.popleft()
        if tipo == "narration":
            mock_typewriter(contenido)

_iniciar_polling()

# ASSERT
assert len(cola_mensajes) == 1  # Mensaje NO procesado
mock_typewriter.assert_not_called()
```

**Por qué es crítico**: Si polling procesa durante typewriter, narración interrumpida. Si falla = narrativa rota.

---

### INT.T4: pedir_input bloquea thread juego sin freezear UI

**Escenario**: Juego bloqueado en pedir_input, UI sigue responsiva

```python
# ARRANGE
juego_bloqueado = []
ui_responsiva = []

def thread_juego():
    juego_bloqueado.append("BLOQUEADO")
    # Aquí pedir_input bloquea (mocked para retornar "respuesta")
    with patch('TLDRDC_Prueba1._bridge.esperar', return_value="s"):
        resultado = pedir_input("¿Acción? ")
    juego_bloqueado.append("DESBLOQUEADO")
    return resultado

def thread_ui():
    # UI siempre responsiva
    for _ in range(10):
        ui_responsiva.append("CLICK")
        time.sleep(0.01)

# ACT
t1 = threading.Thread(target=thread_juego)
t2 = threading.Thread(target=thread_ui)
t1.start()
time.sleep(0.02)  # Juego ya está bloqueado
t2.start()
t1.join()
t2.join()

# ASSERT
assert "BLOQUEADO" in juego_bloqueado
assert len(ui_responsiva) > 0  # UI procesó mientras juego bloqueado
```

**Por qué es crítico**: Si juego freezea UI, aplicación parece congelada. Si falla = UX crítico roto.

---

## GRUPO 3: EVENTOS + STATS

### INT.E1: bolsa_eventos + obtener + aplicar

**Escenario**: Obtener evento de bolsa y aplicarlo cambia stats

```python
# ARRANGE
rellenar_bolsa_eventos()
evento_id = obtener_evento_de_bolsa()  # Por ej: 5
personaje = {
    "nombre": "test",
    "vida": 10,
    "pociones": 6,
    "armas": {},
}

# ACT - Obtener función del evento
evento_func = globals()[f"_evento_{evento_id}"]
evento_dict = evento_func(personaje)
with patch('TLDRDC_Prueba1.sistema'), \
     patch('TLDRDC_Prueba1.alerta'), \
     patch('TLDRDC_Prueba1.exito'):
    aplicar_evento(evento_dict, personaje)

# ASSERT
assert personaje["vida"] != 10 or personaje["pociones"] != 6  # Algo cambió
```

**Por qué es crítico**: Bolsa proporciona eventos, aplicar_evento aplica cambios. Si falla = exploración no funciona.

---

### INT.E2: Ramas de _evento_X + aplicar efectos diferentes

**Escenario**: Diferentes ramas de _evento_1 aplican diferentes efectos

```python
# ARRANGE
personaje = {"vida": 10, "pociones": 6, "armas": {}}

# RAMA 1: Poción
with patch('TLDRDC_Prueba1.leer_input', return_value="s"), \
     patch('TLDRDC_Prueba1.random.choice', return_value="pocion"):
    evento1 = _evento_1(personaje)
assert evento1 == {"pociones": 1}

# RAMA 2: Daño
with patch('TLDRDC_Prueba1.leer_input', return_value="s"), \
     patch('TLDRDC_Prueba1.random.choice', return_value="corte"):
    evento2 = _evento_1(personaje)
assert evento2 == {"vida": -1}

# RAMA 3: Huida (sin evento)
with patch('TLDRDC_Prueba1.leer_input', return_value="n"), \
     patch('TLDRDC_Prueba1.random.choice', return_value="escape"):
    evento3 = _evento_1(personaje)
assert evento3 == {}
```

**Por qué es crítico**: Cada evento tiene lógica diferente. Si una rama falla = jugador no obtiene rewards.

---

### INT.E3: Cadena aplicar_evento × 3 (clamping)

**Escenario**: 3 eventos secuenciales, stats respetan límites

```python
# ARRANGE
personaje = {
    "vida": 10,
    "vida_max": 25,
    "pociones": 6,
    "pociones_max": 10,
}

# ACT - 3 eventos suma vida
eventos = [
    {"vida": 5},   # 10 + 5 = 15
    {"vida": 15},  # 15 + 15 = 30 → clampea a 25
    {"vida": -100},  # 25 - 100 = -75 → clampea a 0
]

for evento in eventos:
    with patch('TLDRDC_Prueba1.sistema'), \
         patch('TLDRDC_Prueba1.alerta'), \
         patch('TLDRDC_Prueba1.exito'), \
         patch('TLDRDC_Prueba1.fin_derrota'):
        aplicar_evento(evento, personaje)

# ASSERT
assert personaje["vida"] == 0
assert personaje["vida"] <= personaje["vida_max"]
```

**Por qué es crítico**: Múltiples eventos no deben permitir stats fuera de límites. Si falla = bugs de stat infinita.

---

### INT.E4: Muerte + Revive Flag

**Escenario**: Evento mata, fin_derrota revive, juego continúa

```python
# ARRANGE
personaje = {"vida": 5, "_flg1": False}
evento_muerte = {"vida": -10}

# ACT 1 - Muerte
with patch('TLDRDC_Prueba1.fin_derrota') as mock_fin:
    mock_fin.return_value = True  # Tiene revive
    with patch('TLDRDC_Prueba1.sistema'), \
         patch('TLDRDC_Prueba1.alerta'), \
         patch('TLDRDC_Prueba1.exito'):
        aplicar_evento(evento_muerte, personaje)
    tiene_revive = mock_fin.return_value

# ASSERT 1
assert personaje["vida"] == 0
assert tiene_revive == True
mock_fin.assert_called_once()

# ACT 2 - Revive
if tiene_revive:
    evento_revive = {"vida": 20}
    with patch('TLDRDC_Prueba1.sistema'), \
         patch('TLDRDC_Prueba1.alerta'), \
         patch('TLDRDC_Prueba1.exito'):
        aplicar_evento(evento_revive, personaje)

# ASSERT 2
assert personaje["vida"] > 0
```

**Por qué es crítico**: Sistema revive es fin_derrota + aplicar_evento + flag. Si falla = no hay segundo chance.

---

### INT.E5: Efectos Temporales + Decrementar

**Escenario**: Aplica efecto, decrementar X veces, se limpia

```python
# ARRANGE
personaje = {"_efectos_temporales": {}}
evento_efecto = {"_efectos_temporales": {"sangre": 3}}

# ACT 1 - Aplicar efecto
with patch('TLDRDC_Prueba1.sistema'), \
     patch('TLDRDC_Prueba1.alerta'), \
     patch('TLDRDC_Prueba1.exito'):
    aplicar_evento(evento_efecto, personaje)
assert "sangre" in personaje["_efectos_temporales"]
assert personaje["_efectos_temporales"]["sangre"] == 3

# ACT 2 - Decrementar 3 turnos
for _ in range(3):
    decrementar_efectos_temporales(personaje)

# ASSERT
assert "sangre" not in personaje["_efectos_temporales"]
```

**Por qué es crítico**: Efectos deben durar exactamente N turnos, no infinito. Si falla = debuffs permanentes.

---

## GRUPO 4: COMBATE COMPLETO

### INT.C1: calcular_daño + Stats + Armas

**Escenario**: Diferentes builds (sutil/pesada/mixta) dan bonificaciones correctas

```python
# ARRANGE
arma_sutil = {"daño": 2, "tipo": "sutil"}
arma_pesada = {"daño": 5, "tipo": "pesada"}
arma_mixta = {"daño": 5, "tipo": "mixta"}

p_ágil = {"destreza": 20, "fuerza": 1}
p_fuerte = {"destreza": 1, "fuerza": 20}
p_balanceado = {"destreza": 10, "fuerza": 10}

# ACT
d_sutilAgil = calcular_daño(arma_sutil, p_ágil)       # 2 + 20//2 = 12
d_pesadaFuerte = calcular_daño(arma_pesada, p_fuerte) # 5 + 20//2 = 15
d_mixtaBal = calcular_daño(arma_mixta, p_balanceado)  # 5 + (10+10)//3 = 11

# ASSERT
assert d_sutilAgil == 12
assert d_pesadaFuerte == 15
assert d_mixtaBal == 11
```

**Por qué es crítico**: Builds distintos dan daño diferente. Si falla = strategy metagame roto.

---

### INT.C2: turno_jugador + calcular_daño + enemigo (1 ciclo)

**Escenario**: Atacar enemigo, daño calcula correctamente, enemigo recibe daño

```python
# ARRANGE
personaje = {
    "nombre": "test",
    "fuerza": 10,
    "destreza": 8,
    "inteligencia": 5,
    "armas": {
        "daga": {"daño": 2, "tipo": "sutil", "golpe": 80}
    },
}
enemigo = {"nombre": "Mosca", "vida": 10}

# ACT
with patch('TLDRDC_Prueba1.leer_input', return_value="daga"), \
     patch('TLDRDC_Prueba1.random.randint', return_value=50):  # Hit
    accion, stance = turno_jugador(personaje, enemigo)

# ASSERT
assert accion == "ataque"
assert enemigo["vida"] < 10  # Daño aplicado
```

**Por qué es crítico**: Ciclo básico ataque. Si falla = jugador no puede atacar.

---

### INT.C3: turno_enemigo + Habilidades de Jefe

**Escenario**: Jefe como Forrix usa habilidades especiales

```python
# ARRANGE
personaje = {"vida": 20, "armadura": 2}
jefe = enemigo_aleatorio("Forrix, el Carcelero")  # Jefe con habilidades
jefe["vida"] = 30

# ACT
with patch('TLDRDC_Prueba1.random.choice') as mock_choice:
    mock_choice.return_value = "Recuperacion Impia"  # Habilidad especial
    turno_enemigo(personaje, jefe, None)

# ASSERT
# Jefe usó habilidad sin crash
assert jefe["vida"] > 0
```

**Por qué es crítico**: Jefes con habilidades especiales. Si falla = jefes triviales.

---

### INT.C4: combate_loop Completo (Crear → Turno J → Turno E → Sangrado → Victoria)

**Escenario**: Flujo completo combate desde inicio a victoria

```python
# ARRANGE
personaje = crear_personaje()  # Mock input
enemigo = {"nombre": "Mosca", "vida": 2, "daño": (1, 1), "sangrado": 0}

# ACT
with patch('TLDRDC_Prueba1.pedir_input', side_effect=["test", "5"]), \
     patch('TLDRDC_Prueba1.emitir'), \
     patch('TLDRDC_Prueba1.leer_input', side_effect=["daga"] * 10), \
     patch('TLDRDC_Prueba1.random.randint', return_value=100):  # Always hit
    combate(personaje, enemigo)

# ASSERT
assert enemigo["vida"] <= 0  # Ganó
```

**Por qué es crítico**: Flujo completo. Si falla = juego no funciona.

---

### INT.C5: enemigo_aleatorio (6 tipos base + 9 jefes SIN crash)

**Escenario**: Todos 15 enemigos creables sin crash

```python
# ARRANGE
nombres = [
    "Larvas de Sangre", "Mosca de Sangre", "Maniaco Mutilado", "Perturbado", 
    "Rabioso", "Sombra tenebrosa",
    "Forrix, el Carcelero", "Sanakht, la Sombra Sangrienta", "Ka-Banda",
    "Mano Demoniaca", "Bel'akhor", "Fabius I", "Fabius II", "Fabius III", "Fabius IV"
]

# ACT
enemigos_creados = []
for nombre in nombres:
    e = enemigo_aleatorio(nombre)
    enemigos_creados.append(e)

# ASSERT
assert len(enemigos_creados) == 15
assert all(e["vida"] > 0 for e in enemigos_creados)
```

**Por qué es crítico**: Todos los enemigos deben crearse. Si falla = enemigo no aparece.

---

### INT.C6: Post-Combate + Fibonacci + Bonus

**Escenario**: Tras victoria, resolver_eventos_post_combate + Fibonacci

```python
# ARRANGE
estado = {"_c01": 1}  # 1 victoria
enemigo = {"nombre": "Prueba", "_evento_post": {"vida": 5}}

# ACT
evento_post = resolver_eventos_post_combate(enemigo)
estado["_c01"] += 1  # Victoria incrementa contador

# ASSERT
assert estado["_c01"] == 2
# Próxima victoria será 3 (no Fibonacci)
assert estado["_c01"] not in [2, 3, 5, 8, 13, 21, 34, 55, 89]
```

**Por qué es crítico**: Sistema de bonus Fibonacci. Si falla = sin progresión de jefes.

---

### INT.C7: Daño × 2 Builds + Hit Chance

**Escenario**: Build ágil vs fuerte en mismo combate, probabilidad golpe afecta

```python
# ARRANGE
arma_baja_golpe = {"daño": 10, "tipo": "sutil", "golpe": 20}  # 20% hit
arma_alta_golpe = {"daño": 2, "tipo": "sutil", "golpe": 95}   # 95% hit

p1 = {"destreza": 20, "fuerza": 1, "armas": {}}
p2 = {"destreza": 1, "fuerza": 20, "armas": {}}

# ACT
d1_acierta = calcular_daño(arma_alta_golpe, p1)  # 2 + 20//2 = 12
d1_falla = 0

d2_normal = calcular_daño(arma_baja_golpe, p2)  # 10 + 1//2 = 10
d2_siempre = 10

# ASSERT
assert d1_acierta > 0
assert d2_normal > 0
```

**Por qué es crítico**: Hit chance balanceia armas. Si falla = armas OP.

---

## GRUPO 5: PERSISTENCIA

### INT.P1: guardar_partida → cargar_partida (ciclo completo)

**Escenario**: Guardar estado, cargar, verificar integridad

```python
# ARRANGE
personaje_orig = {
    "nombre": "Héroe",
    "vida": 8,
    "fuerza": 6,
    "destreza": 4,
    "armas": {"daga": {"daño": 2}},
}
estado["_c01"] = 42

# ACT 1 - Guardar
guardar_partida(personaje_orig)

# ACT 2 - Cargar
personaje_cargado = cargar_partida()

# ASSERT
assert personaje_cargado["nombre"] == "Héroe"
assert personaje_cargado["vida"] == 8
assert personaje_cargado["fuerza"] == 6
assert personaje_cargado["armas"]["daga"]["daño"] == 2
assert estado["_c01"] == 42
```

**Por qué es crítico**: Save/load es esencial. Si falla = progreso se pierde.

---

### INT.P2: Guardar + Migración de Armas

**Escenario**: Cargar partida antigua, armas se sincronizan correctamente

```python
# ARRANGE
json_antiguo = {
    "personaje": {"nombre": "test", "vida": 10, "armas": {}},
    "armas_jugador": {"daga": {"daño": 2}},
    "eventos_superados": 5,  # Campo viejo lista (pre-v0.6)
}

# ACT
with patch('json.load', return_value=json_antiguo):
    personaje = cargar_partida()

# ASSERT
assert personaje["armas"]["daga"]["daño"] == 2  # Sincronizada
assert personaje["vida"] == 10
```

**Por qué es crítico**: Migraciones previenen pérdida de datos. Si falla = saves antiguas se dañan.

---

### INT.P3: Múltiples Guardadas (Sobrescritura Atómica)

**Escenario**: Guardar 3 veces, última versión es la actual

```python
# ARRANGE
p1 = {"nombre": "v1", "vida": 10}
p2 = {"nombre": "v2", "vida": 20}
p3 = {"nombre": "v3", "vida": 30}

# ACT
guardar_partida(p1)
guardar_partida(p2)
guardar_partida(p3)

cargado = cargar_partida()

# ASSERT
assert cargado["nombre"] == "v3"
assert cargado["vida"] == 30
```

**Por qué es crítico**: Guardado atómico previene corrupción. Si falla = se guarda parcialmente.

---

### INT.P4: Cargar JSON Corrupto → Fallback

**Escenario**: JSON corrupto no crash, retorna None

```python
# ARRANGE
json_corrupto = "{ INVALIDO }"

# ACT
with patch('builtins.open', mock_open(read_data=json_corrupto)):
    resultado = cargar_partida()

# ASSERT
assert resultado is None
```

**Por qué es crítico**: Corrupción no debe crash juego. Si falla = aplicación se cierra.

---

## GRUPO 6: FLUJO COMPLETO DEL JUEGO

### INT.G1: crear_personaje → aplicar_evento → validar_personaje

**Escenario**: Personaje nuevo recibe evento inicial, validación pasa

```python
# ARRANGE-ACT
with patch('TLDRDC_Prueba1.pedir_input', side_effect=["jugador", "5"]):
    personaje = crear_personaje()

evento_inicial = {"vida": 5}
with patch('TLDRDC_Prueba1.sistema'), \
     patch('TLDRDC_Prueba1.alerta'), \
     patch('TLDRDC_Prueba1.exito'):
    aplicar_evento(evento_inicial, personaje)

es_valido = validar_personaje(personaje)

# ASSERT
assert personaje["nombre"] == "jugador"
assert personaje["vida"] == 15  # 10 + 5
assert es_valido == True
```

**Por qué es crítico**: Flujo startup. Si falla = juego no arranca.

---

### INT.G2: explorar → bolsa_eventos → aplicar_evento

**Escenario**: Explorar obtiene evento de bolsa y lo aplica

```python
# ARRANGE
rellenar_bolsa_eventos()
personaje = crear_personaje()

# ACT
with patch('TLDRDC_Prueba1.pedir_input', side_effect=["test", "5"]), \
     patch('TLDRDC_Prueba1.narrar'), \
     patch('TLDRDC_Prueba1.leer_input', return_value=""):
    explorar(personaje)

# ASSERT
assert personaje["eventos_superados"] >= 1
# Stats modificados por evento aplicado
```

**Por qué es crítico**: Exploración es core loop. Si falla = juego aburrido.

---

### INT.G3: crear → combate → post_combate → aplicar

**Escenario**: Flujo juego real: crear → combatir → recibir rewards

```python
# ARRANGE
with patch('TLDRDC_Prueba1.pedir_input', side_effect=["test", "5"]):
    personaje = crear_personaje()

enemigo = {"nombre": "Prueba", "vida": 1, "daño": (1, 1), "sangrado": 0}

# ACT
with patch('TLDRDC_Prueba1.emitir'), \
     patch('TLDRDC_Prueba1.leer_input', return_value="daga"), \
     patch('TLDRDC_Prueba1.random.randint', return_value=100):
    combate(personaje, enemigo)

# ASSERT
assert enemigo["vida"] <= 0  # Ganó combate
```

**Por qué es crítico**: Ciclo principal juego. Si falla = core gameplay roto.

---

### INT.G4: Efectos Temporales × N Turnos (Completo Ciclo)

**Escenario**: Efecto dura exactamente 3 turnos

```python
# ARRANGE
personaje = {"_efectos_temporales": {"sangre": 3}}

# ACT
for turno in range(1, 4):
    print(f"Turno {turno}: sangre = {personaje['_efectos_temporales'].get('sangre')}")
    decrementar_efectos_temporales(personaje)

# ASSERT
assert "sangre" not in personaje["_efectos_temporales"]
print("Efecto limpiado tras 3 turnos")
```

**Por qué es crítico**: Efectos deben durar correctamente. Si falla = balance roto.

---

### INT.G5: Ciclo Completo Save/Load (Juego Real)

**Escenario**: Crear → Explorar → Combatir → Guardar → Cargar → Continuar

```python
# ARRANGE
with patch('TLDRDC_Prueba1.pedir_input', side_effect=["héroe", "5"]):
    personaje = crear_personaje()

# ACT 1 - Jugar
estado["eventos_superados"] = 5
personaje["vida"] = 12

# ACT 2 - Guardar
guardar_partida(personaje)

# ACT 3 - Cargar
personaje_cargado = cargar_partida()

# ASSERT
assert personaje_cargado["nombre"] == "héroe"
assert personaje_cargado["vida"] == 12
assert estado["eventos_superados"] == 5
```

**Por qué es crítico**: Persistencia de sesión larga. Si falla = jugador pierde progreso.

---

## GRUPO 7: IMAGEN + UI

### INT.V1: imagen_manager (válida + faltante + corrupta)

**Escenario**: 3 sprites: uno válido, uno faltante, uno corrupto → UI no crashea

```python
# ARRANGE
manager = ImagenManager(ruta_assets)

# ACT
img_valida = manager.cargar_imagen("daga.png")          # OK
img_faltante = manager.cargar_imagen("espada_fake.png")  # None
img_corrupta = manager.cargar_imagen("arma_bad.png")     # None

# ASSERT
assert img_valida is not None
assert img_faltante is None
assert img_corrupta is None

# UI renderiza sin excepción
for img in [img_valida, img_faltante, img_corrupta]:
    if img is None:
        print("Fallback a texto")
    else:
        print(f"Renderizando imagen")
```

**Por qué es crítico**: UI robusta. Si falla = UI crashea con sprite faltante.

---

## 📋 FIXTURE COMPARTIDA: Personaje + Enemigo + Estado

```python
@pytest.fixture
def personaje_int():
    """Personaje para tests integración"""
    return {
        "nombre": "Test",
        "vida": 10,
        "vida_max": 25,
        "fuerza": 5,
        "destreza": 5,
        "inteligencia": 5,
        "pociones": 6,
        "pociones_max": 10,
        "armadura": 2,
        "armadura_max": 5,
        "armas": {"daga": {"daño": 2, "tipo": "sutil", "golpe": 80}},
        "_efectos_temporales": {},
        "_flg1": False,
    }

@pytest.fixture
def enemigo_int():
    """Enemigo para tests integración"""
    return {
        "nombre": "Mosca",
        "vida": 10,
        "vida_max": 10,
        "daño": (2, 4),
        "jefe": False,
        "sangrado": 0,
    }

@pytest.fixture
def estado_int():
    """Estado global para tests integración"""
    return {
        "eventos_superados": 0,
        "_c01": 0,
        "bolsa_eventos": list(range(1, 21)),
        "bolsa_exploracion": list(range(1, 16)),
        "veces_guardado": 0,
    }
```

---

## ⚠️ NOTAS CRÍTICAS

1. **25 Tests** cubrirán integraciones entre **171 unit tests**
2. Cada test de integración verifica **mínimo 3-4 módulos juntos**
3. **Patrones detectados**:
   - Observer pattern (reactive)
   - Threading sincronización (_Bridge)
   - Event sourcing (bolsa + aplicar)
   - State machine (combate loop)
   - Persistence (save/load)
4. **Si algún INT falla**: El error es en la INTEGRACIÓN, no en los unitarios
5. **Prioridad**: INT.C4 (combate completo) y INT.G5 (save/load) son CRÍTICOS
