# Especificación de Tests — TLDRDC CORE

*Versión: 1.0*

**Total: 32 tests**

---

## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| 1.1 | crear_personaje | Entrada válida |
| 1.2 | crear_personaje | Nombre vacío rechazado |
| 1.3 | crear_personaje | Fuerza fuera rango |
| 1.4 | crear_personaje | Armadura según destreza |
| 1.5 | crear_personaje | Nombre a lowercase |
| 1.6 | crear_personaje | Campos máximos y secretos |
| 2.1 | aplicar_evento | Suma vida normal |
| 2.2 | aplicar_evento | Vida clampea máximo |
| 2.3 | aplicar_evento | Vida clampea mínimo |
| 2.4 | aplicar_evento | Muerte → fin_derrota() + early return |
| 2.5 | aplicar_evento | Pociones clampea máximo |
| 2.6 | aplicar_evento | Stats clampean a 20 |
| 2.7 | aplicar_evento | Armadura no baja de 0 |
| 2.8 | aplicar_evento | Añadir arma válida |
| 2.9 | aplicar_evento | Múltiples cambios simultáneos |
| 2.10 | aplicar_evento | Stats negativos sin límite mínimo |
| 2.11 | aplicar_evento | Pociones pueden ser negativas |
| 2.12 | aplicar_evento | Key desconocida se asigna con alerta |
| 2.13 | aplicar_evento | Key válida no existente se suma |
| 2.14 | aplicar_evento | Callback UI armas se invoca |
| 3.1 | fin_derrota | Retorna True si tiene _flg1 |
| 3.2 | fin_derrota | Retorna False sin _flg1 |
| 3.3 | fin_derrota | Limpia _flg1 tras usar |
| 4.1 | resolver_eventos_post_combate | Retorna evento tras victoria |
| 4.2 | resolver_eventos_post_combate | Retorna None sin evento |
| 5.1 | explorar | Retorna texto + aplica evento |
| 5.2 | explorar | Actualiza eventos_superados |
| 5.3 | explorar | Maneja exploración sin evento |
| 6.1 | validar_personaje | Personaje válido retorna True |
| 6.2 | validar_personaje | Personaje inválido retorna False |
| 7.1 | decrementar_efectos_temporales | Decrementa jugador |
| 7.2 | decrementar_efectos_temporales | Limpia enemigo con duración ≤0 |

---

# PARTE 1: CREAR_PERSONAJE (6 tests)

### Descripción
Función que crea un nuevo personaje mediante entrada del usuario. 
- Loop: pregunta nombre (debe ser no vacío, se convierte a lowercase)
- Loop: pregunta fuerza en rango [1-9]
- Calcula destreza = 10 - fuerza
- Calcula armadura según destreza: (≥9→4, ≥6→2, ≥3→1, resto→0)
- Inicializa campos máximos y secretos

### 1.1: Entrada válida primera vez
```
ARRANGE:
  - Mock pedir_input() → ["jugador", "5"]
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "jugador"
  - p["fuerza"] == 5
  - p["destreza"] == 5
  - p["vida"] == 10
  - p["pociones"] == 6
  - p["vida_max"] == 25
  - p["pociones_max"] == 10
  - p["armadura_max"] == 5
```

### 1.2: Nombre vacío se rechaza
```
ARRANGE:
  - Mock pedir_input() → ["", "", "test", "5"]
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "test"
  - pedir_input() llamado 4 veces (2 intentos nombre + 1 ok + 1 fuerza)
```

### 1.3: Fuerza fuera [1-9] se rechaza
```
ARRANGE:
  - Mock pedir_input() → ["test", "0", "10", "5"]
ACT:
  - p = crear_personaje()
ASSERT:
  - p["fuerza"] == 5
  - pedir_input() llamado 4 veces
```

### 1.4: Armadura según destreza (extremos)
```
ARRANGE:
  - Mock pedir_input() → ["test", "1"] (destreza=9)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["destreza"] == 9
  - p["armadura"] == 4

ARRANGE ALTERNATE:
  - Mock pedir_input() → ["test", "9"] (destreza=1)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["destreza"] == 1
  - p["armadura"] == 0
```

### 1.5: Nombre se convierte a lowercase
```
ARRANGE:
  - Mock pedir_input() → ["JuGaDoR", "5"]
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "jugador"
```

