# Especificación de Tests — COMBATE_JUGADOR

*Versión: 1.0*

**Total: 22 tests**
- T1: `calcular_daño(arma, personaje)` (6 tests)
- T2: `turno_jugador(personaje, enemigo)` (16 tests)

---

## PARTE 1: CALCULAR_DAÑO (6 tests)

### Descripción
Función pura que calcula daño base + bonificación según tipo de arma.

```python
# Tipo arma → Bonificación
"sutil" → daño += personaje["destreza"] // 2
"pesada" → daño += personaje["fuerza"] // 2
"mixta" → daño += (fuerza + destreza) // 3
None → sin bonificación
```

### T1.1: Daño base sin tipo
```
ARRANGE:
  - arma = {"daño": 3}
  - personaje = {"fuerza": 10, "destreza": 10}
ACT:
  - resultado = calcular_daño(arma, personaje)
ASSERT:
  - resultado == 3 (sin bonificación)
```

### T1.2: Sutil + destreza baja
```
ARRANGE:
  - arma = {"daño": 2, "tipo": "sutil"}
  - personaje = {"destreza": 4}
ACT:
  - resultado = calcular_daño(arma, personaje)
ASSERT:
  - resultado == 4 (2 + 4//2)
```

### T1.3: Sutil + destreza alta
```
ARRANGE:
  - arma = {"daño": 2, "tipo": "sutil"}
  - personaje = {"destreza": 10}
ACT:
  - resultado = calcular_daño(arma, personaje)
ASSERT:
  - resultado == 7 (2 + 10//2)
```

### T1.4: Pesada + fuerza
```
ARRANGE:
  - arma = {"daño": 5, "tipo": "pesada"}
  - personaje = {"fuerza": 8}
ACT:
  - resultado = calcular_daño(arma, personaje)
ASSERT:
  - resultado == 9 (5 + 8//2)
```

### T1.5: Mixta (fuerza + destreza)
```
ARRANGE:
  - arma = {"daño": 5, "tipo": "mixta"}
  - personaje = {"fuerza": 6, "destreza": 9}
ACT:
  - resultado = calcular_daño(arma, personaje)
ASSERT:
  - resultado == 10 (5 + (6+9)//3)
```

### T1.6: Builds extremos (máxima representación de stats)
```
ARRANGE:
  - arma_sutil = {"daño": 2, "tipo": "sutil"}
  - p_ágil = {"destreza": 20, "fuerza": 1}
  - p_fuerte = {"destreza": 1, "fuerza": 20}
ACT:
  - d1 = calcular_daño(arma_sutil, p_ágil)
  - arma_pesada = {"daño": 5, "tipo": "pesada"}
  - d2 = calcular_daño(arma_pesada, p_fuerte)
ASSERT:
  - d1 == 12 (2 + 20//2)
  - d2 == 15 (5 + 20//2)
```

---

## PARTE 2: TURNO_JUGADOR (16 tests)

### Descripción
Lee acción del jugador (ataque/poción/huida/stance), ejecuta, retorna `("ataque"|"huida", stance_actual)`.

**Acciones:**
- Ataque: nombre de arma
- Poción: "p", "pot", "pocion"
- Huida: "h", "huir"
- Bloquear: "bl", "blo", "bloquear"
- Esquivar: "esq", "esquivar"

**Modificadores de stance:**
- `bloquear`: daño *= 0.5
- `esquivar`: daño *= 0.67, probabilidad -= 33%

### T2.1: Ataque exitoso golpea
```
ARRANGE:
  - p = {"vida": 10, "destreza": 5, "armas": {"daga": {"daño": 2, "golpe": 100, "tipo": "sutil"}}}
  - e = {"vida": 10, "nombre": "Test", "esquiva": 0}
  - Mock leer_input() → "daga"
  - Mock random.randint(1,100) → 90
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "ataque"
  - e["vida"] < 10
  - stance is None
```

### T2.2: Ataque falla por % probabilidad
```
ARRANGE:
  - arma = {"daño": 2, "golpe": 10, "tipo": "sutil"}
  - Mock random.randint(1,100) → 11 (falla)
ACT:
  - turno_jugador(p, e)
ASSERT:
  - e["vida"] == 10 (sin daño)
```

### T2.3: Poción usa y sana +4
```
ARRANGE:
  - p = {"vida": 6, "vida_max": 10, "pociones": 2}
  - Mock leer_input() → "p", luego "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["pociones"] == 1
  - p["vida"] == 10
```

