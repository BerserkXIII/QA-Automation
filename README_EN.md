# [Learning Portfolio] QA Journey to ISTQB-CTFL 

![Status](https://img.shields.io/badge/status-Learning-green) 
![Exam](https://img.shields.io/badge/certified-ISTQB_CTFL-blue)

**[🇪🇸 Versión en Español →](./README.md)**

## 🚀 About this repository
Welcome to my Software Quality learning portfolio. 
This space documents my journey towards **ISTQB-CTFL certification**, from manual testing fundamentals to the first steps in automation.
I'm not Senior, not even Junior, but I'm learning. This code is evidence of study and real practice, with the purpose of documenting my learning and properly structuring a repository.

## 📚 What you'll find here
- **[Lessons Learned](./docs/LECCIONES_APRENDIDAS.md)**: Theory, ISTQB notes and concepts. Notes are integrated here alongside the learning diary.
- **[QA Analysis — TLDRDC](./tests/01-Manual/Analisis_QA_TLDRDC.md)**: Practical exercises in validation and verification of TLDRDC (11 CTs documented).
- **[Defect Reports](./tests/03-Reportes/template_defecto.md)**: Template and examples on how to properly document bugs.
- **[POM + Playwright Architecture](./docs/ARQUITECTURA_POM_PLAYWRIGHT.md)**: Page Object Model pattern implemented in Python.

## 🛠️ Tools in my journey
|          Category               |        Current Status                   |
|----------------------------------|-----------------------------------------|
| Manual Testing                   | ✅ Active (Constant updates)            |
| Git & GitHub                     | ✅ Active (Practical)                   |
| Automation (Playwright/Python)   | ✅ Active (Practical)                   |
| POM + Fixtures + Pytest          | ✅ Active (Learning)                    |

## 🎯 Short-term Goals
- [x] Complete ISTQB exam preparation.
- [x] Upload first automated test report.
- [ ] Document entire app lifecycle testing.

## 🎯 Long-term Goals
- [x] Implementation of automated testing with Python/Playwright.
- [x] CI/CD pipeline integration (GitHub Actions or similar).
- [x] Explore AI testing: prompts for test case generation.
- [ ] Create portfolio with real tested project (end-to-end).
- [x] Transition from manual to automation (document the learning curve).

## 🤖 Automation: POM + Playwright

### The Evolution: Manual → Automation

I implemented the **Page Object Model** pattern to scale maintainable tests.

### Automation Projects

| Project | App | Objective | Status |
|---------|-----|-----------|--------|
| **TLDRDC Testing** | Own RPG game | End-to-end integration | 🔄 In progress |
| **Pruebas-saucedemo** | SauceDemo | Learn POM from scratch | ✅ Completed |
| **AutomationExercise** | Fictional e-commerce | Validate patterns | ✅ Active |



### Architecture & Concepts

- **[ARQUITECTURA_POM_PLAYWRIGHT.md](./docs/ARQUITECTURA_POM_PLAYWRIGHT.md)** — Lego Model: Pages, Conftest, Tests separated
- **Separation of concerns**: Locators in Pages, test logic in fixtures, expectations in tests
- **Maintainability**: UI changes = changes only in Pages

### How to run tests

```bash
cd tests/02-Automatizados/AutomationExercise
pytest test/test_ejercicio3.py -v
```

### What I learned (POM)

✅ UI element encapsulation in classes  
✅ Fixtures for reusable states  
✅ Parametrized fixtures for coverage  
✅ Determinism in tests (avoid random)  
✅ Debugging with `page.pause()`  

---

## 💡 How to read this portfolio
1. Start in [README.md](./README.md) to see the big picture.
2. Review [LECCIONES_APRENDIDAS.md](./docs/LECCIONES_APRENDIDAS.md) for technical and theoretical details.
3. Look at [Analisis_QA_TLDRDC.md](./tests/01-Manual/Analisis_QA_TLDRDC.md) to see how I structure my tests (11 CTs documented).
4. Explore [tests/02-Automatizados/](./tests/02-Automatizados/) to see POM projects in action.
5. Check the [ROADMAP](./docs/ROADMAP.md) to understand my learning plan.

---
*Last update: [02/06/2026]* 
*Maintained by: Salva_BsK*
