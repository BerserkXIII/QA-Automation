# 📋 DE ESPECIFICACIÓN A TESTS — Walkthrough Paso a Paso

*Guía educativa para escribir tests unitarios leyendo especificaciones*

**Nivel:** CTFL (Principiante) | **Duración:** 2-3 horas | **Meta:** Dominar el patrón de conversión

---

## PASO 1: LEE LA MATRIZ DE PRUEBAS (5 min)

Abre `docs/TLDRDC_for_testing/especificaciones/ESPECIFICACION_PERSISTENCIA.md` y busca:

```markdown
## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| P1.1 | guardar_partida | Archivo creado, JSON válido |
| P1.2 | guardar_partida | Contiene estado global |
...
```

**¿Qué te dice esto?**
- **P1.x**: Tests de `guardar_partida()` (6 tests)
- **P2.x**: Tests de `cargar_partida()` (8 tests)
- **P3.x**: Tests de `intentar_guardar()` (1 test)
- **Total:** 15 tests

---

## PASO 2: LEE UN TEST INDIVIDUAL (10 min por test)

Busca el test específico:

```markdown
#### Test P1.1: Guardar partida exitosa

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

**Decodificación AAA:**

| Parte | Pregunta | Respuesta |
|-------|----------|-----------|
| **ARRANGE** | ¿Qué preparo? | personaje dict, carpeta existe, no hay guardado |
| **ACT** | ¿Qué ejecuto? | Llamar `guardar_partida()` |
| **ASSERT** | ¿Qué verifico? | Archivo existe, es JSON válido, tiene nombre |

---

## PASO 3: BUSCA VALORES EN EL CÓDIGO FUENTE

### 3.1 Ubica la función

Ve a `TLDRDC_for_testing/TLDRDC_Prueba1.py`:

```python
# Busca: "def guardar_partida"
def guardar_partida(personaje):
    try:
        tmp_path = os.path.join(CARPETA_SAVE, "guardado_tmp.json")
        datos = {
            "personaje": personaje,
            "armas_jugador": estado["armas_jugador"],
            "ruta_jugador": estado["ruta_jugador"],
            ...
        }
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, RUTA_SAVE)
    except Exception as e:
        alerta(f"Error: {e}")
```

**¿Qué aprendes?**
1. Se crea dict `datos` con varios campos
2. Se usa `json.dump(..., ensure_ascii=False)` → UTF-8
3. Se usa `os.replace()` para atomicidad

### 3.2 Busca la estructura de estado

```python
# Línea ~290
estado = {
    "personaje": {...},
    "armas_jugador": {...},
    "ruta_jugador": [],
    "eventos_superados": 0,
    ...
}
```

**¿Qué aprendes?**
- Los 10 campos que se guardan exactamente

### 3.3 Busca validaciones

```python
# En cargar_partida()
campos_req = {"nombre", "vida", "fuerza", "destreza", "pociones", "nivel"}
if not campos_req.issubset(personaje.keys()):
    alerta("El guardado está incompleto o dañado.")
    return None
