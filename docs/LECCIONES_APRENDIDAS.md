# Lecciones Aprendidas

Esta seccion acumula parte del conocimiento clave de QA en el desarrollo de software.
No es estrictamente "lo mas importante", sino lo mas util para mi aprendizaje personal.

### Diaro de Aprendizaje QA - ISTQB

- En este diario documentare mi aprendizaje de ISTQB con mas frecuencia, añadiendo apuntes, temario estudiado y estado del aprendizaje. 


## Conceptos aprendidos y apuntes interesantes

```text
SDLC (Software Development Life Cycle)
    ├─ Quality Assurance (QA)
        ├─ Quality Control (QC)
            ├─ Testing
                ├─ Depuración
```

## -----------------------------------------

*ERROR ---> DEFECTO ---> FALLA (BUG)* *ANOMALIA*
- Un "error" (humano) produce "defectos" en las funciones, lo cual resulta en "fallos" visible en el software, lo cual es un "bug".
- Un "defecto" es un error en el código que puede o no causar una falla. Un "fallo" es la manifestación visible de un defecto cuando se ejecuta el software.
- Un "bug" es un término coloquial para referirse a cualquier defecto o falla en el software.
- Una "anomalía" es cualquier comportamiento inesperado que no necesariamente es un error, pero que puede indicar un problema potencial.

## -----------------------------------------
- *Ley de Pareto*: el 80% de los fallos son en el 20% de los casos de prueba."Una pequeña minoria de acciones genera la mayoria de los efectos."
- *Paradoja del Pesticida*: Los test pieden efectividad con las repeticiones. Es necesario adaptarlos a cada caso, aun si la modificación es minima.
- **Principio de Pruebas Tempranas**: Es mas facil y barato testear en etapas tempranas de desarrollo. Los test muestran bugs, no su ausencia. No hay pruebas "perfectas" ni sistemas 100% limpios.

## -----------------------------------------

**Buenas practicas y requisitos deseables**:
- Conocimientos tecnicos, de testing y de dominio. KRS
- Pensamiento critico, curiosidad y atención al detalle.
- Comunicación clara y concisa.
- Tener siempre en cuenta el negocio y el cliente final.
- Tener muy en cuenta la ciberseguridad. 

## -----------------------------------------

# 🧠 Concepto Clarificado: Regla de Bloqueo vs. Prioridad

*Fecha: [12/04/2026]*
- **Situación:** Test con dependencias/prioridades.  
- **Regla:** Primero se respeta la dependencia (orden de ejecución), luego aplica prioridad entre opciones paralelas.
- **Explicación:** Una dependencia existe cuando Test B necesita que Test A se complete primero (ej: no puedes probar "combate" sin antes probar "crear personaje"). Eso es obligatorio. Pero si tienes Tests C, D, E que son independientes entre sí, entonces sí aplicas prioridad para decidir cuál ejecutar primero.
- **Nota Personal:** No todos los tests tienen el mismo peso —los unitarios independientes son más flexibles en priorización que los de integración con dependencias forzadas. Primero, comprueba dependencias entre pruebas. Si hubiera pruebas en paralelo, aplicar prioridad.

## 1. Definición y Propósito

- La **Ejecución de Pruebas** bajo estrategias de dependencia prioriza la integridad del flujo lógico sobre el tiempo de ejecución. Este patrón establece una jerarquía en la planificación de pruebas:
- Primero se garantiza la **completitud lógica** (dependencias forzadas).
- Posteriormente se aplica **optimización de recursos** (prioridad entre casos independientes).
- Este enfoque es crítico para evitar fallos en cascada (*failures*) que ocurran al ejecutar tests que dependen de estados previos no validados.

## 2. Fundamento Técnico (Arquitectura)

### Bloqueo por Dependencia (Blocking Rules)
- Existe una dependencia estricta cuando un caso de prueba requiere la preparación o el resultado de otro previamente.
    **Ejemplo:** Validar `Combate` (Test B) requiere que `Crear Personaje` (Test A) haya completado correctamente antes de ejecutarse.
    **Implicación:** El Test B está bloqueado hasta que el estado del sistema se establezca tras el Test A.

### Prioridad entre Opciones Paralelas (Prioritization Rules)
- Cuando existen casos independientes (sin dependencias mutuas), la estrategia de ejecución optimiza el orden basándose en:
    **Riesgo:** ¿Cuál falla con mayor impacto?
    **Valor de Negocio:** ¿Cuál valida requisitos críticos primero?
    **Tiempo:** ¿Cuál es más rápido para obtener feedback temprano?

### Flexibilidad por Tipo de Prueba
- **Unitarios:** Alta flexibilidad en priorización y ejecución independiente.
- **Integración/Aceptación:** Baja flexibilidad; el orden suele ser obligatorio para validar flujos de integración.

## 3. Relación con CTFL y Pensamiento Crítico

| Dimensión | Explicación Didáctica para QA |
| :--- | :--- |
| **Planificación** | Definir el *Test Schedule* considerando dependencias técnicas del sistema (ej: base de datos, estado inicial). |
| **Diseño de Pruebas** | Identificar precondiciones necesarias en los casos antes de escribirlos. |
| **Gestión de Riesgos** | Asignar prioridad a pruebas que cubran funcionalidades críticas si los tiempos son limitados. |
| **Trazabilidad** | Mapear qué tests requieren el estado específico resultante de otros tests para auditoría. |

