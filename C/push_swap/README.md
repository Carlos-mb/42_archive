*This activity has been created as part of the 42 curriculum by cmelero-, catencio*

# Descripción
**push_swap** es un proyecto de 42 cuyo objetivo es ordenar una pila de enteros usando un conjunto limitado de operaciones entre dos pilas (A y B), generando la secuencia mínima posible según una estrategia definida. Este repositorio incluye la implementación del programa, la librería `libft` y varios algoritmos de ordenación.

## Equipo de trabajo
Este proyecto ha sido realizado entre **catencio** y **cmelero-**. Ambos hemos participado en las decisiones sobre algoritmos. Hicimos una lista de tareas (funciones a realizar) y las fuimos completando según nuestra disponibilidad. Todas las tareas se han revisado entre los dos, solucionando juntos los problemas encontrados.

Las cabeceras de los ficheros se corresponden con la última persona que editó el fichero, no con quien lo codificó entero. César (catencio) realizó íntegramente el algoritmo intermedio y Carlos (cmelero-) los algoritmos simple y Radix. El resto se fue codificando tomando decisiones conjuntas y repartiendo el trabajo en pequeñas tareas.

## Algoritmos y justificación
### Concepto de estrategias
En el proyecto, la complejidad se mide por **número de operaciones de push_swap** emitidas (sa, pb, ra, etc.). Las tres clases de estrategias pedidas son:

- **$O(n^2)$**: el número de operaciones crece aproximadamente con el cuadrado de $n$. Es típico de métodos que “revisan” muchos pares o repiten búsquedas completas (por ejemplo, extraer mínimos uno a uno).
- **$O(n\sqrt{n})$**: crece más rápido que lineal pero más lento que $n^2$. Suele aparecer en métodos por *chunks* o rangos, donde se hacen barridos parciales en bloques.
- **$O(n\log n)$**: mucho más eficiente para $n$ grande; típicamente se logra con estrategias tipo radix o particiones más eficientes, donde el coste aumenta casi linealmente multiplicado por $\log n$.

Estas clases no describen el código en sí, sino la **cota superior de operaciones** en el modelo de push_swap.

### Índice de desorden
El índice de desorden se calcula **exactamente** con el algoritmo proporcionado en el subject (contando inversiones sobre todos los pares posibles). Usamos este pseudocódigo como referencia:

```text
function compute_disorder(stack a):
	mistakes = 0
	total_pairs = 0
	for i from 0 to size(a)-1:
		for j from i+1 to size(a)-1:
			total_pairs += 1
			if a[i] > a[j]:
				mistakes += 1
	return mistakes / total_pairs
```
El resorden se calcula en un rango de 0 a 1. Para calcularlo, se revisan todos los pares de números posibles en la pila. Cada vez que un número mayor aparece antes que uno menor, ese par se considera un error. Cuantos más errores haya, más cerca estará el desorden de 1.

### Algoritmo simple (O($n^2$)): extracción del mínimo/máximo
Este enfoque recorre la pila buscando el mínimo (o máximo), lo rota hasta la cima y lo empuja a la pila auxiliar. Se repite hasta ordenar todo.
**Justificación:** Según parece, es fácil de implementar, correcto y eficiente para entradas pequeñas. El coste es O($n^2$) por las búsquedas repetidas y rotaciones. No probamos el resto, sólo utilizamos el que parecía que recomendaban más.

### Algoritmo intermedio (O($n\sqrt{n}$)): Chunks / buckets
Primero recorre la lista creando un índice de órden, igual que usa el Radix. Así trabajamos con números en el rango 0..n-1 (independiente de que el input tenga negativos o valores muy grandes).
Luego se divide el rango de índices en **bloques (chunks)** de tamaño aproximado $\sqrt{n}$. La idea es ir moviendo desde `stack_a` a `stack_b` todos los números que pertenecen al bloque actual.

Mientras el índice del elemento de arriba no esté en el chunk, rotamos `stack_a` hasta encontrar uno que sí lo esté y hacemos `pb`. Para mejorar el coste, cuando empujamos un elemento “pequeño” dentro del chunk, a veces rotamos también `stack_b` para dejar arriba elementos más grandes (así la vuelta a `stack_a` es más rápida).

Cuando `stack_a` se queda vacío, reconstruimos el orden devolviendo desde `stack_b` a `stack_a`: buscamos el máximo (por índice), rotamos `stack_b` en el sentido más corto hasta ponerlo arriba y hacemos `pa`. Repetimos hasta vaciar `stack_b`.

**Justificación:** este método suele usar muchas menos operaciones que el simple en tamaños medianos, pero sin ser tan mecánico como el Radix. La complejidad típica de estrategias por chunks se aproxima a O($n\sqrt{n}$) porque se hacen barridos por bloques y rotaciones controladas.

