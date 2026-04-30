"""
Módulos del Juego TLDRDC

Contiene todos los módulos de configuración, UI, logging y performance monitoring.
"""

# Importaciones principales para facilitar acceso
try:
    from .logging_manager import DEBUG_MODE, LOG_FILE, _log_debug, limpiar_log
except ImportError:
    DEBUG_MODE, LOG_FILE = False, None

try:
    from .performance_monitor import PERF_MODE, PERF_STATS, _medir_tiempo, mostrar_estadisticas_perf, limpiar_estadisticas
except ImportError:
    PERF_MODE, PERF_STATS = False, {}

from .ui_config import COLORES, RUTAS_IMAGENES_PANELES
from .ui_imagen_manager import imagen_manager
from .ui_estructura import estructura_ui

__all__ = [
    'COLORES', 'RUTAS_IMAGENES_PANELES',
    'imagen_manager',
    'estructura_ui',
]
