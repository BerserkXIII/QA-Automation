# Especificación de Tests — COMBATE_LOOP

*Versión: 1.0*

**Total: 15 tests**
- T5: `combate(personaje, enemigo)` (9 tests)
- T6: `aplicar_sangrado(enemigo)` (3 tests)
- T7: Bonus Fibonacci (3 tests)

---

## PARTE 1: COMBATE LOOP (9 tests)

### Descripción
Loop principal: HUD → turno_jugador → turno_enemigo → sangrado

Condiciones fin: huida, victoria, derrota
Post-combate: evento, bonus fibonacci

### T5.1: Crea enemigo si None
```
ARRANGE:
  - enemigo = None
ACT:
  - combate(p, None)
ASSERT:
  - Sin crash (enemigo creado)
```

### T5.2: Loop turno_jugador ejecutado
```
ARRANGE:
  - Mock turno_jugador
ACT:
  - combate(p, e)
ASSERT:
  - turno_jugador() llamado >= 1 vez
```

### T5.3: Loop turno_enemigo ejecutado
```
ARRANGE:
  - Mock turno_enemigo
ACT:
  - combate(p, e)
ASSERT:
  - turno_enemigo() llamado >= 1 vez
```

### T5.4: Sangrado aplicado cada ciclo
```
ARRANGE:
  - e = {"sangrado": 2}
ACT:
  - combate(p, e) [1 ciclo hasta victoria]
ASSERT:
  - aplicar_sangrado() llamado
```

### T5.5: Fin Huida retorna inmediatamente
```
ARRANGE:
  - Mock turno_jugador → ("huida", None)
ACT:
  - combate(p, e)
ASSERT:
  - p["_huyo_combate"] == True
  - Función retorna inmediatamente
```

### T5.6: Fin Victoria (enemigo muere)
```
ARRANGE:
  - Mock turno_jugador → ataque que mata
  - e["vida"] = 1
ACT:
  - combate(p, e)
ASSERT:
  - Break del loop
  - Exito: "Has vencido"
```

### T5.7: Fin Derrota (jugador muere)
```
ARRANGE:
  - Mock turno_enemigo → daño que mata
  - p["vida"] = 1
ACT:
  - combate(p, e)
ASSERT:
  - Alerta: "Has sido derrotado"
  - fin_derrota() llamado
```

### T5.8: Post-combate evento aplicado
```
ARRANGE:
  - Mock resolver_eventos_post_combate() → {"vida": 5}
  - Victoria
ACT:
  - combate(p, e)
ASSERT:
  - aplicar_evento() llamado
```

### T5.9: HUD emitido cada turno
```
ARRANGE:
  - Mock emitir()
ACT:
  - combate(p, e) [1 ciclo]
ASSERT:
  - emitir("hud_combate", {...}) llamado
  - Contiene: vida, enemigo_nombre, etc.
```

---

## PARTE 2: SANGRADO (3 tests)

### Descripción
Aplica daño acumulado de sangrado al final de cada turno.

### T6.1: Sangrado base daño
```
ARRANGE:
  - e = {"sangrado": 3, "vida": 10}
ACT:
  - aplicar_sangrado(e)
ASSERT:
  - e["vida"] == 7
  - Alerta: "sangra"
```

### T6.2: Sin sangrado (0)
```
ARRANGE:
  - e = {"sangrado": 0, "vida": 10}
ACT:
  - aplicar_sangrado(e)
ASSERT:
  - e["vida"] == 10
```

### T6.3: Muerte por sangrado
```
ARRANGE:
  - e = {"sangrado": 15, "vida": 10}
ACT:
  - aplicar_sangrado(e)
ASSERT:
  - e["vida"] == -5 (sin clamp mínimo)
```

---

## PARTE 3: FIBONACCI BONUS (3 tests)

### Descripción
Sistema de bonificación por hitos de victorias (números Fibonacci).

Fibonacci set: {2, 3, 5, 8, 13, 21, 34, 55, 89}
Fates (_fate_01 a _fate_06) activados en hitos

### T7.1: revisar_bonus_fibonacci() se llama
```
ARRANGE:
  - estado["_c01"] = 2 (Fibonacci)
  - Mock revisar_bonus_fibonacci()
ACT:
  - combate(p, e) con victoria
ASSERT:
  - revisar_bonus_fibonacci() llamado
```

### T7.2: Contador victoria incrementado
```
ARRANGE:
  - estado["_c01"] = 10
ACT:
  - combate(p, e) con victoria
ASSERT:
  - estado["_c01"] == 11
```

### T7.3: _fate_04 si _c01 >= 100
```
ARRANGE:
  - estado["_c01"] = 100
  - Mock _fate_04()
ACT:
  - combate(p, e) con victoria
ASSERT:
  - _fate_04() llamado
```

---

## FIXTURES NECESARIAS

```python
personaje_base = {
    "nombre": "jugador",
    "vida": 10,
    "vida_max": 25,
    "fuerza": 5,
    "destreza": 5,
    "pociones": 6,
    "armadura": 2,
    "_huyo_combate": False,
    "_efectos_temporales": {},
    "stun": 0,
}

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

estado_base = {
    "_c01": 0,
}
```

---

## MOCKS NECESARIOS

- `turno_jugador()` - Entrada jugador
- `turno_enemigo()` - Turno enemigo
- `aplicar_sangrado()` - Sangrado
- `emitir()` - HUD
- `fin_derrota()` - Derrota
- `resolver_eventos_post_combate()` - Eventos
- `revisar_bonus_fibonacci()` - Bonus
- `random.randint()` - Tiradas

---

## RESUMEN

| Item | Valor |
|------|-------|
| Total Tests | 15 |
| Funciones | combate, aplicar_sangrado, revisar_bonus_fibonacci |
| Líneas Código | ~3945, ~3900, ~2797 |
| Conditions | huida, victoria, derrota, post-combate |
| Fibonacci Set | {2, 3, 5, 8, 13, 21, 34, 55, 89} |
