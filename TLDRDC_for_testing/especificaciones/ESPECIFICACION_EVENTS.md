# Especificación de Tests — EVENTS.PY

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

`events.py` gestiona **tres sistemas independientes**:
1. **Bolsa de Eventos** — Garantiza que cada evento (1-20) aparezca una sola vez sin repetición inmediata
2. **Bolsa de Exploración** — Similar pero para textos descriptivos (1-15)
3. **Eventos Individuales** — Funciones `_evento_1()...20()` que aplican lógica + narrativa

---

## MATRIZ DE PRUEBAS

| Test ID | Módulo | Función | Validación |
|---------|--------|---------|-----------|
| B1.1 | Bolsa Eventos | rellenar | 20 eventos, sin duplicados |
| B1.2 | Bolsa Eventos | rellenar | Orden aleatorio |
| B1.3 | Bolsa Eventos | rellenar | Reemplaza contenido previo |
| B2.1 | Bolsa Exploración | rellenar | 15 textos |
| B2.2 | Bolsa Exploración | rellenar | IDs 1-15 presentes |
| B3.1 | Bolsa Eventos | obtener | Retorna válido, decrementa |
| B3.2 | Bolsa Eventos | obtener | Rellena automático si vacía |
| B3.3 | Bolsa Eventos | obtener | Ciclo completo 20 eventos |
| B3.4 | Bolsa Eventos | obtener | Sin repetición inmediata |
| B4.1 | Bolsa Exploración | obtener | Retorna válido 1-15 |
| B4.2 | Bolsa Exploración | obtener | Rellena automático |
| E1.1 | Evento 1 | _evento_1 | Retorna dict poción |
| E1.2 | Evento 1 | _evento_1 | Retorna dict daño |
| E1.3 | Evento 1 | _evento_1 | Retorna dict vacío |
| E1.4 | Evento 1 | _evento_1 | Rechaza entrada inválida |
| E1.5 | Evento 1 | _evento_1 | Rama NO funciona |

---
## MÓDULO: Bolsa de Eventos

### Función: `rellenar_bolsa_eventos()`

**¿Qué hace?**
- Llena `estado["bolsa_eventos"]` con lista [1,2,3...,20]
- Mezcla aleatoriamente (shuffle)

**Casos a testear:**

#### Test B1.1: Bolsa se llena con 20 eventos
```
ARRANGE: estado["bolsa_eventos"] = []
ACT: rellenar_bolsa_eventos()
ASSERT:
  - len(estado["bolsa_eventos"]) == 20
  - set(estado["bolsa_eventos"]) == {1,2,3,...,20}
```

#### Test B1.2: Orden aleatorio
```
ARRANGE: estado["bolsa_eventos"] = []
ACT: 
  - rellenar_bolsa_eventos()
  - primer_orden = list(estado["bolsa_eventos"])
  - rellenar_bolsa_eventos()
  - segundo_orden = list(estado["bolsa_eventos"])
ASSERT:
  - primer_orden != segundo_orden  (órdenes diferentes por shuffle)
```

#### Test B1.3: Llamada repetida reemplaza
```
ARRANGE: estado["bolsa_eventos"] = [5, 10]
ACT: rellenar_bolsa_eventos()
ASSERT:
  - len(estado["bolsa_eventos"]) == 20
  - [5, 10] fueron reemplazados
```

---

### Función: `rellenar_bolsa_exploracion()`

**Idéntica a rellenar_bolsa_eventos() pero con [1,2,...,15]**

#### Test B2.1: Bolsa se llena con 15 textos
```
ASSERT: len(estado["bolsa_exploracion"]) == 15
```

#### Test B2.2: Contiene IDs 1-15
```
ASSERT: set(estado["bolsa_exploracion"]) == {1,2,...,15}
```

---

### Función: `obtener_evento_de_bolsa()`

**¿Qué hace?**
- Saca último elemento de `bolsa_eventos`
- Si bolsa vacía, rellenla automáticamente
- Retorna ID del evento

**Casos a testear:**

#### Test B3.1: Obtiene evento válido
```
ARRANGE: rellenar_bolsa_eventos()  (bolsa tiene 20)
ACT: evento = obtener_evento_de_bolsa()
ASSERT:
  - evento in {1,2,...,20}
  - len(estado["bolsa_eventos"]) == 19
```

#### Test B3.2: Rellenamiento automático
```
ARRANGE: estado["bolsa_eventos"] = []
ACT: evento = obtener_evento_de_bolsa()
ASSERT:
  - evento in {1,2,...,20}
  - bolsa rellenada automáticamente
```