### 1.6: Campos máximos y secretos inicializados
```
ARRANGE:
  - Mock pedir_input() → ["test", "5"]
ACT:
  - p = crear_personaje()
ASSERT:
  - Campos max: vida_max=25, pociones_max=10, armadura_max=5
  - Campos secretos: moscas=0, brazos=0, sombra=0, sangre=0
  - _pw=0, tiene_llave=False, rencor=False
  - bolsa_acecho=[1,2,3]
  - _x9f=False
```

---

## PARTE 2: APLICAR_EVENTO (14 tests)

### Descripción
Aplica un evento (dict de cambios) al personaje. Itera claves y suma valores según tipo.
- "vida": suma (clampea [0, vida_max]), si=0→fin_derrota()+return
- "pociones": suma (clampea [0, pociones_max])
- "fuerza"/"destreza": suma (clampea [0, 20])
- "armadura": suma (clampea [0, armadura_max])
- "armas": dict de armas → añade + callback UI

### 2.1: Suma vida normal
```
ARRANGE:
  - p = {"vida": 10, "vida_max": 15}
  - evento = {"vida": 3}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 13
```

### 2.2: Vida clampea máximo
```
ARRANGE:
  - p = {"vida": 12, "vida_max": 15}
  - evento = {"vida": 10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 15
```

### 2.3: Vida clampea 0 (mínimo)
```
ARRANGE:
  - p = {"vida": 5}
  - evento = {"vida": -10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 0
```

### 2.4: Vida a 0 → fin_derrota() + early return
```
ARRANGE:
  - p = {"vida": 2}
  - evento = {"vida": -2, "fuerza": 5}
  - Mock fin_derrota()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - fin_derrota() llamado una vez
  - p["fuerza"] NO modificado (early return)
```

### 2.5: Pociones clampea máximo
```
ARRANGE:
  - p = {"pociones": 8, "pociones_max": 10}
  - evento = {"pociones": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == 10
```

### 2.6: Stats clampean a 20
```
ARRANGE:
  - p = {"fuerza": 18}
  - evento = {"fuerza": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["fuerza"] == 20
```

### 2.7: Armadura no baja de 0
```
ARRANGE:
  - p = {"armadura": 2}
  - evento = {"armadura": -5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["armadura"] == 0
```

### 2.8: Añadir arma válida
```
ARRANGE:
  - p = {"armas": {}}
  - evento = {"armas": {"daga": {"daño": 2}}}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["armas"]["daga"] == {"daño": 2}
```

### 2.9: Múltiples cambios simultáneos
```
ARRANGE:
  - p = {"vida": 10, "fuerza": 5, "pociones": 3}
  - evento = {"vida": 2, "fuerza": 3, "pociones": 1}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 12
  - p["fuerza"] == 8
  - p["pociones"] == 4
```

### 2.10: Stats negativos sin límite mínimo
```
ARRANGE:
  - p = {"fuerza": 5}
  - evento = {"fuerza": -10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["fuerza"] == -5
```

### 2.11: Pociones pueden ser negativas
```
ARRANGE:
  - p = {"pociones": 2, "pociones_max": 10}
  - evento = {"pociones": -5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == -3
```

### 2.12: Key desconocida se asigna con alerta
```
ARRANGE:
  - p = {"vida": 10}
  - evento = {"campo_nuevo": 5}
  - Mock alerta()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - alerta() llamado
  - p["campo_nuevo"] == 5
```

### 2.13: Key válida no existente se suma
```
ARRANGE:
  - p = {"vida": 10}
  - evento = {"moscas": 1}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["moscas"] == 1
```

### 2.14: Callback UI armas se invoca
```
ARRANGE:
  - p = {"armas": {}}
  - evento = {"armas": {"daga": {"daño": 2}}}
  - Mock _callback_ui_armas()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - _callback_ui_armas() llamado
  - p["armas"]["daga"] presente
```

---

## PARTE 3: FIN_DERROTA (3 tests)

### Descripción
Gestiona la derrota del jugador. Si personaje tiene _flg1 (revive), lo limpia y retorna True.
Caso contrario retorna False.

### 3.1: Retorna True si tiene _flg1
```
ARRANGE:
  - p = {"_flg1": True}
  - Mock sistema() para UI
ACT:
  - resultado = fin_derrota(p)
ASSERT:
  - resultado == True
  - "_flg1" not in p
```

### 3.2: Retorna False sin _flg1
```
ARRANGE:
  - p = {"_flg1": False}
  - Mock sistema()
ACT:
  - resultado = fin_derrota(p)
ASSERT:
  - resultado == False
  - p["_flg1"] == False
```

### 3.3: Limpia _flg1 tras usar
```
ARRANGE:
  - p = {"_flg1": True}
  - Mock sistema()
ACT:
  - fin_derrota(p)
  - resultado2 = fin_derrota(p)
ASSERT:
  - Primera llamada: True
  - Segunda llamada: False
```

