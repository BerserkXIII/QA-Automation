# Especificación de Tests — UI IMAGEN MANAGER

*Versión: 0.2 (Test Spec)*

---

## RESUMEN EJECUTIVO

**ImagenManager** — Gestiona caché de imágenes PNG, escalado dinámico, fallbacks defensivos

**Propósito**: Cargar sprites sin fallar si imagen falta o está corrupta

---

## MATRIZ DE PRUEBAS

| Test ID | Función | Validación |
|---------|---------|-----------|
| I1.1 | __init__ | Inicialización correcta |
| I2.1 | cargar_imagen | Carga PNG válido |
| I2.2 | cargar_imagen | Redimensión aplicada |
| I2.3 | cargar_imagen | No existe → None |
| I2.4 | cargar_imagen | Corrupto → None |
| I2.5 | cargar_imagen | Caché funciona |
| I2.6 | cargar_imagen | Caché por (ruta, tamaño) |
| I2.7 | cargar_imagen | Caché LRU o FIFO |
| I2.8 | cargar_imagen | Aspecto preservado |
| I3.1 | validar_rutas | Detecta carpetas faltantes |

---

## CLASE: `ImagenManager`

### Función: `__init__(ruta_base, caché_size=100)`

**¿Qué hace?**
- Inicializa gestor con ruta base de imágenes
- Prepara dict caché vacío
- Establece tamaño máximo caché

#### Test I1.1: Inicialización básica
```
ARRANGE:
  - ruta = "/assets/images"
  - caché_size = 50
ACT:
  - manager = ImagenManager(ruta, caché_size)
ASSERT:
  - manager.ruta_base == ruta
  - manager.caché == {}
  - manager.caché_size == 50
```

---

### Función: `cargar_imagen(ruta, tamaño=None)`

**¿Qué hace?**
- Si está en caché y `tamaño` coincide: retorna cached
- Si no: carga PNG con PIL.Image.open()
- Redimensiona a `tamaño` si se proporciona
- Almacena en caché
- Si archivo no existe: retorna `None` (sin excepción)
- Si PNG corrupto: retorna `None` (captura excepción)

#### Test I2.1: Carga imagen válida
```
ARRANGE:
  - PNG válido en "/assets/daga.png"
  - tamaño = None
ACT:
  - img = manager.cargar_imagen("/assets/daga.png")
ASSERT:
  - img es PIL.Image
  - img mode es RGBA o RGB
  - No es None
```

#### Test I2.2: Redimensión SOLO si PIL disponible
```
ARRANGE:
  - PNG original 200x200
  - tamaño = (50, 50)
ACT:
  - img = manager.cargar_imagen("/assets/daga.png", (50, 50))
ASSERT:
  - Si PIL disponible: img.size == (50, 50)  (redimensionado)
  - Si NO PIL: retorna tk.PhotoImage nativo (sin redimensión, tamaño original)
  - Sin excepción en ambos casos
```

#### Test I2.3: Imagen no existe retorna None
```
ARRANGE: Ruta "/assets/fake.png" no existe
ACT:
  - img = manager.cargar_imagen("/assets/fake.png")
ASSERT:
  - img is None
  - Sin excepción FileNotFoundError
```

#### Test I2.4: PNG corrupto retorna None
```
ARRANGE:
  - Archivo PNG con contenido corrupto
ACT:
  - img = manager.cargar_imagen("/assets/corrupted.png")
ASSERT:
  - img is None
  - Excepción capturada internamente
```

#### Test I2.5: Caché funciona
```
ARRANGE:
  - PNG válido
ACT:
  - img1 = manager.cargar_imagen("/assets/daga.png", (50, 50))
  - img2 = manager.cargar_imagen("/assets/daga.png", (50, 50))
ASSERT:
  - img1 is img2  (mismo objeto de memoria, no recargado)
  - len(manager.caché) == 1
```

#### Test I2.6: Caché con tamaño diferente es nueva entrada
```
ARRANGE: PNG válido
ACT:
  - img1 = manager.cargar_imagen("/assets/daga.png", (50, 50))
  - img2 = manager.cargar_imagen("/assets/daga.png", (100, 100))
ASSERT:
  - img1 is not img2  (diferentes objetos)
  - len(manager.caché) == 2
  - Clave caché incluye (ruta, tamaño)
```

#### Test I2.7: Sin límite hard de caché
```
ARRANGE:
  - manager = ImagenManager()  (sin parámetro caché_size)
  - Cargar 10 imágenes diferentes
ACT:
  - Para i en 1..10: manager.cargar_imagen(f"/img_{i}.png")
ASSERT:
  - len(manager._cache) == 10  (todas permanecen)
  - Sin desalojo automático
  - Limpieza manual vía limpiar_cache()
```

#### Test I2.8: Redimensión preserva aspecto (opcional)
```
ARRANGE:
  - PNG original 100x200 (2:1 ratio)
  - tamaño = (50, 100)  (mantiene ratio)
ACT:
  - img = manager.cargar_imagen("/assets/test.png", (50, 100))
ASSERT:
  - img.size == (50, 100)
  - Imagen no distorsionada
```

---

### Función: `validar_rutas()` (Extra)

**¿Qué hace?**
- Verifica que rutas base de sprites existan
- Detecta carpetas faltantes (ej: `/images/botones/armas/`)

#### Test I3.1: Detecta carpeta faltante
```
ARRANGE:
  - RUTAS_IMAGENES_PANELES = "/modules/imagenes/pruebas/"  (no existe)
ACT:
  - validar_rutas()
ASSERT:
  - Alerta emitida o log de advertencia
  - No crash, pero indica problema
```

---

## FIXTURES NECESARIAS

```python
import PIL.Image
import tempfile
from unittest.mock import Mock, patch
import os

# Crear PNG test válido
@pytest.fixture
def valid_png(tmp_path):
    """Crea PNG válido 100x100 rojo"""
    img = PIL.Image.new("RGB", (100, 100), color="red")
    png_path = tmp_path / "test.png"
    img.save(png_path)
    return str(png_path)

# Crear PNG corrupto
@pytest.fixture
def corrupt_png(tmp_path):
    """Crea archivo PNG corrupto"""
    png_path = tmp_path / "corrupt.png"
    with open(png_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"INVALID_DATA")
    return str(png_path)

# ImagenManager mock
@pytest.fixture
def manager(tmp_path):
    return ImagenManager(str(tmp_path))
```

---

## NOTAS

- **I2.3, I2.4**: Tests defensivos críticos — spritesfaltantes no rompen UI
- **I2.5**: Caché es optimización importante para rendimiento
- **I2.2**: PIL es opcional; fallback a tk.PhotoImage nativo para PNG
  - `manager.pil_disponible` indica si PIL está disponible
  - Sin PIL: redimensión usa `Image.thumbnail()` (aspecto preservado)
- **I2.7**: NO hay límite hard de caché; limpieza manual vía `limpiar_cache()`
- Tests pueden usar `tmp_path` fixture de pytest para archivos temporales
- Fixture debe mockar `PIL_DISPONIBLE` para testear fallback