## 4. Ejemplo Conceptual (Flujo Lógico)
```text
[ESTRUCTURA DE EJECUCIÓN]
-------------------------
// Bloqueo Obligatorio (Fase 1)
Test A: [Crear Personaje]    -> Estado Inicial
      ↓ (Depende de éxito anterior)
Test B: [Realizar Combate]    -> Requiere personaje activo
// Paralelo Independiente (Fase 2)
Test C: [Probar UI Botón X]   -> Sin dependencias con A/B
Test D: [Validar Login]       -> Independiente entre sí
Test E: [Chequear Logs]       -> Independiente entre sí

[REGLA DE ÓRDEN]
----------------
1. Ejecutar Bloque Obligatorio (A → B) en orden secuencial estricto.
2. Dentro del bloque independiente {C, D, E}, aplicar prioridad según riesgo/tiempo.
```
----

## 🧠 Lección: Complejidad Ciclomática

*Fecha: [10/04/2026]*  
**Categoría:** QA Avanzado / White Box Testing  
**Relación con Examen:** ISTQB (Fundamentos & Análisis)  

## 1. El Mapa: Grafo de Flujo de Control (CFG)
- Para probar bien, necesitamos saber **cómo viaja el control** por dentro del código. Esto es lo que llamamos "Caja Blanca".
- Un CFG es una representación gráfica de un programa. En el CFG, se representan los **nodos**, las **aristas** y el **camino** de ejecución.

---
| **Concepto** | **Descripción** | **Ejemplo** |
|-------------------|-----------------------------------------------|-------------------------------------------|
| **Nodos** | Puntos de acción (instrucciones, decisiones). | Bloques de código (if, print). |
| **Aristas** | Vías de conexión. | Las flechas que van del Nodo 1 al Nodo 2. |
| **Camino (Path)** | Secuencia lineal desde inicio hasta fin. | Una ruta específica de ejecución. |

> **Reflexión:** Imaginar el código como un mapa ayuda a ver "dónde están los atajos" y "qué rutas son las más largas".


## 2. La Métrica: Complejidad Ciclomática de McCabe
Este es el número mágico que dice **cuánto esfuerzo** necesitamos para probar la función. No se trata de líneas de código, sino de **decisiones lógicas**.

### La Regla de Oro (Simplificada)
Aunque existen fórmulas complejas con aristas y nodos ($V_G = E - N + 2$), la regla mental para el examen es:
*Complejidad* = *Número de Decisiones* + *1* 
**Decisión:** Cualquier estructura que ramifique (IF, CASE, DO-WHILE).
**+1:** Por el camino base por defecto.

------------------------------------------------------------------------------------------------------------------

## 🧠 Lección: Caja Blanca vs Gris vs Negra - Diferencias Clave

*Fecha: [11/04/2026]*  
**Categoría:** Fundamentos de Testing 

## 🎭 Definición Visual (Acceso al Código)

---

| Tipo | Nivel de Acceso | ¿Qué "ve"? | Quién lo hace típicamente |
|------|-----------------|------------|---------------------------|
| **Caja Negra** | 🔴 CERO (0%) | SOLO entradas y salidas. No sé CÓMO funciona dentro. | QA funcional / Testing manual de usuario |
| **Caja Gris** | 🟡 ALGUNOS (30-50%) | Ve partes del código, pero no todo el sistema completo. | QA que colabora con dev (análisis de APIs) |
| **Caja Blanca** | 🔷 TOTAL (100%) | VEO TODO el código interno y la lógica. | QA Dev / Ingeniero QA automatizado |

---
## 📋 Tabla Comparativa Detallada

---

| Criterio | Caja Negra | Caja Gris | Caja Blanca |
|----------|------------|-----------|-------------|
| **Visibilidad del código** | ❌ NO veo nada | ⚠️ Veo partes selectivas | ✅ VEO TODO |
| **Cobertura de prueba** | Estructura/Comportamiento | Hibrido estructural + funcional | Estructural (Decisiones, ramas) |
| **Herramientas típicas** | Selenium, TestRail | Proxy API, Postman con headers de debug | SonarQube, JUnit/Coverage tools |
| **Costo/Tiempo** | ✅ Bajo | 🟡 Medio | ❌ Alto (más difícil diseñar) |
| **Ejemplo Real** | Usuario final probando login desde una app web | QA recibe tokens de API para pruebas específicas | QA revisa código antes de testear (estática + dinámica) |

---
## 🧩 Analogía: La Caja Misteriosa 📦

Imagina que te dan una caja con dos botones (A y B) y un panel LED que enciende o no.

---

| Tipo | ¿Qué puedes hacer? |
|------|--------------------|
| **Negra** | Pulsas A → LED ON / Pulsas B → LED OFF. No abres la caja para ver circuitos. |
| **Gris** | Ves parcialmente el interior: ves que hay un micro-controlador, pero no las rutas exactas del código. |
| **Blanca** | Abres la caja y lees cada línea de código: `IF (A) THEN LED=ON`. Sabes qué líneas cubrir en tu test. |

---
## 🎯 ¿Para qué sirve cada una en el examen?

### ✏️ Caja Negra (Pregunta tipo "Diseña casos")
- **Objetivo:** Probar la funcionalidad desde la perspectiva del usuario.
- **Ejemplo ISTQB:** "Proponer 5 casos para login con datos válidos e inválidos".
- **Clave:** No necesitas saber el código, solo entradas → salidas.

