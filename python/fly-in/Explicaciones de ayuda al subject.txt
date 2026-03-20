CONTEXTO ADICIONAL SOBRE FLY-IN (interpretación operativa del proyecto)

El siguiente contexto debe considerarse como una interpretación operativa consensuada del subject de Fly-in. No sustituye al PDF oficial, pero aclara ambigüedades prácticas para la simulación.

## Modelo de turno

La simulación es discreta y funciona por turnos.

En cada turno:

* Cada dron puede realizar **como máximo una acción**:

  * moverse
  * esperar voluntariamente
  * esperar porque está en tránsito hacia zona restricted

* Los movimientos deben considerarse como un **conjunto globalmente válido**, no como una ejecución secuencial real.

* Sin embargo, dentro de un turno puede existir **encadenamiento lógico de movimientos**, porque:

  * cuando un dron sale de una zona, **libera capacidad en ese mismo turno**
  * otros drones que aún no han actuado pueden aprovechar esa capacidad

Por tanto:

Un turno puede modelarse como la construcción incremental de un conjunto de movimientos compatibles.

Esto NO significa que exista un orden real de ejecución, sino que el algoritmo puede explorar movimientos en cualquier orden mientras el resultado final respete todas las restricciones.

## Movimiento hacia zonas restricted

El movimiento hacia una zona restricted tiene coste 2 turnos y se interpreta como:

* Turno T: el dron ocupa la conexión hacia la zona restricted
* Turno T+1: el dron llega obligatoriamente a la zona restricted

Durante el tránsito:

* el dron ocupa la conexión
* no puede esperar ni cambiar de decisión
* no puede actuar en ese turno

Este modelo implica que:

* las zonas restricted NO están ocupadas durante 2 turnos
* lo que se ocupa durante el turno intermedio es la conexión

## Capacidad de zonas

* La capacidad de una zona se evalúa dinámicamente dentro del turno.
* Si un dron sale de una zona, esa zona puede ser ocupada por otro dron en el mismo turno.
* La validez se evalúa sobre el conjunto total de movimientos del turno.

## Capacidad de conexiones

* Durante el tránsito hacia zonas restricted, el dron ocupa la conexión durante el turno intermedio.
* La liberación de la conexión ocurre al finalizar ese turno.
* El turno de llegada ya no cuenta como ocupación de la conexión.

## Prioridad de zonas priority

* Las zonas priority tienen coste de movimiento 1.
* Deben considerarse preferibles en el pathfinding como criterio heurístico.
* No constituyen una restricción funcional obligatoria si la solución sigue siendo válida y eficiente.

## Interpretación de benchmarks

* Los benchmarks del subject son objetivos de optimización orientativos.
* No forman parte de las reglas de validez de la simulación.
* Una solución puede ser válida aunque no alcance esos números.

## Notas sobre mapas de ejemplo

* Existen mapas de ejemplo que no cumplen todas las reglas formales del parser (por ejemplo coordenadas negativas o zonas con mismas coordenadas).
* Estos mapas deben interpretarse como casos de prueba adicionales o inputs potencialmente inválidos, no como contradicciones operativas del modelo de simulación.

