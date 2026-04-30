# Plan de Testing TLDRDC — ISTQB

*Fecha: 27 de abril de 2026*

---

## 1. MAPEO DE MÓDULOS Y RIESGO

| Módulo | Tier | Riesgo | Funciones Core | Impacto si Falla |
|--------|------|--------|---|---|
| **TLDRDC_Prueba1.py** | 1 | CRÍTICO | `main()`, `aplicar_evento()`, `combate()` | Juego no inicia / flujo roto |
| **events.py** | 1 | CRÍTICO | `evento_aleatorio()`, `rellenar_bolsa()`, `_evento_1()...20()` | Narrativa/eventos no funcionan |
| **reactive.py** | 1 | CRÍTICO | `Personaje.observe()`, `Personaje.__setitem__()` | Estado del personaje corrupto |
| **logging_manager.py** | 1 | CRÍTICO | `_log_debug()`, `limpiar_log()` | Sin feedback al jugador |
| **ui_estructura.py** | 1.5 | ALTO | `_Bridge.esperar()`, `_Bridge.recibir()`, `polling()` | Thread-safety roto / UI no responde |
| **ui_imagen_manager.py** | 1.5 | ALTO | `cargar_imagen()`, `ImagenManager.__init__()` | Sprites no cargan / fallback roto |
| **ui_config.py** | 1.5 | ALTO | `obtener_recursos()`, `resource_path()` | Rutas de recursos incorrectas |
| **performance_monitor.py** | 2 | MEDIO | `medir_tiempo()`, `registrar_metrica()` | Métricas ausentes (no es bloqueador) |

---

## 2. ESTRATEGIA DE TESTING

### **Nivel 1: Unit Tests** (Módulos aislados)
- **reactive.py**: Testear `observe()`, `__setitem__()` con diccionarios simple
- **logging_manager.py**: Testear escritura a archivo sin DEBUG_MODE activado
- **ui_imagen_manager.py**: Testear caché, fallback cuando imagen falta
- **events.py**: Testear lógica de bolsa (obtener evento, rellenar, sin repetir)

**Enfoque**: Mock de dependencias inyectadas, entrada/salida controlada.

### **Nivel 2: Integration Tests** (Módulos conectados)
- **reactive.py + TLDRDC_Prueba1.py**: Observer dispara callback cuando personaje cambia
- **ui_estructura.py + threading**: `_Bridge` sincroniza hilos correctamente
- **events.py + aplicar_evento()**: Evento modificar stats → personaje sincroniza correctamente
- **ui_imagen_manager.py + ui_estructura.py**: Sprites cargan y se redibujan en UI

**Enfoque**: Mocks más complejos (personaje reactivo, UI parcial), validar flujo.

### **Nivel 3: E2E (completo)** [FASE 2]
- Iniciar partida → completar combate → observer actualiza UI ✓
- Aplicar evento → stats suben → siguiente combate impacto correcto ✓

**Enfoque**: Partidas cortas/script, validar estado final.

---

## 3. SCOPE

### ✅ **TESTEAREMOS**:
- Lógica pura (cálculos, condiciones) 
- Sincronización de estado (observers, flags)
- Integridad de datos (armas, stats, eventos)
- Thread-safety (no race conditions)
- Fallbacks defensivos (imagen falta → texto, etc.)

### ❌ **NO TESTEAREMOS**:
- Interfaz gráfica visual (posición de widgets, colores)
- Juego completo E2E (demasiado costoso, ya cubierto en manual CTs)
- Performance exacto (métricas relativas sí, absolutas no)
- Contenido narrativo (es responsabilidad del diseño, no código)

---

## 4. FASES DE IMPLEMENTACIÓN

| Fase | Duración Est. | Objetivo |
|------|---|---|
| **FASE 1** | 1-2 días | Unit tests + fixtures base |
| **FASE 2** | 2-3 días | Integration tests |
| **FASE 3** | 1 día | E2E scripts |
| **FASE 4** | 1 día | CI/CD setup (pytest en git) |

---

## 5. ORGANIZACIÓN EN QA_PROJECT

```
QA_project/
├── docs/
│   ├── PLAN_TESTING_TLDRDC.md  ← TÚ ESTÁS AQUÍ
│   └── ARQUITECTURA_TESTS.md   [próximo]
├── tests/
│   ├── unit/                   [FASE 1]
│   │   ├── test_reactive.py
│   │   ├── test_logging.py
│   │   ├── test_imagen_manager.py
│   │   └── test_events.py
│   ├── integration/            [FASE 2]
│   │   ├── test_reactive_ui.py
│   │   ├── test_events_aplicar.py
│   │   └── test_threading.py
│   ├── e2e/                    [FASE 3]
│   │   └── test_partida_completa.py
│   └── fixtures/               [Datos de test]
│       ├── mock_personaje.py
│       ├── mock_ui.py
│       └── datos_eventos.py
└── scripts/
    └── run_tests.sh            [FASE 4]
```

---

## 6. CRITERIOS DE ACEPTACIÓN Y VALIDACIÓN

### Unit Tests
- **Cobertura mínima**: 80% de funciones críticas
- **Criterio de paso**: Todos los tests pasan sin falsos positivos
- **Documentación**: Cada test incluye docstring con objetivo y precondiciones

### Integration Tests
- **Criterio de paso**: Flujos completos funcionales (evento → UI actualiza)
- **Regresión**: Validar que cambios en un módulo no rompen otro

### E2E Tests
- **Criterio de paso**: Partida inicializa, combate completo, estado final correcto
- **Cobertura**: Mínimo 2 paths (happy path + error path)

---

## 7. ARTEFACTOS DE TESTING

La documentación generada incluirá:

1. **ARQUITECTURA_TESTS.md** — Diseño técnico de fixtures y mocks
2. **test_*.py** — Archivos de test (unit, integration, e2e)
3. **conftest.py** — Configuración pytest y fixtures compartidas
4. **fixtures/mock_*.py** — Objetos mock reutilizables
5. **COVERAGE_REPORT.md** — Cobertura de código tras completar tests

---

## 8. REFERENCIAS Y ESTÁNDARES

- **Framework**: pytest (estándar de industria Python)
- **Convención de nombres**: `test_<módulo>_<función>.py`
- **Patrón**: Arrange-Act-Assert (AAA)
- **Mocking**: unittest.mock (librería estándar)
- **Type hints**: PEP 484 (mejora maintainability)
- **Estándar**: ISO/IEC/IEEE 29119 (Testing Standards)


