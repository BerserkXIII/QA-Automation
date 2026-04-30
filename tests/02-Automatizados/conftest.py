# ════════════════════════════════════════════════════════════════════
# CONFTEST PARA TESTS AUTOMATIZADOS (02-Automatizados/)
# ════════════════════════════════════════════════════════════════════
"""
Re-exporta fixtures de la raíz (conftest.py, conftest_combate.py)
para que pytest las descubra en esta subcarpeta.

Cortafuegos contra loops infinitos:
- test_integration.py: ✅ IMPLEMENTADO (@pytest.mark.timeout en cada test)
- test_threading.py: ✅ INTEGRADO (join(timeout=N))
- Otros tests: ✅ SEGUROS (mocks + loops acotados)

Para agregar timeout global (opcional), usar:
  pytest tests/02-Automatizados/ --timeout=30

Ver: ANALYSIS_LOOP_PROTECTION.md para detalles de protección.
"""

import sys
import os

# Agregar ruta de tests raíz a sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar y re-exportar todos los fixtures
from conftest import *
from conftest_combate import *

# ════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN OPCIONAL DE CORTAFUEGOS
# ════════════════════════════════════════════════════════════════════

"""
Para ACTIVAR timeout global en CI/CD:

Opción 1: pytest.ini
    [pytest]
    addopts = --timeout=30

Opción 2: Línea de comando
    pytest tests/02-Automatizados/ --timeout=30

Opción 3: Variable de entorno
    export PYTEST_TIMEOUT=30
    pytest tests/02-Automatizados/

Status actual: ✅ Deshabilitado (tests corren sin límite)
Razón: Ya están protegidos donde importa (test_integration.py)
"""
