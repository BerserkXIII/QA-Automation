# Análisis QA AutomationExercise

## Descripción
Este documento recoge los casos de prueba manuales y los hallazgos más importantes del ejercicio AutomationExercise. Se incluyen los problemas detectados en el popup `google_vignette`, la automatización del carrito, la validación de la API y la integración entre UI y API.

*Fecha de última actualización:* 27/08/2026

## Casos de prueba importantes

### AE-001: Cierre del popup inicial de consentimiento / ads
- **ID**: AE-001
- **Descripción**: Al iniciar la página de AutomationExercise, aparece un popup de consentimiento o publicidad que debe cerrarse para continuar con el flujo de pruebas.
- **Severidad**: MEDIA
  - Razón: Bloquea el flujo de pruebas si no se cierra correctamente.
  - Impacto: Interrumpe los pasos de registro, login y navegación inicial.
  - Reproducibilidad: Alta en entornos normales.
- **Precondiciones**: Navegador abierto en `https://automationexercise.com/`.
- **Pasos**:
  1. Abrir la página principal.
  2. Detectar el popup de consentimiento / anuncio.
  3. Pulsar el botón de cierre o aceptar en el popup.
  4. Verificar que la página principal es accesible y que no hay elementos bloqueando la interacción.
- **Resultado esperado**: El popup se cierra y la página principal queda lista para interactuar. El flujo puede continuar hacia login o navegación de productos.
- **Resultado actual / bug**: En la práctica puede aparecer un banner o popup con contenido dinámico que no siempre responde al mismo selector, lo que complica el cierre fiable.
- **Código de referencia**:
```python
for name in ["Consentir", "Consent"]:
    boton = self.page.get_by_role("button", name=name)
    try:
        boton.wait_for(state="visible", timeout=3000)
        boton.click()
        return
    except:
        continue
```
- **Notas**: Este caso es importante porque refleja la fragilidad del test ante ads o popups externos. Permite validar la capacidad del suite para manejar elementos volátiles.
- **Lección aprendida**: Los popups externos deben manejarse con lógica de cierre flexible y con retries; no se puede confiar en un único selector fijo.

### AE-002: Agregar producto al carrito con sistema flexible
- **ID**: AE-002
- **Descripción**: Seleccionar productos desde la página de productos y agregarlos al carrito con un mecanismo flexible para múltiples elementos.
- **Severidad**: MEDIA
  - Razón: Es una operación central del ecommerce.
  - Impacto: Verifica que el flujo de compra inicial funciona.
  - Reproducibilidad: Alta si la página carga correctamente.
- **Precondiciones**: Usuario logueado o en la página de productos; la lista de productos visible.
- **Pasos**:
  1. Ir a la página de productos.
  2. Seleccionar varios productos mediante sus IDs.
  3. Añadir cada producto al carrito.
  4. Ir al carrito.
  5. Verificar que los productos añadidos aparecen en el carrito.
- **Resultado esperado**: Los productos seleccionados se muestran en el carrito con sus precios correctos.
- **Resultado actual / bug**: N/A. El flujo es correcto, pero requiere validaciones adicionales sobre cambios dinámicos en la UI.
- **Notas**: Es importante que la lógica de selección sea flexible y no dependa de un orden fijo de productos, ya que el DOM puede cambiar.
- **Código de referencia**:
```python
for numero_prod in productos_agregados:
    self.page.locator(f".productinfo [data-product-id='{numero_prod}']").click()
    self.page.get_by_role("button", name="Continue Shopping").click()
```
- **Lección aprendida**: Construir pruebas de carrito con listas de IDs y checks independientes permite modificar fácilmente qué productos se comprueban.

### AE-003: `google_vignette` impredecible en test 13
- **ID**: AE-003
- **Descripción**: La aparición del popup `google_vignette` durante el test 13 es intermitente y rompe la verificación de URL, haciendo que el test falle en aproximadamente el 70% de las ejecuciones.
- **Severidad**: ALTA
  - Razón: Genera un comportamiento flaky difícil de estabilizar.
  - Impacto: El test no es fiable y produce falsos negativos.
  - Reproducibilidad: Relativa — aparece con frecuencia, pero no siempre.