#### Test B3.3: Sacar 20 eventos (ciclo completo)
```
ARRANGE: rellenar_bolsa_eventos()
ACT: 
  - eventos = [obtener_evento_de_bolsa() for _ in range(20)]
  - bolsa debería rellenarse automáticamente
ASSERT:
  - len(eventos) == 20
  - set(eventos) == {1,2,...,20}  (todos aparecen una vez en ciclo)
```

#### Test B3.4: Sin repetición inmediata (estadístico)
```
ARRANGE: Hacer 50+ ciclos
ACT: evento_anterior = None
     eventos = []
     for i in range(50):
       e = obtener_evento_de_bolsa()
       assert e != evento_anterior
       evento_anterior = e
       eventos.append(e)
ASSERT:
  - Ningún evento aparece 2 veces seguidas
```

---

### Función: `obtener_texto_exploracion_de_bolsa()`

**Idéntica a obtener_evento_de_bolsa() pero con textos 1-15**

#### Test B4.1: Obtiene texto válido
```
ASSERT: texto in {1,2,...,15}
```

#### Test B4.2: Rellenamiento automático cuando vacía
```
ASSERT: Funciona igual que B3.2
```

---

## MÓDULO: Evento Individual (Sample)

### Función: `_evento_1(personaje)`

**Qué hace:**
- LOOP mientras respuesta invalida:
  - Pregunta: \"Quieres abrir el cofre? (s/n)\"
  - Si \"s\": random.choice([\"pocion\", \"vacio\", \"corte\"])
    - pocion -> retorna {\"pociones\": 1}
    - corte -> retorna {\"vida\": -1}
    - vacio -> retorna {}
  - Si \"n\": random.choices([\"sombra\", \"mutilado\", \"escape\"])
    - sombra -> llama combate(), retorna {}
    - mutilado -> llama combate(), retorna {}
    - escape -> narración, retorna {}
  - Otro -> alerta, loop reintenta

**Casos a testear:**

#### Test E1.1: rama ABRIR cofre -> POCION
```
ARRANGE:
  - p = Personaje({vida: 10})
  - Mock leer_input() retorna "s"
  - Mock random.choice() retorna "pocion"
ACT:
  - resultado = _evento_1(p)
ASSERT:
  - resultado == {pociones: 1}
```

#### Test E1.2: rama ABRIR -> CORTE (dano)
```
ARRANGE:
  - p = Personaje({vida: 10})
  - Mock leer_input() retorna "s"
  - Mock random.choice() retorna "corte"
ACT:
  - resultado = _evento_1(p)
ASSERT:
  - resultado == {vida: -1}
```

#### Test E1.3: rama NO ABRIR -> SOMBRA (combate)
```
ARRANGE:
  - p = Personaje({vida: 10})
  - Mock leer_input() retorna "n"
  - Mock random.choices retorna "sombra"
  - Mock combate()
ACT:
  - resultado = _evento_1(p)
ASSERT:
  - resultado == {}
  - combate() fue llamado (llamada a enemigo_aleatorio)
```

#### Test E1.4: rechaza input invalido (loop reintenta)
```
ARRANGE:
  - p = Personaje({})
  - Mock leer_input() retorna ["xyz", "s"]
  - Mock alerta()
ACT:
  - resultado = _evento_1(p)
ASSERT:
  - alerta() llamado con "Respuesta no válida"
  - Loop continuó, resultado es válido
```

#### Test E1.5: rama ABRIR -> VACIO (sin treasuro)
```
ARRANGE:
  - p = Personaje({})
  - Mock leer_input() retorna "s"
  - Mock random.choice() retorna "vacio"
ACT:
  - resultado = _evento_1(p)
ASSERT:
  - resultado == {}
```

---


## FIXTURES NECESARIAS

```python
from unittest.mock import Mock, patch
import random

# Mock personaje
personaje_mock = {
    "nombre": "Test",
    "vida": 10,
    "fuerza": 5,
    "destreza": 5,
}

# Mock estado global
estado_mock = {
    "bolsa_eventos": [],
    "bolsa_exploracion": [],
}

# Mock leer_input
with patch('events.leer_input') as mock_input:
    mock_input.return_value = "s"  # o "n", "xyz", etc.

# Mock random
with patch('random.choice') as mock_choice:
    mock_choice.return_value = "poción"
```

---

## NOTAS

- Tests B3.4 y B4.2 son **estadísticos** (necesitan múltiples iteraciones)
- _evento_1 tiene dependencias inyectadas (narrar, preguntar, etc.) — mockar todas
- Otros eventos (_evento_2..._evento_20) siguen mismo patrón que _evento_1
