# Especificación de Tests — COMBATE_ENEMIGO

*Versión: 2.0*

**Total: 23 tests**
- T3: `enemigo_aleatorio(nombre)` + Jefes especiales (14 tests)
- T4: `turno_enemigo(personaje, enemigo, stance)` (9 tests)

---

## PARTE 1: ENEMIGO_ALEATORIO + JEFES (14 tests)

### Descripción
Genera enemigos aleatorios o específicos. Mapeo completo de 6 tipos base + 9 jefes especiales.

**Enemigos base (6):**
- Larvas de Sangre (10 hp)
- Mosca de Sangre (15 hp)
- Maniaco Mutilado (14 hp)
- Perturbado (18 hp)
- Rabioso (22 hp)
- Sombra tenebrosa (15 hp)

**Jefes especiales (9) — Orden de tests:**
1. Forrix: 30 hp (sangrado pasivo + recuperación impia)
2. Sanakht: 20 hp (acuchillamiento + esquiva)
3. Ka-Banda: 50 hp (frensi demoniaco)
4. Mano Demoniaca: 30 hp (regeneración)
5. Bel'akhor: 150 hp (4 habilidades)
6. Fabius v1: 45 hp (Hoz de Sangre)
7. Fabius v2: 60 hp (Hoja Noche)
8. Fabius v3: 30 hp (default)
9. Fabius v4: 0 hp (estado crítico/fallido)

### T3.1: Retorna enemigo con nombre
```
ARRANGE:
  - nombre = "Larvas de Sangre"
ACT:
  - e = enemigo_aleatorio("Larvas de Sangre")
ASSERT:
  - e["nombre"] == "Larvas de Sangre"
  - e["vida"] == 10
```

### T3.2: 6 tipos base diferentes
```
ARRANGE: Sin params
ACT:
  - enemigos = {enemigo_aleatorio()["nombre"] for _ in range(100)}
ASSERT:
  - len(enemigos) >= 4 (al menos 4 tipos en 100 intentos)
```

### T3.3: Nombre inexistente → aleatorio
```
ARRANGE:
  - nombre = "Enemigo Falso"
ACT:
  - e = enemigo_aleatorio("Enemigo Falso")
ASSERT:
  - e["nombre"] in lista_enemigos_validos
```

### T3.4: Estructura completa
```
ARRANGE: Cualquier enemigo
ACT:
  - e = enemigo_aleatorio()
ASSERT:
  - Campos presentes: nombre, vida, vida_max, daño, esquiva, jefe, armadura, habilidades, _efectos_temporales
```

### T3.5: Habilidades inicializadas
```
ARRANGE:
  - e = enemigo_aleatorio("Maniaco Mutilado")
ACT:
  - resultado
ASSERT:
  - e["habilidades"] es lista
  - len(e["habilidades"]) >= 1
```

### T3.6: Forrix, el Carcelero (30 hp - Jefe #1)
```
ARRANGE: crear_carcelero()
ACT:
  - e = enemigo_aleatorio("Forrix, el Carcelero")
ASSERT:
  - e["nombre"] == "Forrix, el Carcelero"
  - e["vida"] == 30
  - e["vida_max"] == 30
  - e["jefe"] == True
  - Habilidades incluyen:
    - Gancho de Carnicero (pasiva, sangrado 1)
    - Recuperacion Impia (activa, heal 4 + damage_boost 20%)
  - e["armadura"] >= 0
  - e["daño"] es tupla (min, max)
```

### T3.7: Sanakht, la Sombra Sangrienta (20 hp - Jefe #2)
```
ARRANGE: crear_sombra_sangrienta()
ACT:
  - e = enemigo_aleatorio("Sanakht, la Sombra Sangrienta")
ASSERT:
  - e["nombre"] == "Sanakht, la Sombra Sangrienta"
  - e["vida"] == 20
  - e["vida_max"] == 20
  - e["jefe"] == True
  - Habilidades incluyen:
    - Acuchillamiento (ataque especial + sangrado 2)
    - Sombra Oculta (pasiva, reduce precisión 2 turnos)
  - e["esquiva"] tiene valor específico
```