- **Precondiciones**: Ejecución normal del test de la suite contra `automationexercise.com`, con navegación previa y acciones de usuario que generan tráfico.
- **Pasos**:
  1. Ejecutar el test de la suite que alcanza el punto donde se dispara `google_vignette`.
  2. Observar si aparece el popup overlay de Google.
  3. Verificar si el test sigue intentando validar la URL o continúa con la siguiente acción.
- **Resultado esperado**: Si aparece el popup, debe cerrarse o ignorarse sin que la comprobación de URL falle.
- **Resultado actual / bug**: El popup aparece de forma random y bloquea el flujo. El test reporta fallo de URL porque la página no llega al estado esperado mientras el popup está activo.
- **Intentos de mitigación**:
  - Se implementó un fixture `setup_ads()` en `conftest.py` que bloquea patrones de URLs de anuncios con `page.route(..., lambda route: route.abort())`.
  - El patrón incluye `**/*google_vignette*` y otros dominios de ads, pero no evita la aparición aleatoria del overlay en todos los entornos.
- **Notas**: El bug es típico de contenido publicitario externo: incluso bloqueadores por IP o scripts no garantizan que desaparezca, porque depende de la navegación y del timing.
- **Lección aprendida**: Con pruebas web reales, los anuncios terceros son una fuente de flaky que conviene documentar como riesgo técnico y no intentar “arreglarlos” con soluciones frágiles.

### AE-004: Doble capa de status en la API (`responseCode` vs status HTTP)
- **ID**: AE-004
- **Descripción**: Validar que las respuestas de la API de AutomationExercise se comprueban tanto a nivel HTTP como a nivel de negocio mediante el campo `responseCode` del JSON.
- **Severidad**: ALTA
  - Razón: Un status HTTP `200` puede ocultar un error funcional de la petición.
  - Impacto: Los tests podrían marcar como correcto un método no soportado o una operación fallida.
  - **Reproducibilidad**: Alta al enviar un método incorrecto al endpoint.
- **Precondiciones**: Acceso a `https://automationexercise.com/api_list` y posibilidad de realizar peticiones HTTP.
- **Pasos**:
  1. Enviar una petición POST al endpoint `productsList`, que solo admite GET.
  2. Inspeccionar el status HTTP de la respuesta.
  3. Inspeccionar el campo `responseCode` y el mensaje del JSON.
  4. Comparar ambos resultados antes de definir las aserciones del test.
- **Resultado esperado**: El status HTTP y el código de negocio se validan por separado. Para este caso, el status HTTP es `200` y `responseCode` es `405`, indicando que el método no está soportado.
- **Resultado actual / bug**: La API devuelve `200` HTTP aunque la operación no sea válida. El error solo se identifica al leer `responseCode` y el mensaje de la respuesta.
- **Código de referencia**: [test_API.py](../../tests/02-Automatizados/AutomationExercise/test/test_API.py), test `test_post_products_list()`.
- **Notas**: El descubrimiento se produjo al observar en consola un status aparentemente correcto junto a un mensaje de método no soportado.
- **Lección aprendida**: En APIs con este diseño no se debe confiar en el status HTTP en solitario; hay que inspeccionar el body antes de escribir el assert.

### AE-005: Nombres de campo distintos entre creación y consulta
- **ID**: AE-005
- **Descripción**: Verificar que los datos enviados a `createAccount` se corresponden correctamente con los datos devueltos por `getUserDetailByEmail`, aunque algunos campos utilicen nombres diferentes.
- **Severidad**: MEDIA
  - Razón: Una comparación directa de los payloads puede fallar aunque los datos se hayan persistido correctamente.
  - Impacto: Puede producir falsos negativos o esconder errores reales de persistencia.
  - **Reproducibilidad**: Alta en cualquier creación de cuenta seguida de una consulta.
- **Precondiciones**: Datos válidos de una cuenta nueva y acceso a los endpoints `createAccount` y `getUserDetailByEmail`.
- **Pasos**:
  1. Crear una cuenta mediante `createAccount`.
  2. Consultar la cuenta usando `getUserDetailByEmail`.
  3. Comparar el payload enviado con la respuesta, campo a campo.
  4. Aplicar un mapeo para los nombres que cambian entre endpoints.
