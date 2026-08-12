# Análisis QA API-GoRest

## Descripción
Este documento recoge los hallazgos y aprendizajes obtenidos durante la construcción de la suite de tests para `gorest.co.in`. El enfoque principal ha sido comprender el comportamiento de los status codes de la API y descubrir las limitaciones prácticas al testear rate limiting. El hallazgo más relevante es que el contador de rate limit (`x-ratelimit-remaining`) no se actualiza en tiempo real síncrono, lo que invalida su uso como condición de parada en bucles de prueba.

*Fecha de última actualización:* 12/08/2026

## Casos de prueba importantes

### GR-001: Contador `x-ratelimit-remaining` no es síncrono — test de rate limit no confiable
- **ID**: GR-001
- **Descripción**: El test `test_requests_rate_limit` intenta forzar un límite de tasa haciendo peticiones hasta agotar el contador de `x-ratelimit-remaining`. Sin embargo, este contador no se actualiza en tiempo real síncrono, lo que provoca que el bucle no sepa cuándo detenerse de forma confiable.
- **Severidad**: ALTA
  - Razón: No es un bug del servidor, sino una limitación arquitectónica que invalida un test que depende de datos no síncronos para controlar su flujo.
  - Impacto: El test no es confiable como herramienta de validación — puede pasar o fallar intermitentemente según el timing de actualización del contador en el servidor.
  - Reproducibilidad: Baja en el sentido de que es difícil reproducir exactamente cuándo el contador se actualizará, lo que lo hace inútil como test determinista.
- **Precondiciones**: Usuario autenticado con `token` válida; servidor GoRest accesible; cuota de rate limit disponible.
- **Pasos**:
  1. Hacer una petición inicial `GET /users` y guardar el valor de `x-ratelimit-remaining`.
  2. En un bucle, hacer peticiones consecutivas hasta que `remaining == 0` (o hasta que se reciba `429`).
  3. En cada iteración, imprimir el valor de `x-ratelimit-remaining` observado.
  4. Registrar cuándo se recibe el primer `429` y comparar con el valor esperado.
- **Resultado esperado**: El contador debería decrementarse de forma predecible en cada petición, permitiendo que el bucle se detenga exactamente cuando el límite se alcance.
- **Resultado actual / problema**: El contador no refleja el estado real en tiempo síncrono. Múltiples peticiones consecutivas pueden devolver el mismo valor de `remaining`, o pueden "saltarse" valores. El servidor devuelve `429` en algún punto indeterminado que no coincide necesariamente con `remaining == 0` en la última respuesta recibida.
- **Código de referencia**:
```python
def test_requests_rate_limit(headers):
    response1 = requests.get(f"{BASE_URL}/users", headers=headers, timeout=10)
    for _ in range(int(response1.headers.get('x-ratelimit-remaining', 0)) + 1):
        response = requests.get(f"{BASE_URL}/users", headers=headers, timeout=10)
        if response.status_code == 429:
            break
        else:
            print(f"Remaining requests: {response.headers.get('x-ratelimit-remaining')}")
            print(f"Rate limit reset time: {response.headers.get('x-ratelimit-reset')}")
            print(f"Rate limit limit: {response.headers.get('x-ratelimit-limit')}")
            print(f"Intento {_}: remaining={response.headers.get('x-ratelimit-remaining')}")
            print(f"cache: {response.headers.get('cf-cache-status')}")
    assert response.status_code == 429
    assert "x-ratelimit-reset" in response.headers
```
- **Notas**: 
  - El servidor sí incluye las cabeceras de rate limit (`x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-reset`), lo que sugiere que el mecanismo existe.
  - Sin embargo, el contador parece actualizarse en el backend con cierto retraso o granularidad que no coincide con el timing de las peticiones del cliente.
  - Está presente también la cabecera `cf-cache-status` (Cloudflare), pero el comportamiento inconsistente del contador sugiere que el problema es en el servidor de GoRest, no en la capa de caché.
  - Este test como está escrito **no es válido** porque depende de un dato no síncrono para tomar decisiones sobre el flujo.
- **Lección aprendida**: No asumir que una cabecera de "estado actual" (como `remaining`) se actualiza en tiempo real síncrono con el servidor. En sistemas distribuidos o con backends complejos, puede haber retraso o granularidad en la actualización. Para testear rate limiting de forma confiable, es mejor esperar un `429` y luego validar que las cabeceras de reset están presentes, sin depender del contador exacto como condición de parada.

### GR-002: Status codes y comportamiento de validación de datos
- **ID**: GR-002
- **Descripción**: GoRest implementa validación de esquema de datos más robusta que otros APIs mock. Los status codes devueltos son consistentes y sirven como señales claras del resultado de la operación.
- **Severidad**: BAJA (información, no es un bug)
  - Razón: Es un comportamiento esperado de una API seria — el servidor valida datos y devuelve errores explícitos.
  - Impacto: Positivo — permite escribir tests de validación confiables.
  - Reproducibilidad: Alta y consistente.
