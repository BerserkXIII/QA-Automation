# Lecciones Aprendidas

## Sobre Testing Manual
- Fundamentos ISTQB
- Casos de Prueba Manuales
- Reportes de Defectos
- Estructura de un Caso de Prueba
- Tipos de pruebas

## Sobre Git & GitHub
- Uso basico de Git y GitHub (commits, push, pull, branchs, etc.)

## Sobre Automatización
- (Próximamente)

## Errores cometidos y cómo los resolví
- Mucha IA en el pasado. Actualmente la uso como punto de apoyo en casos especificos, adecuando promps, agents, etc.

## Lección aprendida

# 🧠 Concepto Clarificado: Regla de Bloqueo vs. Prioridad

**Situación:** Test con dependencias (ej: CP003 → CP002)  
**Regla:** Primero se respeta la dependencia (orden de ejecución), luego aplica prioridad entre opciones paralelas.

**Nota Personal:** No todos los tests tienen el mismo peso —los unitarios independientes son más flexibles en priorización que los de integración con dependencias forzadas. 
Primero, comprueba dependencias entre pruebas. Si hubiera pruebas en paralelo, aplicar prioridad.


---

*Última actualización: [09/04/2026]*