### ✏️ Caja Gris (Pregunta tipo "API Testing")
- **Objetivo:** Probar usando información parcial de la infraestructura (ej: conocer headers de API pero no el backend completo).
- **Ejemplo ISTQB:** "Probar un endpoint POST `/api/user` con datos validados por contrato OpenAPI".
- **Clave:** Sabes *algo* del interior, pero no todo.

### ✏️ Caja Blanca (Pregunta tipo "Cobertura de decisión")
- **Objetivo:** Cubrir cada línea, rama y decisión lógica (como la pregunta 157 que vimos).
- **Ejemplo ISTQB:** "Diseñar casos para lograr 100% cobertura de ramas en una función con IF/ELSE".
- **Clave:** Conoces el código, necesitas cubrir todas las rutas.

## Mi Reflexión Personal

**Lo que entendí hoy:**  
- No hay "mejor" técnica, depende de *qué quiero probar* y *quién lo hace*.  
- **Caja Negra:** Útil cuando soy un tester funcional sin acceso a código.  
- **Caja Gris:** El punto medio ideal para QA que trabaja con devs (APIs + UI).  
- **Caja Blanca:** Esencial si quiero automatizar tests estructurales o revisar código propio.

**Lo que me preocupa para el examen:**  
- A veces los exámenes piden "diseño de pruebas en Caja Gris" y no lo especifican claramente. Tengo que leer bien si dan acceso a APIs parciales.
- Recordar que **no necesito saber código para Caja Negra**, pero sí lógica de negocio.

**Plan de estudio:**  
1. Practicar 5 casos por técnica (ej: login, búsqueda, reportes).  
2. Identificar qué tipo sería un examen ISTQB según el prompt.  
3. No confundir "Caja Gris" con "Blanca total" —eso es una trampa común.

---

## 🧠 Lección: Code Coverage para Pruebas Automatizadas

*Fecha: [12/04/2026]*  
**Categoría:** Fundamentos de Testing 

## 1. Definición y Propósito

- La **Code Coverage** es una métrica de calidad que mide qué proporción del código fuente está siendo ejecutada durante las pruebas automatizadas. Es parte fundamental de los estándares **ISTQB CTFL** para garantizar la integridad y robustez del software.
- Este enfoque mejora el **rendimiento** y la **trazabilidad** del sistema, permitiendo identificar áreas no cubiertas por casos de prueba activos.

## 2. Fundamento Técnico (Arquitectura)

### Cobertura de Sentencia (Statement Coverage)
- Mide qué porcentaje de las líneas de código han sido ejecutadas al menos una vez. Es la métrica más básica pero no garantiza que se prueben todas las condiciones lógicas.

### Cobertura de Decisión (Decision Coverage)
- También conocida como *Branch Coverage*, mide si cada rama condicional (`if`, `else`, `case`) ha sido evaluada por Verdadero y Falso. Garantiza que la lógica de decisión sea completamente validada.

### Cobertura de Condición (Condition Coverage)
- Evalúa las condiciones dentro de los expresiones booleanas complejas (ej: `if age > 18 and status == "active"`). Asegura que cada componente lógico de una condición haya sido probado individualmente.

### Cobertura de Camino (Path Coverage)
- Analiza todas las combinaciones posibles de rutas a través del código condicional. Es la más exhaustiva pero también la más costosa en términos de esfuerzo y tiempo.

### Cobertura de Negocio (Business Coverage)
- Mide qué porcentaje de los requisitos de negocio o reglas de negocio están siendo validados por las pruebas. Es la métrica estratégica que alinea pruebas con objetivos de valor del producto.

---

## 3. Relación con CTFL y Pensamiento Crítico
| Dimensión | Explicación Didáctica para QA |
| :--- | :--- |
| **Diseño de Pruebas** | Las coberturas definen los criterios de aceptación automática (Entry Criteria). |
| **Calidad del Código** | Identifica código no probado que representa deuda técnica o riesgo oculto. |
| **Trazabilidad** | Vincula Requisitos -> Casos -> Cobertura de Sentencia/Decisión para auditoría. |
| **Robustez** | Reduce el riesgo de fallos críticos en áreas con 0% de cobertura activa. |

## 4. Ejemplo Conceptual (Esqueleto Lógico)
```text
[Código Fuente]
--------------
if user.age > 18:           # Cobertura Condición (TRUE)
    if has_license:         # Cobertura Decisión (TRUE/FALSE necesaria)
        process_user()      # Sentencia ejecutada
else:                        # Cobertura Decisión (FALSE)
    reject_registration()   # Sentencia ejecutada
```
---

## 🧠 Lección: Page Object Model (POM) para Pruebas Automatizadas

*Fecha: [12/04/2026]*  
**Categoría:** Fundamentos Avanzados de Testing (Not yet)

# 1. Definición y Propósito
- El **Page Object Model (POM)** es un patrón de diseño de prueba, reconocido por el estándar **ISTQB**, que promueve la separación entre:
- La **representación** de los elementos de una página/pantalla.
- El **comportamiento** o acción a ejecutar sobre esos elementos.
- Este enfoque mejora el **rendimiento** y la **trazabilidad** del sistema, permitiendo mantener la estructura de la aplicación encapsulada dentro de clases específicas para cada página.

