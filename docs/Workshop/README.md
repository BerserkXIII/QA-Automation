# 📚 TALLER DE TESTS TLDRDC — Guía Completa

**Nivel:** CTFL (Principiante) | **Duración:** 18-25 horas | **Resultado:** 96 tests implementados

---

## 🎯 ¿Qué es este taller?

Un **sistema completo de 96+ tests automatizados** para TLDRDC, dividido en 7 módulos con 60+ fixtures reutilizables.

**Módulos cubiertos:**
- reactive.py (13 tests) 🟢 Fácil
- core functions (21 tests) 🟡 Medio
- events.py (16 tests) 🟡 Medio
- persistencia (14 tests) 🟡 Medio
- threading (14 tests) 🔴 Difícil
- imaging (10 tests) 🟡 Medio
- integration (8 tests) 🔴 Difícil

---

## 📖 Cómo Navegar Este Taller

### 🔵 PRINCIPIANTE (Primer día)

1. **Lee esta página** (2 min) — Entiendes qué es el taller
2. **Abre [01-CONCEPTOS_Y_WORKFLOW.md](01-CONCEPTOS_Y_WORKFLOW.md)** (45 min)
   - Aprenderás: assert, AAA pattern, fixtures, mocks
   - Mirarás: ejemplo resuelto comentado
   - Usarás: comandos pytest frecuentes
3. **Empieza con test_reactive.py** (2-3 horas)
   - Es el módulo más fácil
   - Copia template, llena gaps, ejecuta: `pytest tests/02-Automatizados/test_reactive.py -v`

### 🟡 INTERMEDIO (Segundo día)

4. **Estudia [02-DE_ESPECIFICACION_A_TESTS.md](02-DE_ESPECIFICACION_A_TESTS.md)** (30 min)
   - Walkthrough: cómo leer especificación → escribir test
   - Patrón: ARRANGE (preparar) → ACT (ejecutar) → ASSERT (verificar)
5. **Continúa con otros módulos** (en orden recomendado)
   - test_core (3-4h)
   - test_events (3-4h)
   - test_persistencia (2-3h)

### 🔴 AVANZADO (Tercer día)

6. **Domina threading e integration** (5-7 horas)
   - Lee: [03-LOOP_PROTECTION.md](03-LOOP_PROTECTION.md) para protección contra loops
   - test_threading (3-4h) — Aprenderás sobre timeouts, threads, deadlocks
   - test_integration (2-3h) — Testeas módulos interactuando

7. **Ejecuta la suite completa** (5 min)
   ```bash
   pytest tests/02-Automatizados/ -v
   ```
   Deberías ver: `96 passed ✅`

---

## ⚡ Flujo Rápido

```
┌─────────────────────────────────────┐
│ 1. Abre especificación (docs/)     │
├─────────────────────────────────────┤
│ 2. Copia template (test_*_TEMPLATE │
├─────────────────────────────────────┤
│ 3. Lee CONCEPTOS (01-.md) si nuevo │
├─────────────────────────────────────┤
│ 4. Llena ARRANGE/ACT/ASSERT (AAA)  │
├─────────────────────────────────────┤
│ 5. Ejecuta: pytest -v test_*.py    │
├─────────────────────────────────────┤
│ 6. ¿Falla? → Lee error + debug     │
├─────────────────────────────────────┤
│ 7. ¿Pasa? → git commit             │
└─────────────────────────────────────┘
```

---

## 📂 Estructura de Archivos

```
tests/
├── conftest.py                    ← Fixtures reutilizables (60+)
├── conftest_combate.py            ← Fixtures de combate específicas
└── 02-Automatizados/
    ├── test_reactive.py           ← TU TRABAJO (llena vacíos)
    ├── test_core.py
    ├── test_events.py
    ├── test_combate_jugador.py
    ├── test_combate_enemigo.py
    ├── test_combate_loop.py
    ├── test_persistencia.py
    ├── test_threading.py
    ├── test_imagen.py
    └── test_integration.py

docs/Workshop/
├── README.md                      ← Esta página (punto de entrada)
├── 01-CONCEPTOS_Y_WORKFLOW.md    ← Teoría + AAA + fixtures + comandos
├── 02-DE_ESPECIFICACION_A_TESTS.md ← Walkthrough paso a paso
└── 03-LOOP_PROTECTION.md         ← Protección contra loops infinitos
```

---

## 🎯 Roadmap (Tu Checklist)

| Día | Módulo | Tests | Tiempo | Dificultad |
|-----|--------|-------|--------|-----------|
| 1 | **reactive** | 13 | 2-3h | 🟢 Fácil |
| 1-2 | **core** | 21 | 3-4h | 🟡 Medio |
| 2 | **events** | 16 | 3-4h | 🟡 Medio |
| 2 | **persistencia** | 14 | 2-3h | 🟡 Medio |
| 2-3 | **threading** | 14 | 3-4h | 🔴 Difícil |
| 3 | **imagen** | 10 | 2-3h | 🟡 Medio |
| 3 | **integration** | 8 | 2-3h | 🔴 Difícil |
| **TOTAL** | **96** | **18-25h** | - |