### Algoritmo complejo (O($n \log n$)): Radix LSD
Primero recorre la lista creando un índice de órden. Cada elemento pasa a tener un número que indica su posición en la lista. Eso es el índice y se utilizará para el algoritmo Radix. Esto es muy importante para reducir el número de vueltas, por cómo hemos implementado Radix.
Se procesan dígitos desde el menos significativo (derecha) al más significativo (izquierda). Primero se pasan al stack_b todos los elementos que tienen un "1", luego un "2", hasta "9". Después pasamos de stack_b a stack_a siguiendo el mismo criterio, pero aplicado al segundo dígito (decenas). Así, hasta que se procesan todos los dígitos. 
Cada intero puede medir 10 dígitos, utilizando el índice, en una lista de 500 elementos, se recorren sólo 3 dígitos (de 0 a 499), por eso se optimizan los movimientos.
**Justificación:** Mucha gente nos recomendó el KSort, pero queríamos hacer algo diferente. Se supone que este garantiza complejidad O($n \log n$) y reduce drásticamente el número de operaciones en entradas grandes, pero no hemos probado el resto.

### Estrategia adaptativa: selección automática de algoritmo
La estrategia `--adaptive` decide qué algoritmo aplicar según el tamaño de entrada y el **índice de desorden** (calculado con el pseudocódigo del subject).

La idea es:
- Si la entrada es pequeña o está casi ordenada (desorden bajo), usar la estrategia **simple**.
- Si la entrada es mediana y no está demasiado desordenada, usar la estrategia **intermedia (chunks)**.
- Si la entrada es grande o muy desordenada, usar **Radix**.

**Justificación:** con esto intentamos aprovechar lo mejor de cada algoritmo: pocas operaciones en casos fáciles, y un comportamiento estable y eficiente cuando $n$ crece.


# Instrucciones
## Compilación
```bash
make
```

## Limpieza
```bash
make clean
# o
make fclean
```

## Ejecución
```bash
./push_swap 4 2 1
# o con argumentos generados y checker en linux
ARG=$(shuf -i 1-1000 -n 100 | tr '\n' ' '); ./push_swap $ARG | ./checker_linux $ARG
```

## Normas de uso

El programa se llama **`push_swap`** y recibe por argumentos:

- **La pila A**, formateada como una lista de enteros (el **primer** argumento es el **top** de la pila).
- Un **selector de estrategia opcional** (puede ir presente junto al resto de enteros):
	- `--simple`: fuerza el uso del algoritmo **O($n^2$)**.
	- `--medium`: fuerza el uso del algoritmo **O($n\sqrt{n}$)**.
	- `--complex`: fuerza el uso del algoritmo **O($n \log n$)**.
	- `--adaptive`: fuerza el uso de la estrategia **adaptativa** (basada en desorden).
		- Si **no** se indica ningún selector, este es el **comportamiento por defecto**.

### Salida estándar (stdout)

- Imprime **la lista más pequeña posible** de operaciones de push_swap para ordenar la pila A (el menor arriba).
- Las operaciones están **separadas por `\n`** y **nada más**.
- Si no se pasan parámetros, el programa **no debe imprimir nada** y debe devolver el control al prompt.

### Errores (stderr)

En caso de error, debe imprimir exactamente:

- `Error\n` en **stderr**.

Se consideran errores, por ejemplo:
- argumentos que no son enteros,
- enteros fuera de rango,
- valores duplicados.

### Modo benchmark (`--bench`)

Cuando se pasa el flag `--bench`, tras ordenar debe mostrar (y **solo** en ese caso):

- El desorden calculado (**% con dos decimales**).
- El nombre de la estrategia usada y su **clase de complejidad teórica**.
- El número total de operaciones.
- El recuento de cada operación (sa, sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr).

El output de benchmark debe enviarse a **stderr**.

# Recursos
- Páginas `man` de C (`man 3 malloc`, `man 3 write`, etc.).
- Documentación del proyecto **push_swap** del campus 42.
- Ordenación por Radix: https://en.wikipedia.org/wiki/Radix_sort
- Algoritmo de extracción min/máx (Selection Sort): https://en.wikipedia.org/wiki/Selection_sort
- Artículos sobre análisis de complejidad: https://www.bigocheatsheet.com/
- Durante las evaluaciones a otros compañeros, les preguntamos cómo lo habían implementado y pedimos consejo.

## Uso de IA
- Explicación de conceptos de C y complejidad algorítmica.
- Revisión del código terminado para detectar posibles bugs.
- No se ha usado IA para generar código final del proyecto.
