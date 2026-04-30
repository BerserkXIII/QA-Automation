# Proceso: De Especificación a Tests Implementados

*Guía educativa para escribir tests unitarios leyendo especificaciones*

**Autor**: Tutoring Session | **Nivel**: CTFL (Principiante) | **Duración estimada**: 2-3 horas para dominar el patrón

---

## 1. ESTRUCTURA DE UNA ESPECIFICACIÓN

Tomemos **ESPECIFICACION_PERSISTENCIA.md** como ejemplo. La estructura es:

```
RESUMEN EJECUTIVO
↓
MATRIZ DE PRUEBAS (tabla: Test ID | Función | Validación)
↓
FUNCIÓN 1: guardar_partida()
  ├─ "¿Qué hace?" (descripción de comportamiento)
  ├─ "Ruta esperada" (contexto de archivo)
  └─ Test P1.1, P1.2, ... (casos individuales)
↓
FUNCIÓN 2: cargar_partida()
  └─ Test P2.1, P2.2, ...
↓
FIXTURES NECESARIAS (código reutilizable)
↓
NOTAS (contexto crítico, gotchas)
```

**Tu objetivo**: Convertir cada **Test Pxx** en una función pytest real.

---

## 2. PASO 1: LEE LA MATRIZ DE PRUEBAS (5 min)

Abre `ESPECIFICACION_PERSISTENCIA.md` y localiza:

```markdown
## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| P1.1 | guardar_partida | Archivo creado, JSON válido |
| P1.2 | guardar_partida | Contiene estado global |
...
```

**¿Qué te dice esto?**
- **P1.x**: Tests de `guardar_partida()` 
- **P2.x**: Tests de `cargar_partida()`
- **P3.x**: Tests de `intentar_guardar()` (extra)

**Total de tests**: 15 (P1.1-P1.6, P2.1-P2.8, P3.1)

---

## 3. PASO 2: LEE UN TEST INDIVIDUAL (10 min por test)

Busca el test específico. Ejemplo: **Test P1.1: Guardar partida exitosa**

```markdown
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
```

**Decodificación AAA (Arrange-Act-Assert)**:

| Parte | Pregunta | Respuesta en P1.1 |
|-------|----------|-------------------|
| **ARRANGE** | ¿Qué necesito preparar? | personaje dict, carpeta existe, no hay guardado previo |
| **ACT** | ¿Qué acción ejecuto? | Llamar `guardar_partida(personaje)` |
| **ASSERT** | ¿Qué verifico? | Archivo existe, es JSON válido, contiene nombre |

---

## 4. PASO 3: BUSCA LOS VALORES EN EL CÓDIGO FUENTE

El test dice `personaje = {"nombre": "Test", "vida": 10, ...}` pero **¿de dónde saco esos campos?**

### 4.1 Ubica el código original

Ve a `docs/TLDRDC_for_testing/TLDRDC_Prueba1.py` (copia de prueba para testing):

```python
# Busca: "def guardar_partida"
# Línea ~624
def guardar_partida(personaje):
    try:
        tmp_path = os.path.join(CARPETA_SAVE, "guardado_tmp.json")
        datos = {
            "personaje": personaje,
            "armas_jugador": estado["armas_jugador"],
            "ruta_jugador": estado["ruta_jugador"],
            "eventos_superados": estado["eventos_superados"],
            ...
        }
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, RUTA_SAVE)
    except Exception as e:
        alerta(f"✘ Error al guardar: {e}")
```

**¿Qué aprendes?**
1. `personaje` es un dict que se guarda como-está
2. Se crea un dict `datos` que TAMBIÉN incluye `estado["armas_jugador"]`, `estado[...]`, etc.
3. Se escribe con `json.dump(..., ensure_ascii=False)` — esto significa **UTF-8, sin escapar caracteres especiales**
4. Se usa `os.replace()` para atomicidad

### 4.2 Busca la estructura de `personaje` en el estado inicial

Busca en el mismo archivo: `estado = {...}`

```python
# Línea ~290
estado = {
    "personaje": {
        "nombre": "Aventurero",
        "vida": 20,
        "fuerza": 5,
        "destreza": 5,
        "armadura": 0,
        "pociones": 6,
        "nivel": 1,
        "armas": {...}
    },
    "armas_jugador": {...},
    "ruta_jugador": [],
    "eventos_superados": 0,
    "bolsa_eventos": [],
    ...
}
```

**¿Qué aprendes?**
- Los campos de `personaje` son: `nombre`, `vida`, `fuerza`, `destreza`, `armadura`, `pociones`, `nivel`, `armas`
- Los campos de `estado` que se guardan son: `armas_jugador`, `ruta_jugador`, `eventos_superados`, `bolsa_eventos`, etc.

### 4.3 Busca los campos mínimos requeridos

Vuelve a `cargar_partida()`:

```python
campos_req = {"nombre", "vida", "fuerza", "destreza", "pociones", "nivel"}
if not campos_req.issubset(personaje.keys()):
    alerta("✘ El guardado está incompleto o dañado.")
    return None
```

**¿Qué aprendes?**
- Para que `cargar_partida()` valide correctamente, `personaje` DEBE tener estos 6 campos
- La especificación ya lo documenta en P2.8, ahora ves el código que lo valida

---

## 5. PASO 4: CREA EL PERSONAJE DE PRUEBA

Con la información anterior, construye un `personaje_test`:

