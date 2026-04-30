# Especificación de Tests — COMBATE_ENEMIGO

*Versión: 1.0*

**Total: 20 tests**
- T3: `enemigo_aleatorio(nombre)` + Jefes especiales (11 tests)
- T4: `turno_enemigo(personaje, enemigo, stance)` (9 tests)

---

## PARTE 1: ENEMIGO_ALEATORIO + JEFES (11 tests)

### Descripción
Genera enemigos aleatorios o específicos. Mapeo completo de 6 tipos base + 8 jefes especiales.

**Enemigos base (6):**
- Larvas de Sangre (10 hp)
- Mosca de Sangre (15 hp)
- Maniaco Mutilado (14 hp)
- Perturbado (18 hp)
- Rabioso (22 hp)
- Sombra tenebrosa (15 hp)

**Jefes especiales (8):**
- Forrix: 30 hp (sangrado pasivo + recuperación impia)
- Fabius v1: 45 hp (Hoz de Sangre)
- Fabius v2: 60 hp (Hoja Noche, sin _pw)
- Fabius v3: 30 hp (default)
- Sanakht: 20 hp (acuchillamiento + esquiva)
- Mano Demoniaca: 30 hp (regeneración)
- Bel'akhor: 150 hp (4 habilidades)
- Ka-Banda: 50 hp (frensi demoniaco)

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

### T3.6: Forrix (Jefe - 30 hp)
```
ARRANGE: crear_carcelero()
ACT:
  - e = enemigo específico
ASSERT:
  - e["nombre"] == "Forrix, el Carcelero"
  - e["vida"] == 30
  - e["jefe"] == True
  - Habilidades: Gancho de Carnicero (pasiva, sangrado 1), Recuperacion Impia (activa, heal 4 + damage_boost 20%)
```

### T3.7: Fabius v1 (45 hp - Hoz de Sangre)
```
ARRANGE: crear_amo_mazmorra() con Hoz
ACT:
  - e = enemigo específico
ASSERT:
  - e["vida"] == 45
  - Habilidades: Sutura de Dolor (pasiva, sangrado 2), Inyección Quirúrgica (activa, heal 3 + damage_boost 25%)
```

### T3.8: Fabius v2 (60 hp - Hoja Noche)
```
ARRANGE: crear_amo_mazmorra() con Hoja (sin _pw==1)
ACT:
  - e = enemigo específico
ASSERT:
  - e["vida"] == 60
  - Incluye: Incisión Mortal (activa, 50%, damage_boost 40% + sangrado 3)
```

### T3.9: Fabius v3 (30 hp - default)
```
ARRANGE: crear_amo_mazmorra() sin condiciones
ACT:
  - e = enemigo específico
ASSERT:
  - e["vida"] == 30
  - Solo Sutura de Dolor
```

### T3.10: Sanakht (20 hp)
```
ARRANGE: crear_sombra_sangrienta()
ACT:
  - e = enemigo específico
ASSERT:
  - e["vida"] == 20
  - e["nombre"] == "Sanakht, la Sombra Sangrienta"
  - Habilidades: Acuchillamiento (ataque + sangrado 2), Sombra Oculta (reduce precisión 2 turnos)
```

### T3.11: Otros jefes (multi-check)
```
Validar que existen:
- Mano Demoniaca (30 hp, regeneración)
- Bel'akhor (150 hp, 4 habilidades)
- Ka-Banda (50 hp, frensi demoniaco)
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