**Recomendación:** Uno por sesión. Descansos ayudan.

---

## 📋 Checklist Previo

Antes de empezar, valida:

- [ ] Tienes Python 3.8+ instalado
- [ ] Tienes pytest instalado (`pip install pytest pytest-mock`)
- [ ] Clonaste el repo y estás en la carpeta correcta
- [ ] Abriste [01-CONCEPTOS_Y_WORKFLOW.md](01-CONCEPTOS_Y_WORKFLOW.md) en VS Code

---

## 🐛 Solucionar Problemas

### "ImportError: No module named TLDRDC_Prueba1"
Valida que la ruta en `conftest.py` es correcta:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../TLDRDC_for_testing'))
```

### "fixture 'personaje_base' not found"
Verifica que `conftest.py` está en la carpeta `tests/` (no en `02-Automatizados/`).

### "Test passed locally but fails in CI/CD"
Lee [03-LOOP_PROTECTION.md](03-LOOP_PROTECTION.md) — probablemente hay loop infinito sin protección.

### "pytest runs forever (se cuelga)"
`Ctrl+C` para interrumpir. Luego:
```bash
pytest tests/02-Automatizados/test_integration.py -v
# Si esto se cuelga, hay timeout sin configurar
# Lee 03-LOOP_PROTECTION.md
```

---

## 💡 Tips Profesionales

1. **Lee la especificación ANTES de escribir test**
   - Ubicada en `docs/TLDRDC_for_testing/especificaciones/`
   - Cada test tiene ID (P1.1, U2.3, etc.) que mapea a spec

2. **Ejecuta tests mientras trabajas**
   ```bash
   pytest tests/02-Automatizados/test_reactive.py -v -s
   # -v = verbose (muestra cada test)
   # -s = muestra prints
   ```

3. **Usa fixtures, no copies datos**
   ```python
   # ✅ BIEN
   def test_1(self, personaje_base):
       p = personaje_base
   
   # ❌ MAL
   def test_1(self):
       p = {"nombre": "X", "vida": 10, ...}  # repetido 50 veces
   ```

4. **Sigue AAA Pattern** — siempre
   - ARRANGE: Preparar datos
   - ACT: Ejecutar función
   - ASSERT: Verificar resultado

5. **Un test = una cosa**
   - ❌ No testees calcular_daño Y guardar en el mismo test
   - ✅ Un test para calcular_daño, otro para guardar

---

## 🚀 Comenzar Ahora

### Opción A: Principiante (Recomendado)
```bash
# 1. Lee teoría
code docs/Workshop/01-CONCEPTOS_Y_WORKFLOW.md

# 2. Ejecuta ejemplo
pytest tests/02-Automatizados/ -v --collect-only
# (Ve qué tests existen)

# 3. Empieza con reactive
pytest tests/02-Automatizados/test_reactive.py -v
```

### Opción B: Ya Conoces Testing
```bash
# 1. Salta directamente a especificación
code docs/TLDRDC_for_testing/especificaciones/ESPECIFICACION_REACTIVE.md

# 2. Copia y empieza
cp tests/02-Automatizados/test_reactive_TEMPLATE.py tests/02-Automatizados/test_reactive.py
code tests/02-Automatizados/test_reactive.py

# 3. Llena gaps, ejecuta
pytest tests/02-Automatizados/test_reactive.py -v
```

---

## 📞 Ayuda Rápida

| Pregunta | Respuesta |
|----------|-----------|
| ¿Cómo ejecuto UN test? | `pytest tests/02-Automatizados/test_reactive.py::TestInit::test_init_vacio -v` |
| ¿Cómo veo prints del test? | `pytest tests/02-Automatizados/test_reactive.py -s` |
| ¿Qué fixtures hay disponibles? | Lee **01-CONCEPTOS_Y_WORKFLOW.md** sección "Fixtures Disponibles" |
| ¿Cómo debuggeo? | `pytest --pdb tests/02-Automatizados/test_reactive.py` (abre debugger) |
| ¿Qué significa este error? | Lee [02-DE_ESPECIFICACION_A_TESTS.md](02-DE_ESPECIFICACION_A_TESTS.md) sección "Debugging" |
| ¿Test se cuelga? | Lee [03-LOOP_PROTECTION.md](03-LOOP_PROTECTION.md) |

---

## ✨ ¿Listo?

→ Abre **[01-CONCEPTOS_Y_WORKFLOW.md](01-CONCEPTOS_Y_WORKFLOW.md)** y comienza 🚀
