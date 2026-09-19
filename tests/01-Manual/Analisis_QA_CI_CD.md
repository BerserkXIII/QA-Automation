# Análisis QA CI/CD con GitHub Actions

## Descripción
Este documento recoge el análisis del proceso de implementación de pipelines de integración continua para las cuatro suites automatizadas del portfolio: AutomationExercise, SauceDemo, ReqRes y GoRest. Se documentan la separación de ejecuciones mediante filtros de rutas, la gestión de credenciales y los problemas de configuración descubiertos durante la puesta en marcha.

*Fecha de última actualización:* 19/09/2026

## Contexto
La primera configuración de GitHub Actions ejecutaba los cuatro pipelines ante cualquier `push` o `pull_request` relevante para `main`. Aunque las suites estaban separadas por proyecto, el disparador común provocaba ejecuciones innecesarias: un cambio en un solo playground podía iniciar también las pruebas de los otros tres.

La solución consistió en mantener un workflow independiente por proyecto y restringir sus eventos mediante el filtro `paths` del bloque `on:`. Cada pipeline instala sus dependencias en un runner Linux limpio y ejecuta únicamente la suite que le corresponde.

## Casos de prueba importantes

### CI-001: Desacoplamiento de los cuatro pipelines por proyecto
- **ID**: CI-001
- **Descripción**: Verificar que AutomationExercise, SauceDemo, ReqRes y GoRest se ejecutan de forma independiente cuando cambia únicamente el contenido de su propia carpeta.
- **Severidad**: MEDIA
  - Razón: Una configuración acoplada no impide necesariamente validar el código, pero consume recursos y ralentiza la retroalimentación.
  - Impacto: Se ejecutaban pruebas no relacionadas y se gastaban minutos de GitHub Actions sin aportar información sobre el cambio realizado.
  - Reproducibilidad: Alta si los workflows no filtran las rutas modificadas.
- **Precondiciones**:
  - Repositorio conectado a GitHub Actions.
  - Los cuatro workflows disponibles en `.github/workflows/`.
  - Rama `main` configurada como destino de `push` y `pull_request`.
- **Pasos**:
  1. Modificar un archivo dentro de `tests/02-Automatizados/AutomationExercise/`.
  2. Crear un `push` o `pull_request` hacia `main`.
  3. Revisar los workflows iniciados en GitHub Actions.
  4. Repetir la comprobación modificando únicamente `Pruebas-saucedemo`, `API-ReqRes` y `API-GoRest`.
  5. Modificar, como control, uno de los archivos de workflow.
- **Resultado esperado**: Solo se ejecuta el pipeline cuyo directorio de proyecto contiene cambios. Si se modifica un workflow, se ejecuta el pipeline correspondiente a ese archivo.
- **Resultado actual / solución**: Cada workflow declara en `push.paths` y `pull_request.paths` su propia carpeta y su propio archivo YAML:
  - `tests-automationexercise.yml` apunta a `tests/02-Automatizados/AutomationExercise/**`.
  - `test_saucedemo.yml` apunta a `tests/02-Automatizados/Pruebas-saucedemo/**`.
  - `test_reqres.yml` apunta a `tests/02-Automatizados/API-ReqRes/**`.
  - `test_gorest.yml` apunta a `tests/02-Automatizados/API-GoRest/**`.
- **Causa raíz**: El disparador inicial no distinguía qué parte del repositorio había cambiado.
- **Solución implementada**: Se desacoplaron los workflows con filtros `paths` específicos para cada proyecto y para el propio workflow. Así, una modificación aislada no dispara las otras tres suites.
- **Código de referencia**:
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'tests/02-Automatizados/API-ReqRes/**'
      - '.github/workflows/test_reqres.yml'
  pull_request:
    branches: [main]
    paths:
      - 'tests/02-Automatizados/API-ReqRes/**'
      - '.github/workflows/test_reqres.yml'
