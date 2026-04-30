# Especificación de Tests — PERSISTENCIA (guardar_partida, cargar_partida)

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

Dos funciones que manejan **guardado y cargado de partidas**:
1. **guardar_partida(personaje)** — Escribe partida a JSON de forma atómica
2. **cargar_partida()** — Lee partida desde JSON (con migraciones de compatibilidad)

**CRÍTICO**: Guardado atómico con fichero temporal (no corrupción si falla a mitad)

---

## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| P1.1 | guardar_partida | Archivo creado, JSON válido |
| P1.2 | guardar_partida | Contiene estado global |
| P1.3 | guardar_partida | Integridad de datos (valores correctos) |
| P1.4 | guardar_partida | Fichero temporal se limpia |
| P1.5 | guardar_partida | Carpeta se crea si no existe |
| P1.6 | guardar_partida | Error emite alerta sin crash |
| P2.1 | cargar_partida | Carga exitosa |
| P2.2 | cargar_partida | Restaura estado global |
| P2.3 | cargar_partida | No existe → None |
| P2.4 | cargar_partida | Migración: eventos_superados lista → int |
| P2.5 | cargar_partida | JSON corrupto → None + alerta |
| P2.6 | cargar_partida | Campos requeridos presentes |
| P2.7 | cargar_partida | Sincroniza armas desde estado |
| P2.8 | cargar_partida | Valida campos mínimos |
| P3.1 | intentar_guardar | Incrementa veces_guardado |

---

## FUNCIÓN: `guardar_partida(personaje)`

**¿Qué hace?**
- Crea dict con datos (personaje + estado global)
- Escribe a fichero temporal `guardado_tmp.json`
- Si éxito: `os.replace(tmp, guardado.json)` (atómico)
- Si fallo: excepción capturada, alerta emitida

**Ruta esperada**: `AppData/TLDRDC/guardado.json`

#### Test P1.1: Guardar partida exitosa
```
ARRANGE:
  - personaje = {"nombre": "Test", "vida": 10, ...}
  - CARPETA_SAVE existe
  - RUTA_SAVE no existe (primera partida)
ACT:
  - guardar_partida(personaje)
ASSERT:
  - Archivo guardado.json existe
  - JSON válido (parseable)
  - personaje["nombre"] en JSON
```

#### Test P1.2: JSON contiene estado global COMPLETO
```
ARRANGE: personaje + todo estado global
ACT: guardar_partida(personaje)
ASSERT:
  - JSON contiene TODOS estos campos:
    - "personaje" (dict)
    - "armas_jugador" (dict)
    - "ruta_jugador" (list)
    - "eventos_superados" (int)
    - "bolsa_eventos" (list)
    - "bolsa_exploracion" (list)
    - "pasos_nivel2" (list) ← CRÍTICO, no documentado antes
    - "pasos_secretos" (list) ← CRÍTICO, no documentado antes
    - "veces_guardado" (int)
    - "_c01" (int, contador combates)
```

#### Test P1.3: Integridad de datos
```
ARRANGE:
  - personaje = {
      "nombre": "Test",
      "vida": 10,
      "fuerza": 5,
      "armas": {"daga": {"daño": 2}}
    }
ACT:
  - guardar_partida(personaje)
  - data = json.load("guardado.json")
ASSERT:
  - data["personaje"]["vida"] == 10
  - data["personaje"]["fuerza"] == 5
  - data["personaje"]["armas"]["daga"]["daño"] == 2
```

#### Test P1.4: Fichero temporal se elimina tras éxito (atomic write)
```
ARRANGE: Guardar exitosa completada
ACT:
  - Inmediatamente después de guardar_partida(), revisar si guardado_tmp.json existe
  - Verificar que guardado.json sí existe y contiene datos válidos
ASSERT:
  - guardado_tmp.json NO existe (eliminado por os.replace() que es atómico)
  - guardado.json existe y es válido
  - Garantiza que crash durante escritura no deja archivo corrupto
```

#### Test P1.5: Si carpeta no existe, se crea
```
ARRANGE: CARPETA_SAVE no existe
ACT: guardar_partida(personaje)
ASSERT:
  - Carpeta creada (os.makedirs)
  - Archivo guardado
```

#### Test P1.6: Error durante escritura emite alerta
```
ARRANGE:
  - Mock open() para lanzar IOError
ACT:
  - guardar_partida(personaje)
ASSERT:
  - alerta() fue llamado
  - Sin excepción no capturada
```

---

## FUNCIÓN: `cargar_partida()`

**¿Qué hace?**
- Si archivo no existe: retorna None
- Lee JSON desde guardado.json (UTF-8 encoding)
- Restaura estado global desde JSON
- **MIGRACIONES**: Si eventos_superados es lista (guardados pre-v0.6), convertir a int 0
- Valida que campos requeridos estén presentes
- Sincroniza armas: copia desde estado["armas_jugador"] hacia personaje["armas"]
- Retorna personaje dict o None si falla validación

#### Test P2.1: Cargar partida exitosa
```
ARRANGE:
  - Fichero guardado.json válido con datos completos
ACT:
  - personaje = cargar_partida()
ASSERT:
  - personaje es dict
  - personaje["nombre"], personaje["vida"], etc. presentes
  - No es None
```