```

**¿Qué aprendes?**
- 6 campos mínimos requeridos para validación

---

## PASO 4: CREA DATOS DE PRUEBA

Con la información anterior, construye tu personaje de test:

```python
personaje_test = {
    "nombre": "TestPlayer",
    "vida": 10,
    "fuerza": 5,
    "destreza": 5,
    "armadura": 0,
    "pociones": 6,
    "nivel": 1,
    "armas": {"daga": {"daño": 2, "tipo": "sutil"}},
}
```

**¿Por qué estos valores?**
- Mínimos válidos: suficientes para testing
- Campos opcionales pero realistas
- Matches con los 6 campos requeridos

---

## PASO 5: CREA ESTADO DE PRUEBA

```python
estado_test = {
    "personaje": personaje_test.copy(),
    "armas_jugador": {"daga": {"daño": 2, "tipo": "sutil"}},
    "ruta_jugador": [],
    "eventos_superados": 0,
    "bolsa_eventos": [1, 2, 3],
    "bolsa_exploracion": [],
    "pasos_nivel2": [],
    "pasos_secretos": [],
    "veces_guardado": 0,
    "_c01": 5,
}
```

**¿Por qué?**
- Son los 10 campos exactos que `guardar_partida()` guarda
- Valores mínimos válidos
- Representa estado realista para testing

---

## PASO 6: IMPLEMENTA UN TEST (20 min)

```python
def test_P1_1_guardar_partida_exitosa(tmp_path):
    """
    Test P1.1: Guardar partida exitosa
    
    Valida que:
    - Archivo guardado.json se crea
    - JSON es válido (parseable)
    - Contiene el nombre del personaje
    """
    # ARRANGE
    with patch('TLDRDC_Prueba1.CARPETA_SAVE', str(tmp_path)):
        with patch('TLDRDC_Prueba1.RUTA_SAVE', str(tmp_path / "guardado.json")):
            personaje = {
                "nombre": "TestPlayer",
                "vida": 10,
                "fuerza": 5,
                "destreza": 5,
                "pociones": 6,
                "nivel": 1,
                "armas": {},
            }
            
            with patch.dict('TLDRDC_Prueba1.estado', {
                "personaje": personaje,
                "armas_jugador": {},
                "ruta_jugador": [],
                "eventos_superados": 0,
                "bolsa_eventos": [],
                "bolsa_exploracion": [],
                "pasos_nivel2": [],
                "pasos_secretos": [],
                "veces_guardado": 0,
                "_c01": 0,
            }, clear=False):
                
                # ACT
                guardar_partida(personaje)
                
                # ASSERT
                guardado_path = tmp_path / "guardado.json"
                assert guardado_path.exists(), "Archivo no existe"
                
                # Validar JSON
                with open(guardado_path, "r", encoding="utf-8") as f:
                    data = json.load(f)  # Si falla, JSON inválido
                
                # Validar contenido
                assert data["personaje"]["nombre"] == "TestPlayer"
```

---

## PASO 7: DEBUGGING (Si Falla)

### Import Error
¿Importaste la función correctamente?
```python
from TLDRDC_Prueba1 import guardar_partida  # ✓
```

### Mock Error
¿Las rutas de mock son exactas?
```python
patch('TLDRDC_Prueba1.CARPETA_SAVE')  # ✓ exacto
patch('code.TLDRDC_Prueba1.CARPETA_SAVE')  # ✗ incorrecto
```

### Assertion Error
¿El archivo no existe?
```python
print(f"Archivos en tmp_path: {list(tmp_path.glob('*'))}")
print(f"¿Existe guardado.json? {(tmp_path / 'guardado.json').exists()}")
```

### JSON Error
¿`json.load()` falla?
```python
with open(guardado_path) as f:
    content = f.read()
print(content)  # ¿Está vacío? ¿Malformado?
```

---

## PASO 8: PATRÓN GENERAL

Una vez domines un test, el patrón es repetible:

| Test | Patrón | Desafío |
|------|--------|---------|
| P1.1 | Crear archivo | Setup fixture |
| P1.2 | Contiene campos | ¿Cuáles campos? |
| P1.3 | Integridad datos | Validación de tipos |
| P1.4 | Temp file limpio | Verificar cleanup |
| P1.5 | Carpeta se crea | Mock os.makedirs |
| P1.6 | Error handling | Exception handling |
| P2.x | Cargar partida | Similar pero inverso |

**Patrón**: Cada test es una variación sobre "guardar/cargar con condición X, verificar resultado Y"

---

## PASO 9: CHECKLIST FINAL

Antes de commitar:

- [ ] 15 tests implementados (P1.1-P1.6, P2.1-P2.8, P3.1)
- [ ] Cada test pasa: `pytest tests/02-Automatizados/test_persistencia.py -v`
- [ ] Fixtures reutilizadas (no hardcoding)
- [ ] Mocks correctos
- [ ] Docstrings presentes
- [ ] Sin paths absolutos

---

## ✨ Próximo Paso

Ahora que entiendes el walkthrough:

1. Elige una especificación
2. Lee su matriz de pruebas
3. Implementa 3 tests usando este patrón
4. Cuando todos pasen, sigue con otro módulo

**¡Vamos!** 🚀
