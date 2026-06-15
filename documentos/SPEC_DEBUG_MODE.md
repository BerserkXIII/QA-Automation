# SPEC: Modo Debug en TLDRDC — Comando `set` en `leer_input`

**Estado**: Propuesto — pendiente de implementación  
**Fecha**: 2026-04-18  
**Motivación**: CT-012 y futuros CTs que requieren estado inicial controlado tienen
testabilidad baja sin un mecanismo para establecer variables del personaje directamente.
Ver sección *Testabilidad* de CT-012.

---

## 1. Objetivo

Añadir un comando de debug `set <variable> <valor>` accesible durante la partida,
que permita modificar variables del personaje en cualquier momento en que el juego
esté esperando input del jugador. Esto convierte precondiciones como `vida == 2` en
reproducibles en segundos en lugar de ~15 minutos de juego natural.

---

## 2. Análisis de impacto

### Archivo a modificar
**Un único archivo**: `TLDRDC/code/TLDRDC_Prueba1.py`  
**Una única función**: `leer_input(prompt, personaje)` — línea **2402**

### Función actual (completa)
```python
def leer_input(prompt, personaje):
    while True:
        valor = pedir_input().strip().lower()
        if valor in ["stats", "st", "stat"]:
            mostrar_stats(personaje)
            continue
        separador()
        return valor
```

### Por qué este es el punto correcto
- Todos los eventos (`events.py`) llaman a `leer_input("> ", personaje)` para leer
  cada input del jugador.
- Ya existe el precedente del comando `stats`: cuando el usuario escribe "stats",
  la función lo intercepta, ejecuta la acción y vuelve a pedir input. El juego
  no recibe ese valor — lo maneja `leer_input` internamente.
- Añadir `set` sigue exactamente el mismo patrón. Riesgo de regresión: **mínimo**.

### Archivos que NO hay que tocar
- `modules/events.py` — ningún cambio
- `modules/reactive.py` — ningún cambio
- `ui_tester/` — ningún cambio
- Cualquier otro archivo — ningún cambio

---

## 3. Cambio propuesto

Añadir un bloque `elif` en `leer_input`, inmediatamente después del bloque `stats`:

```python
def leer_input(prompt, personaje):
    while True:
        valor = pedir_input().strip().lower()
        if valor in ["stats", "st", "stat"]:
            mostrar_stats(personaje)
            continue
        # --- INICIO: comando debug ---
        if valor.startswith("set "):
            partes = valor.split(maxsplit=2)
            if len(partes) == 3:
                var, val_str = partes[1], partes[2]
                vars_permitidas = {
                    "vida", "vida_max", "pociones", "pociones_max",
                    "armadura", "armadura_max", "fuerza", "destreza"
                }
                if var in vars_permitidas:
                    try:
                        personaje[var] = int(val_str)
                        alerta(f"[DEBUG] {var} = {int(val_str)}")
                    except ValueError:
                        alerta(f"[DEBUG] Valor inválido: '{val_str}'")
                else:
                    alerta(f"[DEBUG] Variable '{var}' no permitida.")
            else:
                alerta("[DEBUG] Uso: set <variable> <valor>")
            continue
        # --- FIN: comando debug ---
        separador()
        return valor
```

### Variables permitidas (whitelist explícita)
| Variable | Rango sugerido |
|---|---|
| `vida` | 1 – `vida_max` |
| `vida_max` | 1 – 20 |
| `pociones` | 0 – `pociones_max` |
| `pociones_max` | 0 – 10 |
| `armadura` | 0 – `armadura_max` |
| `armadura_max` | 0 – 20 |
| `fuerza` | 1 – 25 |
| `destreza` | 1 – 25 |

> **Nota**: La implementación propuesta NO valida rangos. Establece el valor
> directamente, igual que hace `cmd_set` en `ui_tester/parser.py`. Esto es
> intencional: el tester tiene control total. Si se quiere añadir clamp, es
> trivial hacerlo después.

---

## 4. Efectos esperados

### ✅ Lo que funciona tras el cambio
- `set vida 2` durante cualquier evento → `personaje["vida"] = 2`
- `set fuerza 5` antes de una decisión de combate → stats modificados
- Si `Personaje` es reactivo (clase `Personaje` de `reactive.py`), los
  observadores se dispararán automáticamente → HUD y sprites se actualizan.
- El juego no recibe la cadena "set ..." como respuesta válida a ninguna pregunta
  (el `continue` se encarga).

### ⚠️ Lo que no cambia / no se rompe
- Los eventos que ya validan la respuesta del jugador (`if resp in ["s", "si"]`)
  siguen funcionando igual — `set` nunca llega hasta ellos.
- El comando `stats` existente sigue funcionando.
- `fin_derrota()` no se ve afectado.
- El hilo de UI (Vista / Tkinter) no se toca.

### ❌ Riesgos a verificar tras implementar
| Riesgo | Probabilidad | Cómo verificar |
|---|---|---|
| `set vida 0` sin pasar por `fin_derrota` | Media | Probar `set vida 0` y ver si el juego continúa en estado inválido. Documentar como limitación conocida del modo debug. |
| Valores fuera de rango rompen la UI (ej. `set fuerza 999`) | Baja | La UI usa los valores de `personaje` para mostrar, no para validar. Puede mostrar valores extraños pero no crashear. |
| `pedir_input()` devuelve el valor ya en lowercase | Verificado | La función ya hace `.strip().lower()` antes de comparar. El `set` se escribe en minúsculas, funciona. |

---

## 5. Plan de implementación paso a paso

1. **Abrir** `TLDRDC/code/TLDRDC_Prueba1.py`
2. **Ir a la línea 2402** (función `leer_input`)
3. **Hacer backup mental**: la función tiene 7 líneas. Cualquier error es fácil de revertir.
4. **Añadir** el bloque `if valor.startswith("set "):` después del bloque `stats` (ver §3)
5. **Guardar** el archivo
6. **Verificar sin ejecutar**: buscar que no haya errores de sintaxis (`get_errors`)
7. **Prueba de humo**: iniciar partida, llegar a cualquier evento con `leer_input`, escribir `set vida 2`, verificar con `stats` que cambió, responder la pregunta del evento normalmente
8. **Prueba de regresión mínima**: verificar que `stats` sigue funcionando, que respuestas normales (`s`, `n`) siguen siendo procesadas por los eventos

---

## 6. Reversión

Si algo sale mal, el cambio es un bloque de ~14 líneas entre los comentarios
`# --- INICIO: comando debug ---` y `# --- FIN: comando debug ---`.
Borrar ese bloque completo deja la función exactamente como estaba.

---

## 7. CTs desbloqueados tras implementación

| CT | Precondición difícil | Con `set` |
|---|---|---|
| CT-012 | `vida == 2` antes del Evento 4 | `set vida 2` → inmediato |
| Futuros CTs de combate | Stats específicos (`fuerza`, `destreza`) | `set fuerza X` |
| Futuros CTs de `fin_derrota` | Cualquier path de muerte | `set vida 1` + evento de daño |

---

*Spec generada en sesión QA — 2026-04-18*