- **Resultado esperado**: Los datos equivalentes coinciden después de aplicar el mapeo: `birth_date` se consulta como `birth_day`, y `firstname`/`lastname` como `first_name`/`last_name`.
- **Resultado actual / bug**: Los endpoints representan algunos atributos con nomenclaturas distintas. Una comparación literal de nombres no permite verificar correctamente la persistencia.
- **Código de referencia**: [test_API.py](../../tests/02-Automatizados/AutomationExercise/test/test_API.py), test `test_post_create_account()`.
- **Notas**: La verificación end-to-end utiliza un diccionario de mapeo, por ejemplo `{"birth_date": "birth_day"}`.
- **Lección aprendida**: Dos endpoints del mismo recurso no tienen por qué compartir nomenclatura; hay que inspeccionar ambas respuestas antes de compararlas.

### AE-006: Campos enviados que no aparecen en la respuesta de consulta
- **ID**: AE-006
- **Descripción**: Comprobar qué campos de una cuenta creada están disponibles al consultar el usuario mediante `getUserDetailByEmail`.
- **Severidad**: MEDIA
  - Razón: No todos los datos enviados durante la creación forman parte de la respuesta pública.
  - Impacto: Comparar todos los campos a ciegas provoca fallos que no representan un problema de persistencia.
  - **Reproducibilidad**: Alta al consultar una cuenta creada por API.
- **Precondiciones**: Una cuenta creada correctamente mediante `createAccount`.
- **Pasos**:
  1. Crear una cuenta enviando todos los campos requeridos, incluido `password` y `mobile_number`.
  2. Consultar la cuenta con `getUserDetailByEmail`.
  3. Revisar qué campos devuelve la respuesta.
  4. Excluir de la comparación los campos que no forman parte del contrato de consulta.
- **Resultado esperado**: La validación compara únicamente los campos que la API devuelve. La contraseña no se expone y `mobile_number` tampoco aparece en la respuesta observada.
- **Resultado actual / bug**: `password` y `mobile_number` están ausentes en la respuesta de consulta, aunque se enviaron al crear la cuenta.
- **Código de referencia**: [test_API.py](../../tests/02-Automatizados/AutomationExercise/test/test_API.py), test `test_post_create_account()`.
- **Notas**: La ausencia de la contraseña es coherente con una API que no debe devolver credenciales. La ausencia de `mobile_number` debe tratarse como una particularidad del contrato público observado.
- **Lección aprendida**: Al verificar la creación de un recurso hay que comparar el contrato real de la respuesta, excluyendo explícitamente los campos que no se reflejan.

### AE-007: Diferencia entre el formulario web y la API al crear una cuenta
- **ID**: AE-007
- **Descripción**: Comparar la implementación de la creación de cuentas desde el formulario web con la operación equivalente en la API pública.
- **Severidad**: MEDIA
  - Razón: La misma acción de negocio utiliza contratos y pasos técnicos diferentes según el canal.
  - Impacto: Un test diseñado para la API no valida automáticamente el flujo web, ni al contrario.
  - **Reproducibilidad**: Alta al observar las peticiones de ambos flujos.
- **Precondiciones**: Acceso al formulario de registro de AutomationExercise y a la API pública de creación de cuentas.
- **Pasos**:
  1. Iniciar el registro desde el formulario web.
  2. Capturar la petición real enviada por el navegador.
  3. Observar que el formulario utiliza `csrfmiddlewaretoken` y separa el registro en dos fases.
  4. Comparar esa petición con el payload enviado a `/api/createAccount`.
- **Resultado esperado**: Cada test valida el contrato correspondiente a su canal: el formulario web gestiona CSRF y dos fases, mientras que la API recibe todos los campos en una sola petición sin CSRF.
- **Resultado actual / bug**: La web y la API llegan al mismo resultado de negocio mediante implementaciones internas diferentes: la web comienza con nombre y email, y la API espera el conjunto completo de datos.
- **Código de referencia**: Tests de UI de [AutomationExercise](../../tests/02-Automatizados/AutomationExercise/test/test_UI.py) y [test_API.py](../../tests/02-Automatizados/AutomationExercise/test/test_API.py).
- **Notas**: La petición web se inspeccionó mediante `page.expect_request()` durante un test de Playwright existente.
- **Lección aprendida**: No se debe asumir que dos canales comparten la misma lógica interna solo porque producen el mismo resultado funcional.

