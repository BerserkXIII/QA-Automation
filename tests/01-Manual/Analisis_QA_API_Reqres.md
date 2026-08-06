# Análisis QA API-Reqres

## Descripción
Este documento recoge los casos de prueba de API detectados durante la construcción de la suite de tests para `reqres.in`. Se incluyen los hallazgos sobre estructura inconsistente de respuestas, comportamiento del mock ante datos arbitrarios, y un falso negativo causado por caché de CDN en el test de autenticación.

*Fecha de última actualización:* 06/08/2026

## Casos de prueba importantes

### AR-001: Estructura de respuesta inconsistente entre GET y PUT
- **ID**: AR-001
- **Descripción**: El endpoint `GET /api/users/{id}` envuelve el usuario en una clave `data` (`{"data": {...}}`), mientras que `PUT /api/users/{id}` devuelve los campos del usuario sueltos, sin envoltorio, junto con un bloque `_meta` informativo.
- **Severidad**: BAJA
  - Razón: No es un bug de la API, es una diferencia de contrato entre endpoints del mismo recurso.
  - Impacto: Provoca `KeyError` si se accede a la respuesta de PUT asumiendo la misma forma que GET.
  - Reproducibilidad: Alta y consistente — no es intermitente, es el comportamiento fijo del mock.
- **Precondiciones**: Usuario autenticado con `x-api-key` válida; usuario existente (`id=2`) para el GET previo.
- **Pasos**:
  1. Hacer `GET /api/users/2` y guardar la respuesta.
  2. Hacer `PUT /api/users/2` con un payload de actualización y guardar la respuesta.
  3. Comparar la forma (`keys()`) de ambos JSON de respuesta.
- **Resultado esperado**: Ambas respuestas deberían tener una estructura predecible y, idealmente, consistente entre sí.
- **Resultado actual / bug**: `response_get.json()["data"]` funciona, pero `response_put.json()["data"]` lanza `KeyError` porque PUT no envuelve el resultado — hay que acceder directamente a `response_put.json()["first_name"]`, etc.
- **Código de referencia**:
```python
data1 = response1.json()          # GET -> viene envuelto
user1 = data1["data"]

data2 = response2.json()          # PUT -> viene plano, sin envoltorio
user2 = data2
```
- **Notas**: El bloque `_meta` de la respuesta de PUT indica explícitamente que es un endpoint de demo de solo lectura (`"message": "This is a read-only demo endpoint..."`), lo que explica también por qué los cambios no persisten en un GET posterior.
- **Lección aprendida**: Nunca asumir que dos endpoints del mismo recurso comparten estructura de respuesta — hay que inspeccionar cada uno por separado (con un `print` del JSON completo) antes de escribir los asserts, en vez de reutilizar el mismo patrón de acceso a ciegas.

### AR-002: El mock no valida esquema — acepta y refleja datos arbitrarios
- **ID**: AR-002
- **Descripción**: El endpoint `POST /api/users` no valida los campos recibidos: acepta un body vacío (`{}`) y devuelve `201` igualmente, y si se envían campos inventados (ej. `partidas`, `puntos`), los refleja tal cual en la respuesta sin ningún error.
- **Severidad**: MEDIA
  - Razón: No es un fallo, pero cambia por completo el enfoque de testing — no se puede testear validación de esquema porque no existe.
  - Impacto: Un test que espere un `400` ante datos inválidos o incompletos fallaría siempre, porque el mock nunca lo devuelve.
  - Reproducibilidad: Alta y consistente.
- **Precondiciones**: Usuario autenticado con `x-api-key` válida.
- **Pasos**:
  1. Hacer `POST /api/users` con `json={}`.
  2. Verificar el status code y el body de respuesta.
  3. Repetir con `json={"partidas": 10, "puntos": 100}` (campos que no existen en el modelo de usuario real).
  4. Verificar que ambos devuelven `201` y que el segundo refleja exactamente los valores enviados.
- **Resultado esperado (de una API real)**: `400 Bad Request` ante body vacío o campos no reconocidos.
- **Resultado actual (mock)**: `201 Created` en ambos casos. Con body vacío, la respuesta no contiene `name` (porque nunca se envió). Con campos arbitrarios, `data["partidas"] == 10` y `data["puntos"] == 100`, reflejo exacto del payload.
- **Código de referencia**:
```python
def test_crear_usuario_datos_aleatorios(headers):
    payload = {"partidas": 10, "puntos": 100}
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload)
    data = response.json()
    assert response.status_code == 201
    assert data["partidas"] == payload["partidas"]
    assert data["puntos"] == payload["puntos"]
```
- **Notas**: Este hallazgo no estaba en el plan original de la suite — surgió al investigar por qué un test que "debería fallar" pasaba en verde, y se convirtió en su propio caso de prueba documentado en vez de forzarlo dentro de otro test.
- **Lección aprendida**: Ante un resultado inesperado (un test que pasa cuando "no debería"), el paso correcto es investigar el dato real con un `print`, no forzar el assert a lo que salga. La ausencia de validación en un mock es información legítima sobre su comportamiento, no un motivo para simular una comprobación que la API nunca va a hacer de verdad.

