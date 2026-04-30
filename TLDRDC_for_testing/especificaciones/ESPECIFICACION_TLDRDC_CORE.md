# Especificación de Tests — TLDRDC_PRUEBA1.PY (CORE)

*Versión: 0.3 (Test Spec)*

---

## RESUMEN EJECUTIVO

**Dos funciones pures del monolito (NO incluyen combate):**
1. **crear_personaje()** — Inicialización: stats balanceados, campos secretos, validación input
2. **aplicar_evento(evento, personaje)** — Aplicación genérica: modifica stats, pociones, armas, campos personalizados

---

## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| C1.1 | crear_personaje | Entrada válida |
| C1.2 | crear_personaje | Nombre vacío rechazado |
| C1.3 | crear_personaje | Fuerza fuera rango |
| C1.4 | crear_personaje | Armadura según destreza |
| C1.5 | crear_personaje | Nombre a lowercase |
| C1.6 | crear_personaje | Campos máximos y secretos |
| C2.1 | aplicar_evento | Suma vida normal |
| C2.2 | aplicar_evento | Vida clampea máximo |
| C2.3 | aplicar_evento | Vida clampea mínimo |
| C2.4 | aplicar_evento | Muerte → fin_derrota + early return |
| C2.5 | aplicar_evento | Pociones se clampean máximo |
| C2.6 | aplicar_evento | Stats se clampean a 20 |
| C2.7 | aplicar_evento | Armadura no baja de 0 |
| C2.8 | aplicar_evento | Añadir arma válida |
| C2.9 | aplicar_evento | Múltiples cambios simultáneamente |
| C2.10 | aplicar_evento | Stats negativos sin límite mínimo |
| C2.11 | aplicar_evento | Pociones pueden ser negativas |
| C2.12 | aplicar_evento | Key desconocida se asigna |
| C2.13 | aplicar_evento | Key válida no existente se suma |
| C2.14 | aplicar_evento | Callback UI armas se invoca |

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

#### Test C1.1: Entrada válida primera vez
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

#### Test C1.2: Nombre vacío se rechaza
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

#### Test C1.3: Fuerza fuera de rango rechazada
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

#### Test C1.4: Armadura según destreza (extremos)
```
ARRANGE:
  - Mock retorna fuerza = 1 (destreza = 9)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["armadura"] == 4
```

#### Test C1.5: Nombre se convierte a lowercase
```
ARRANGE:
  - Mock retorna "JuGaDoR" (mayúsculas)
  - Mock retorna "5" (fuerza)
ACT:
  - p = crear_personaje()
ASSERT:
  - p["nombre"] == "jugador"  (lowercase)
```

#### Test C1.6: Campos máximos y secretos inicializados
```
ARRANGE: Entrada válida (1-9 para fuerza)
ACT: p = crear_personaje()
ASSERT:
  - Campos máximos:
    - vida_max: 25
    - pociones_max: 10
    - armadura_max: 5
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

#### Test C2.1: Suma vida (sin límite)
```
ARRANGE:
  - p = {"vida": 10, "vida_max": 15}
  - evento = {"vida": 3}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 13
```

#### Test C2.2: Vida clampea a máximo
```
ARRANGE:
  - p = {"vida": 12, "vida_max": 15}
  - evento = {"vida": 10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 15  (no 22)
```

#### Test C2.3: Vida clampea a 0 (mínimo)
```
ARRANGE:
  - p = {"vida": 5}
  - evento = {"vida": -10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["vida"] == 0
```

#### Test C2.4: Vida a 0 llama fin_derrota() y retorna
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

#### Test C2.5: Pociones se clampean
```
ARRANGE:
  - p = {"pociones": 8, "pociones_max": 10}
  - evento = {"pociones": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == 10  (no 13)
```

#### Test C2.6: Stats se clampean a 20
```
ARRANGE:
  - p = {"fuerza": 18}
  - evento = {"fuerza": 5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["fuerza"] == 20
```

#### Test C2.7: Armadura no baja de 0
```
ARRANGE:
  - p = {"armadura": 2}
  - evento = {"armadura": -5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["armadura"] == 0
```

#### Test C2.8: Añadir arma válida
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

#### Test C2.9: Múltiples cambios simultáneamente
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

#### Test C2.10: Stats negativos sin límite mínimo
```
ARRANGE:
  - p = {"fuerza": 5}  (sin fuerza_max)
  - evento = {"fuerza": -10}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["fuerza"] == -5  (Sin protección si no existe *_max)
```

#### Test C2.11: Pociones pueden ser negativas
```
ARRANGE:
  - p = {"pociones": 2, "pociones_max": 10}
  - evento = {"pociones": -5}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["pociones"] == -3  (No hay límite mínimo)
```

#### Test C2.12: Key desconocida se asigna si no está en personaje
```
ARRANGE:
  - p = {"vida": 10}  (sin "campo_nuevo")
  - evento = {"campo_nuevo": 5}
  - Mock alerta()
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - alerta() fue llamado (key_desconocida)
  - p["campo_nuevo"] == 5  (Se creó el campo)
```

#### Test C2.13: Key válida pero no existente se suma
```
ARRANGE:
  - p = {"vida": 10}  (sin "moscas" que es válida)
  - evento = {"moscas": 1}
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - p["moscas"] == 1  (Se creó y se asignó)
```

#### Test C2.14: Callback UI armas se invoca al aplicar armas
```
ARRANGE:
  - p = {"armas": {}}
  - evento = {"armas": {"daga": {"daño": 2}}}
  - Mock _callback_ui_armas
ACT:
  - aplicar_evento(evento, p)
ASSERT:
  - _callback_ui_armas() fue llamada una vez
  - p["armas"] contiene "daga"
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

### Hallazgos de Implementación (v0.3):
- **crear_personaje()**: 
  - Nombre se convierte a lowercase (línea ~770)
  - vida_max (25), pociones_max (10), armadura_max (5) se establecen siempre (líneas ~818-821)
  - Loop de validación para nombre vacío y fuerza fuera [1-9]

- **aplicar_evento()**: 
  - _KEYS_VALIDAS define 18 claves permitidas (línea 2562-2572)
  - Vida: se clampea [0, vida_max], si llega a 0 → fin_derrota() + early return
  - Pociones: NO tiene límite mínimo (puede ser negativa)
  - Fuerza/Destreza: Solo se clampean si existe *_max en personaje (sin protección por defecto)
  - Armadura: Se clampea [0, armadura_max]
  - Armas: Invoca _callback_ui_armas() después (línea 2645-2646)
  - Keys desconocidas: Emiten alerta pero se asignan igual

### Critical Path:
- **C2.4**: Early return en muerte es **DEBE testear** con mock de fin_derrota
- **C2.11**: Pociones sin límite mínimo es comportamiento intencional (no defender como vida)
- **C2.10**: Stats sin _max pueden ser negativos (diseño para flexibilidad)

### Líneas de Código (v0.3):
- crear_personaje: líneas 759-843
- aplicar_evento: líneas 2570-2660
- _KEYS_VALIDAS: líneas 2562-2572
- _callback_ui_armas: líneas 725, 2645-2646