## 2. Fundamento Técnico (Arquitectura)
### Encapsulamiento
- La ubicación, los IDs y los métodos de interacción se agrupan en una clase única (ej: `LoginPage`). Un cambio en la UI solo requiere modificar esa clase, sin afectar todo el script de prueba.
### Reutilización
- Los elementos de la página no se replican repetidamente; son referenciados por su nombre lógico dentro del framework de prueba.
### Independencia
- El caso de prueba (lógica) no depende de la estructura interna del código de la aplicación, lo cual reduce el acoplamiento y mejora la robustez ante cambios menores.

## 3. Relación con CTFL y Pensamiento Crítico
| Dimensión | Explicación Didáctica para QA |
| :--- | :--- |
| **Diseño de Pruebas** | El POM es un modelo de alto nivel que demuestra cómo estructurar pruebas complejas (Sistemas). |
| **Calidad del Código** | Reduce la duplicación de código (*DRY*), clave para métricas de calidad. |
| **Trazabilidad** | Permite rastrear claramente qué elementos de UI están siendo probados en cada caso, vinculando Requisito -> Caso -> Elemento UI. |
| **Robustez** | Mitiga el riesgo de fragilidad (tests que fallan por cambios menores en la app). |

## 4. Ejemplo Conceptual (Esqueleto Lógico)
```text
[CLASE: PaginaLogin]
---------------------
+ loginEmail = 'Input Email'       # Elemento
+ loginPassword = 'Input Pass'    # Elemento
+ botonesCargar = 'Button Login'  # Acción

+ ingresar_credenciales(email)   # Método de interacción
+ validar_error_generado()       # Método de validación
```

---

###### 🧠 Lección: Un flag con dos responsabilidades es un bug esperando pasar

*Fecha: [16/04/2026]*  
**Categoría:** QA Práctico / Diseño de Software  
**Relacionado con:** CT-009, CT-011 (TLDRDC)

Cuando el flag `_en_combate` controlaba tanto *bloquear botones fuera de combate* como *decidir si actualizar sprites*, parecía correcto.
Pero en cuanto se corrigió el primer bug (CT-009), el segundo apareció (CT-011): los sprites dejaron de actualizarse fuera de combate porque el mismo flag los bloqueaba.
**Lección:** Un solo flag que hace dos cosas distintas es una deuda técnica. Cuando se parchea uno de sus efectos, el otro se rompe.  
**Solución aplicada:** Separar responsabilidades: `_en_combate` solo bloquea interacción, los callbacks reactivos (`root.after(0, cb)`) actualizan la UI independientemente del estado de combate.  
**Señal de alerta en testing:** Si al corregir un bug aparece otro en un área aparentemente no relacionada, sospecha de un flag o variable con doble responsabilidad.

---

###### 🧠 Lección: Antes de delegar a la IA, necesitas saber qué le estás pidiendo

*Fecha: [16/04/2026]*  
**Categoría:** QA Práctico / Trabajo con IA  
**Relacionado con:** CT-010 (TLDRDC)
Al implementar sprites en botones Canvas (CT-010), se intentó delegar la implementación completa a la IA sin conocer Tkinter/PIL. El resultado fue código que no funcionaba, referencias incorrectas a la arquitectura real del proyecto, y tiempo perdido depurando suposiciones.
**Lección:** La IA puede ayudarte a implementar, pero no puede sustituir el conocimiento técnico mínimo del dominio.  
**Lo que funcionó:** Hacer backup, estudiar la API de PIL/ImageTk mínima necesaria, luego sí usar la IA para estructurar el código con ese contexto.  
**Aplicación a testing:** Lo mismo vale para automatización. Antes de pedir a la IA un test de Selenium, conviene entender qué hace `find_element` y cuándo puede fallar. De lo contrario, el test pasa en local y falla en CI sin saber por qué.

---

###### 🧠 Lección: Thread-safety en UI — nunca toques widgets desde un hilo secundario

*Fecha: [16/04/2026]*  
**Categoría:** QA Técnico / Arquitectura Tkinter  
**Relacionado con:** CT-011 (TLDRDC)
TLDRDC usa dos hilos: el hilo Tkinter (UI) y un hilo worker (lógica del juego). Actualizar un widget directamente desde el hilo worker causa condiciones de carrera silenciosas — la UI no lanza error, simplemente no se actualiza o se corrompe en momentos aleatorios.
**Solución aplicada:** `root.after(0, callback)` programa la ejecución del callback en el hilo de Tkinter, garantizando que la UI solo se toca desde el hilo correcto.  
**Patrón general:** En cualquier framework con event loop (Tkinter, Qt, Android, etc.) la regla es la misma — la UI solo se modifica desde el hilo principal.  
**Implicación para testing:** Un bug de threading puede no reproducirse en cada ejecución. Si un test de UI falla de forma intermitente sin causa aparente, el primer sospechoso es una actualización de widget fuera del hilo principal.

---

## 🧠 Lección: Estándares ISO y su rol en el marco ISTQB

*Fecha: [17/04/2026]*  
**Categoría:** Fundamentos Teóricos / Estándares Internacionales  
**Relación con Examen:** ISTQB CTFL — Vocabulario, Técnicas y Procesos
Los estándares no son "burocracia": son el respaldo normativo detrás de cada definición del glosario ISTQB. Saber qué estándar define qué término ayuda a responder preguntas de examen con precisión y a entender *por qué* las cosas se definen así.