### AR-003: Falso negativo en test de autenticación por caché de CDN (Cloudflare)
- **ID**: AR-003
- **Descripción**: El test `test_get_users_sin_api_key` (que espera `401` al no enviar `x-api-key`) pasaba en verde al ejecutarse solo, pero fallaba con `200` al ejecutarse dentro de la suite completa, de forma intermitente.
- **Severidad**: ALTA
  - Razón: Es un falso negativo — el test parece confirmar que la API rechaza peticiones sin autenticar, cuando en realidad a veces no está comprobando nada.
  - Impacto: Podría ocultar una regresión real de seguridad (que la API dejara de exigir autenticación) sin que el test lo detectara.
  - Reproducibilidad: Intermitente — depende de si un test anterior en la misma suite ya pidió esa URL con éxito.
- **Precondiciones**: Ejecutar la suite completa, con al menos un test previo que haga `GET /api/users` autenticado correctamente antes del test de autenticación negativo.
- **Pasos**:
  1. Ejecutar `test_get_users_sin_api_key` de forma aislada → `401`, test en verde.
  2. Ejecutar la suite completa → el mismo test devuelve `200`, test en rojo.
  3. Inspeccionar `response.headers` en ambos casos.
- **Resultado esperado**: `401` de forma consistente, sin importar qué se haya ejecutado antes.
- **Resultado actual / bug**: En la ejecución aislada, la cabecera `cf-cache-status` es `BYPASS` (sin caché, petición real al backend). Dentro de la suite, `cf-cache-status` es `HIT` — Cloudflare sirve una respuesta cacheada de un test anterior (autenticado, con datos reales) para la misma URL, sin volver a comprobar la cabecera `x-api-key`.
- **Código de referencia**:
```python
# Antes (vulnerable a servir una respuesta cacheada de otro test)
response = requests.get(f"{BASE_URL}/users")

# Después (cache-buster: URL única, nunca coincide con caché existente)
import time
response = requests.get(f"{BASE_URL}/users?_cb={time.time()}")
```
- **Notas**: Se descartó primero la hipótesis de que el propio servidor tuviera caché (`Cache-Control: no-store` en la respuesta aislada lo contradecía) — la caché real estaba en la capa de Cloudflare (CDN), que cachea por URL exacta sin tener en cuenta las cabeceras de autenticación de la petición.
- **Lección aprendida**: En tests de API, el orden de ejecución de la suite puede afectar al resultado de un test que parece independiente, si comparten URL y hay una capa de caché de por medio (CDN, proxy, etc.). Ante un resultado que solo falla "en compañía" de otros tests y no en solitario, hay que sospechar de efectos colaterales entre tests — en este caso, inspeccionar los headers de la respuesta (`cf-cache-status`) permitió confirmar la causa exacta en vez de adivinarla.

## Observaciones generales
- **Contratos de API no uniformes**: Dentro del mismo recurso (`/users`), cada verbo HTTP puede tener su propia forma de respuesta — no se puede asumir consistencia sin comprobarlo.
- **Mocks vs. APIs reales**: Un mock como reqres es excelente para aprender sintaxis y patrones de testing, pero no sirve para practicar testing de validación de negocio, porque no valida nada. Hay que ser explícito sobre esta limitación al documentar los tests.
- **Caso de mayor riesgo**: AR-003 es el más importante de los tres — a diferencia de AR-001 y AR-002 (comportamientos del mock, fáciles de detectar), un falso negativo por caché puede pasar desapercibido y dar falsa confianza sobre un test de seguridad.

## Recomendaciones para la suite
- Aplicar cache-busting (`?_cb=<timestamp>`) en cualquier test negativo de autenticación, ya que son los más sensibles a servir contenido cacheado de tests anteriores.
- Antes de escribir asserts sobre una respuesta nueva, inspeccionar su estructura real con un `print(response.json())` — no asumir que sigue el mismo patrón que otro endpoint ya testeado.
- Documentar explícitamente en el propio test (comentario) cuándo un comportamiento "raro" es una limitación conocida del mock (no validación, no persistencia) para que no se confunda con un bug futuro.
