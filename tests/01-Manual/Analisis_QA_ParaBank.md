# Análisis QA — ParaBank

Suite automatizada de UI, API e híbrida sobre [ParaBank](https://parabank.parasoft.com), la aplicación bancaria de demostración de Parasoft.

**Estado (noviembre 2026):** 11 tests en verde y 1 `xfail` (suite completa en ~2 min, con 5 s de pausa entre tests).

---

## 1. Cobertura

| Capa | Test | Qué comprueba |
|---|---|---|
| UI | `test_create_user_account` | Registro correcto de un usuario nuevo |
| UI | `test_create_user_account_with_existing_username` | Rechazo de un username duplicado |
| UI | `test_create_user_account_required_fields` | Mensaje de error por cada campo obligatorio vacío (bucle sobre `CAMPOS_OBLIGATORIOS`) |
| UI | `test_create_new_bank_account` | Apertura de cuenta y presencia de la cuenta inicial y la nueva en Accounts Overview |
| UI | `test_transfer_funds` | Transferencia válida: el origen baja y el destino sube el importe exacto (saldos leídos en Accounts Overview) |
| UI | `test_transfer_funds_sin_limite_saldo_negativo_confirmado` | Fija el comportamiento actual: transferir más que el saldo está permitido y deja el origen en negativo |
| UI | `test_create_bank_account_insufficient_funds` (`xfail`) | Comportamiento esperado: no debería permitirse abrir cuenta sin fondos suficientes |
| Híbrido | `test_accounts_UI_checking_API` | Cuentas creadas por UI existen en el backend (comprobadas por API) |
| Híbrido | `test_transfer_funds_UI_checking_API` | Transferencia por UI, saldos antes y después leídos por API |
| API | `test_get_userID`, `test_get_accountID` | Consulta de cliente y de cuentas por API |
| API | `test_transfer_funds_API` | Crear cuenta y transferir por API, saldos verificados antes y después |

---

## 2. Decisiones técnicas

**Selectores por atributo `id` en el formulario de registro.**
ParaBank es una aplicación antigua, y en el formulario de registro los textos visibles no están asociados a sus campos (no hay `label` enlazada), por lo que `get_by_label` no es una opción. Para los campos se usan selectores por atributo, `[id="customer.firstName"]`, con la sintaxis de atributo porque el punto del `id` rompería un selector CSS `#customer.firstName`. Los botones y enlaces sí se localizan con `get_by_role`.

**Arquitectura.**
Page Objects para las páginas (sin `assert`), fixtures en `conftest.py` para el montaje, tests que verifican. Las consultas a la API viven en `api_helpers.py` como funciones normales y no como fixtures, porque deben poder llamarse varias veces dentro de un mismo test (un fixture se evalúa una vez y su resultado queda guardado).

**Cuentas identificadas por id, no por posición.**
`crear_cuenta_bancaria_nueva` devuelve el id de la cuenta de origen y el de la nueva; las transferencias seleccionan las cuentas por ese id. El orden de los desplegables o de la lista de la API no está garantizado.

**Patrón antes / acción / después en transferencias.**
Se leen los saldos, se transfiere, se vuelven a leer y se comparan **diferencias** (`pytest.approx`), sin suponer ningún saldo inicial. Tras cada cambio de estado se vuelve a consultar el servidor en lugar de reutilizar datos ya descargados.

**Verificación por dos vías.**
Los tests de UI leen los saldos de Accounts Overview; los híbridos usan la API como fuente independiente. Así se comprueba tanto lo que ve el usuario como lo que registra el backend.

**`xfail` y regresión.**
El bug de saldo negativo se documenta de dos maneras: un `xfail(raises=AssertionError)` que expresa el comportamiento esperado, y un test de regresión que fija el comportamiento actual. `raises=AssertionError` evita que un fallo de entorno (por ejemplo, un 500) se disfrace de fallo esperado.

**Fallo de servidor con mensaje claro.**
Al abrir "Open New Account", si el desplegable no aparece y la página muestra `p.error`, el test falla con `pytest.fail("ParaBank: error interno (500)...")`. Si no hay mensaje de error, se relanza el timeout original, porque entonces el problema puede estar en el test.

---

## 3. Hallazgos de la aplicación

1. **Saldo negativo en transferencias.** La aplicación acepta transferir un importe superior al saldo disponible y deja la cuenta de origen en negativo. Fijado en `test_transfer_funds_sin_limite_saldo_negativo_confirmado`.
2. **Saldo negativo al abrir cuentas.** Abrir cuentas sucesivas desde la misma cuenta de origen permitió llegar a un saldo de `-100.0` (observado por API el 05/11). Marcado en el `xfail`. *[Revisa la redacción con tu test: si la UI anuncia un depósito mínimo, añádelo aquí.]*
3. **Códigos de estado.** El endpoint de creación de cuenta responde `200`, no `201`. Swagger documenta `200`, por lo que no es un defecto, solo una desviación de la convención REST.
4. **Sin endpoint REST para crear clientes.** El registro solo puede hacerse por UI, por lo que todos los tests necesitan una sesión de registro por navegador.

---

## 4. Incidencias de entorno

ParaBank es un servidor de demostración compartido y estas incidencias no corresponden a defectos de los tests.

**Error 500 intermitente (04/11, ~11:00 hora local).**
Al entrar en "Open New Account", la petición `account` devolvía `500` y la aplicación mostraba "An internal error has occurred and has been logged". Ocurría con usuarios recién creados. En el test aparecía como timeout, porque el desplegable nunca llegaba a pintarse. No reproducible el 05/11.

**Rate limiting de Cloudflare, error 1015 (04/11, 14:24 UTC).**
Pasar la suite completa dispara el límite de peticiones de Cloudflare ("You are being rate limited"). El bloqueo se levantó solo, tras unos 15 minutos *[confirma la hora: 14:24 UTC es 15:24 hora local; si lo desbloquearon a las 15:40 locales, son 14:40 UTC]*. Se reprodujo después y volvió a ocurrir el 11/11.
Los límites los define el propietario del sitio y no se publican.

**Mitigación.**

| Medida | Efecto |
|---|---|
| Bloquear imágenes y fuentes con `page.route` (fixture `autouse`) | De **103 a 26 peticiones** en `test_transfer_funds_UI_checking_API` (−75 %) |
| Pausa de 5 s entre tests (fixture `autouse`) | Suite completa sin bloqueo: 11 passed, 1 xfailed en 1:56 |

---

## 5. Limitaciones

- Al bloquear imágenes y fuentes, estos tests no detectarían un fallo de carga de esos recursos; no es su objetivo.
- Ejecuciones fiables solo con pausa y, aun así, sujetas a la disponibilidad de un servidor ajeno.
- La suite completa solo se ha verificado limpia en una ejecución; falta confirmarla en más.

## 6. Pendiente

- CI en GitHub Actions: workflow manual, con capturas de pantalla como artefacto para diagnosticar fallos.
- Smoke test de las páginas del menú (con marker propio y ejecución programada de baja frecuencia).
- Limpiar los parámetros no usados de los fixtures restantes y retirar el fixture temporal que cuenta peticiones.
