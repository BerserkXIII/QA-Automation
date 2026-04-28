# ⚡ QUICK START — Comandos Frecuentes

## Ejecutar Tests

```bash
# Todos (cuando termines todo)
pytest tests/unit/ -v

# Un archivo
pytest tests/unit/test_reactive.py -v

# Una clase
pytest tests/unit/test_reactive.py::TestReactiveInit -v

# Un test específico
pytest tests/unit/test_reactive.py::TestReactiveInit::test_init_vacio -v

# Modo "rápido" (sin output detallado)
pytest tests/unit/test_reactive.py -q

# Con prints visibles
pytest tests/unit/test_reactive.py -s
```

## Debugging

```bash
# Ver más detalles si algo falla
pytest tests/unit/test_reactive.py -vv

# Traceback completo
pytest tests/unit/test_reactive.py --tb=long

# Debugger interactivo (pausa en errores)
pytest tests/unit/test_reactive.py --pdb
```

## Configurar tu Primer Test

```bash
# Copia template
cp tests/unit/test_reactive_TEMPLATE.py tests/unit/test_reactive.py

# Abre en editor
code tests/unit/test_reactive.py

# Ejecuta mientras trabajas
pytest tests/unit/test_reactive.py -v
```

## Git Commits

```bash
# Cuando termines un archivo
git add tests/unit/test_reactive.py
git commit -m "test: test_reactive implementado (13 tests)"

# Cuando termines TODO
git add tests/unit/test_*.py
git commit -m "test: todos los 96 tests implementados"
```

---

**¿Más info?** Lee INDICE.md (orden de trabajo) o TALLER_README.md (conceptos detallados).