## 1. Mapa de Estándares — "¿Qué ISO hace qué?"
| Estándar | Función dentro de ISTQB |
| :--- | :--- |
| **ISO 25010** | Características de calidad del *producto*: funcionalidad, fiabilidad, usabilidad, mantenibilidad, portabilidad... |
| **ISO 24765** | Vocabulario general de ingeniería de software. Es el "diccionario maestro" detrás de términos como *defecto*, *anomalía*, *criterios de aceptación*. |
| **ISO 29119** | Estándares específicos de pruebas: procesos, técnicas y pruebas de IA. Dividido en partes (ver sección 2). |
| **ISO 20246** | Revisiones de productos de trabajo: inspecciones, revisiones formales, guiadas y basadas en roles. |
| **ISO 9241** | Ergonomía e interacción humano-sistema. Base para términos de usabilidad y diseño centrado en la persona. |
| **ISO 26262** | Seguridad funcional en automoción. Define el NISFA (Nivel de Integridad de Seguridad Física del Automóvil). |
| **NIST.IR.7298** | Seguridad de la información. Fuente para términos de ciberseguridad: ataque, ingeniería social, descifrado. |
| **IEEE 1028** | Revisiones técnicas formales. Complementa a ISO 20246 en ese ámbito. |
| **CMMI** | Mejora de procesos. Referencia para modelos de madurez y análisis de causa raíz. |

## 2. ISO 29119 — Todas las partes relevantes
```text
ISO 29119
    ├─ Parte 1 — Conceptos y definiciones
    │       (condición de prueba, plan de prueba, prueba basada en riesgo,
    │        criterios de entrada/salida, nivel de prueba)
    ├─ Parte 2 — Procesos de prueba
    │       (gestión del proceso, planificación, monitoreo y control,
    │        diseño, implementación, ejecución, cierre)
    ├─ Parte 3 — Documentación de prueba
    │       (estructura del plan de prueba, especificación de casos,
    │        informe de progreso, informe de resumen)
    ├─ Parte 4 — Técnicas de diseño
    │       (prueba de a pares, flujo de control, partición de equivalencia,
    │        valores límite, tabla de decisión)
    └─ Parte 11 — Pruebas de Inteligencia Artificial
            (ejemplos adversos, pruebas metamórficas, entornos virtuales,
             sesgo de datos, robustez del modelo)
```

> **Nota para el examen:** Las partes 1, 4 y 11 son las más citadas en preguntas de vocabulario y técnicas. La parte 2 aparece en preguntas sobre *procesos* y la parte 3 en preguntas sobre *documentación*.

## 3. Términos clave agrupados por estándar

### ISO 25010 — Calidad del producto
- **Adecuación funcional**: grado en que el sistema satisface necesidades explícitas e implícitas.
- **Fiabilidad**: capacidad de funcionar correctamente bajo condiciones específicas durante un período.
- **Disponibilidad**: grado en que el sistema está operativo y accesible cuando se requiere.
- **Adaptabilidad**: grado en que puede adaptarse a distintos entornos, hardware o plataformas.
- **Instalabilidad**: capacidad de ser instalado o desinstalado correctamente en un entorno específico.
- **Interoperabilidad**: grado en que dos sistemas pueden intercambiar y usar información.
- **Mantenibilidad**: facilidad de modificación por quien tiene ese rol previsto.
- **Portabilidad**: capacidad de transferirse de un entorno a otro.
- **No repudio**: capacidad de demostrar que una acción o evento ha tenido lugar y no puede ser negado.
- **Responsabilidad** *(Accountability)*: capacidad de rastrear acciones hasta la entidad que las realizó.
- **Capacidad de recuperación**: grado en que el sistema reanuda operación normal tras una interrupción.
### ISO 24765 — Vocabulario general (diccionario maestro)
- **Defecto**: imperfección o deficiencia en un producto de trabajo que puede causar que el producto no cumpla sus requisitos.
- **Anomalía**: cualquier condición que se desvía de lo esperado; no necesariamente un error confirmado.
- **Análisis de impacto**: evaluación de los cambios identificados en la documentación, código y pruebas.
- **Aseguramiento de la calidad (QA)**: proceso orientado a garantizar que los productos cumplan los requisitos de calidad.
- **Bitácora de prueba**: registro cronológico de los detalles relevantes de la ejecución de pruebas.
- **Criterios de aceptación**: condiciones que deben cumplirse para que un componente sea aceptado.
- **Gestión de la calidad**: actividades coordinadas para dirigir y controlar la calidad en una organización.
- **Ciclo de vida del software (SDLC)**: marco que describe los procesos, actividades y tareas del desarrollo de software.
### ISO 29119 — Procesos y técnicas de prueba
- **Condición de prueba**: aspecto de un componente susceptible de ser probado.
- **Criterios de entrada/salida**: condiciones que deben cumplirse para iniciar o finalizar una actividad de prueba.
- **Resultado esperado**: comportamiento previsto observable basado en la base de prueba.
- **Prueba metamórfica**: técnica donde entradas y resultados se extrapolan de un caso previo que ha pasado.
- **Relación metamórfica**: descripción de cómo un cambio en la entrada afecta al cambio en la salida esperada.
### ISO 20246 — Revisiones
- **Inspección**: revisión formal con roles definidos y métricas para identificar defectos.
- **Revisión guiada**: el autor guía al equipo a través del producto para identificar problemas.
- **Revisión técnica**: realizada por expertos para examinar calidad y discrepancias respecto a estándares.
- **Revisión ad hoc**: revisión informal sin preparación previa ni proceso estructurado.
- **Revisión basada en roles**: los revisores adoptan perspectivas específicas (usuario, mantenedor, etc.).
- **Revisión basada en escenarios**: los revisores siguen escenarios de uso definidos para guiar su análisis.
### ISO 9241 — Usabilidad y experiencia de usuario
- **Usabilidad**: grado en que un sistema puede ser usado por usuarios específicos para lograr objetivos con eficacia, eficiencia y satisfacción.
- **Efectividad**: precisión y completitud con que los usuarios logran objetivos específicos.
- **Diseño centrado en la persona**: proceso de desarrollo que coloca al usuario en el centro de las decisiones.
- **Experiencia de usuario (UX)**: percepciones y respuestas del usuario resultantes del uso de un sistema.
### NIST.IR.7298 — Seguridad
- **Ingeniería social**: intento de engañar a alguien para que revele información confidencial.
- **Ataque contra la seguridad**: intento de acceso no autorizado o compromiso de la integridad del sistema.
- **Descifrado de contraseña**: proceso de recuperar contraseñas desde datos almacenados o transmitidos.

