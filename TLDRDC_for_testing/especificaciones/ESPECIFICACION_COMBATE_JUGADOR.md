# Especificación de Tests — COMBATE_JUGADOR

*Versión: 1.3 (Simplificado + Stances)*

**Total: 16 tests**
- T1: `calcular_daño(arma, personaje)` (6 tests)
- T2: `turno_jugador(personaje, enemigo)` (10 tests)

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

## PARTE 2: TURNO_JUGADOR (8 tests)

### Descripción
Lee acción del jugador (ataque/poción/huida/stance), ejecuta, retorna `("ataque"|"huida", stance)`.

**Nota**: Versión simplificada (8 tests) enfocada en **diferenciadores de comportamiento**. 
Combate completo e integraciones testadas en COMBATE_LOOP.md (T5-T7).

---

### T2.1: Ataque exitoso reduce vida enemigo
```
ARRANGE:
  - p = personaje_combate (armas cargadas)
  - e = enemigo_combate (vida 10)
  - Mock leer_input() → "daga"
  - Mock random.randint() → 96 (> 95% golpe, éxito)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "ataque"
  - e["vida"] < 10 (daño aplicado)
  - stance is None
```

### T2.2: Ataque falla cuando roll > probabilidad golpe
```
ARRANGE:
  - arma = {"daño": 2, "golpe": 10}
  - Mock leer_input() → nombre_arma
  - Mock random.randint() → 11 (> 10%, falla)
ACT:
  - turno_jugador(p, e)
ASSERT:
  - e["vida"] == 10 (sin daño)
```

### T2.3: Poción sana +4 vida
```
ARRANGE:
  - p["vida"] = 6, p["vida_max"] = 10, p["pociones"] = 2
  - Mock leer_input() → "p", luego "daga"
ACT:
  - turno_jugador(p, e)
ASSERT:
  - p["pociones"] == 1 (consumida)
  - p["vida"] == 10 (6 + 4, clampeada a max)
```

### T2.4: Poción bloqueada sin pociones
```
ARRANGE:
  - p["pociones"] = 0, p["vida"] = 5
  - Mock leer_input() → "p", luego "daga"
  - Mock alerta()
ACT:
  - turno_jugador(p, e)
ASSERT:
  - alerta.called (rechazada)
  - p["vida"] == 5 (sin cambios)
```

### T2.5: Huida exitosa cuando 1d20+destreza ≥ 15
```
ARRANGE:
  - p["destreza"] = 5
  - Mock leer_input() → "h"
  - Mock random.randint(1,20) → 10 (10+5=15, éxito)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "huida"
  - stance is None
```

### T2.6: Huida falla cuando 1d20+destreza < 15
```
ARRANGE:
  - p["destreza"] = 2
  - Mock leer_input() → "h", luego "daga"
  - Mock random.randint(1,20) → 5 (5+2=7, falla)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "ataque" (continúa turno)
  - Mock alerta() emitido (falla anunciada)
```

### T2.7: Stance bloquear activa
```
ARRANGE:
  - Mock leer_input() → "bl", "daga"
  - Mock sistema()
ACT:
  - turno_jugador(p, e)
ASSERT:
  - sistema.called (anuncio de stance)
  - "bloqueo" in última llamada a sistema()
```

### T2.8: Stance esquivar activa
```
ARRANGE:
  - Mock leer_input() → "esq", "daga"
  - Mock sistema()
ACT:
  - turno_jugador(p, e)
ASSERT:
  - sistema.called (anuncio de stance)
  - "esquiva" in última llamada a sistema()
```

### T2.9: Sin stance (ataque normal sin modificadores)
```
ARRANGE:
  - p = personaje_combate (sin stance activo)
  - e = enemigo_combate (vida 10)
  - arma = {"daño": 3, "golpe": 100}
  - Mock leer_input() → nombre_arma
  - Mock random.randint() → 80 (éxito)
ACT:
  - resultado, stance = turno_jugador(p, e)
ASSERT:
  - resultado == "ataque"
  - stance is None (sin stance)
  - e["vida"] == 7 (daño completo: 10 - 3)
```

### T2.10: Efectos de arma aplicados (sangrado, stun, vida)
```
ARRANGE:
  - arma = {"daño": 5, "golpe": 100, "sangrado": 2, "stun": 3, "vida": 1, "tipo": "sutil"}
  - e = {"vida": 10, "sangrado": 0, "stun": 0}
  - p["vida"] = 5, p["vida_max"] = 10
  - Mock leer_input() → nombre_arma
  - Mock random.randint() → 100 (éxito + stun activation)
ACT:
  - turno_jugador(p, e)
ASSERT:
  - e["sangrado"] == 2
  - e["stun"] >= 1
  - p["vida"] == 6 (lifesteal aplicado: 5 + 1)
```

---

## FIXTURES NECESARIAS

```python
# Desde conftest_combate.py
personaje_combate = {
    "nombre": "jugador",
    "vida": 10,
    "vida_max": 25,
    "fuerza": 5,
    "destreza": 5,
    "pociones": 6,
    "pociones_max": 10,
    "armadura": 2,
    "armadura_max": 5,
    "armas": {...},  # Cargadas desde estado_global_mock
    "_huyo_combate": False,
    "_efectos_temporales": {},
    "stun": 0,
}

enemigo_combate = {
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
| Total Tests | 16 |
| T1 (calcular_daño) | 6 tests |
| T2 (turno_jugador) | 10 tests (simplificado didáctico) |
| Versión | 1.3 (Simplified + Stances) |
| Mocks Principales | leer_input, random.randint, alerta, sistema |
| Nota | Integración completa de combate en COMBATE_LOOP.md |
