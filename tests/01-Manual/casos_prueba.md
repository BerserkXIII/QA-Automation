# Casos de Prueba Manuales

## Descripción
Ejercicios prácticos de validación y verificación basados en ISTQB-CTFL.
El objeto de practica sera "TLDRDC", un repositorio propio de un juego de combate en consola.
Analizare los casos de prueba que he realizado para "TLDRDC", aplicando el metodo de ISTQB-CTFL.
El objetivo es analizar de manera profesional y con fundamento los casos de prueba que he realizado a lo largo del tiempo para mejorar, encontrar bugs y corregir "TLDRDC". A pesar de que he trabajado mucho con IA en "TLDRDC"", he utilizado ciertas tecnicas de QA sin saberlo, y analizar mis propias buenas/malas practicas y profesionalizarlas.
Los ejemplos son casos reales, pero no estructurados de ninguna manera, puesto que el proceso de "TLDRDC" fue bastante caotico. Voy recuperando las estructuras y codigos que he utilizado y analizandolos sobre la marcha, con el fin de realizar este ejercicio teorico.

*Fecha de ultima actualizacion:* 10/04/2026

## Ejemplo de Estructura de un Caso de Prueba
- **ID**: Identificador único
- **Descripción**: Qué se prueba
- **Severidad**: ALTA / MEDIA / BAJAciones**: Estado inicial requerido
- **Pasos**: Acciones a ejecutar
- **Resultado actual**: Qué pasó realmente
- **Resultado esperado**: Qué debería pasar
- **Causa raíz**: Que pasa realmente
- **Solución implementada**: Que solución se implementó
- **Estado**: Pasado/Fallido/Bloqueado
- **Notas**: Notas adicionales
- **Complejidad**: Lo dificil que me resulto llegar a una solución.
- **Lección aprendida**: Que aprendí a traves de la solución o del propio caso.

## Casos de Prueba 

### CT-001: Problema de flujo de comabates en "Eventos"
- **ID**: CT-001
- **Descripción**: El juego da los beneficios de terminar un "Evento" a pesar de huir de un combate generado por ese "Evento".
- **Severidad**: MEDIA / BAJA
  - Razón: Beneficios sin combate
  - Impacto: es un exploit del sistema de combate.
  - Reproducibilidad: 60%, se necesita activar un evento donde pueda haber combate.
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

-------------------------------------------------------------------------------------------------------------------------------

### CT-002: Problema de control de comportamiento de botones
- **ID**: CT-002
- **Severidad**: ALTA / CRÍTICA
  - Razón: Afecta la jugabilidad en combate (núcleo del juego)
  - Impacto: Hace que el juego sea "antiintuitivo"
  - Reproducibilidad: 100% (siempre ocurre cada combate)
- **Descripción**: El comportamiento de los botones de combate antiintuitivo: se activaba la Stance pero el toggle no se mostraba activo, las armas no se mostraban debidamente, etc.
- **Precondiciones**: Ninguna, el bug se mostraba en combate siempre, con mas problemas contra mas armas tenias.
- **Pasos**:
1. Iniciar juego
2. Llegar a una pantalla de combate
   (Puede ser: evento aleatorio, o combate forzoso en escena específica)
3. Observar el estado INICIAL del toggle (debería estar en OFF)
4. Click en botón "Esquivar" (o la stance que sea)
5. Observar:
   - ¿El toggle visualmente cambió a ON?
   - ¿El juego aplicó "esquivar" como acción?
   - ¿Después del turno del enemigo, el toggle sigue en ON?
6. Click en botón de arma para atacar
7. Observar:
   - ¿El sprite del arma sigue visible?
   - ¿El juego aplicó "atacar" con el arma correcta?