## 4. Estándares de nicho — para no confundirlos
| Estándar | Ámbito específico | Trampa de examen |
| :--- | :--- | :--- |
| **ISO 26262** | Seguridad funcional *en automoción* (NISFA) | No confundir con **IEC 61508**, que es la versión genérica de seguridad funcional para sistemas eléctricos. ISO 26262 *deriva* de IEC 61508 pero es específica para vehículos. |
| **CMMI** | Modelos de madurez y mejora de procesos | No es un estándar ISO/IEC. Es un modelo de referencia para medir y mejorar la capacidad de los procesos de una organización. |

## 5. Tabla de autoevaluación rápida

| Pregunta | Respuesta |
| :--- | :--- |
| ¿Qué estándar define "Mantenibilidad" y "Adecuación Funcional"? | **ISO 25010** |
| ¿Qué estándar se cita para Revisión Formal e Inspección? | **ISO 20246** |
| ¿De dónde vienen "Defecto", "Anomalía" y "Análisis de Impacto"? | **ISO 24765** |
| ¿Qué parte de ISO 29119 cubre pruebas de IA? | **ISO 29119-11** |
| ¿Qué parte de ISO 29119 cubre documentación de prueba? | **ISO 29119-3** |
| ¿Qué estándar es base para pruebas de UX/usabilidad? | **ISO 9241-210** |
| ¿Qué estándar define el NISFA (automoción)? | **ISO 26262** |
| ¿Qué diferencia hay entre ISO 26262 e IEC 61508? | ISO 26262 es la versión automotriz de IEC 61508 (genérica) |
| ¿Qué estándar cubre "criterios de aceptación" y "ciclo de vida"? | **ISO 24765** |
| ¿Qué estándar cubre "revisión ad hoc" y "revisión basada en roles"? | **ISO 20246** |

## Mi Reflexión Personal
**Lo que entendí:**
- Antes veía los estándares como nombres de fondo. Ahora entiendo que cada definición del glosario ISTQB tiene una *fuente normativa* concreta, y conocerla ayuda a no confundir términos en el examen.
- ISO 24765 es el vocabulario base; ISO 25010 habla de *qué* calidad medir; ISO 29119 habla de *cómo* probar.
- ISO 9241 es el que respalda todo lo relacionado con UX — si una pregunta menciona "satisfacción del usuario" o "diseño centrado en la persona", el estándar detrás es este.
**Trampas frecuentes en examen:**
- Confundir **ISO 20246 con IEEE 1028**: ambos hablan de revisiones, pero el glosario ISTQB usa ISO 20246 para inspecciones y revisiones formales. IEEE 1028 es específico de la *revisión técnica* formal.
- Confundir **ISO 26262 con IEC 61508**: la segunda es la base genérica, la primera es su derivado automotriz. En preguntas de automoción, la respuesta correcta es ISO 26262.
- Confundir **ISO 24765 con ISO 25010** para términos como "calidad": ISO 24765 define el *vocabulario* general; ISO 25010 define las *características* medibles de calidad del producto.

-------------------------------------------------------------------------------

## 🧠 Lección: Primer análisis de Complejidad Ciclomática sobre TLDRDC con Lizard

*Fecha: [17/04/2026]*  
**Categoría:** QA Práctico / Análisis Estático  
**Herramienta:** Lizard (analizador estático de complejidad)  
**Relación con Examen:** ISTQB CTFL — White Box Testing, Gestión de Riesgos
Este fue el primer análisis real de complejidad ciclomática sobre un proyecto propio. El proceso fue completamente automático — Lizard lee el código sin ejecutarlo y sin modificarlo, y devuelve métricas por función.

## 1. ¿Qué mide Lizard exactamente?
Lizard analiza el código fuente y calcula por cada función:
| Columna | Significado |
| :--- | :--- |
| **NLOC** *(Non-comment Lines of Code — líneas de código sin contar comentarios)* | Tamaño real de la función |
| **CCN** *(Cyclomatic Complexity Number — número de complejidad ciclomática)* | Cuántos caminos independientes existen dentro de la función |
| **token** | Número de unidades sintácticas (palabras clave, operadores...) |
| **PARAM** | Número de parámetros que recibe la función |
| **length** | Líneas totales incluyendo comentarios y espacios |
El número más importante para nosotros es **CCN**: indica cuántos **CT** *(Case Test — Casos de Prueba)* serían necesarios *como mínimo* para recorrer todos los caminos posibles de esa función.