### AE-008: Inconsistencia del banner de sesión según el flujo de autenticación
- **ID**: AE-008
- **Descripción**: Verificar si el banner `Logged in as X` muestra la misma información cuando la cuenta se crea por API y cuando se crea desde el formulario web.
- **Severidad**: MEDIA
  - Razón: El usuario ve resultados distintos para una misma funcionalidad de autenticación.
  - Impacto: La experiencia y las comprobaciones de UI no son consistentes entre flujos.
  - **Reproducibilidad**: Alta en los dos recorridos híbridos definidos.
- **Precondiciones**: Suite de UI y API disponible, cuenta nueva y capacidad de comparar capturas de Allure.
- **Pasos**:
  1. Crear una cuenta mediante API.
  2. Iniciar sesión con esa cuenta desde la UI y observar el banner.
  3. Crear otra cuenta mediante el formulario web.
  4. Observar el banner inmediatamente después del registro.
  5. Comparar el resultado visual de ambos recorridos.
- **Resultado esperado**: El banner muestra de forma consistente el nombre y apellido del usuario autenticado, independientemente del canal utilizado para crear la cuenta.
- **Resultado actual / bug**: Tras crear la cuenta por API y hacer login por UI, el banner muestra nombre y apellido completos. Tras completar el registro directamente por UI, muestra únicamente el nombre.
- **Código de referencia**: [test_hibrido.py](../../tests/02-Automatizados/AutomationExercise/test/test_hibrido.py).
- **Hipótesis técnica**: La primera fase del registro web, que recibe solo nombre y email, podría crear la sesión con esos datos parciales. La segunda fase actualiza el perfil, pero no refresca el banner; un login posterior sí construye el mensaje con los datos completos.
- **Notas**: La diferencia se descubrió al comparar capturas de Allure de los dos tests híbridos. No se afirma la hipótesis sin inspeccionar el código de la aplicación, pero el comportamiento es reproducible y los tests se adaptan a él.
- **Lección aprendida**: Los tests híbridos UI + API permiten detectar inconsistencias que permanecen ocultas al probar cada capa de forma aislada.

## Observaciones generales
- **Popups dinámicos**: El caso más complejo de AutomationExercise no es un bug de la app, sino la interferencia de un elemento externo que requiere un guard fallback en el suite.
- **Flexibilidad del carrito**: El diseño de los page objects con listas de IDs y verificaciones por producto mejora la mantenibilidad.
- **Caso de mayor riesgo**: AE-003 es el motivo principal del flaky test 13 y debe considerarse un caso de prueba de estabilidad del entorno más que una falla funcional de aplicación.
- **Contrato de API**: AE-004, AE-005 y AE-006 muestran que una API debe validarse por su contrato real de respuesta, no solo por el status HTTP ni por la igualdad literal de nombres.
- **Integración entre capas**: AE-007 y AE-008 evidencian que UI y API pueden representar la misma acción de negocio de forma diferente y que los tests híbridos ayudan a encontrar inconsistencias entre ambas.

## Conclusiones de la sesión
- La comparación automatizada de estructuras entre dos respuestas de API requiere mapeos explícitos de nombres de campo.
- Los métodos de Page Object deben aceptar parámetros opcionales con valores por defecto para reutilizarse con datos fijos y con datos dinámicos generados durante los tests híbridos.
- Un hallazgo de comportamiento inconsistente aporta valor al portfolio porque demuestra capacidad de diagnóstico, no solo ejecución de tests.

## Recomendaciones para el suite
- Añadir una función `cerrar_popup()` con retries y detección de varios patrones, incluido `google_vignette`.
- Marcar el test 13 como flaky en el informe y documentar la causa raíz externa.
- Mantener los casos de carrito como flujo flexible, de modo que no dependan de IDs de producto fijos si la página cambia.

## Allure y reporting mejorado
- Se implementó en `conftest.py` un fixture `attach_screenshot()` que captura pantalla tras un fallo de test y la adjunta al reporte de Allure.
- Esto permite tener evidencia visual inmediata de los errores, especialmente útil para casos flaky como `google_vignette`.
- Fragmento de código de referencia:
```python
@pytest.fixture(autouse=True)
def attach_screenshot(page, request):
    yield
    if request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
```
- Esta implementación mejora la trazabilidad y ayuda a diagnosticar fallos de UI en los reportes generados por Allure.

