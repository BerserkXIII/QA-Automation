# [Recorrido QA hacia ISTQB-CTFL] QA Journey to ISTQB-CTFL

![Estado](https://img.shields.io/badge/estado-Aprendiendo-green) 
![Examen](https://img.shields.io/badge/certificado-ISTQB_CTFL-blue)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/BerserkXIII/QA-Automation/actions)

**[📖 English Version →](./README_EN.md)**

## 🚀 Sobre este repositorio
Bienvenido a mi portafolio de aprendizaje en Calidad de Software. 
Este espacio documenta mi camino hacia la certificación **ISTQB-CTFL**, desde las bases manuales hasta el primer paso en automatizació, uso de PlayWright, APIs y demas.
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

## Integración Continua (CI) con GitHub Actions

La automatización ya no depende únicamente de una ejecución local. Se implementaron cuatro pipelines independientes, uno por proyecto, que se ejecutan automáticamente en cada `push` y `pull_request` hacia `main`. Cada pipeline instala las dependencias desde cero en una máquina Linux limpia y ejecuta la suite completa, sin depender de la configuración local de ningún desarrollador.

| Proyecto | Cobertura | Estado |
|----------|-----------|--------|
| AutomationExercise | UI, API e híbridos | [![AutomationExercise](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml) |
| SauceDemo | UI con Playwright | [![SauceDemo](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_saucedemo.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_saucedemo.yml) |
| API-ReqRes | Tests de API | [![API-ReqRes](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_reqres.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_reqres.yml) |
| API-GoRest | Tests de API | [![API-GoRest](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_gorest.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_gorest.yml) |

### Problemas reales resueltos durante la implementación

Estos pipelines aportaron aprendizaje técnico además de dejar las suites en verde:

- **Diferencias entre Windows y Linux:** un `ModuleNotFoundError` causado por la sensibilidad a mayúsculas y minúsculas en los nombres de archivo no aparecía en Windows, pero sí en el runner Linux de GitHub. Se resolvió corrigiendo los imports y configurando `sys.path` de forma explícita, sin depender del sistema operativo.
- **Gestión de secretos:** las API keys nunca se suben al repositorio (`.env` permanece en `.gitignore`). Se usan **GitHub Secrets**, inyectados como variables de entorno en el pipeline. También se documentó un error de copia habitual: pegar `CLAVE=valor` en lugar de solo el valor, lo que añade texto basura al secreto y provoca fallos de autenticación silenciosos. Comparar la longitud del string ayuda a diagnosticarlo.
- **Alcance de permisos de las keys:** ReqRes distingue una key `public` (solo lectura) de una `manage` (lectura y escritura). Usar la incorrecta produce un `403` o `invalid_api_key`, indistinguible a simple vista de una key inválida. Quedó documentado como hallazgo de autenticación por scopes.
- **Caracteres invisibles en credenciales:** se añadió `.strip()` al leer tokens desde las variables de entorno para proteger el código frente a espacios o saltos de línea introducidos al copiar y pegar.
- **Servicios externos no deterministas en CI:** `test_get_users_sin_api_key` (hallazgo AR-003) también resultó inestable en CI. Tras intentar estabilizarlo con `pytest-rerunfailures` y hasta 15 reintentos, apareció además un rate limiting real. Se decidió omitirlo conscientemente con `@pytest.mark.skip`, dejando el motivo documentado en el código: se priorizó la honestidad sobre conseguir un estado verde a toda costa.
- **Bug propio de infraestructura:** se corrigió un `AttributeError` en la fixture `attach_screenshot`, que fallaba silenciosamente cuando un test se rompía durante `setup` en vez de durante la ejecución (`call`). Era un bug preexistente que solo se manifestó al aparecer el primer fallo de ese tipo.

El resultado es un portfolio con cuatro proyectos y badges de estado verificables, ejecutando sus suites automáticamente ante cualquier cambio y sin intervención manual. Se consigue así el ciclo de “portfolio con tests” a “portfolio con pipeline de calidad verificable”.

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
