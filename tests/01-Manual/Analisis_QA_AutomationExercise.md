# Análisis QA AutomationExercise

## Descripción
Este documento recoge los casos de prueba manuales y los hallazgos más importantes del ejercicio AutomationExercise. Se incluyen los problemas detectados en el popup `google_vignette`, la automatización del carrito y la validación del cierre del popup inicial.

*Fecha de última actualización:* 05/08/2026

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

## Observaciones generales
- **Popups dinámicos**: El caso más complejo de AutomationExercise no es un bug de la app, sino la interferencia de un elemento externo que requiere un guard fallback en el suite.
- **Flexibilidad del carrito**: El diseño de los page objects con listas de IDs y verificaciones por producto mejora la mantenibilidad.
- **Caso de mayor riesgo**: AE-003 es el motivo principal del flaky test 13 y debe considerarse un caso de prueba de estabilidad del entorno más que una falla funcional de aplicación.

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

