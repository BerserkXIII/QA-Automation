# Especificación de Tests — TLDRDC_PRUEBA1.PY (CORE)

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

Tres funciones críticas del monolito:
1. **calcular_daño(arma, personaje)** — Retorna daño + bonificaciones por stats
2. **crear_personaje()** — Crea nuevo personaje con stats iniciales balanceados
3. **aplicar_evento(evento, personaje)** — Aplica cambios de evento al personaje (stats, armas, vida, etc.)

---

## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| C1.1 | calcular_daño | Sin tipo: daño base |
| C1.2 | calcular_daño | Sutil + destreza baja |
| C1.3 | calcular_daño | Sutil + destreza alta |
| C1.4 | calcular_daño | Pesada + fuerza |
| C1.5 | calcular_daño | Mixta (fórmula correcta) |
| C1.6 | calcular_daño | Mínimo 1 daño |
| C2.1 | crear_personaje | Entrada válida |
| C2.2 | crear_personaje | Nombre vacío rechazado |
| C2.3 | crear_personaje | Fuerza fuera rango |
| C2.4 | crear_personaje | Armadura según destreza |
| C2.5 | crear_personaje | Campos requeridos |
| C3.1 | aplicar_evento | Suma vida normal |
| C3.2 | aplicar_evento | Vida clampea máximo |
| C3.3 | aplicar_evento | Vida clampea mínimo |
| C3.4 | aplicar_evento | Muerte → fin_derrota + early return |
| C3.5 | aplicar_evento | Pociones se clampean |

---

## FUNCIÓN: `calcular_daño(arma, personaje)`

**¿Qué hace?**
- Toma dict arma con `{"daño": X, "tipo": Y, ...}`
- Calcula bonificación según tipo de arma:
  - `"sutil"` → daño += destreza // 2
  - `"pesada"` → daño += fuerza // 2
  - `"mixta"` → daño += (fuerza + destreza) // 3
  - Sin tipo → sin bonificación
- Retorna daño final (número ≥ 1)

**Datos de Test (Constants)**
```python
ARMAS = {
    "daga": {"daño": 2, "tipo": "sutil"},
    "martillo": {"daño": 5, "tipo": "pesada"},
    "cimitarra": {"daño": 5, "tipo": "mixta"},
}
PERSONAJE_BAJO = {"fuerza": 2, "destreza": 2}
PERSONAJE_ALTO = {"fuerza": 10, "destreza": 10}
```

#### Test C1.1: Daño base sin tipo
```
ARRANGE:
  - arma = {"daño": 3}  (sin "tipo")
  - p = PERSONAJE_ALTO
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 3  (sin bonificación)
```

#### Test C1.2: Tipo sutil + destreza baja
```
ARRANGE:
  - arma = ARMAS["daga"]  (daño: 2, tipo: sutil)
  - p = {"destreza": 4}
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 2 + (4 // 2) == 4
```

#### Test C1.3: Tipo sutil + destreza alta
```
ARRANGE:
  - arma = ARMAS["daga"]
  - p = {"destreza": 10}
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 2 + 5 == 7
```

#### Test C1.4: Tipo pesada + fuerza
```
ARRANGE:
  - arma = ARMAS["martillo"]  (daño: 5, tipo: pesada)
  - p = {"fuerza": 8}
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 5 + (8 // 2) == 9
```

#### Test C1.5: Tipo mixta
```
ARRANGE:
  - arma = ARMAS["cimitarra"]  (daño: 5, tipo: mixta)
  - p = {"fuerza": 6, "destreza": 9}
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 5 + ((6 + 9) // 3) == 5 + 5 == 10
```

#### Test C1.6: Daño mínimo sin garantía (no clampea)
```
ARRANGE:
  - arma = {"daño": 0, "tipo": "sutil"}
  - p = {"destreza": 0}
ACT:
  - resultado = calcular_daño(arma, p)
ASSERT:
  - resultado == 0  (código no clampea a 1, es responsabilidad del caller)
```

---

## FUNCIÓN: `crear_personaje()`

**¿Qué hace?**
- Loop: pregunta nombre (debe ser no vacío)
- Loop: pregunta fuerza en rango [1-9]
- Calcula destreza = 10 - fuerza
- Calcula armadura según destreza:
  - destreza ≥ 9 → armadura = 4
  - destreza ≥ 6 → armadura = 2
  - destreza ≥ 3 → armadura = 1
  - resto → armadura = 0
- Retorna Personaje dict con todos los stats

#### Test C2.1: Entrada válida primera vez
```
ARRANGE:
  - Mock pedir_input():
    - retorna "jugador" (nombre)
    - retorna "5" (fuerza)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "jugador"
  - p["fuerza"] == 5
  - p["destreza"] == 5  (10-5)
  - p["vida"] == 10
  - p["pociones"] == 6
  - p["armas"] == {}  (vacío, sin daga previa)
  - p["vida_max"] == 25
  - p["pociones_max"] == 10
  - p["armadura_max"] == 5
```

#### Test C2.2: Nombre vacío se rechaza
```
ARRANGE:
  - Mock pedir_input():
    - retorna ""  (vacío)
    - retorna ""  (vacío de nuevo)
    - retorna "test"  (válido)
    - retorna "5"
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "test"
  - Se repitió pregunta (alerta emitida)
```

