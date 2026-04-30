# ════════════════════════════════════════════════════════════════════
# CONFTEST PARA TESTS AUTOMATIZADOS (02-Automatizados/)
# ════════════════════════════════════════════════════════════════════
"""
Re-exporta fixtures de la raíz (conftest.py, conftest_combate.py)
para que pytest las descubra en esta subcarpeta.
"""

import sys
import os

# Agregar ruta de tests raíz a sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar y re-exportar todos los fixtures
from conftest import *
from conftest_combate import *
