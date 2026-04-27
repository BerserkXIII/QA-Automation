# 📋 ÍNDICE — Paso a Paso

## Estructura de Archivos

```
tests/unit/
├── conftest.py                   ← Fixtures (NO EDITES)
├── QUICK_START.md                ← Comandos frecuentes
├── INDICE.md                     ← Este archivo
├── TALLER_README.md              ← Guía completa y detallada
├── test_ejemplo_evento1.py       ← ⭐ Ejemplo RESUELTO
├── test_*_TEMPLATE.py            ← 7 templates para llenar
└── ...
```

---

## 🎯 Tu Roadmap (4 Pasos)

### PASO 1: Aprende (20 minutos)

1. Lee **QUICK_START.md** — comandos útiles
2. Lee **TALLER_README.md** — AAA pattern y fixtures
3. Estudia **test_ejemplo_evento1.py** — ve un ejemplo completo
4. Ejecuta el ejemplo:
   ```bash
   pytest tests/unit/test_ejemplo_evento1.py -v
   ```

✅ Cuando entiendas cómo funciona el ejemplo, avanza.

---

### PASO 2: Comienza con Reactive (2-3 horas)

Este es el **MÁS FÁCIL** (13 tests, lógica simple).

1. Abre especificación:
   ```bash
   cat docs/especificaciones/ESPECIFICACION_REACTIVE.md
   ```

2. Copia el template:
   ```bash
   cp tests/unit/test_reactive_TEMPLATE.py tests/unit/test_reactive.py
   ```

3. Abre y empieza a llenar:
   ```bash
   code tests/unit/test_reactive.py
   ```

4. Para cada test:
   - Lee en la spec qué debe testear (U1.1, U2.3, etc.)
   - Llena ARRANGE/ACT/ASSERT en el template
   - Ejecuta: `pytest tests/unit/test_reactive.py -v`
   - Cuando pase, sigue al siguiente

5. Cuando todos pasen (13/13 ✅):
   ```bash
   git add tests/unit/test_reactive.py
   git commit -m "test: test_reactive implementado (13 tests)"
   ```

✅ Cuando termines reactive, avanza.

---

### PASO 3: Continúa con Otros (orden recomendado)

Repite PASO 2 para cada uno (en este orden):

| # | Archivo | Spec | Tests | Dificultad | Tiempo |
|---|---------|------|-------|------------|---------:|
| 1 | test_reactive | ESPECIFICACION_REACTIVE | 13 | 🟢 Fácil | 2-3h |
| 2 | test_core | ESPECIFICACION_TLDRDC_CORE | 21 | 🟡 Medio | 3-4h |
| 3 | test_events | ESPECIFICACION_EVENTS | 16 | 🟡 Medio | 3-4h |
| 4 | test_persistencia | ESPECIFICACION_PERSISTENCIA | 14 | 🟡 Medio | 2-3h |
| 5 | test_threading | ESPECIFICACION_UI_THREADING | 14 | 🔴 Difícil | 3-4h |
| 6 | test_imagen | ESPECIFICACION_UI_IMAGEN | 10 | 🟡 Medio | 2-3h |
| 7 | test_integration | ESPECIFICACION_INTEGRATION | 8 | 🔴 Difícil | 2-3h |

**Recomendación:** Uno por sesión. Descansos ayudan.

✅ Cuando termines TODOS, avanza.

---

### PASO 4: Celebra (5 minutos)

Ejecuta todo junto:
```bash
pytest tests/unit/ -v
```

Deberías ver:
```
96 passed ✅
```

Commit final:
```bash
git add tests/unit/test_*.py
git commit -m "test: todos los 96 tests implementados"
```

🎉 **TERMINADO. El taller está completo.**

---

## ⚡ Tips Rápidos

- **¿Qué fixture necesito?** → Ver sección en TALLER_README.md
- **¿Mi test no pasa?** → Lee el error con `pytest -vv`
- **¿Qué significa esta línea del spec?** → Pregunta al senior
- **¿Puedo hacer dos templates al mismo tiempo?** → No, uno a la vez

---

## 📞 Ayuda

- Comandos → QUICK_START.md
- AAA pattern → TALLER_README.md
- Ejemplo resuelto → test_ejemplo_evento1.py
- ¿Confundido? → Pregunta al senior antes de avanzar