### T3.8: Ka-Banda (50 hp - Jefe #3)
```
ARRANGE: crear_ka_banda()
ACT:
  - e = enemigo_aleatorio("Ka-Banda")
ASSERT:
  - e["nombre"] == "Ka-Banda"
  - e["vida"] == 50
  - e["vida_max"] == 50
  - e["jefe"] == True
  - Habilidades incluyen:
    - Frensi Demoniaco (activa, damage_boost 50% por 2 turnos)
  - e["daño"] valor base para frensi
```

### T3.9: Mano Demoniaca (30 hp - Jefe #4)
```
ARRANGE: crear_mano_demoniaca()
ACT:
  - e = enemigo_aleatorio("Mano Demoniaca")
ASSERT:
  - e["nombre"] == "Mano Demoniaca"
  - e["vida"] == 30
  - e["vida_max"] == 30
  - e["jefe"] == True
  - Habilidades incluyen:
    - Regeneración (pasiva, heal 2 cada turno)
    - Garra Demoniaca (activa, damage_boost 25%)
  - e["_efectos_temporales"] inicializado
```

### T3.10: Bel'akhor (150 hp - Jefe #5)
```
ARRANGE: crear_bel_akhor()
ACT:
  - e = enemigo_aleatorio("Bel'akhor")
ASSERT:
  - e["nombre"] == "Bel'akhor"
  - e["vida"] == 150
  - e["vida_max"] == 150
  - e["jefe"] == True
  - Habilidades: exactamente 4 habilidades especiales
    - Drenaje de Almas (activa, heal 5 + damage_boost 30%)
    - Arrebato Apocalíptico (activa, 60% probabilidad, damage_boost 75%)
    - Azotazo Demoniaco (pasiva, sangrado 3)
    - Otro efecto adicional
  - e["armadura"] valor alto (jefe potente)
  - e["daño"] rango significativo
```

### T3.11: Fabius v1 — Hoz de Sangre (45 hp - Jefe #6)
```
ARRANGE: crear_amo_mazmorra() con _pw=="hoz"
ACT:
  - e = enemigo_aleatorio("Fabius, Amo de Mazmorra (v1)")
ASSERT:
  - e["nombre"] == "Fabius, Amo de Mazmorra"
  - e["vida"] == 45
  - e["vida_max"] == 45
  - e["jefe"] == True
  - e["_pw"] == "hoz" (arma codificada)
  - Habilidades:
    - Sutura de Dolor (pasiva, sangrado 2)
    - Inyección Quirúrgica (activa, heal 3 + damage_boost 25%)
  - e["daño"] bonus por arma
```

### T3.12: Fabius v2 — Hoja Noche (60 hp - Jefe #7)
```
ARRANGE: crear_amo_mazmorra() con _pw=="hoja" (_pw != 1)
ACT:
  - e = enemigo_aleatorio("Fabius, Amo de Mazmorra (v2)")
ASSERT:
  - e["nombre"] == "Fabius, Amo de Mazmorra"
  - e["vida"] == 60
  - e["vida_max"] == 60
  - e["jefe"] == True
  - e["_pw"] == "hoja" (arma codificada)
  - Habilidades incluyen:
    - Sutura de Dolor (pasiva, sangrado 2)
    - Incisión Mortal (activa, 50% probabilidad, damage_boost 40% + sangrado 3)
  - e["daño"] mayor que v1
```

### T3.13: Fabius v3 — Default (30 hp - Jefe #8)
```
ARRANGE: crear_amo_mazmorra() sin condiciones especiales
ACT:
  - e = enemigo_aleatorio("Fabius, Amo de Mazmorra (v3)")
ASSERT:
  - e["nombre"] == "Fabius, Amo de Mazmorra"
  - e["vida"] == 30
  - e["vida_max"] == 30
  - e["jefe"] == True
  - e["_pw"] == None (sin arma especial)
  - Habilidades:
    - Solo Sutura de Dolor (pasiva, sangrado 2)
  - Versión base, menos habilidades que v1/v2
```

