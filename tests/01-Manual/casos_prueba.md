# Casos de Prueba Manuales

## Descripción
Ejercicios prácticos de validación y verificación basados en ISTQB-CTFL.
El objeto de practica sera "TLDRDC", un repositorio propio de un juego de combate en consola.
Analizare los casos de prueba que he realizado para "TLDRDC", aplicando el metodo de ISTQB-CTFL.
El objetivo es analizar de manera profesional y con fundamento los casos de prueba que he realizado a lo largo del tiempo para mejorar, encontrar bugs y corregir "TLDRDC". A pesar de que he trabajado mucho con IA en "TLDRDC"", he utilizado ciertas tecnicas de QA sin saberlo, y analizar mis propias buenas/malas practicas y profesionalizarlas.
Los ejemplos son casos reales, pero no estructurados de ninguna manera, puesto que el proceso de "TLDRDC" fue bastante caotico. Voy recuperando las estructuras y codigos que he utilizado y analizandolos sobre la marcha, con el fin de realizar este ejercicio teorico.

## Ejemplo de Estructura de un Caso de Prueba
- **ID**: Identificador único
- **Descripción**: Qué se prueba
- **Precondiciones**: Estado inicial requerido
- **Pasos**: Acciones a ejecutar
- **Resultado esperado**: Qué debería pasar
- **Resultado actual**: Qué pasó realmente
- **Causa raíz**: Que pasa realmente
- **Solución implementada**: Que solución se implementó
- **Estado**: Pasado/Fallido/Bloqueado

## Casos de Prueba 

### CT-001: Problema de flujo de comabates en "Eventos"
- **ID**: CT-001
- **Descripción**: El juego da por terminado un "Evento" a pesar de huir de un combate generado por ese "Evento".
- **Precondiciones**: Una ramificacion de un "Evento" que termine en combate y conseguir "huir" del combate.
- **Pasos**:
1. Iniciar juego
2. Seleccionar evento X
3. Elegir opción que lleva a combate
4. Terminar combate con "huir"
5. Observar si retorna a "Exploración"
- **Resultado actual**: Cuando se huye de un combate generado por un "Evento", el juego retorna a "Exploración" como si hubiera ganado el combate, ganando recompensas y nivel. Fallo "ludonarrativo".
- **Resultado esperado**: Se puede huir de un combate generado por un "Evento", y el evento termina y se retorna a "Exploración" sin los beneficios de ganar el combate, como si el personaje hubiera huido del "Evento" entero.
- **Causa raíz**: La accion de "huir" en combate tiene un flag para termina el combate, eso es correcto. Sin embargo, no hay flag para que "Evento" detecte la huida, con lo cual seguia el "Evento" de manera normal.
- **Solución implementada**: Se añadio un flag dentro de "Eventos" para que el detecte el uso de "huir" en combate, y en consonancia, "Evento" termine al mismo tiempo que combate, y retorne al flujo previsto sin ganar beneficios.
- **Estado**: Fixed. 
- **Notas**: En este caso, encontre el bug en una sesion de debugging, dandome cuenta del error narrativo de conseguir beneficios sin ganar el combate. Itere con Copilot sobre el codigo de combate, teniendo claro que habia que vincular la huida y el flag de terminar el combate con otro flag analogo para los eventos. Gracias a la IA fue facil encontrar el "hueco" donde colocar ese flag, y corregir el error de decenas de combates mal hechos de una solo sesion de debugging.
- **Complejidad**: Baja (patrón análogo ya implementado, solo tuve que vincularlos)
- **Lección aprendida**: Reconocer patrones similares aceleró significativamente la resolución, y al no tener mucha complejidad sintatica, me resulto sencillo identificarlos. 

---

*Última actualización: [07/04/2026]*