```
- **Lección aprendida**: Separar las suites en workflows no basta; también hay que separar sus condiciones de entrada. Un filtro de rutas bien definido reduce el tiempo de espera y el consumo de minutos sin perder cobertura relevante.

### CI-002: Gestión segura de credenciales para ReqRes y GoRest
- **ID**: CI-002
- **Descripción**: Verificar que las credenciales de las APIs no se almacenan en el repositorio y que llegan a los tests tanto en local como en CI.
- **Severidad**: ALTA
  - Razón: Exponer una API key o un token puede permitir usos no autorizados y comprometer la trazabilidad de las pruebas.
  - Impacto: Riesgo de seguridad, revocación de credenciales y fallos de autenticación en los pipelines.
  - Reproducibilidad: Alta cuando una credencial se escribe directamente en un archivo versionado o no se configura en GitHub.
- **Precondiciones**: Dependencias de `python-dotenv` instaladas localmente y secretos `REQRES_API_KEY` y `GOREST_TOKEN` configurados en GitHub.
- **Pasos**:
  1. Configurar las credenciales en el `.env` local de cada proyecto de API.
  2. Confirmar que `.env` está ignorado por Git y no forma parte del commit.
  3. Crear en GitHub los Secrets `REQRES_API_KEY` y `GOREST_TOKEN` con solo el valor de cada credencial.
  4. Revisar el bloque `env:` del workflow correspondiente.
  5. Ejecutar el pipeline y comprobar únicamente que la variable llega, por ejemplo mediante su longitud, sin imprimir el secreto.
- **Resultado esperado**: El código obtiene las credenciales desde variables de entorno. Localmente se cargan desde `.env`; en producción, desde GitHub Secrets. Ningún valor secreto aparece en el repositorio ni en los logs.
- **Resultado actual / solución**: ReqRes usa `REQRES_API_KEY: ${{ secrets.REQRES_API_KEY }}` y GoRest usa `GOREST_TOKEN: ${{ secrets.GOREST_TOKEN }}` dentro de `env:` a nivel del job. Los archivos `.env` quedan fuera del control de versiones.
- **Causa raíz**: Las pruebas de API necesitan autenticación, pero una credencial no debe formar parte del código ni de la configuración pública del pipeline.
- **Solución implementada**: Se separó la configuración sensible del código mediante `.env` local y GitHub Secrets en CI. El pipeline inyecta los valores como variables de entorno y el código los lee con `os.getenv()`.
- **Lección aprendida**: La misma suite debe poder ejecutarse localmente y en CI sin duplicar código ni transportar secretos al repositorio. La configuración sensible pertenece al entorno de ejecución.

### CI-003: Secret mal copiado y caracteres invisibles en tokens
- **ID**: CI-003
- **Descripción**: Analizar el fallo de autenticación producido por un secret copiado con el nombre de la variable, espacios o saltos de línea invisibles.
- **Severidad**: ALTA
  - Razón: El pipeline puede fallar con mensajes poco descriptivos aunque la variable exista y parezca estar configurada.
  - Impacto: Errores `InvalidHeader`, respuestas `401` o mensajes `Invalid token`, dificultando distinguir una credencial incorrecta de un problema de código.
  - Reproducibilidad: Alta cuando se pega `REQRES_API_KEY=valor` o `GOREST_TOKEN=valor` en lugar de pegar solo el valor.
- **Precondiciones**: Secret configurado en GitHub o variable cargada desde `.env`, y un test que realice una petición autenticada.
- **Pasos**:
  1. Copiar una credencial incluyendo accidentalmente el nombre de la variable, espacios o un salto de línea.
  2. Ejecutar el test autenticado.
  3. Observar el error devuelto por la librería HTTP o por la API.
  4. Revisar la longitud de la variable sin imprimir su contenido.
  5. Leer el token aplicando limpieza de espacios en los extremos y repetir la prueba.
- **Resultado esperado**: El valor se interpreta como una credencial limpia y la petición autenticada funciona. El diagnóstico no expone el secreto en consola.
- **Resultado actual / problema**: El valor contaminado produce fallos en silencio o errores genéricos como `InvalidHeader`, `401` o `Invalid token`. La variable puede existir y tener una longitud distinta, por lo que el problema no siempre se identifica mirando solo el nombre del secret.
- **Causa raíz**: El contenido de la variable no era exactamente el token esperado; incluía el nombre de la variable o caracteres de formato introducidos durante el copiado.
- **Solución implementada**: Se añadió `.strip()` al leer los tokens desde las variables de entorno. También se documentó comprobar la longitud de la variable, sin mostrar nunca el valor completo.
- **Código de referencia**:
```python
api_key = os.getenv("REQRES_API_KEY", "").strip()
token = os.getenv("GOREST_TOKEN", "").strip()
```
- **Lección aprendida**: Que un secret esté definido no garantiza que su contenido sea válido. La normalización en el punto de lectura y un diagnóstico que no revele credenciales reducen el tiempo de investigación sin comprometer la seguridad.

### CI-004: Matching exacto de nombres en filtros `paths`
- **ID**: CI-004
- **Descripción**: Verificar que las rutas declaradas en los workflows coinciden exactamente con los nombres reales de carpetas y archivos.
- **Severidad**: MEDIA
  - Razón: Un error de nomenclatura puede impedir que el pipeline se dispare aunque el cambio sea válido.
  - Impacto: El cambio llega a la rama sin la validación automática esperada y GitHub no muestra un error explícito que señale el carácter incorrecto.
  - Reproducibilidad: Alta ante cualquier diferencia entre `-` y `_`, mayúsculas o el nombre real del archivo.
- **Precondiciones**: Workflow con un filtro `paths` y una carpeta cuyo nombre contiene guiones o guiones bajos.
- **Pasos**:
  1. Comparar el nombre real del directorio o workflow con cada entrada de `paths`.
  2. Confirmar especialmente los caracteres `-` y `_`.
  3. Modificar un archivo de la ruta correcta y abrir un `push` o `pull_request`.
  4. Observar si el workflow aparece como ejecutado o si queda omitido.
  5. Corregir la ruta si no coincide y repetir la comprobación.
- **Resultado esperado**: El workflow se activa cuando la ruta modificada coincide exactamente con el patrón declarado.
- **Resultado actual / problema**: Los caracteres `-` y `_` no son intercambiables en el matching de `paths`. Un único desajuste impide reconocer el archivo y no genera un error explícito de configuración.
- **Causa raíz**: La ruta del filtro se escribió con una nomenclatura distinta a la del sistema de archivos o del propio workflow.
- **Solución implementada**: Se verificaron los nombres reales y se mantuvieron coincidencias exactas, por ejemplo `API-ReqRes`, `API-GoRest` y `test_saucedemo.yml`.
- **Lección aprendida**: Los filtros de GitHub Actions deben validarse como rutas literales. Un detalle visual pequeño en el nombre puede cambiar completamente el comportamiento del pipeline sin producir un mensaje de error evidente.

## Observaciones generales
- **Desacoplamiento**: Los cuatro pipelines comparten la misma estrategia de ejecución, pero cada uno responde únicamente a los cambios de su proyecto.
- **Ahorro de recursos**: La configuración evita ejecutar tres suites que no están relacionadas con un cambio, reduciendo consumo de minutos de Actions y ruido en los reportes.
- **Seguridad**: Las API keys de ReqRes y GoRest no deben subirse al repositorio. `.env` es una configuración local ignorada por Git y GitHub Secrets es la configuración de producción.
- **Diagnóstico**: Comprobar la longitud de un secreto ayuda a detectar valores mal copiados, pero nunca se debe imprimir el token completo.
- **Nomenclatura**: Los nombres de carpetas y workflows forman parte del contrato del filtro `paths`; guiones y guiones bajos deben conservarse exactamente.

## Recomendaciones para la suite
1. Mantener un workflow por proyecto para conservar responsabilidades y diagnósticos aislados.
2. Revisar cada bloque `paths` cuando se renombre una carpeta, un test o un archivo de workflow.
3. Validar localmente que las credenciales se leen desde `.env` y en CI que llegan desde GitHub Secrets, sin incluir valores sensibles en logs.
4. Conservar `.strip()` en la lectura de tokens y documentar los errores de autenticación esperables.
5. Usar los badges del README junto con el historial de Actions para comprobar el estado de cada pipeline.

## Conclusiones de la sesión
La implementación convirtió una ejecución global y costosa en cuatro pipelines independientes, con disparadores alineados con la carpeta de cada proyecto. La separación de credenciales permite mantener el mismo código entre local y CI sin publicar información sensible. Los problemas más instructivos no estuvieron solo en pytest, sino también en la configuración del entorno: un token con caracteres invisibles y una ruta con un guion incorrecto pueden producir fallos silenciosos o difíciles de interpretar.