### T3.14: Fabius v4 — Estado Crítico (0 hp - Jefe #9)
```
ARRANGE: crear_amo_mazmorra() con condición especial (_pw == 1)
ACT:
  - e = enemigo_aleatorio("Fabius, Amo de Mazmorra (v4)")
ASSERT:
  - e["nombre"] == "Fabius, Amo de Mazmorra"
  - e["vida"] == 0
  - e["vida_max"] == 0
  - e["jefe"] == True
  - Estado especial: enemy_muerto o _estado == "critico"
  - Habilidades: vacías o solo pasivas inactivas
  - Representa versión final/fallida de Fabius
```

---

## PARTE 2: TURNO_ENEMIGO (9 tests)

### Descripción
Ejecuta turno del enemigo con habilidades, efectos, y modificadores de stance.

### T4.1: Ataque base daño
```
ARRANGE:
  - e = {"nombre": "Test", "vida": 10, "daño": (2,4), "habilidades": []}
  - p = {"vida": 10, "armadura": 2, "destreza": 3}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] <= 10 (recibe daño)
```

### T4.2: Stun bloquea turno
```
ARRANGE:
  - e = {"stun": 2}
  - p = {"vida": 10}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] == 10 (sin daño)
  - e["stun"] == 1 (decrementado)
```

### T4.3: Habilidad pasiva sangrado
```
ARRANGE:
  - e = {
      "daño": (2,2),
      "habilidades": [
        {"tipo": "pasiva", "prob": 1.0, "condicion": "siempre", "efecto": "sangrado", "valor": 1}
      ]
    }
  - p = {"sangrado": 0}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["sangrado"] == 1
```

### T4.4: Habilidad pasiva damage_boost
```
ARRANGE:
  - e = {
      "daño": (2,2),
      "habilidades": [
        {"tipo": "pasiva", "prob": 1.0, "condicion": "siempre", "efecto": "damage_boost", "valor": 0.5}
      ]
    }
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - Daño aplicado >= 3 (2 + 50% boost)
```

### T4.5: Habilidad activa ejecuta
```
ARRANGE:
  - e = {
      "vida": 20,
      "vida_max": 20,
      "daño": (2,2),
      "habilidades": [
        {"tipo": "activa", "prob": 1.0, "condicion": "siempre", "efecto": "damage_boost", "valor": 0.5}
      ]
    }
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - e["_damage_boost"] == 0.5 (preparado para próximo turno)
```

### T4.6: Bloquear reduce daño 50%
```
ARRANGE:
  - e = {"daño": (10,10)}
  - p = {"vida": 10, "fuerza": 10}
  - stance = "bloquear"
ACT:
  - turno_enemigo(p, e, "bloquear")
ASSERT:
  - p["vida"] > 5 (menos daño por bloqueo)
```

### T4.7: Esquivar exitosa evita ataque
```
ARRANGE:
  - stance = "esquivar"
  - Mock tirada 1d20 + destreza > 12
ACT:
  - turno_enemigo(p, e, "esquivar")
ASSERT:
  - p["vida"] sin cambios (esquiva completa)
```

### T4.8: Validación integridad
```
ARRANGE:
  - personaje sin "vida"
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - Alerta de validación
  - Sin crash
```

### T4.9: Efectos temporales decrementados
```
ARRANGE:
  - e = {"_efectos_temporales": {"damage_boost": {"valor": 0.5, "turnos_restantes": 1}}}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - e["_efectos_temporales"]["damage_boost"]["turnos_restantes"] == 0
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
    "stun": 0,
    "sangrado": 0,
    "_efectos_temporales": {},
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
```

---

## RESUMEN

| Item | Valor |
|------|-------|
| Total Tests | 20 |
| Funciones | enemigo_aleatorio (5 base + 6 jefes), turno_enemigo |
| Jefes Mapeados | 8 |
| Líneas Código | ~2816 (aleatorio), ~3698 (turno) |
| Efectos Especiales | 12 tipos |