- **Resultado actual**: 
- Al clickar en "Esquivar": La acción se ejecuta correctamente (mensaje de esquivar en consola)
- PERO el botón visualmente muestra estado OFF (no presionado)
- Al cambiar a "Bloquear": Ambos botones aparecen OFF
- Al cambiar de arma: Los sprites desaparecen y aparece [ARMA_NOMBRE]
- **Resultado esperado**: El toggle de Stance refleja el estado real, actuando como un switch: si activas "esquivar", desactivas "bloquear", y viceversa. Las armas deben aparecer con sus sprites, sin nombre/placeholder. 
- **Causa raíz**: Muy mala estructura en los paneles y botones de Tkinter. Trabajo hecho por la IA por falta de conocimiento sintactico, lo cual provocaba muy mal flujo de trabajo, y dado que en combate hay muchas funciones cruzadas, es imposible de mantener los botones "funcionales" sin una estructura correcta.
- **Solución implementada**: Limpieza total del sistema de botones. Hice trabajo de iteracion con IA, para encontrar puntos criticos en el codigo y limpiar los placeholders, para lo cual cree iamgenes para todas las armas, implementadolas en lugar de los placeholders que solo mostraban nombres de armas. Pidiendole a la IA especificaciones y documentacion del sistema de botones consegui crear uno mas sencillo y funcional, el cual pude modulizar para mejorar el funcionamiento, lo cual fue muy util, pues pude usar la logica para implementar un sistema donde los sprites se vinculaban al diccionario de "jugador", haciendo el sistema de sprites "instantaneo". El toggle de los botones fue mas costoso, tuve que buscar documentación oficial de Tkinter para entederlo bien, y junto a la documentación especifica del caso de prueba, pude encontrar una solución consistente y funcional, a traves de pedirle a la IA que encontrara los puntos criticos del comportamiento de los botones, creando flags pre-combate, post-turno jugador para un comportamiento correcto del toggle, y reestructurando el sistema interno de esquiva/bloqueo, evitando así que cualquier cambio de stats o armas pudiera resultar en bug.
- **Estado**: Fixed.
- **Notas**: Fue de los bugs mas dificiles de resolver, sobretodo por mi falta de conocimiento sintactico y el fallo garrafal de delegar demasiado en la IA sin entender lo que estaba haciendo. De hecho, tengo una version "muerta" en ese punto, la cual se rompio sin remedio por mala praxis con la IA.
- **Complejidad**: Alta. Mi falta de experiencia y la "animosidad" por implementar el sistema hicieron que confiara demasiado en la IA. A pesar de los promps precisos, los retest, las comprobaciones y las iteraciones, no se debe confiar a nivel estructural algo tan delicado a la IA. Al menos no sin conocimientos sintacticos del lenguaje/biblioteca.
- **Lección aprendida**: Conocer y entender el comportamiento de una biblioteca es fundamental. Nunca delegar puntos criticos a la IA. Lo que creia que avanzaba en una noche, luego tarde dias en arreglarlo. E incluso llegando a hacer un backup, por acumulación de bugs. Aprendí a las malas los "limites", o usos indevido de la IA.

------------------------------------------------------------------------------------------------------------------------------------

## CT-003: Error de referencia en las armas
- **ID**: CT-003
- **Descripción**: Al conseguir ciertas armas, el juego da un error de "Arma desconocida!", haciendo que no se agrege al inventario y "deshabilitando" esa arma durante toda la partida.
- **Severidad**: Media/Alta
  - Razón: Afecta la jugabilidad en combate, lo limita mucho.
  - Impacto: Hace que ciertas armas sean inaccesibles, a pesar de estar implementadas.
  - Reproducibilidad: 50%, se necesita conseguir ciertas armas para ver el error.
- **Precondiciones**: 
  - Juego iniciado
  - Activar evento que ofrezca la opción de conseguir armas
  - Armas afectadas: Hoz de Sangre, Hoja de la Noche, Hacha Maldita, Mano de Dios, estoque, cimitarra. El resto no se ven afectadas.
- **Pasos**: 
1. Iniciar juego
2. Terminar un evento con posibilidad de conseguir una arma.
3. Llegar a la decisión de conseguir armas
   -Sí hay espacio en el inventario, se agregara el arma automaticamente.
   -Sí no, se debe elegir arma para sustituir.
- **Resultado actual**: 
   -Sí hay hueco en el inventario, se agrega el arma automaticamente.
   -Sí no, el juego pregunta que arma sustituir por la nueva.
      (Aqui el bug no se muestra si el jugador elige "no" sustituir una de sus armas por la nueva.)
   -Sí el arma nueva es una de las afectadas, el juego muestra un error de "Arma desconocida!". 
   -El juego continua de manera normal, pero limitado a ciertas armas, haciendolo bastante dificil y bloqueando cierto eventos activables por ciertas armas.
