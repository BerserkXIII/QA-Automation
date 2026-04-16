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

-------------------------------------------------------------------------------------------

### CT-002: Problema de control de comportamiento de botones de Stance en combate
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

-----------------------------------------------------------------------------------------

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


----------------------------------------------------------------------------------

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

-----------------------------------------------------------------------------------------

## CT-005: Implementación del Sistema de Lectura de Input (leer_input)
- **ID**: CT-005
- **Descripción**: Refactorización centralizada de la lógica de entrada de usuario para permitir la coexistencia entre comandos críticos (como "stats") y el flujo principal del juego sin interferencias.
- **Severidad**: MEDIA
   Razón: Complejidad de integración arquitectónica vs impacto funcional positivo.
   Impacto: Elimina bloqueos en inputs originales (derecha/izquierda, sí/no) tras implementación de nuevas funciones.
   Reproducibilidad: Alta al detectar la limitación sintáctica del input() nativo en nodos críticos.
- **Razón**: Complejidad de integración arquitectónica vs impacto funcional positivo.
- **Impacto**: Habilita comando "stats" sin bloqueos en inputs originales (derecha/izquierda, sí/no) tras implementación de nuevas funciones.
- **Precondiciones**: Sistema base con lógica de "stats" definida, pero acoplada a entradas input() directas, y panel UI funcional con decisiones de nodo predefinidas.
- **Pasos**:
   1.Identificar colisión entre comandos del juego (stats) y flujos de navegación (inputs originales).
   2.Detectar limitación sintáctica al intentar leer input sin afectar el flujo de decisión principal.
   3.Consultar IA (Copilot) para refactorizar la lectura hacia una función centralizada leer_input().
   4.Reemplazar todas las llamadas a input() simples por la nueva función encapsulada.
   5.Validar ejecución del comando "stats" en cada posible nodo de decisión.
   6.Verificar que los paths se redireccionen correctamente y retornen a la decisión inicial sin bloqueos.
- **Resultado actual**: La lógica original ha sido centralizada; el comando stats ahora puede ejecutarse en cualquier punto del flujo sin detener las decisiones originales (izquierda/derecha, elecciones de combate). El sistema responde en todos los nodos probados.
- **Resultado esperado**: Un flujo de input unificado donde la lectura sea neutral respecto al contexto (no interfiere con navegación) y permita extensibilidad para futuras funcionalidades sin riesgo de romper paths existentes.
- **Fundamentación técnica**: El input() nativo en Python tenía una restricción de alcance (scope) que limitaba su uso concurrente con las funciones del juego, forzando un redimensionamiento o bloqueos no deseados. La solución requirió encapsular la lectura para aislar el estado de entrada globalmente.
- **Solución implementada**: Se definió la función leer_input() como punto único de entrada (Singleton-like), sustituyendo las llamadas dispersas. Se implementó control estricto para no capturar entradas del jugador en momentos donde el juego requiere navegación fluida.
- **Estado**: Completed / Validated.
- **Notas**: Caso crítico de refactorización impulsado por IA. La limitación original fue sintáctica (acoplamiento de input y lógica), lo cual Copilot ayudó a resolver al proponer la centralización cuando las pruebas manuales no encontraban el patrón óptimo. Se realizaron pruebas de regresión exhaustivas: se probó el comando "stats" en cada nodo del árbol de decisiones para asegurar que ningún path quedaba bloqueado por la nueva función.
- **Complejidad**: Media (Refactorización sin ruptura funcional).
- **Lección aprendida**: Cuando una función simple (input) empieza a colisionar con nuevas necesidades (como stats), refactorizar hacia una API centralizada es más escalable que parchear. La IA fue vital para proponer la abstracción técnica en el momento exacto de la limitación sintáctica, permitiendo avanzar sin bloqueos previos.
- **Codigo implementado**: 
   def leer_input(prompt, personaje):
      while True:
         valor = pedir_input().strip().lower()
         if valor in ["stats", "st", "stat"]:
            mostrar_stats(personaje)
            continue
         separador()
         return valor