---

## PARTE 4: RESOLVER_EVENTOS_POST_COMBATE (2 tests)

### Descripción
Retorna un evento al jugador tras victoria en combate si existen condiciones especiales.
Retorna None si no hay evento especial.

### 4.1: Retorna evento tras victoria
```
ARRANGE:
  - personaje = {"vida": 10}
  - enemigo = {"nombre": "Carcelero"}
  - Mock obtener_evento_de_bolsa() → {"vida": 2}
ACT:
  - evento = resolver_eventos_post_combate(personaje, enemigo)
ASSERT:
  - evento is not None
  - evento["vida"] == 2
```

### 4.2: Retorna None sin evento
```
ARRANGE:
  - personaje = {"vida": 10}
  - enemigo = {"nombre": "Carcelero"}
  - Mock obtener_evento_de_bolsa() → None
ACT:
  - evento = resolver_eventos_post_combate(personaje, enemigo)
ASSERT:
  - evento is None
```

---

## PARTE 5: EXPLORAR (3 tests)

### Descripción
Realiza exploración: obtiene texto + evento, aplica cambios, retorna descripción.

### 5.1: Retorna texto + aplica evento
```
ARRANGE:
  - p = personaje_base.copy()
  - Mock obtener_texto_exploracion_de_bolsa() → "Encuentras un cofre..."
  - Mock obtener_evento_de_bolsa() → {"vida": 1}
ACT:
  - resultado = explorar(p)
ASSERT:
  - resultado contiene "cofre" (o similar)
  - p["vida"] fue modificado
```

### 5.2: Actualiza eventos_superados
```
ARRANGE:
  - estado["eventos_superados"] = 0
  - Mock obtener_texto/evento
ACT:
  - explorar(personaje)
ASSERT:
  - estado["eventos_superados"] == 1
```

### 5.3: Maneja exploración sin evento
```
ARRANGE:
  - Mock obtener_evento_de_bolsa() → None
ACT:
  - resultado = explorar(personaje)
ASSERT:
  - personaje NO modificado
  - resultado contiene texto
```

---

## PARTE 6: VALIDAR_PERSONAJE (2 tests)

### Descripción
Valida que personaje tenga todos los campos críticos requeridos.

### 6.1: Personaje válido retorna True
```
ARRANGE:
  - p = personaje_base.copy() (con todos campos)
ACT:
  - valido = validar_personaje(p)
ASSERT:
  - valido == True
```

### 6.2: Personaje inválido retorna False
```
ARRANGE:
  - p = personaje_base.copy()
  - del p["vida"]
ACT:
  - valido = validar_personaje(p)
ASSERT:
  - valido == False
```

---

## PARTE 7: DECREMENTAR_EFECTOS_TEMPORALES (2 tests)

### Descripción
Decrementa duración de efectos temporales cada turno.
- Jugador: resta 1 a cada efecto
- Enemigo: además limpia efectos con duración ≤ 0

### 7.1: Decrementa jugador
```
ARRANGE:
  - p = {"_efectos_temporales": {"stun": 2, "bleed": 1}}
ACT:
  - decrementar_efectos_temporales_jugador(p)
ASSERT:
  - p["_efectos_temporales"]["stun"] == 1
  - p["_efectos_temporales"]["bleed"] == 0
```

### 7.2: Limpia enemigo con duración ≤ 0
```
ARRANGE:
  - e = {"_efectos_temporales": {"stun": 0, "bleed": 1}}
ACT:
  - decrementar_efectos_temporales_enemigo(e)
ASSERT:
  - "stun" not in e["_efectos_temporales"]
  - e["_efectos_temporales"]["bleed"] == 0
```

---

## FIXTURES

```python
@pytest.fixture
def personaje_core():
    return {
        "nombre": "test",
        "vida": 10,
        "vida_max": 25,
        "fuerza": 5,
        "destreza": 5,
        "pociones": 6,
        "pociones_max": 10,
        "armadura": 2,
        "armadura_max": 5,
        "armas": {},
        "_efectos_temporales": {},
        "_flg1": False,
    }

@pytest.fixture
def enemigo_core():
    return {
        "nombre": "Carcelero",
        "vida": 20,
        "vida_max": 20,
        "daño": (2, 4),
        "jefe": False,
        "_efectos_temporales": {},
    }

@pytest.fixture
def estado_core():
    return {
        "eventos_superados": 0,
        "_c01": 0,
    }
```