- **Resultado esperado**: Poder conseguir todas las armas del juego sin problematicas, añadiendose o sustituyendose correctamente segun el caso.
- **Causa raíz**: Mala nomenclatura y referenciado de los nombres clave de las armas. 
- **Solución implementada**: Revision de todos los nombres de armas, y todos los eventos donde se consiguen. Gracias al soporte de la IA, se pudo encontrar todas las referencias mal escritas y corregirlas. Esto soluciona el problema cuando hay hueco en el inventario. Pero para poder sustituir correctamente las armas al encontrar una nueva, hubo que crear un diccionario de abreviaturas, para poder sustituir y activar las armas correctamente. Asi, da igual que el jugador escriba "espada", "esp" o incluso que se equivoque, se sustituye correctamente o repregunta.
- **Estado**: Fixed.
- **Notas**: Fue un ejemplo de necesidad de uniformidad en variables y terminos. Gracias a Copilot, fue relativamente sencillo encontrar todos los puntos donde se referenciaban erroneamente las armas y estandarizarlos para que sean consistentes.
- **Complejidad**: Media. La IA hizo el trabajo pesado de navegar por el codigo en busca de los terminos mal escritos, y retestear que esten todos corregidos. El fix en sí no era dificil, eran simples cambios ortograficos, y sobretodo, mayusculas.
- **Lección aprendida**: Las mayusculas importan, y mucho! Buscar siempre la consistencia y uniformidad en las variables. La implementacion del diccionario ayudo a mejorar el sistema de combate tambien, y permite añadir nuevas armas sin problemas. De un bug se puede sacar un feat!


-----------------------------------------------------------------------------------------------------------------------------------

## CT-004: Rediseño de Botones con forma libre
- **ID**: CT-004
- **Descripción**: Migración del sistema de botones estándar a un sistema modular basado en Canvas para permitir formas libres, integración de PIL para escalado multi-monitor y activación dinámica mediante Toggle.
- **Severidad**: MEDIA
   -Razón: Complejidad técnica implementada vs impacto en UX (fue una iteración intencional).
   -Impacto: Arquitectura UI más flexible e independiente del contenido (sprites intercambiables).
   -Reproducibilidad: 100%, tras iterar y validar el ajuste de escalado.
- **Precondiciones**: Entorno Python instalado con librería Tkinter base definida y panel UI inicial configurado en modo estándar.
- **Pasos**: 
   1.Iniciar entorno Tkinter y configurar paneles base.
   2.Implementar botones estándar como prototipo inicial.
   3.Iterar hacia el reemplazo por elementos Canvas con formas libres (free-form).
   4.Integrar lógica de Toggle debajo del Canvas para activar desactivar acciones.
   5.Validar ajuste automático de contenido (sprites) escalando según tamaño del canvas.
   6.Escalar toggle dinámicamente para ajustarse al área máxima, dejando margen a tolerancia de esquinas irregulares.
- **Resultado actual**: El sistema permite botones con formas irregulares sin romper el layout original, permitiendo contenido independiente. Se logra la activación correcta en la mayoría de áreas; algunas esquinas no tenían toggle inicialmente, pero fue considerado un bug menor aceptable para avanzar rápido con recursos visuales pendientes.
- **Resultado esperado**: Un sistema donde las formas de los botones no estén limitadas a rectángulos rígidos, contenido (sprites) sea intercambiable y autoajustado, y el toggle respete la geometría del diseño sin deformar visualmente la interfaz crítica.
- **Fundamentación técnica**: Tkinter nativo carecía de soporte para formas libres complejas, limitando la estética y uso de espacios irregulares. La solución implementada consistió en encapsular la lógica en Canvas (superposición) y utilizar PIL para escalar imágenes dinámicamente, evitando distorsiones en diversos monitores.
- **Solución implementada**: Se migró el flujo usando "placeholders" temporales hasta obtener los PNG finales, se documentó a la IA para obtener medidas exactas en pixeles de los sprites pequeños (costoso pero preciso) y se vinculó el toggle con la geometría del canvas.
- **Estado**: Implemented / Verificado.
- **Notas**: Este caso es una mejora de arquitectura/funcionalidad, no un "bug", por lo que la Severidad fue clasificada como MEDIA para reflejar la dificultad técnica alta y el tiempo invertido en iterar hasta cubrir las necesidades (diseño vs funcionalidad). Se detectó brechas menores en esquinas irregulares, aceptadas bajo el principio de entrega incremental. La colaboración con IA fue clave para calcular aproximaciones de píxeles en imágenes pequeñas y entender la librería PIL para escalado multi-monitor sin redimensionar assets manuales.
- **Complejidad**: Media (requirió integración externa: Canvas + PIL, lógica de escalado dinámico).
- **Lección aprendida**: Iterar sobre el diseño arquitectónico (Tkinter → Canvas) permite mayor flexibilidad estética en juegos y apps. Usar IA para validar medidas técnicas (píxeles exactos) es eficiente para optimizar espacios UI cuando los recursos son limitados o pequeños. El equilibrio entre perfección visual absoluta (esquinas con toggle) vs funcionalidad aceptable debe decidirse según el MVP del proyecto.