**La función encapsula la lectura de input, permitiendo validaciones adicionales sin afectar el flujo principal del juego. Mas adelante, se aprovechara mas esta función para implementar otros comandos críticos.**

-------------------------------------------------------------------------

## CT-006: Implementación de Sistema de Flavor Text Aleatorio
- **ID**: CT-006
- **Descripción**: Integración de la función susurros_aleatorios en nodos críticos para generar contenido narrativo dinámico y evitar repetición constante, añadiendo profundidad al lore sin sobrecargar el código.
- **Severidad**: MEDIA
   Razón: Impacto directo en la experiencia inmersiva (Flavor) y uso de módulos matemáticos (random).
   Impacto: Diversificación del texto narrativo según el contexto del juego.
   Reproducibilidad: Alta (función aislada, lógica clara).
- **Precondiciones**: Nodos de narrativa definidos, función emitir() disponible y motor de juego cargado sin errores de importación.
- **Pasos**:
   Iniciar escena con activación de evento que contiene la llamada a susurros_aleatorios().
   Verificar que se emitan entre 1 y 3 líneas (según random.randint(1, 3)).
   Cambiar entre 5-10 veces el nodo para validar variedad en las cadenas de texto devueltas.
   Confirmar que no interfiere con el flujo principal del combate/exploración tras la emisión.
- **Resultado actual**: La función se ejecuta correctamente, seleccionando aleatoriamente frases de la lista predefinida y emitiendo entre 1 a 3 instancias. No hay bloqueos en el hilo principal.
- **Resultado esperado**: El sistema debe variar el contenido mostrado según el contexto (aleatoriedad efectiva) y respetar la lógica de integración con emitir(), asegurando que cada susurro tenga su impacto narrativo deseado.
- **Fundamentación técnica**: Uso del módulo estándar random para simular variabilidad natural en la experiencia de juego, permitiendo reutilizar una pequeña base de datos de frases sin escribir texto único por cada nodo escénico.
- **Solución implementada**: Se encapsuló la lógica dentro de una función dedicada que controla el volumen (1-3 mensajes) y la selección (random.choice), separando el contenido del texto de la lógica de ejecución del juego.
- **Estado**: Completed / Validated.
- **Notas**: Este caso valida una funcionalidad nueva, no un error. Se comprobó exhaustivamente que la aleatoriedad no era falsa (no se repetían los mismos susurros en cada llamada inmediata sin cambio). El uso de emitir("susurros", ...) centraliza el manejo de audio/texto visual, facilitando futuras modificaciones sin tocar el bucle principal.
- **Complejidad**: Baja (Lógica estándar de Python), pero alto impacto narrativo.
- **Lección aprendida**: Las funciones pequeñas encargadas de "flavor" mejoran significativamente la calidad percibida del juego con muy poco coste técnico. Es vital probar no solo si funciona, sino si la aleatoriedad real aporta variedad y no es predecible a corto plazo.
- **Codigo implementado**:
   def susurros_aleatorios():
      susurros = [
         "'dolor... poder... sangre... herida... abierta...'",
         "'nido... manos... sostienen... abajo... abajo...'",
         "'rey... oculto... pronunciado... no pronuncia...'",
         "'costura... carne... torre... invertida...'",
         ............
      ]
      for _ in range(random.randint(1, 3)):
         emitir("susurros", random.choice(susurros))
**La función encapsula la generación de susurros aleatorios, permitiendo una variedad en el contenido narrativo sin afectar el flujo principal del juego. Simple, pero efectivo.**

-------------------------------------------------------------------------

## CT-007: Expansion de leer_input() para soportar "inputs secretos"
- **ID**: CT-007
- **Descripción**: Ampliación de la función central leer_input() para soportar "inputs secretos" (easter eggs) que desbloquean rutas narrativas alternativas sin interferir con el flujo principal del juego.
- **Severidad**: MEDIA
   Razón: Complejidad lógica interna oculta vs impacto alto en la profundidad narrativa.
   Impacto: Aumenta el factor sorpresa y rejugabilidad (inspirado en mecánicas de Dark Souls y Fear & Hunger).
   Reproducibilidad: Alta una vez definido el input secreto, pero accesible solo bajo condiciones específicas.
