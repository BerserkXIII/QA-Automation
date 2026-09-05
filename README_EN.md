# [Learning Portfolio] QA Journey to ISTQB-CTFL 

![Status](https://img.shields.io/badge/status-Learning-green) 
![Exam](https://img.shields.io/badge/certified-ISTQB_CTFL-blue)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)](https://github.com/BerserkXIII/QA-Automation/actions)

**[🇪🇸 Versión en Español →](./README.md)**

## 🚀 About this repository
Welcome to my Software Quality learning portfolio. 
This space documents my journey towards **ISTQB-CTFL certification**, from manual testing fundamentals to the first steps in automation.
I'm not Senior, not even Junior, but I'm learning. This code is evidence of study and real practice, with the purpose of documenting my learning and properly structuring a repository.

## 📚 What you'll find here
- **[Lessons Learned](./docs/LECCIONES_APRENDIDAS.md)**: Theory, ISTQB notes and concepts. Notes are integrated here alongside the learning diary.
- **[QA Analysis — TLDRDC](./tests/01-Manual/Analisis_QA_TLDRDC.md)**: Practical exercises in validation and verification of TLDRDC (11 CTs documented).
- **[Automated TLDRDC Tests](./tests/02-Automatizados/TLDRDC)**: Suitecase implemented with AI for TLDRDC.
- **[POM + Playwright Architecture](./docs/ARQUITECTURA_POM_PLAYWRIGHT.md)**: Page Object Model pattern implemented in Python.
- **[Allure Report](https://berserkxiii.github.io/QA-Automation/)**: Automated test report with Allure.

## 🛠️ Tools in my journey
|          Category               |        Current Status                   |
|----------------------------------|-----------------------------------------|
| Manual Testing                   | ✅ Active (Constant updates)            |
| Git & GitHub                     | ✅ Active (Practical)                   |
| Automation (Playwright/Python)   | ✅ Active (Practical)                   |
| POM + Fixtures + Pytest          | ✅ Active (Learning)                    |
| API Testing (ReqRes + AutomationExercise) | ✅ Active (Practical)               |

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
| **ReqRes API** | ReqRes.in | Learn API testing | ✅ Active |

> ⚠️ **Note about AutomationExercise**: This website has very aggressive, randomly-appearing advertising (`google_vignette` popup in a dynamic Google Ads iframe). **It's not realistic for a clean production test suite**, but it was excellent for practicing popup handling, dynamic handlers, network interception, and debugging non-deterministic third-party issues. After trying several strategies (network blocking, `add_locator_handler`, `frame_locator`), the root cause was documented as not 100% mitigable due to depending on an external adversarial system, and the affected test was consciously marked as `flaky` using `pytest-rerunfailures`, instead of chasing an impossible fix.



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
✅ Debugging with `page.pause()`, `print()`, and screenshots  
✅ Working with dynamic iframes (`frame_locator`) and their limitations with `add_locator_handler`  
✅ Pytest hooks (`pytest_runtest_makereport`) for correct Allure reporting  
✅ Judgment for marking a test as `flaky` with justification, instead of chasing 100% against non-deterministic systems  

### Recent Evolution: API and Hybrid Integration

- **[test_API.py](./tests/02-Automatizados/AutomationExercise/test/test_API.py)** was added to expand AutomationExercise coverage with API tests, within the same project and virtual environment as the Playwright suite.
- **[test_hibrido.py](./tests/02-Automatizados/AutomationExercise/test/test_hibrido.py)** was subsequently created, combining UI and API to check both flows against the same system.

## Continuous Integration (CI) with GitHub Actions

Automation no longer depends only on local execution. Four independent pipelines were implemented, one per project, and they run automatically on every `push` and `pull_request` to `main`. Each pipeline installs dependencies from scratch on a clean Linux machine and runs the complete suite, without relying on any developer's local configuration.

| Project | Coverage | Status |
|---------|----------|--------|
| AutomationExercise | UI, API, and hybrid tests | [![AutomationExercise](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml) |
| SauceDemo | Playwright UI tests | [![SauceDemo](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_saucedemo.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_saucedemo.yml) |
| API-ReqRes | API tests | [![API-ReqRes](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_reqres.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_reqres.yml) |
| API-GoRest | API tests | [![API-GoRest](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_gorest.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_gorest.yml) |

### Real problems solved during implementation

These pipelines provided technical learning in addition to making the suites pass:

- **Windows vs. Linux differences:** a `ModuleNotFoundError` caused by case sensitivity in file names did not appear on Windows, but did appear on GitHub's Linux runner. It was resolved by correcting imports and configuring `sys.path` explicitly instead of depending on the operating system.
- **Secret management:** API keys are never committed to the repository (`.env` remains in `.gitignore`). **GitHub Secrets** are used instead and injected as environment variables in the pipeline. A common copy-and-paste error was also documented: pasting `KEY=value` instead of only the value adds unwanted text to the secret and causes silent authentication failures. Comparing string lengths helps diagnose it.
- **Key permission scope:** ReqRes distinguishes a `public` key (read-only) from a `manage` key (read and write). Using the wrong one produces a `403` or `invalid_api_key`, which looks like an invalid key at first glance. This was documented as a scope-related authentication finding.
- **Invisible characters in credentials:** `.strip()` was added when reading tokens from environment variables to protect the code against spaces or line breaks introduced during copy and paste.
- **Non-deterministic external services in CI:** `test_get_users_sin_api_key` (finding AR-003) was also unstable in CI. After trying to stabilize it with `pytest-rerunfailures` and up to 15 retries, a real rate-limiting problem appeared as well. It was consciously skipped with `@pytest.mark.skip`, with the reason documented in the code: honesty was prioritized over achieving a green status at all costs.
- **An infrastructure bug in the project:** an `AttributeError` was fixed in the `attach_screenshot` fixture. It failed silently when a test broke during `setup` rather than during test execution (`call`). This pre-existing bug only appeared when the first failure of that kind occurred.

The result is a portfolio with four projects and verifiable status badges, running their suites automatically on every change without manual intervention. This closes the loop from “portfolio with tests” to “portfolio with a verifiable quality pipeline”.

---

## 💡 How to read this portfolio
1. Start in [README.md](./README.md) to see the big picture.
2. Review [LECCIONES_APRENDIDAS.md](./docs/LECCIONES_APRENDIDAS.md) for technical and theoretical details.
3. Look at [01-Manual](./tests/01-Manual) to see how I structure my tests in different contexts.
4. Explore [tests/02-Automatizados/](./tests/02-Automatizados/) to see my finished projects.
5. Check the [ROADMAP](./docs/ROADMAP.md) to understand my learning plan.
6. Review [documents](./docs/) for additional learning material.

---
*Last update: [27/08/2026]*
*Maintained by: Salva_BsK*