### T2.4: Poción solo 1x por turno
```
ARRANGE:
  - Mock leer_input() → "p", "p", "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["pociones"] == 4 (solo 1 consumida)
```

### T2.5: Sin pociones rechaza
```
ARRANGE:
  - p = {"vida": 5, "pociones": 0}
  - Mock leer_input() → "p", luego "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - Alerta emitida
  - p["vida"] == 5
```

### T2.6: Vida máxima rechaza poción
```
ARRANGE:
  - p = {"vida": 10, "vida_max": 10, "pociones": 1}
  - Mock leer_input() → "p", luego "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["pociones"] == 1 (no consumida)
```

### T2.7: Huida cálculo 1d20 + destreza ≥ 15
```
ARRANGE:
  - p = {"vida": 10, "destreza": 5}
  - Mock leer_input() → "h"
  - Mock random.randint(1,20) → 10 (10+5=15, éxito)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "huida"
  - stance is None
```

### T2.8: Huida solo 1 intento por turno
```
ARRANGE:
  - Mock leer_input() → "h", "h", "daga"
  - Mock random.randint → 5 (falla primer intento)
ACT:
  - turno_jugador(p, e)
ASSERT:
  - Alerta 2º intento: "Ya has intentado huir"
```

### T2.9: Huida retorna tupla
```
ARRANGE:
  - Mock random.randint → 20 (éxito garantizado)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - isinstance(resultado, str) and resultado == "huida"
  - stance is None
```

### T2.10: Stance Bloquear toggle ON
```
ARRANGE:
  - Mock leer_input() → "bl", "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - Sistema: "Postura de bloqueo activa"
```

### T2.11: Stance Esquivar toggle ON
```
ARRANGE:
  - Mock leer_input() → "esq", "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - Sistema: "Postura de esquiva activa"
```

### T2.12: Stance Bloquear reduce daño 50%
```
ARRANGE:
  - p = {"vida": 10, "fuerza": 10, "armas": {"test": {"daño": 10, "golpe": 100}}}
  - e = {"vida": 20, "nombre": "Test", "esquiva": 0}
  - stance = "bloquear"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - Daño aplicado < 10 (reducido por bloqueo)
```

### T2.13: Arma Sangrado
```
ARRANGE:
  - arma = {"daño": 5, "golpe": 100, "sangrado": 2, "tipo": "sutil"}
  - e = {"vida": 10, "sangrado": 0}
ACT:
  - turno_jugador(p, e)
ASSERT:
  - e["sangrado"] == 2
```

### T2.14: Arma Stun
```
ARRANGE:
  - arma = {"daño": 5, "golpe": 100, "stun": 3, "tipo": "sutil"}
  - e = {"vida": 10, "stun": 0}
  - Mock random.randint(1,6) → 2 (≤ 3, activa stun)
ACT:
  - turno_jugador(p, e)
ASSERT:
  - e["stun"] >= 1
```

### T2.15: Arma Vida (lifesteal)
```
ARRANGE:
  - arma = {"daño": 5, "golpe": 100, "vida": 3, "tipo": "sutil"}
  - p = {"vida": 5, "vida_max": 10}
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["vida"] == 8
```

### T2.16: Arma Auto-Daño
```
ARRANGE:
  - arma = {"daño": 7, "golpe": 100, "auto_daño": 1, "tipo": "sutil"}
  - p = {"vida": 10}
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["vida"] == 9
```

---

## FIXTURES NECESARIAS

```python
# Personaje base
personaje_base = {
    "nombre": "jugador",
    "vida": 10,
    "vida_max": 25,
    "fuerza": 5,
    "destreza": 5,
    "pociones": 6,
    "pociones_max": 10,
    "armadura": 2,
    "armadura_max": 5,
    "armas": {"daga": {"daño": 2, "golpe": 95, "sangrado": 1, "tipo": "sutil"}},
    "_huyo_combate": False,
    "_efectos_temporales": {},
    "stun": 0,
}

# Enemigo base
enemigo_base = {
    "nombre": "Larvas de Sangre",
    "vida": 10,
    "vida_max": 10,
    "daño": (1, 2),
    "esquiva": 17,
    "jefe": False,
    "armadura": 0,
    "stun": 0,
    "sangrado": 0,
    "habilidades": [],
    "_efectos_temporales": {},
}
```

---

## RESUMEN

| Item | Valor |
|------|-------|
| Total Tests | 22 |
| Función Principal | calcular_daño, turno_jugador |
| Líneas Código | ~864, ~3794 |
| Categorías | 2 |
| Mocks Necesarios | leer_input, random.randint |
