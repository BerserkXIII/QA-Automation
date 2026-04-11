# Lecciones Aprendidas

Esta seccion acumula parte del conocimiento clave de QA en el desarrollo de software.
No es estrictamente "lo mas importante", sino 

## Lecciónes aprendidas

------------------------------------------------------------------------------------------------------------------

# 🧠 Concepto Clarificado: Regla de Bloqueo vs. Prioridad

*Fecha: [09/04/2026]*
**Situación:** Test con dependencias/prioridades.  
**Regla:** Primero se respeta la dependencia (orden de ejecución), luego aplica prioridad entre opciones paralelas.
**Explicación:** Una dependencia existe cuando Test B necesita que Test A se complete primero (ej: no puedes probar "combate" sin antes probar "crear personaje"). Eso es obligatorio. Pero si tienes Tests C, D, E que son independientes entre sí, entonces sí aplicas prioridad para decidir cuál ejecutar primero.

**Nota Personal:** No todos los tests tienen el mismo peso —los unitarios independientes son más flexibles en priorización que los de integración con dependencias forzadas. Primero, comprueba dependencias entre pruebas. Si hubiera pruebas en paralelo, aplicar prioridad.

------------------------------------------------------------------------------------------------------------------

# 🧠 Lección: Complejidad Ciclomática

**Fecha:** 10/04/2026  
**Categoría:** QA Avanzado / White Box Testing  
**Relación con Examen:** ISTQB (Fundamentos & Análisis)  

## 1. El Mapa: Grafo de Flujo de Control (CFG)
Para probar bien, necesitamos saber **cómo viaja el control** por dentro del código. Esto es lo que llamamos "Caja Blanca".
Un CFG es una representación gráfica de un programa. En el CFG, se representan los **nodos**, las **aristas** y el **camino** de ejecución.

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

**Fecha:** 11/04/2026  
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

## 🧠 Mi Reflexión Personal

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



