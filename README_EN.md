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
- **[QA Analysis — CI/CD](./tests/01-Manual/Analisis_QA_CI_CD.md)**: Implementation, decoupling, and credential management for the four automatic pipelines and ParaBank's manual workflow.
- **[QA Analysis — ParaBank](./tests/01-Manual/Analisis_QA_ParaBank.md)**: Automated UI, API, and hybrid coverage of a demo banking application.
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
| **AutomationExercise** | Fictional e-commerce | UI, API, and E2E integration testing | ✅ Completed |
| **ParaBank** | Demo banking app | UI, API, and hybrid integration testing | 🧪 In progress |
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

### AutomationExercise: from isolated learning to E2E integration

I decided to build this suite to test AutomationExercise end to end, first by testing its layers separately and then by combining them. That is why this playground contains three complementary test suites:

- **[test_UI.py](./tests/02-Automatizados/AutomationExercise/test/test_UI.py)**: validates the frontend and visible flows with Playwright.
- **[test_API.py](./tests/02-Automatizados/AutomationExercise/test/test_API.py)**: validates the backend through the application's APIs.
- **[test_hibrido.py](./tests/02-Automatizados/AutomationExercise/test/test_hibrido.py)**: combines UI and API in the same scenario to check E2E behavior and consistency between both layers.

SauceDemo helped me learn UI testing with Playwright, while ReqRes and GoRest provided practice with API testing. I then applied those foundations in AutomationExercise, which is the most consistent playground I have used so far for bringing all these practices together in one application.

### ParaBank: UI, API, and hybrid banking tests

The [ParaBank suite](./tests/01-Manual/Analisis_QA_ParaBank.md) combines Playwright and API checks for registration, account opening, and transfers, verifying balances before and after each operation. Hybrid tests compare the accounts and balances visible in the UI with backend data.

- **Functional findings:** ParaBank allows transfers exceeding the available balance and account opening with insufficient funds. The latter is recorded as `xfail`; the suite documents both the observed behavior and the expected behavior.
- **Documented run (November 2026):** 11 tests passed and 1 was `xfail`. As ParaBank is a shared demo server, the suite requires pauses between tests and may be affected by server errors or Cloudflare rate limiting.

## Continuous Integration (CI) with GitHub Actions

The complete implementation process, including `paths` filters, secret management, and configuration findings, is documented in [QA Analysis — CI/CD](./tests/01-Manual/Analisis_QA_CI_CD.md).

Automation no longer depends only on local execution. Four pipelines run automatically on every `push` and `pull_request` to `main`, and a fifth workflow for ParaBank is run manually. The ParaBank workflow is started on demand to limit requests to its shared server and avoid Cloudflare rate limiting. Each workflow installs dependencies from scratch on a clean Linux machine and runs its suite, without relying on any developer's local configuration.

| Project | Coverage | Status |
|---------|----------|--------|
| AutomationExercise | UI, API, and hybrid tests | [![AutomationExercise](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/tests-automationexercise.yml) |
| ParaBank | UI, API, and hybrid tests (manual) | [![ParaBank](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_parabank.yml/badge.svg)](https://github.com/BerserkXIII/QA-Automation/actions/workflows/test_parabank.yml) |
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

The result is a portfolio with five CI test suites and verifiable status badges. Four run automatically on changes; ParaBank is started manually to respect the external service's limits. This closes the loop from “portfolio with tests” to “portfolio with a verifiable quality pipeline”.

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