## 2. Escala de riesgo
| CCN | Nivel | Significado práctico |
| :--- | :--- | :--- |
| 1–5 | 🟢 Simple | Fácil de probar, pocas ramas |
| 6–10 | 🟡 Moderada | Requiere atención |
| 11–20 | 🟠 Alta | Difícil cubrir completamente |
| +20 | 🔴 Peligrosa | Muy difícil de probar; candidata a refactorizar |
| >50 | 🚨 Crítica | Prácticamente imposible de cubrir con pruebas manuales |
| >100 | 💀 Monolito | Deuda técnica severa; difícil de mantener y probar |
| >200 | ☠️ Apocalíptica | Código que probablemente necesite ser reescrito desde cero |

## 3. Resultados del análisis sobre TLDRDC

**Resumen general:**
- **317 funciones** analizadas en total
- **18 warnings** (funciones con CCN > 15 o longitud > 1000 líneas)
- **CCN promedio: 6.2** — moderado-alto para el proyecto completo

**Funciones en zona de peligro (warnings reales):**
| Función | CCN | NLOC | Interpretación |
| :--- | :--- | :--- | :--- |
| `_explorar_paso` | **208** | 1290 | Prácticamente todo el juego vive aquí — el monolito |
| `resolver_eventos_post_combate` | **60** | 463 | Lógica post-combate enorme, difícil de aislar |
| `turno_jugador` | **31** | 136 | Core del combate, alto riesgo |
| `aplicar_evento` | **28** | 85 | Ya cubierto parcialmente con CTs existentes |
| `enemigo_aleatorio` | **27** | 147 | Cada tipo de enemigo es una rama diferente |
| `ejecutar_habilidad_activa` | **19** | 114 | Cada habilidad del juego es un path distinto |
| `validar_habilidad` | **17** | 64 | Validaciones encadenadas |
| `_planificar_efectos` | **16** | 77 | Lógica de efectos de combate |
| `actualizar_botones_combate` | **16** | 94 | UI reactiva con muchas condiciones |

## 4. El hallazgo más importante: `_explorar_paso` con CCN 208
Un CCN de **208** significa que, teóricamente, harían falta **208 CTs distintos** solo para cubrir todos los caminos de esa función. Eso es prácticamente imposible en testing manual.
Pero lo que esto revela no es solo "hay muchos paths" — es la confirmación técnica de que el juego es un **monolito**: una sola función gigante que contiene la lógica de exploración, combate, eventos, narrativa, UI y estado del personaje todo junto.

```text
Monolito = una función que hace demasiadas cosas
         = CCN artificialmente alto
         = difícil de probar en aislamiento
         = cuando falla, difícil saber exactamente por qué
```

Esto no significa que el código esté mal escrito en términos de lógica — significa que está organizado de una manera que complica el testing. Es una deuda técnica, no un bug.

## 5. ¿Qué hacer con esta información?
No hay que cubrir los 208 paths de `_explorar_paso`. La estrategia práctica es:

**Priorizar por riesgo real**, no por CCN máximo:
| Prioridad | Función | Por qué |
| :--- | :--- | :--- |
| 🔴 Alta | `aplicar_evento` (CCN 28) | Ya hay CTs sobre ella — ampliar cobertura |
| 🔴 Alta | `turno_jugador` (CCN 31) | Core del combate, cualquier bug aquí es crítico |
| 🟠 Media | `ejecutar_habilidad_activa` (CCN 19) | Muchas habilidades sin CTs documentados |
| 🟠 Media | `enemigo_aleatorio` (CCN 27) | Cada enemigo es un path — ¿se generan todos correctamente? |
| 🟡 Baja | `_explorar_paso` (CCN 208) | Imposible cubrir completamente; enfocar en los sub-flujos conocidos |

## 6. Diferencia clave que aprendí aquí
Antes de hacer este análisis no tenía claro que **complejidad ciclomática** y **code coverage** son dos cosas distintas que se complementan:

| Concepto | Herramienta | Te dice... |
| :--- | :--- | :--- |
| **Complejidad ciclomática** | Lizard, Radon | Cuántos paths *existen* en el código |
| **Code coverage** *(cobertura de código)* | coverage.py | Cuáles paths se *ejecutaron* durante una prueba |

Lizard te da el mapa. Coverage te dice por dónde caminaste en el mapa.

## Mi Reflexión Personal
**Lo más sorprendente:**  
CCN 208 en `_explorar_paso`. Sabía que era un monolito, pero verlo en número hace que el concepto de "deuda técnica" deje de ser abstracto. "Debo" mucho más de lo que creía ^^u
**Lo más útil:**  
La tabla de warnings. En 10 segundos lizard me dijo dónde están las 18 funciones de mayor riesgo del proyecto — información que habría tardado horas en obtener leyendo el código manualmente.
**Lo que cambió en mi forma de pensar los CTs:**  
Un CT no es solo "probar que algo funciona" — es diseñar la entrada que fuerza al código a tomar un path específico. CCN me dice cuántos paths hay; mis CTs deben intentar cubrir los más críticos.

**Comando usado:**
```bash
lizard "ruta/al/codigo" --sort cyclomatic_complexity -l python
```
- `--sort cyclomatic_complexity` → ordena los resultados de menor a mayor CCN
- `-l python` → analiza solo archivos Python

---

## 📝 Apuntes de Estudio CTFL — P.M.A.D.I.E.C. (Procesos y Actividades de Prueba)

*Fecha: [22/04/2026] — Transcritos de cuaderno físico*

### 1️⃣ PLANIFICACIÓN

