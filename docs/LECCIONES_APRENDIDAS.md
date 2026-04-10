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

# 🧠 Lección: Caja Blanca y Complejidad Ciclomática

**Fecha:** 10/04/2026  
**Categoría:** QA Avanzado / White Box Testing  
**Relación con Examen:** ISTQB (Fundamentos & Análisis)  

## 1. El Mapa: Grafo de Flujo de Control (CFG)
Para probar bien, necesitamos saber **cómo viaja el control** por dentro del código. Esto es lo que llamamos "Caja Blanca".
Un CFG es una representación gráfica de un programa. En el CFG, se representan los **nodos**, las **aristas** y el **camino** de ejecución.

| **Concepto**      | **Descripción**                               | **Ejemplo**                               |
| **Nodos**         | Puntos de acción (instrucciones, decisiones). | Bloques de código (`if`, `print`).        |
| **Aristas**       | Vías de conexión.                             | Las flechas que van del Nodo 1 al Nodo 2. |
| **Camino (Path)** | Secuencia lineal desde inicio hasta fin.      | Una ruta específica de ejecución.         |

> **Reflexión:** Imaginar el código como un mapa ayuda a ver "dónde están los atajos" y "qué rutas son las más largas".

## 2. La Métrica: Complejidad Ciclomática de McCabe
Este es el número mágico que dice **cuánto esfuerzo** necesitamos para probar la función. No se trata de líneas de código, sino de **decisiones lógicas**.

### La Regla de Oro (Simplificada)
Aunque existen fórmulas complejas con aristas y nodos ($V_G = E - N + 2$), la regla mental para el examen es:
*Complejidad* = *Número de Decisiones* + *1* 
**Decisión:** Cualquier estructura que ramifique (IF, CASE, DO-WHILE).
**+1:** Por el camino base por defecto.