- **Precondiciones**: Usuario autenticado con token válido; acceso a los endpoints CRUD.
- **Pasos**:
  1. Hacer `POST /users` con un payload completo y válido → esperar `201 Created`.
  2. Hacer `GET /users/{id}` sobre el usuario creado → esperar `200 OK`.
  3. Hacer `PATCH /users/{id}` con actualización válida → esperar `200 OK`.
  4. Hacer `DELETE /users/{id}` → esperar `204 No Content`.
  5. Hacer `GET /users/{id_inexistente}` → esperar `404 Not Found`.
- **Resultado esperado**: Todos los status codes anteriores se devuelven de forma consistente.
- **Resultado actual**: Confirmado — los status codes son fiables y coinciden con la especificación HTTP estándar.
- **Código de referencia**:
```python
def test_get_users_status_200(headers):
    response = requests.get(f"{BASE_URL}/users", headers=headers, timeout=10)
    assert response.status_code == 200

def test_post_new_user(headers):
    payload = {
        "name": "test_user",
        "email": f"test{time.time()}@example.com",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload, timeout=10)
    assert response.status_code == 201

def test_get_users_id_invalido(headers, id_invalido):
    response = requests.get(f"{BASE_URL}/users/{id_invalido}", headers=headers, timeout=10)
    assert response.status_code == 404
```
- **Notas**: A diferencia de algunos mocks que aceptan y reflejan datos arbitrarios, GoRest es más exigente. Esto hace que los tests sean más significativos desde el punto de vista de QA.
- **Lección aprendida**: Una API que valida datos y devuelve status codes explícitos es mejor para testing de casos negativos que un mock permisivo. Aunque requiere preparar datos válidos, produce tests de mayor valor.

## Observaciones generales

### Sobre la complejidad del servidor
- **GoRest es un servidor "real"**, no un mock simple. Esto significa que algunos comportamientos que idealmente serían fáciles de testear (como agotar un límite de tasa) requieren en realidad esperar a que infraestructura backend distribuida se sincronice.
- **Caché distribuida**: La presencia de `cf-cache-status` indica que hay Cloudflare de por medio, lo que añade una capa más de complejidad. Aunque en este caso el problema parece ser en GoRest, la arquitectura distribuida es un factor a considerar.
- **Rate limit como concepto**: El rate limiting es un mecanismo importante para producción, pero su testing es complejo cuando el contador no es síncrono. Las alternativas son: (a) testear que las cabeceras de reset están presentes, (b) esperar a un `429` real sin predecir cuándo ocurrirá, o (c) usar un cliente que sí permita medir el timing y validar que el `429` ocurre en un rango razonable.

### Lecciones de arquitectura de testing
- **No todos los comportamientos son testeables de la misma forma**: Rate limiting es una característica de producción crítica, pero testearlo de forma determinista requiere acceso a datos síncronos, que GoRest no proporciona de forma confiable en el contador del header.
- **Los datos "informativos" pueden no ser síncronos**: El header `x-ratelimit-remaining` es informativo, no una garantía de comportamiento. El servidor puede devolver `429` sin que el contador llegue exactamente a cero.
- **Comparación con otros APIs**: 
  - **Reqres**: Mock simple, no valida datos, útil para aprender patrones básicos.
  - **GoRest**: API funcional real, valida datos, tiene rate limiting real, más cercano a producción.
  - **SauceDemo**: Aplicación web interactiva, enseña POM, no es API.

## Recomendaciones para la suite

1. **Eliminar o rediseñar `test_requests_rate_limit`**:
   - Opción A: Eliminar si no es crítico para el plan de testing.
   - Opción B: Rediseñar para no depender del contador exacto de `remaining`. En su lugar, hacer un número elevado de peticiones e ir contando hasta recibir `429`, sin predecir cuándo.
   - Opción C: Si la intención es validar que las cabeceras de rate limit existen y están presentes, hacer un test más simple que no intente agotar el límite.

2. **Mantener tests de status codes**: Son el aspecto más confiable de GoRest y tienen mayor valor de validación que los tests con datos arbitrarios del mock de Reqres.

3. **Documentar limitaciones conocidas**: En los comentarios del código, dejar claro cuándo un test no intenta cubrir un aspecto porque la infraestructura del servidor lo hace impredecible (como el contador exacto de rate limit).

4. **Considerar tiempo de ejecución**: Los tests que intentan agotar cuotas de rate limit pueden ser lentos. Separar estos en una suite opcional o nocturna si el plan lo permite.

## Hallazgo final
El descubrimiento principal no es un bug del servidor, sino un aprendizaje arquitectónico: **la complejidad real de los servidores hace que ciertos datos reportados (como contadores de estado) no sean confiables como condiciones de control de flujo en tests**. Esto es un conocimiento valioso para futuro testing, donde se aprende a distinguir entre datos informativos y datos que realmente controlan el comportamiento del sistema.