- **Definir Objetivos:**Basándose en las expectativas del usuario, buscamos objetivos claros para definir qué características se probarán y la mejor manera de hacerlo.
- **Identificar Riesgos:** Buscamos qué posibles riesgos puedan surgir durante las siguientes fases.
- **Establecer Estrategia:** Sabiendo objetivos y riesgos, se planifica cómo se actuará.
- **Determinar Restricciones:** Pueden ser varias: económicas, de tiempo, tamaño de personal, software...
**Conceptos Clave:**
- **Criterios de Entrada →** Son las condiciones que se deben cumplir para poder empezar a probar (Ej: que el código está listo). Se define en Planificación.
- **Criterios de Salida →** Son los matices que indican cuándo podemos probar (Ej: cobertura 100%). Se definen en Planificación pero se evalúan después.
- **Estimación →** Tiempo, costo y personal necesarios.
- **Trazabilidad →** Requisitos → Casos → Resultados.
- **Plan de Prueba →** Producto Final de la fase Planificación.

### 2️⃣ MONITOREO Y CONTROL

- **Seguimiento del Progreso:** Con Afinamos a Objetivos.
- **Vigilancia de Desviaciones:** Se comunica el seguimiento de la Estrategia y la Gestión de Riesgos.
- **Control:** Si hay desviaciones, se aplican Acciones Correctivas o Ajuste de Expectativas, según el caso.
- **Real VS Planificado:** Adhesión a Criterios Sólida.
**Conceptos Clave:**
- **Control →** Brazo ejecutor de Monitorizar. Aplica Acciones Correctivas o Ajuste de Expectativas.
- **Informe de Avance →** Producto Final de esta etapa. Se produce varios veces, visto que M/C es continuo.

### 3️⃣ ANÁLISIS DE PRUEBAS

- **Analizar Base de Índice:** Documentación "Base de Pruebas para diseñar pruebas a través con requisitos".
- **Identificar Datos de Prueba:** Combinamos las Bases de Prueba con los casos. Importa la Pruebas en sus versiones y test hilados esperados para concretar qué datos son importantes.
- **Estimar:** Estimación de tiempo, costo y recursos necesarios.
- **Definiciones de Prueba Clara:** Fijar qué es error/fallo y definiciones de Prueba para establecer criterios sólidos.
- **Trazabilidad Bidireccional:** Relación Requisitos con Casos y con Resultados, para utr rieles definitivos.
**Conceptos Clave:**
- **Trazabilidad →** Durante el análisis de las Bases de Prueba, se debe determinar si los requisitos se pueden testear.

### 4️⃣ DISEÑO DE PRUEBAS

- **Caso Prueba Alto Nivel:** Con toda la documentación generada, podemos comenzar a definir casos, sin especificaciones concretas, pero necesarios para la correcta estructura de Pruebas.
- **Identificar Datos de Prueba:** Combinamos las Bases de Prueba con los casos de Alto Nivel, y así se concreta qué datos son importantes.
- **Diseñar Entorno e Infraestructura:** Con los datos de Pruebas identificados, podemos empacarlos en Frameworks y herramientas concretas.
- **Priorizar Escenarios:** Con definidos, se preparan casos específicos, basados en Prioridades del Negocio.
**Conceptos Clave:**
- **Trazabilidad entre Condiciones y Casos →** Garantiza Pruebas efectivas y representativas.

### 5️⃣ IMPLEMENTACIÓN

- **Procedimientos y Scripts:** Se crean guiones/scripts detallados, y se prioriza el orden de ejecución para maximizar la eficiencia.
- **Crear Suites:** Agrupar los Datos en packs lógicos.
- **Preparar Datos:** Se transforman las Pruebas Alto Nivel en Pruebas Bajo Nivel, combinando los datos necesarios.
- **Verificar Entorno:** Comprobación final que revisa que Infraestructura, herramientas y datos son correctos.
- **Script:** Doc con pasos de Prueba/Calendario Ejecución: cronograma de Prueba: Pruebas Bajo Nivel / que define orden de Suites Concretos.

### 6️⃣ EJECUCIÓN

- **Ejecución Manual o Automática:** Se ejecutan los Suites siguiendo el Calendario y los Scripts.
- **Computar Resultados:** Se verifica el comportamiento del software en base a lo establecido en Diseño.
- **Registrar Anomalías e Informar Defectos:** Si hay discrepancias en el comportamiento, se documenta como Incidente, detallando pasos e impacto.
- **Re-testing y Regresión:** Se repiten las Pruebas que fallaron (Re-testing) y se prueban áreas no modificadas para evitar efectos secundarios (Regresión).
**Conceptos Clave:**
- **Incidente/Defecto →** Discrepancia entre Resultado Real y Esperado.
- **Log de Pruebas →** Reporte aclaratorio que verifica detalles de qué se ejecutó, quién y resultado (paso/fallo).

### 7️⃣ COMPLECIÓN (Finalización y Cierre)

- **Evaluar Criterios de Salida:** Verificar resultados y registrar si se ejecutaron Eventos, Objetivos de forma para saber si hemos probado suficiente.
- **Test Summary:** Generar reporte final que resuma actividades y resultados, para que los interesados valoren el proyecto.
- **Finalizar/Archivar Textuario:** Organizar y guardar todo el material de Prueba e Infraestructura para su reutilización.
- **Lecciones Aprendidas:** Analizar tiempo y esfuerzos del equipo para mejora continua en cada ciclo.

---


