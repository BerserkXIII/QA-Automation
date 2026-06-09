# [Cuadernillo de aprendizaje] QA Journey to ISTQB-CTFL 

![Estado](https://img.shields.io/badge/estado-Aprendiendo-green) 
![Examen](https://img.shields.io/badge/certificado-ISTQB_CTFL-blue)

**[📖 English Version →](./README_EN.md)**

## 🚀 Sobre este repositorio
Bienvenido a mi portafolio de aprendizaje en Calidad de Software. 
Este espacio documenta mi camino hacia la certificación **ISTQB-CTFL**, desde las bases manuales hasta el primer paso en automatización.
No soy Senior, ni siquiera Junior, pero estoy aprendiendo. Este código es evidencia de estudio y práctica real, y tiene el proposito de documentar mi aprendizaje y estructurar debidamente un repositorio.

## 📚 Qué encontrarás aquí
- **[Lecciones Aprendidas](./docs/LECCIONES_APRENDIDAS.md)**: Teoría, apuntes ISTQB y conceptos. Los apuntes están integrados aquí junto con el diario de aprendizaje.
- **[Análisis QA — TLDRDC](./tests/01-Manual/Analisis_QA_TLDRDC.md)**: Ejercicios prácticos de validación y verificación sobre TLDRDC (11 CTs documentados).
- **[Reportes de Defectos](./tests/03-Reportes/template_defecto.md)**: Template y ejemplos de cómo documentar bugs correctamente.
- **[Arquitectura POM + Playwright](./docs/ARQUITECTURA_POM_PLAYWRIGHT.md)**: Patrón Page Object Model implementado en Python.

## 🛠️ Herramientas en mi camino
|          Categoría               |        Estado Actual                    |
|----------------------------------|-----------------------------------------|
| Testing Manual                   | ✅ Activo (Actualización constante)     |
| Git & GitHub                     | ✅ Activo (Práctico)                    |
| Automatización (Playwright/Python) | ✅ Activo (Práctico)                    |
| POM + Fixtures + Pytest           | ✅ Activo (Aprendiendo)                 |

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

> ⚠️ **Nota sobre AutomationExercise**: Esta web tiene publicidad muy agresiva que aparece aleatoriamente. **No es realista para una suite de tests limpia en producción**, pero es excelente para practicar manejo de popups, handlers dinámicos y debugging de problemas inesperados. No es un buen escenario real de prueba, pero si para entender el manejo de estos elementos. Hay codigo en los tests para manejarlo, pero en varias ocasiones por run no lo consigue.


### Arquitectura & Conceptos

- **[ARQUITECTURA_POM_PLAYWRIGHT.md](./docs/ARQUITECTURA_POM_PLAYWRIGHT.md)** — Modelo de Lego: Pages, Conftest, Tests separados
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

---

## 💡 Cómo leer este portafolio
1.  Comienza en [README.md](./README.md) para ver el panorama general.
2.  Revisa [LECCIONES_APRENDIDAS.md](./docs/LECCIONES_APRENDIDAS.md) para los detalles técnicos y teóricos.
3.  Mira [Analisis_QA_TLDRDC.md](./tests/01-Manual/Analisis_QA_TLDRDC.md) para ver cómo estructuro mis pruebas (11 CTs documentados).
4.  Explora [tests/02-Automatizados/](./tests/02-Automatizados/) para ver los proyectos POM en acción.
5.  Consulta el [ROADMAP](./docs/ROADMAP.md) para entender mi plan de aprendizaje.

---
*Última act 
*Última actualización: [02/06/2026]* 
*Mantenido por: Salva_BsK*