#### Test P2.2: Restaura estado global COMPLETO
```
ARRANGE:
  - guardado.json con todos los campos:
    - _c01: 42
    - eventos_superados: 15
    - bolsa_eventos: [1,2,3]
    - pasos_nivel2: ["d", "i"]
    - pasos_secretos: []
    - veces_guardado: 3
ACT:
  - cargar_partida()
ASSERT:
  - estado["_c01"] == 42
  - estado["eventos_superados"] == 15
  - estado["bolsa_eventos"] == [1,2,3]
  - estado["pasos_nivel2"] == ["d", "i"]
  - estado["pasos_secretos"] == []
  - estado["veces_guardado"] == 3
```

#### Test P2.3: Archivo no existe retorna None
```
ARRANGE: No hay guardado.json
ACT:
  - personaje = cargar_partida()
ASSERT:
  - personaje is None
  - alerta() emitida ("No hay partida guardada")
```

#### Test P2.4: Migración: eventos_superados lista → int (backward compatibility)
```
ARRANGE:
  - Guardado antiguo (pre-v0.6) con "eventos_superados": [1,2,3]  (lista de IDs, no contador int)
ACT:
  - personaje = cargar_partida()
ASSERT:
  - estado["eventos_superados"] == 0  (convertido a int, valor seguro)
  - Código no crashea (isinstance() valida tipo)
  - Juego funciona aunque se pierda info de lista (diseño intencional de cambio de versión)
```

#### Test P2.5: JSON corrupto emite alerta
```
ARRANGE:
  - guardado.json con JSON inválido (ej: "{vida: 10}" sin comillas)
ACT:
  - personaje = cargar_partida()
ASSERT:
  - alerta("JSON corrupto")
  - personaje is None
  - Sin excepción no capturada
```

#### Test P2.6: Campos requeridos ausentes
```
ARRANGE:
  - guardado.json sin campo "vida" requerido
ACT:
  - personaje = cargar_partida()
ASSERT:
  - alerta("incompleto o dañado")
  - personaje is None
```

#### Test P2.7: Sincroniza armas desde estado a personaje
```
ARRANGE:
  - guardado.json con:
    - personaje: {"nombre": "Test", "vida": 10, "armas": {}}
    - armas_jugador: {"daga": {"daño": 2, "tipo": "sutil"}}
ACT:
  - personaje = cargar_partida()
ASSERT:
  - personaje["armas"] ahora tiene: {"daga": {"daño": 2, "tipo": "sutil"}}
  - Armas de estado["armas_jugador"] se copiaron a personaje["armas"]
  - (El diseño guarda armas en estado, no en personaje, por lo que requiere sincronización al cargar)
```

#### Test P2.8: Validación de campos mínimos
```
ARRANGE: guardado.json sin algunos campos requeridos
ACT: personaje = cargar_partida()
ASSERT:
  - Campos requeridos: {nombre, vida, fuerza, destreza, pociones, nivel}
  - Si faltan: retorna None + alerta
```

---

## FUNCIÓN: `intentar_guardar(personaje)` (Extra)

**¿Qué hace?**
- Intenta guardar con riesgo creciente
- `veces_guardado` += 1 siempre (delata posición)
- Si no combate/sobrevive: guardar exitoso

#### Test P3.1: Incrementa veces_guardado
```
ARRANGE:
  - estado["veces_guardado"] = 5
ACT:
  - intentar_guardar(personaje)
ASSERT:
  - estado["veces_guardado"] == 6
```

---

## FIXTURES NECESARIAS

```python
import json
import tempfile
import os
from unittest.mock import Mock, patch

# Personaje test
personaje_test = {
    "nombre": "TestPlayer",
    "vida": 10,
    "fuerza": 5,
    "destreza": 5,
    "pociones": 6,
    "nivel": 1,
    "armas": {"daga": {"daño": 2}},
}

# Estado test
estado_test = {
    "armas_jugador": {"daga": {"daño": 2}},
    "ruta_jugador": [],
    "eventos_superados": 0,
    "bolsa_eventos": [1,2,3],
    "bolsa_exploracion": [],
    "_c01": 5,
}

# Tmp file para tests
@pytest.fixture
def tmp_save_file(tmp_path):
    save_dir = tmp_path / "TLDRDC"
    save_dir.mkdir()
    return save_dir / "guardado.json"

# Mock CARPETA_SAVE, RUTA_SAVE
with patch('TLDRDC_Prueba1.CARPETA_SAVE') as mock_carpeta:
    mock_carpeta = tmp_path / "TLDRDC"
```

---

## NOTAS

- **CRÍTICO P1.4**: Guardar atómico con temp file (`os.replace()`) es defensa contra corrupción. Si el proceso crashea durante `json.dump()`, `guardado.json` anterior permanece intacto.
- **P2.4**: Test de migración es crucial para backward compatibility. Datos de partidas guardadas en v0.5 o anterior donde `eventos_superados` era lista.
- **P2.7**: Sincronización de armas es necesaria porque el diseño persiste armas en `estado["armas_jugador"]`, no en `personaje["armas"]`. Al cargar, hay que copiarlas.
- Tests de persistencia deben reutilizar archivos temporales (`pytest tmp_path`) para aislar del AppData real del usuario.
- **IMPORTANTE**: Todas las operaciones I/O usan UTF-8 encoding para soportar caracteres especiales en nombres de personaje.
- P1.5: `os.makedirs(CARPETA_SAVE, exist_ok=True)` debe ser verificado en mock.
- P1.6: Mockear `open()` para forzar IOError, no intentar escritura a disco protegido real.
