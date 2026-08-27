# [Cuadernillo de aprendizaje] QA Journey to ISTQB-CTFL 

![Estado](https://img.shields.io/badge/estado-Aprendiendo-green) 
![Examen](https://img.shields.io/badge/certificado-ISTQB_CTFL-blue)

**[📖 English Version →](./README_EN.md)**

## 🚀 Sobre este repositorio
Bienvenido a mi portafolio de aprendizaje en Calidad de Software. 
Este espacio documenta mi camino hacia la certificación **ISTQB-CTFL**, desde las bases manuales hasta el primer paso en automatización.
No soy Senior, ni siquiera Junior, pero estoy aprendiendo. Este código es evidencia de estudio y práctica real, y tiene el proposito de documentar mi aprendizaje y estructurar debidamente un repositorio.

## 📚 Qué encontrarás aquí
- **[Lecciones Aprendidas](./documentos/LECCIONES_APRENDIDAS.md)**: Teoría, apuntes ISTQB y conceptos. Los apuntes están integrados aquí junto con el diario de aprendizaje.
- **[Análisis QA — TLDRDC](./tests/01-Manual/Analisis_QA_TLDRDC.md)**: Ejercicios prácticos de validación y verificación sobre TLDRDC (11 CTs documentados).
- **[Test TLDRDC automatizados](./tests/02-Automatizados/TLDRDC)**: Suitecase implementada con IA para TLDRDC.
- **[Arquitectura POM + Playwright](./documentos/ARQUITECTURA_POM_PLAYWRIGHT.md)**: Patrón Page Object Model implementado en Python.
- **[Reporte de Allure](https://berserkxiii.github.io/QA-Automation/)**: Reporte de pruebas automatizadas con Allure.

## 🛠️ Herramientas en mi camino
|          Categoría               |        Estado Actual                    |
|----------------------------------|-----------------------------------------|
| Testing Manual                   | ✅ Activo (Actualización constante)     |
| Git & GitHub                     | ✅ Activo (Práctico)                    |
| Automatización (Playwright/Python) | ✅ Activo (Práctico)                    |
| POM + Fixtures + Pytest           | ✅ Activo (Aprendiendo)                 |
| API Testing (ReqRes + AutomationExercise) | ✅ Activo (Práctico)               |
## 🎯 Meta a Corto Plazo
- [x] Completar exámenes de preparación para ISTQB.
- [x] Subir mi primer reporte de prueba automatizado.
- [ ] Documentar todo el ciclo de vida de una app real.

## 🎯 Meta a Largo Plazo
- [x] Implementación de testing automatizado con Python/Playwright.
- [x] Integración de CI/CD pipelines (GitHub Actions o similares).
- [x] Explorar testing con IA: prompts para generar casos de prueba.
- [ ] Crear un portafolio con proyecto real testeado (end-to-end).
- [x] Transición de manual a automatización (documentar la curva de aprendizaje).

----

# 🤖 Automatización: POM + Playwright

### La evolución: Manual → Automatización

Implementé el patrón **Page Object Model** para escalar pruebas mantenibles.

### Proyectos de Automatización

| Proyecto | App | Objetivo | Estado |
|----------|-----|----------|--------|
| **TLDRDC Testing** | Juego de rol propio | Integración end-to-end | 🔄 En progreso (IA based) |
| **Pruebas-saucedemo** | SauceDemo | Aprender POM desde cero | ✅ Completado |
| **AutomationExercise** | E-commerce ficticio | Validar patrones | ✅ Activo |
| **ReqRes API** | ReqRes.in | Aprender testing de APIs | ✅ Activo |

> ⚠️ **Nota sobre AutomationExercise**: Esta web tiene publicidad muy agresiva que aparece aleatoriamente (popup `google_vignette` en iframe dinámico de Google Ads). **No es realista para una suite de tests limpia en producción**, pero fue excelente para practicar manejo de popups, handlers dinámicos, network interception y debugging de problemas no deterministas de terceros. Tras varias estrategias (bloqueo de red, `add_locator_handler`, `frame_locator`), se documentó la causa raíz como no mitigable al 100% por depender de un sistema adversarial externo, y se marcó el test afectado como `flaky` de forma consciente con `pytest-rerunfailures`, en vez de perseguir un fix imposible.


### Arquitectura & Conceptos

- **[ARQUITECTURA_POM_PLAYWRIGHT.md](./documentos/ARQUITECTURA_POM_PLAYWRIGHT.md)** — Modelo de Lego: Pages, Conftest, Tests separados
- **Separación de responsabilidades**: Locators en Pages, lógica de test en fixtures, expectations en tests
- **Mantenibilidad**: Cambios de UI = cambios solo en Pages

### Cómo ejecutar tests

```bash
cd tests/02-Automatizados/AutomationExercise
pytest test/test_ejercicio3.py -v
```

### Lo que aprendí (POM)

✅ Encapsulación de elementos UI en clases  
✅ Fixtures para estados reutilizables  
✅ Fixtures parametrizadas para cobertura  
✅ Determinismo en tests (evitar random)  
✅ Debugging con `page.pause()`, `print()` y screenshots
✅ Diferencias de ejecucion entre `headless` y `headed` (UI puede comportarse distinto)
✅ Interacción con iframes dinámicos (`frame_locator`) y sus limitaciones con `add_locator_handler`
✅ Hooks de pytest (`pytest_runtest_makereport`) para reporting correcto en Allure
✅ Criterio para marcar un test como `flaky` de forma justificada, en vez de perseguir el 100% contra sistemas no deterministas

### Evolución reciente: API e integración híbrida

- Se añadió **[test_API.py](./tests/02-Automatizados/AutomationExercise/test/test_API.py)** para ampliar la cobertura de AutomationExercise con tests de API, dentro del mismo proyecto y entorno virtual que la suite de Playwright.
- Posteriormente se creó **[test_hibrido.py](./tests/02-Automatizados/AutomationExercise/test/test_hibrido.py)**, combinando UI y API para comprobar ambos flujos sobre el mismo sistema.

---

## 💡 Cómo leer este portafolio
1.  Comienza en [README.md](./README.md) para ver el panorama general.
2.  Revisa [LECCIONES_APRENDIDAS.md](./documentos/LECCIONES_APRENDIDAS.md) para los detalles técnicos y teóricos.
3.  Mira [01-Manual](./tests/01-Manual) para ver cómo estructuro mis pruebas en los diferentes contextos.
4.  Explora [tests/02-Automatizados/](./tests/02-Automatizados/) para ver los proyectos terminados.
5.  Consulta el [ROADMAP](./documentos/ROADMAP.md) para entender mi plan de aprendizaje.
6.  Revisa [documents](./documentos/) para material extra de aprendizaje.

---
*Última actualización: [27/08/2026]*
*Mantenido por: Salva_BsK*