- **Precondiciones**: Motor leer_input() centralizado implementado (CT-005), narrativa principal establecida y sistema de "emitir" activo.
- **Pasos**:
   1.Navegar a un nodo crítico donde el input está disponible (ejemplo: final de combate o diálogo).
   2.Introducir la secuencia/valor secreto específico en el campo de entrada.
   3.Verificar que el sistema no bloquee ni caiga al detectar el valor atípico.
   4.Confirmar la activación del evento oculto/narrativo asociado a ese input sin forzar reinicios.
   5.Probar nuevamente un input estándar para asegurar que la lógica central no colapsó (regresión).
- **Resultado actual**: El sistema reconoce comandos opacos y ejecuta sus rutas alternativas, manteniendo la integridad del flujo normal. No hay filtrado de errores ni bloqueos en el hilo principal.
- **Resultado esperado**: Poder interactuar con caminos ocultos para obtener información extra o beneficios (ej. revivir personaje) sin arruinar la experiencia estándar para jugadores que no lo sepan.
- **Fundamentación técnica**: La función leer_input() pasó de ser un simple input() a un parser robusto capaz de validaciones implícitas. Permitió añadir lógica condicional interna (if secret_input) sin contaminar la interfaz gráfica ni los menús.
- **Solución implementada**: Se mantuvo el encapsulamiento en leer_input(). La detección de "comandos secretos" se realizó mediante una capa de validación interna (sanitization y check de strings ocultos), aislándolos del flujo normal para evitar que se detecten por errores de codificación.
- **Estado**: Implemented / Validated.
- **Notas**: Caso especial de diseño. Se utilizó la misma arquitectura centralizada para añadir profundidad sin reescribir el kernel de entrada. Inspirado en juegos como Dark Souls, donde una línea específica puede cambiar el destino. La función leer_input actúa ahora como puerta de acceso a estas rutas ocultas, evitando duplicar lógica de input por cada ruta secreta.
- **Complejidad**: Media-Alta (Requiere mantenimiento de secretos seguros sin exponerlos en logs o errores).
- **Lección aprendida**: La centralización del input (leer_input) hace posible añadir complejidad (como inputs secretos) sin que la estructura base se rompa. Es una lección clave sobre escalabilidad: una función bien diseñada puede crecer para soportar mecánicas profundas (easter eggs, secretos) manteniendo el código limpio.
- **Codigo implementado**:
    # [SECRETO 6] Posibilidad de revivir (una sola vez)
    preguntar("(Presiona enter para terminar)")
    respuesta_final = pedir_input().strip().lower()
    if respuesta_final == "Lorem ipsum dolor sit amet, consectetur adipiscing elit" and not personaje.get("_x9f"):
        narrar("\n========================================\n")
        narrar("Pero la muerte aquí no es el final.")
        narrar("La mazmorra es un lugar donde los muertos siguen sirviendo.")
        narrar("Y algo en ti aún tiene hambre. Aún tiene propósito.")
        narrar("Los ojos se abren. El cuerpo se recompone.")
        narrar("========================================\n")
        narrar("Horas después... o quizás minutos. No lo sabes. Despiertas en un cruce desconocido.")
        narrar("Tu cuerpo duele. Tu mente está confusa. Pero estás vivo.")
        # Restaurar vida
        personaje["_x9f"] = True
        personaje["vida"] = max(1, personaje.get("vida_max", 10) // 2)
        personaje["_flg1"] = True
        return False
    else:
        sys.exit()

---------------------------------------------------------------------------

## CT-008: Implementación del sistema de doble hilo (PiJ/PoJ)

- **ID**: CT-008
- **Descripción**: Diseño e implementación de un sistema de doble hilo para separar la lógica del juego (PoJ: Parser-Output-Juego) de la entrada del jugador (PiJ: Parser-Input-Jugador), evitando condiciones de carrera y garantizando que el jugador no pueda interactuar mientras el juego está narrando.
- **Severidad**: ALTA
  - Razón: Sin este sistema, el juego con UI de Tkinter sería injugable: el hilo principal se bloquea y la ventana deja de responder.
  - Impacto: Afecta a la totalidad del flujo del juego, desde el menú inicial hasta cada turno de combate.
  - Reproducibilidad: 100% reproducible al iniciar una partida nueva, donde el texto de introducción es suficientemente largo para provocar el solapamiento.
- **Precondiciones**:
  - UI de Tkinter implementada con panel de texto (PoJ) y Entry de input (PiJ).
  - Juego con al menos un texto narrativo largo al inicio (intro de partida nueva).
- **Pasos**:
  1. Iniciar el juego con una partida nueva.
  2. Observar el texto de introducción narrándose en el panel de texto.
  3. Mientras el texto se está escribiendo, introducir texto en el parser (Entry) y pulsar Enter.
  4. Observar si el input se mezcla visualmente con el texto del juego.
  5. Observar si el input se procesa de inmediato, se acumula, o queda bloqueado.
  6. Tras implementar el bloqueo: repetir los pasos 2-3 y verificar que la Entry permanece desactivada mientras el juego narra.
  7. Verificar que los botones de combate también quedan bloqueados durante la narración.
- **Resultado actual (fase 1 — cola)**:
  - Los inputs no se pierden, pero se acumulan en la cola durante la narración.
  - Al terminar el texto, todos los inputs acumulados se procesan de golpe, generando acciones no intencionadas.
  - El problema técnico estaba resuelto, pero el comportamiento para el jugador era confuso e incontrolable.
- **Resultado actual (fase 2 — bloqueo)**:
  - La Entry del parser queda desactivada mientras `_ocupado = True` (PoJ narrando).
  - Los botones de combate también quedan bloqueados, ya que son análogos al parser (envían comandos al mismo sistema).
  - Al terminar la narración, el sistema desbloquea ambos canales de input simultáneamente.
- **Resultado esperado**: El jugador no puede interactuar (ni por parser ni por botones) mientras el juego está narrando. Al terminar la narración, el input se habilita limpiamente, sin acumulación de entradas previas.
- **Causa raíz**: Al usar Tkinter con `input()` nativo en el mismo hilo, el event loop de Tkinter se bloquea y la UI deja de responder. Separar en dos hilos resuelve la responsividad, pero sin sincronización adicional ambos hilos compiten por los mismos canales de entrada: condición de carrera entre PiJ y PoJ.
- **Solución implementada**: Sistema `_Bridge` basado en `threading.Event`: el hilo del juego llama a `_bridge.esperar()` que bloquea ese hilo hasta recibir el input del jugador. El hilo de Tkinter, al detectar Enter en la Entry, llama a `_bridge.recibir(texto)` para desbloquearlo. La `cola_mensajes` (deque thread-safe) transporta los mensajes del juego hacia la UI. El flag `_ocupado` en la Vista bloquea Entry y botones mientras el typewriter está activo, impidiendo inputs cruzados.
- **Estado**: Implemented / Validated.
- **Notas**: Fue la feature más grande del proyecto, tardé casi un día completo en planearla e implementarla con Copilot. El problema se detectó en la fase de planning: al preguntar cómo se comportaría el juego mezclando inputs de botones y parser, fue Copilot quien propuso el sistema de hilos. La decisión de centralizar en un único punto de sincronización (`_Bridge`) la saqué de `aplicar_evento()`, una función análoga de gameplay que ya centralizaba efectos. La cola fue la primera solución implementada y funcionó técnicamente, pero al ver que acumulaba y soltaba inputs de golpe, decidí cortar por lo sano con el bloqueo, que era más limpio y no rompía nada.
- **Complejidad**: Alta. Sin conocimiento sintáctico propio del modelo de hilos de Python ni de Tkinter, la implementación dependió casi totalmente del planning con IA. A pesar de eso, el razonamiento del problema (qué debía pasar, qué no debía pasar, por qué la cola no era suficiente) fue propio.
- **Lección aprendida**: Una solución puede ser correcta técnicamente y aun así incorrecta para el usuario. La cola no perdía ningún dato, pero rompía el contrato implícito con el jugador: "si el juego habla, yo espero". Cuando una solución técnica choca con la expectativa del usuario, la solución correcta no es la más elegante en código, sino la que respeta ese contrato. Además, entendí los conceptos de condición de carrera, sincronización de hilos e inputs cruzados, no de forma teórica, sino porque los viví y los tuve que resolver.

---------------------------------------------------------------------------------

## CT-009: Botones de combate activos fuera del contexto de combate

- **ID**: CT-009
- **Descripción**: Los botones del panel de combate (armas, poción, stances) permanecían activos durante la exploración y cualquier contexto donde el juego esperaba un input . Pulsarlos enviaba el comando igualmente, el juego lo recibía y respondía "no es una opción válida", generando un bucle inútil, sin consecuencias reales pero sin ningún sentido funcional.
- **Severidad**: BAJA
  - Razón: El sistema de hilos (CT-008) absorbía los inputs sin acumularlos ni romper el estado. No había corrupción de datos.
  - Impacto: Loop sin sentido visible en el PoJ. Experiencia confusa para el jugador si spameaba botones fuera de combate.
  - Reproducibilidad: 100% — cualquier click en botón de combate fuera de combate reproducía el comportamiento.
- **Precondiciones**:
  - Sistema de doble hilo implementado (CT-008).
  - Panel de botones de combate visible/accesible fuera del bucle de combate.
- **Pasos**:
  1. Iniciar partida y pasar a fase de exploración (fuera de combate).
  2. Observar que los botones del panel de combate siguen activos.
  3. Pulsar cualquier botón de combate (ej. botón "daga").
  4. Observar que el PoJ muestra "no es una opción válida".
  5. Repetir — el juego sigue respondiendo igual, indefinidamente.
- **Resultado actual**: El botón envía su comando vía `_enviar_comando()`, el hilo juego lo recibe, evalúa que no corresponde al contexto actual y devuelve mensaje de opción inválida. El juego no se rompe pero responde a inputs sin sentido.
- **Resultado esperado**: Los botones del panel de combate deben estar inactivos (bloqueados) fuera del bucle de combate. Ningún click debe generar respuesta del juego en ese contexto.
- **Causa raíz**: El panel de botones se diseñó con foco en el comportamiento dentro de combate. No se implementó ningún guard de contexto: los botones estaban siempre activos independientemente del estado del juego.
- **Solución implementada**: Implementación del flag `_en_combate` (inicializado a `False` en el constructor de la Vista) que se activa al inicio del bucle de combate mediante `opciones_combate()` y se desactiva al salir. Los botones consultan este flag antes de procesar el click: si `_en_combate = False`, el evento se ignora sin enviar ningún comando. Se reutilizó el patrón de bloqueo por flag ya establecido en CT-008 (`_ocupado`).
- **Estado**: Fixed.
- **Notas**: Detectado durante el playtest posterior a CT-008. El sistema de hilos mantenía el juego estable, lo que hizo que no fuera urgente, pero sí evidente como comportamiento inútil. La solución fue sencilla una vez identificado el patrón: un flag de contexto que desactiva todo el panel de botones fuera de combate. La dificultad no estuvo en la implementación, sino en identificar dónde colocar ese guard sin romper la lógica existente.
- **Complejidad**: Baja-Media. Sin conocimiento profundo del sistema de botones, pero conociendo la arquitectura de flags del proyecto, fue aplicar un patrón conocido a un problema nuevo. La dificultad estuvo en saber dónde colocar el guard, no en la lógica a seguir.
- **Lección aprendida**: Cuando no tienes claro si una solución es la óptima, aplicar un patrón que ya conoces y que encaja con la arquitectura existente es una decisión válida. No siempre hay que buscar la solución ideal: conocer el sistema y saber qué quieres que ocurra es suficiente para avanzar con criterio.
- **Código implementado**:
  ```python
  # En el constructor de Vista — inicialización
  self._en_combate = False  # Flag: True cuando estamos EN combate. Botones solo activos durante combate.

  # Guard en stances (dentro de _select_stance)
  def _select_stance(cual):
      if not self._en_combate:
          return  # Ignorar clicks fuera de combate
      ...

  # Guard en armas (dentro de opciones_combate, al re-asignar bindings)
  cmd = (lambda a: lambda: self._enviar_comando(a) if self._en_combate else None)(arma)
  cvs.bind("<Button-1>", lambda e, c=cmd: c())

  # Guard en poción
  cvs_pocion.bind("<Button-1>", lambda e: self._enviar_comando("p") if self._en_combate else None)

  # Activación al inicio de combate (en opciones_combate)
  estaba_inactivo = not self._en_combate
  self._en_combate = True
  ```

-------------------------------------------------------------------------

## CT-010: Implementación del sistema de sprites en los botones de combate

- **ID**: CT-010
- **Descripción**: Migración del sistema de botones de combate de texto plano 
  ("arma1", "bloqueo", "pociones: 0-10") a sprites PNG de pixel art, vinculados 
  dinámicamente al diccionario del personaje reactivo. El proceso incluyó 
  una iteración fallida que produjo una "versión muerta" del código, 
  requirió backup, estudio de la arquitectura y modularización para poder 
  aislar y resolver los fallos.
- **Severidad**: ALTA
  - Razón: Complejidad técnica alta (integración PIL + Canvas + sistema reactivo) 
    vs impacto en UX directo. No era un bug previo, sino una mejora planificada.
  - Impacto: Sin sprites, los botones mostraban nombres de texto sin información 
    visual. La UI resultaba funcional pero sin identidad visual.
  - Reproducibilidad: N/A (implementación nueva, no bug).
- **Precondiciones**:
  - Panel de botones Canvas implementado y funcional (CT-004).
  - Flag _en_combate operativo (CT-009).
  - Assets PNG de armas, stances y pociones disponibles en assets/btns/ e 
    images/Botones/.
  - ImagenManager disponible en modules/ui_imagen_manager.py.
- **Pasos**:
  1. Definir _cargar_imgs_btns() como función modular separada, invocada 
     una sola vez en el constructor de Vista.
  2. Cargar sprites de armas dinámicamente desde images/Botones/armas/*.png 
     via imagen_manager.cargar_imagen().
  3. Registrar cada sprite bajo dos claves en _IMG_BTN: nombre de fichero 
     y display name (vía _ARMAS_DISPLAY_A_SPRITE).
  4. Cargar sprites de pociones (0-10) y stances por separado desde sus 
     subcarpetas.
  5. Vincular los sprites a los botones Canvas en opciones_combate(), 
     que se llama cada turno y refleja el estado actual del personaje.
  6. Validar que los sprites aparecen al conseguir armas, que el contador 
     de pociones se actualiza, que las stances muestran su estado activo/inactivo y que los stats de personaje se reflejan correctamente.
- **Resultado actual (fase iteración fallida)**: Al intentar implementar los 
  sockets de imagen dentro de los botones Canvas sin modularización, el sistema 
  acumuló bugs de tamaño de panel, orden de grid y prioridades de layout 
  que superaron el alcance de conocimiento disponible. Se llegó a una versión 
  muerta irrecuperable.
- **Resultado actual (tras fix)**: Los sprites aparecen correctamente en los 
  botones al entrar en combate. Las armas muestran su imagen al conseguirlas, 
  el botón de poción refleja el número correcto (0-10 sprites distintos), 
  y las stances muestran estado activo/inactivo. Todo vinculado al dict 
  de personaje reactivo.
- **Resultado esperado**: Sistema de sprites estable, modular, con fallback 
  silencioso (si un PNG no existe, el botón muestra texto sin romper la UI).
- **Causa raíz**: Falta de conocimiento técnico de Tkinter Canvas + PIL + 
  gestión de grid para delegar correctamente a la IA. Sin entender la 
  estructura, las instrucciones a la IA eran imprecisas y producían soluciones 
  que introducían bugs acumulativos fuera del alcance de depuración manual.
- **Solución implementada**: Backup del estado funcional previo. Estudio de 
  la arquitectura existente y de la documentación de Tkinter/PIL consultando 
  múltiples IAs (Copilot, Claude, GPT, Qwen). Modularización de _cargar_imgs_btns() 
  como función aislada para poder acceder y depurar las partes específicas 
  (tamaños, orden de grid, prioridades de panel). Prueba y error iterativa 
  hasta encontrar la configuración correcta. Fallback silencioso en ImagenManager 
  (retorna None sin excepción si el PNG no existe).
- **Estado**: Implemented / Validated.
- **Notas**: Primera iteración que produjo una "versión muerta" documentada 
  del proyecto. Derivó en un aprendizaje estructural sobre los límites de 
  delegar a la IA sin conocimiento técnico propio, análogo al de CT-002 
  pero con una resolución más metódica gracias a la experiencia acumulada.
- **Complejidad**: Alta. Semana completa de prueba y error. Requirió consulta 
  simultánea de múltiples IAs y documentación oficial de Tkinter y PIL.
- **Lección aprendida**: Cuando la IA no puede resolver un problema con 
  prompts genéricos, la solución no es iterar más prompts sino entender 
  primero el sistema. Pedir documentación explicatoria específica de tu 
  propio código a la IA, antes de pedir soluciones, cambia completamente 
  la calidad de las respuestas. Modularizar funciones concretas no solo 
  mejora el código, sino que hace los problemas depurables.
- **Código implementado**:
  ```python
  # 1. CARGA ÚNICA al construir la Vista
  #    _IMG_BTN es un dict global que actúa como caché de sprites
  _IMG_BTN = {}

  def _cargar_imgs_btns(self):
      base = pathlib.Path(resource_path("assets/btns"))

      # Cargar sprites estáticos (stances, huir, navegación...)
      for nombre in ["bloquear", "esquivar", "huir", ...]:
          img = imagen_manager.cargar_imagen(str(base / f"{nombre}.png"))
          if img:
              _IMG_BTN[nombre] = img  # Fallback silencioso: si no existe, no se carga

      # Cargar sprites de armas dinámicamente desde carpeta
      for archivo_png in armas_base.glob("*.png"):
          img = imagen_manager.cargar_imagen(str(archivo_png))
          if img:
              _IMG_BTN[archivo_png.stem] = img
              # Registrar también bajo el display name del juego
              for display_name, sprite_name in _ARMAS_DISPLAY_A_SPRITE.items():
                  if sprite_name == archivo_png.stem:
                      _IMG_BTN[display_name] = img

      # Cargar sprites de pociones (0pociones.png ... 10pociones.png)
      for i in range(11):
          img = imagen_manager.cargar_imagen(str(pociones_base / f"{i}pociones.png"))
          if img:
              _IMG_BTN[f"{i}pociones"] = img

  # 2. VINCULACIÓN al dict de personaje reactivo
  #    opciones_combate() se llama cada turno y refresca los botones
  #    con el estado actual de personaje["armas"] y personaje["pociones"]
  def opciones_combate(self, armas, pociones, ...):
      self._en_combate = True
      for i, arma in enumerate(slots):
          img = _IMG_BTN.get(arma)           # Sprite del arma si existe
          img_fondo = _IMG_BTN.get("fondo_armas")  # Fondo compartido
          self._redibujar_boton(cvs, arma, tiene, imagen=img, imagen_fondo=img_fondo)

      # Poción: sprite según número actual (0-10)
      img_pocion = _IMG_BTN.get(f"{pociones}pociones")
      self._redibujar_boton(cvs_pocion, "", tiene_pocion, imagen=img_pocion)

  # 3. FALLBACK en ImagenManager
  #    Si el PNG no existe, retorna None sin lanzar excepción
  def cargar_imagen(self, ruta, tamaño=None):
      if not os.path.exists(ruta):
          return None  # El botón mostrará texto en lugar de sprite
      ...
  ```

  -------------------------------------------------------------------------