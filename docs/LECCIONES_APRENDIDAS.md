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

# 🧠 Lección: Complejidad Ciclomática

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

# 🧠 Lección: Caja Blanca vs Gris vs Negra - Diferencias Clave

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

# 🧠 Lección: Code Coverage para Pruebas Automatizadas

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