```python
# Basado en el código original, pero simplificado para testing
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
- Mínimos válidos: `vida: 10` es suficiente para testing (no necesita 20 reales)
- Campos opcionales pero realistas: `armadura: 0` (sin protección), `armas` con una sola arma
- Matches con campos requeridos: todos los 6 están presentes

---

## 6. PASO 5: CREA EL ESTADO DE PRUEBA

Similar, pero para `estado`:

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
- Estos 10 campos son exactamente los que `guardar_partida()` guarda (ver línea ~636 de TLDRDC_Prueba1.py)
- Usa valores mínimos válidos (listas vacías, contadores en 0)
- `_c01: 5` = 5 combates ganados (valor realista para un test)

---

## 7. PASO 6: IMPLEMENTA UN TEST (20 min)

Ahora sí, escribe el código:

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
            
            # Mock del estado global
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
                assert guardado_path.exists(), "Archivo guardado.json no existe"
                
                # Validar JSON
                with open(guardado_path, "r", encoding="utf-8") as f:
                    data = json.load(f)  # Si falla aquí, JSON es inválido
                
                # Validar contenido
                assert data["personaje"]["nombre"] == "TestPlayer"
```

**Analicemos cada parte**:

| Línea | Propósito | Aprendizaje |
|-------|-----------|-------------|
| `tmp_path` | Pytest fixture para temp directory | Aislamos del AppData real |
| `patch('TLDRDC_Prueba1.CARPETA_SAVE')` | Mock de ruta global | El código original usa variables globales, las mocking |
| `patch.dict('TLDRDC_Prueba1.estado')` | Mock del dict estado | `estado` es global también |
| `json.load()` | Validación de JSON | Si no lanza exception, JSON es válido |
| `assert guardado_path.exists()` | Verificación explícita | Si falla, sabes exactamente qué falló |

---

## 8. PASO 7: VALIDACIÓN Y DEBUGGING

¿El test falla? Aquí está el checklist:

1. **Import error**: ¿Importaste `guardar_partida` correctamente?
   ```python
   from docs.TLDRDC_for_testing.TLDRDC_Prueba1 import guardar_partida
   ```

2. **Mock error**: ¿Las rutas de mock son exactas?
   - Busca en TLDRDC_Prueba1.py: `CARPETA_SAVE`, `RUTA_SAVE`, `estado`
   - El path del mock debe coincidir: `'TLDRDC_Prueba1.CARPETA_SAVE'` ✓ vs `'code.TLDRDC_Prueba1.CARPETA_SAVE'` ✗

3. **Assertion error**: ¿El archivo no existe?
   - Agregua debug print:
   ```python
   print(f"Archivos en tmp_path: {list(tmp_path.glob('*'))}")
   print(f"¿Existe guardado.json? {(tmp_path / 'guardado.json').exists()}")
   ```
   - Verifica que `guardar_partida()` fue llamada (¿está dentro del mock context?)

4. **JSON error**: ¿`json.load()` falla?
   - Lee el contenido:
   ```python
   with open(guardado_path) as f:
       content = f.read()
   print(content)  # ¿Está vacío? ¿Malformado?
   ```

---

## 9. PATRÓN GENERAL: DE TEST A TEST

Una vez domines P1.1, el patrón es repetible:

| Spec | Test | Patrón AAA | Desafío |
|------|------|-----------|---------|
| P1.1 | Crear archivo | Arrange personaje → Act guardar → Assert existe | Setup fixture |
| P1.2 | Contiene campos | Arrange personaje + estado → Act guardar → Assert 10 campos en JSON | Entender qué campos se guardan |
| P1.3 | Integridad datos | Arrange valores específicos → Act guardar → Act cargar JSON → Assert valores iguales | Validación de tipos (int vs string) |
| P1.4 | Temp file limpio | Arrange → Act → Assert temp NO existe | Verificar cleanup |
| P1.5 | Carpeta se crea | Arrange carpeta NO existe → Act guardar → Assert carpeta existe | Mock os.makedirs |
| P1.6 | Error handling | Arrange mock IOError → Act guardar → Assert alerta() llamado | Exception handling |
| P2.1-P2.8 | Cargar partida | Similar pero inverso (Act = cargar en lugar de guardar) | Restauración de estado |

**Patrón**: Cada test es una variación sobre "guardar/cargar con condición X, verificar resultado Y"

---

## 10. CHECKLIST FINAL: ANTES DE COMMITAR

Antes de enviar `test_persistencia.py`, valida:

- [ ] **15 tests implementados** (P1.1-P1.6, P2.1-P2.8, P3.1)
- [ ] **Cada test pasa** (`pytest tests/02-Automatizados/test_persistencia.py -v`)
- [ ] **Fixtures reutilizadas** (personaje_test, estado_test en conftest.py o locales)
- [ ] **Mocks correctos** (rutas, globales, excepciones)
- [ ] **Docstrings presentes** (cada función tiene `"""Spec: P1.1: ...."""`)
- [ ] **Sin hardcoding** (usa fixtures, no paths absolutos)
- [ ] **UTF-8 validado** (al menos un test con caracteres especiales)

---

## REFERENCIAS RÁPIDAS

**¿Cómo encontrar X en el código?**

| Necesito | Busco en | Línea aprox | Comando grep |
|----------|----------|------------|--------------|
| Campo de personaje | `TLDRDC_Prueba1.py` | ~290 | `grep -n "estado = {"` |
| Función guardar | `TLDRDC_Prueba1.py` | ~624 | `grep -n "def guardar_partida"` |
| Función cargar | `TLDRDC_Prueba1.py` | ~651 | `grep -n "def cargar_partida"` |
| RUTA_SAVE | `TLDRDC_Prueba1.py` | ~620 | `grep -n "RUTA_SAVE ="` |
| Campos que se guardan | `guardar_partida()` | ~636 | Dentro de `datos = {` |
| Validación campos | `cargar_partida()` | ~664-669 | `campos_req = ` |

---

**Fin del walkthrough. ¡Ahora crea test_persistencia.py!**
