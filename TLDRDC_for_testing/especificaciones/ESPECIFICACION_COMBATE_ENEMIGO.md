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

## PARTE 2: TURNO_ENEMIGO + HABILIDADES (20 tests)

### Descripción
Ejecuta turno del enemigo con habilidades, efectos, y modificadores de stance.
Tests agrupados por categoría: Base (3), Pasivas Sangrado (3), Pasivas Boost (3),
Pasivas Especiales (2), Activas (3), Stances (3), Validación (3).

---

### CATEGORÍA A: TESTS BASE (T4.1-T4.3)

### T4.1: Ataque base daño
```
ARRANGE:
  - e = {"daño": (2,4), "habilidades": []}
  - p = {"vida": 10, "armadura": 0}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] < 10 (recibe daño)
```

### T4.2: Stun bloquea turno
```
ARRANGE:
  - e = {"stun": 2, "daño": (10,20)}
  - p = {"vida": 10}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] == 10 (sin daño)
  - e["stun"] < 2 (disminuye)
```

### T4.3: Vida límite > 0
```
ARRANGE:
  - e = {"daño": (1,1)}
  - p = {"vida": 100, "armadura": 0}
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] >= 0 (nunca negativa)
```

---

### CATEGORÍA B: PASIVAS SANGRADO — Límites 3 puntos (T4.4-T4.6)

**Habilidades testadas:**
- Huesos Punzantes (sangrado 1)
- Gancho de Carnicero (sangrado 1)
- Sutura de Dolor (sangrado 2)
- Colmillos de Sombra (sangrado 1)

### T4.4: Pasiva sangrado bajo (1)
```
ARRANGE:
  - e habilidades = [pasiva sangrado 1, prob 0.8]
  - p["sangrado"] = 0
ACT:
  - turno_enemigo(p, e, None) × 3 ciclos
ASSERT:
  - p["sangrado"] >= 0 (puede o no aplicarse)
  - Tipo: int
```

### T4.5: Pasiva sangrado medio (2)
```
ARRANGE:
  - e habilidades = [pasiva sangrado 2, prob 0.8]
  - p["sangrado"] = 0
ACT:
  - turno_enemigo(p, e, None) × 3 ciclos
ASSERT:
  - p["sangrado"] >= 0
  - Si aplicado: >= 2
  - Tipo: int
```

### T4.6: Pasiva sangrado con vida_baja
```
ARRANGE:
  - e["vida"] = 10, e["vida_max"] = 30 (< 50%, vida_baja)
  - e habilidades = [pasiva sangrado, condicion: vida_baja]
  - Mock probabilidad = 1.0 (garantizado)
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["sangrado"] > 0 (dispara en vida baja)
```

---

### CATEGORÍA C: PASIVAS DAMAGE_BOOST — Límites 3 puntos (T4.7-T4.9)

**Habilidades testadas:**
- Arrebato de Locura (damage_boost 0.3)
- Arrebato de Ira (damage_boost 0.3)
- Rugido Infernal (damage_boost 0.3)

### T4.7: Pasiva boost bajo (0.3)
```
ARRANGE:
  - e["daño"] = (10,10)
  - e habilidades = [pasiva damage_boost 0.3, prob 1.0]
  - p["vida"] = 50
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - daño_recibido >= 13 (10 + 30%)
```

### T4.8: Pasiva boost con vida_baja
```
ARRANGE:
  - e["vida"] = 5, e["vida_max"] = 30 (< 60%, vida_baja)
  - e["daño"] = (2,2)
  - e habilidades = [pasiva damage_boost 0.3, condicion: vida_baja, prob 1.0]
  - p["vida"] = 20
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - daño_recibido >= 2.6 (2 + 30%)
```

### T4.9: Pasiva healing
```
ARRANGE:
  - e["vida"] = 10, e["vida_max"] = 30
  - e habilidades = [pasiva heal 3, prob 1.0]
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - e["vida"] > 10 (se heala)
  - e["vida"] <= 13 (+3)
```

---

### CATEGORÍA D: PASIVAS ESPECIALES (T4.10-T4.11)

### T4.10: Pasiva stun (Hoja Sombría)
```
ARRANGE:
  - e habilidades = [pasiva stun 1, prob 1.0]
  - p = personaje
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["estun"] >= 1 (aplicado)
```

### T4.11: Activa reduce_armadura
```
ARRANGE:
  - e habilidades = [activa reducir_armadura 1, prob 1.0]
  - p["armadura"] = 5
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["armadura"] < 5 (reducida)
```

---

### CATEGORÍA E: ACTIVAS CUSTOM (T4.12-T4.14)

### T4.12: Activa recuperacion_impia
```
ARRANGE:
  - e = Forrix o similar con recuperacion_impia
  - e["vida"] = 10, e["vida_max"] = 30
  - e["vida"] <= 50% (dispara vida_baja)
  - p["vida"] = 30
ACT:
  - turno_enemigo(p, e, None) con mock prob 1.0
ASSERT:
  - e["vida"] > 10 (se heala 4)
  - p["vida"] < 30 (recibe daño)
```

### T4.13: Activa acuchillamiento (Sanakht)
```
ARRANGE:
  - e = Sanakht con acuchillamiento
  - e["vida"] <= 70% (condicion: vida_baja)
  - p["vida"] = 20
ACT:
  - turno_enemigo(p, e, None) con prob 1.0
ASSERT:
  - p["vida"] < 20 (daño + sangrado)
  - p["sangrado"] >= 2
```

### T4.14: Activa frensi_demoniaco (Ka-Banda)
```
ARRANGE:
  - e = Ka-Banda con frensi_demoniaco
  - e["vida"] <= 50% (vida_baja)
  - p["vida"] = 40
ACT:
  - turno_enemigo(p, e, None) con prob 1.0
ASSERT:
  - Daño significativo (frensi = boost alto)
  - p["vida"] <= 20
```

---

### CATEGORÍA F: STANCES (T4.15-T4.17)

### T4.15: Bloquear reduce daño 50%
```
ARRANGE:
  - e["daño"] = (10,10)
  - p["vida"] = 50, stance = "bloquear"
  - Mock randint éxito
ACT:
  - turno_enemigo(p, e, "bloquear")
ASSERT:
  - p["vida"] > 45 (daño <= 5)
```

### T4.16: Esquivar puede evitar
```
ARRANGE:
  - e["daño"] = (20,20)
  - p["destreza"] = 20, stance = "esquivar"
  - Mock randint éxito esquiva
ACT:
  - turno_enemigo(p, e, "esquivar")
ASSERT:
  - p["vida"] >= 30 (poco o sin daño)
```

### T4.17: Sin stance = normal
```
ARRANGE:
  - e["daño"] = (5,5)
  - p["vida"] = 20, stance = None
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - p["vida"] < 20 (daño completo)
```

---

### CATEGORÍA G: VALIDACIÓN (T4.18-T4.20)

### T4.18: Personaje sin "vida"
```
ARRANGE:
  - personaje = {"nombre": "Broken"} (sin vida)
  - e = {"daño": (1,1)}
ACT:
  - turno_enemigo(personaje, e, None)
ASSERT:
  - No crash (manejo graceful)
```

### T4.19: Enemigo sin habilidades
```
ARRANGE:
  - e["habilidades"] = []
  - p["vida"] = 20
ACT:
  - turno_enemigo(p, e, None)
ASSERT:
  - Ejecuta solo daño base
```

### T4.20: Efectos temporales limpios
```
ARRANGE:
  - e["_efectos_temporales"] = {}
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