#### Test C2.3: Fuerza fuera de rango rechazada
```
ARRANGE:
  - Mock pedir_input():
    - retorna "test"
    - retorna "0"  (fuera)
    - retorna "10"  (fuera)
    - retorna "5"  (válido)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["fuerza"] == 5
  - Se repitió pregunta 2 veces
```

#### Test C2.4: Armadura según destreza (extremos)
```
ARRANGE:
  - Mock retorna fuerza = 1 (destreza = 9)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["armadura"] == 4

ARRANGE:
  - Mock retorna fuerza = 9 (destreza = 1)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["armadura"] == 0
```

#### Test C2.5: Campos secretos inicializados
```
ARRANGE: Entrada válida (1-9 para fuerza)
ACT: p = crear_personaje()
ASSERT:
  - Campos requeridos: nombre, vida, pociones, fuerza, destreza, armadura, armas, nivel
  - Campos secretos inicializados:
    - moscas: 0
    - brazos: 0
    - sombra: 0
    - sangre: 0
    - _pw: 0
    - tiene_llave: False
    - rencor: False
    - hitos_brazos_reclamados: []
    - evento_brazos_final_completado: False
    - evento_brazos_segundo_completado: False
    - bolsa_acecho: [1, 2, 3]
    - _x9f: False
```

---

## FUNCIÓN: `aplicar_evento(evento, personaje)`

**¿Qué hace?**
- Itera sobre claves en `evento` dict
- Aplica cambios según clave:
  - `"vida"`: suma valor (clampea [0, vida_max])
  - `"pociones"`: suma valor (clampea [0, pociones_max])
  - `"fuerza"`: suma valor (clampea [0, 20])
  - `"destreza"`: suma valor (clampea [0, 20])
  - `"armadura"`: suma valor (clampea [0, armadura_max])
  - `"armas"`: dict {nombre: stats} → añade armas
- **CRÍTICO**: Si vida llega a 0, llama `fin_derrota()` y retorna inmediatamente

**Test Constants**
```python
EVENTO_VIDA_POSITIVA = {"vida": 5}
EVENTO_VIDA_NEGATIVA = {"vida": -3}
EVENTO_MUERTE = {"vida": -100}
EVENTO_ARMA = {"armas": {"daga": {}}}
EVENTO_STATS = {"fuerza": 2, "destreza": 1}
```

#### Test C3.1: Suma vida (sin límite)
```
ARRANGE:
  - p = {"vida": 10, "vida_max": 15}
  - evento = {"vida": 3}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 13
```

#### Test C3.2: Vida clampea a máximo
```
ARRANGE:
  - p = {"vida": 12, "vida_max": 15}
  - evento = {"vida": 10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 15  (no 22)
```

#### Test C3.3: Vida clampea a 0 (mínimo)
```
ARRANGE:
  - p = {"vida": 5}
  - evento = {"vida": -10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 0
```

#### Test C3.4: Vida a 0 llama fin_derrota() y retorna
```
ARRANGE:
  - p = {"vida": 2}
  - evento = {"vida": -2, "fuerza": +5}  (fuerza no debe aplicarse)
  - Mock fin_derrota()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - fin_derrota.assert_called_once()
  - p["fuerza"] NO fue modificado (retorno early)
```

#### Test C3.5: Pociones se clampean
```
ARRANGE:
  - p = {"pociones": 8, "pociones_max": 10}
  - evento = {"pociones": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == 10  (no 13)
```

#### Test C3.6: Stats se clampean a 20
```
ARRANGE:
  - p = {"fuerza": 18}
  - evento = {"fuerza": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["fuerza"] == 20
```

#### Test C3.7: Armadura no baja de 0
```
ARRANGE:
  - p = {"armadura": 2}
  - evento = {"armadura": -5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["armadura"] == 0
```

#### Test C3.8: Añadir arma válida
```
ARRANGE:
  - p = {"armas": {}}
  - evento = {"armas": {"daga": {"daño": 2}}}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - "daga" in p["armas"]
  - p["armas"]["daga"] == {"daño": 2}
```

#### Test C3.9: Múltiples cambios simultáneamente
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

#### Test C3.10: Key desconocida emite alerta pero procesa
```
ARRANGE:
  - p = {"vida": 10, "otros_campos": 0}
  - evento = {"key_fake": 999}
  - Mock alerta()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - alerta() fue llamado con "[DEV] aplicar_evento: key desconocida 'key_fake'"
  - p["key_fake"] == 999 (se asignó igual)
  - Sin excepción
```

---

## FIXTURES NECESARIAS

```python
from unittest.mock import Mock, patch

# Personajes base
personaje_base = {
    "nombre": "Test",
    "vida": 10,
    "vida_max": 25,
    "fuerza": 5,
    "destreza": 5,
    "pociones": 6,
    "pociones_max": 10,
    "armadura": 2,
    "armas": {},
}

# Mock funciones globales
with patch('TLDRDC_Prueba1.fin_derrota') as mock_fin:
    pass

with patch('TLDRDC_Prueba1.pedir_input') as mock_input:
    mock_input.return_value = "5"
```

---

## NOTAS

- C3.4 es **CRÍTICO**: test de early return (muerte bloquea resto de aplicación)
- Todos los clamping son límites defensivos necesarios
- aplicar_evento() inyecta callback para sincronizar UI (si es necesario, mockar)
