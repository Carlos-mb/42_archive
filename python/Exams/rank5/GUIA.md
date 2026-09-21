# Nivel 1

## py_compress_decompress

**Enunciado:** escribe dos funciones, `compress` y `decompress`.

- `compress` comprime los caracteres repetidos seguidos poniendo detrás del carácter cuántas veces se repite.
  - Si un carácter aparece una sola vez seguida, no se escribe el `1`.
  - Si la cadena está vacía, devuelve `""`.
- `decompress` recibe una cadena comprimida y la devuelve a su forma original.
  - Acepta números de varias cifras: `"a12"` son 12 `a`.
  - Si detrás de un carácter no hay número, cuenta como 1.

```python
def compress(s: str) -> str:
def decompress(s: str) -> str:

compress("aabcccccaaa")    # "a2bc5a3"
decompress("a2bc5a3")      # "aabcccccaaa"
compress("")               # ""
```

**Frase para recordar:** «Coge una letra y cómete lo que viene detrás».

**compress** (truco 1):
1. `result = ""`, `i = 0`.
2. Mientras `i < len(s)`: guarda `char = s[i]` y pon `count = 0`.
3. Bucle interior: mientras `s[i] == char` → `count += 1`, `i += 1`.
4. Añade `char` y, **solo si `count > 1`**, añade `str(count)`.

**decompress** (el mismo esqueleto):
1. `char = s[i]`, `i += 1` (la letra ya está leída).
2. Bucle interior: mientras `s[i].isdigit()` → `number += s[i]`, `i += 1`.
3. Si `number == ""` añade `char`; si no, añade `char * int(number)`.

**Trampas:**
- Dentro del `while` interior pon **siempre** `i < len(s) and ...` delante, o te sales de la cadena.
- Los números van en un **string** (`number += s[i]`), así `"12"` funciona solo.

## py_spiral_matrix

**Enunciado:** genera una matriz `n x n` con los números del 1 a `n²` colocados en espiral en el sentido de las agujas del reloj.

La espiral empieza en la casilla de arriba a la izquierda `(0, 0)` y avanza hacia la derecha; después baja, va a la izquierda, sube, y sigue así hacia dentro.

```python
def generate_spiral(n: int) -> list[list[int]]:

generate_spiral(3)    # [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
generate_spiral(1)    # [[1]]
```

**Frase para recordar:** «Una serpiente que anda recto y gira a la derecha cuando choca».

1. Matriz de ceros `n x n` con un bucle y `append([0] * n)`.
2. `moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]` → derecha, abajo, izquierda, arriba (el sentido del reloj). `d = 0`.
3. `row = 0`, `col = 0`. Para `number` de `1` a `n * n`:
   - Escribe `matrix[row][col] = number`.
   - Calcula la siguiente casilla con `moves[d]`.
   - Si está **fuera** (truco 2) **o ya tiene número** (`!= 0`): gira `d = (d + 1) % 4` y recalcula la siguiente.
   - Avanza.

**Trampas:**
- **Nunca** `[[0] * n] * n`: las filas serían la misma lista y al cambiar una cambian todas.
- `range(1, n * n + 1)`: el `+ 1` es para llegar hasta `n²`.
- En `moves`, el primer número es la fila y el segundo la columna. Derecha = misma fila, columna +1 → `(0, 1)`.

---

# Nivel 2

## py_graph_cycle_detector

**Enunciado:** di si un grafo dirigido tiene al menos un ciclo.

El grafo llega como un diccionario (lista de adyacencia): cada clave es un nodo (entero) y su valor es la lista de nodos a los que apunta.

- Devuelve `True` si el grafo tiene algún ciclo.
- Devuelve `False` si no tiene ciclos o si el diccionario está vacío.
- Tiene que funcionar con grafos formados por varias partes separadas.

```python
def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:

py_graph_cycle_detector({0: [1], 1: [2], 2: [0]})    # True
py_graph_cycle_detector({0: [1], 1: [2], 2: []})     # False
py_graph_cycle_detector({})                          # False
```

**Frase para recordar:** «Si mientras camino vuelvo a pisar mi propio camino, hay ciclo».

1. Función `visit(graph, node, path)` (truco 4):
   - Si `node in path` → `True`.
   - Para cada vecino en `graph.get(node, [])`: si `visit(graph, vecino, path + [node])` → `True`.
   - Al final → `False`.
2. Función principal: para cada `node in graph`, si `visit(graph, node, [])` → `True`. Al final → `False`.

**Trampas:**
- `graph.get(node, [])` y no `graph[node]`: un vecino puede no tener clave en el diccionario.
- `path + [node]` crea una lista nueva: así cada rama tiene su propio camino y no hay que «deshacer» nada.
- El bucle principal sobre **todos** los nodos es lo que cubre los grafos con varias partes separadas.
- Un grafo vacío no entra en el bucle y devuelve `False` sin código extra.

## py_room_scheduler


**Enunciado:** reparte reuniones en salas. Cada reunión es una lista de dos enteros `[inicio, fin]`.

Haz una función en python. 
Recibirá una lista de tuplas. Cada tupla tiene dos enteros. Cada entero se refiere a hora de inicio y hora de fin de una reunión. 
La función debe calcular el número mínimo de salas que hacen falta para permitir todas las reuniones. Debe devolver un diccionario con dos elementos. El primer elemento tiene clave "Numero de salas" y el valor será el número de salas requerido. El segundo valor del diccionario será un diccionario, cada elemento será el número de la sala, comenzando desde 0 y su valor será una lista de tuplas con la hora de inicio y final de cada reunión. 
El resultado estará ordenado por la hora de comienzo de la reunión. 

- Ordena las reuniones por hora de inicio y asígnalas a las salas disponibles, una tras otra.
- Devuelve un diccionario con:
  - `"total_rooms"`: el número de salas necesarias.
  - `"schedule"`: una lista con las reuniones de cada sala (una lista por sala).
- Si la lista está vacía, devuelve `{"total_rooms": 0, "schedule": []}`.

```python
def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:

py_room_scheduler([[0, 30], [5, 10], [15, 20]])
# {"total_rooms": 2, "schedule": [[[0, 30]], [[5, 10], [15, 20]]]}
py_room_scheduler([])
# {"total_rooms": 0, "schedule": []}
```

**Frase para recordar:** «Ordeno por hora de inicio y meto cada reunión en la primera sala que ya ha terminado».

1. `rooms = []` (cada sala es una lista de reuniones).
2. Recorre `sorted(meetings, key=start_time)`, donde `start_time(meeting)` devuelve `meeting[0]`.
3. Para cada reunión: `placed = False`. Recorre las salas; si `room[-1][1] <= meeting[0]` (la última reunión de la sala acaba antes o justo cuando empieza esta), añádela, `placed = True`, `break`.
4. Si `not placed` → `rooms.append([meeting])` (sala nueva).
5. Devuelve `{"total_rooms": len(rooms), "schedule": rooms}`.

**Trampas:**
- `<=` y no `<`: una reunión que acaba a las 10 deja la sala libre para otra que empieza a las 10.
- `rooms.append([meeting])` con **corchetes**: la sala nueva es una lista que contiene la reunión.
- `from typing import Any` arriba del todo (la firma lo usa).
- Con la lista vacía ya sale `{"total_rooms": 0, "schedule": []}` sin código extra.

## py_island_matrix_counter

**Enunciado:** cuenta las islas de una matriz 2D que contiene los strings `"1"` y `"0"`.

- `"1"` es tierra y `"0"` es agua.
- Una isla es un grupo de casillas `"1"` conectadas. Solo están conectadas las casillas pegadas en horizontal (izquierda, derecha) o en vertical (arriba, abajo); **las diagonales no cuentan**.
- Cada isla se cuenta una sola vez.
- Una matriz vacía (o sin filas) devuelve `0`.
- Se permite recorrer con DFS/BFS o modificar la matriz para explorar cada isla completa.

```python
def island_matrix_counter(matrix: list[list[str]]) -> int:

island_matrix_counter([["1", "1", "1", "1", "0"],
                       ["1", "1", "1", "0", "0"],
                       ["1", "1", "1", "1", "0"],
                       ["0", "0", "0", "0", "0"]])    # 1
island_matrix_counter([["1", "1", "0", "0", "0"],
                       ["1", "1", "0", "0", "0"],
                       ["0", "0", "1", "0", "0"],
                       ["0", "0", "0", "1", "1"]])    # 3
island_matrix_counter([])                             # 0
```

**Frase para recordar:** «Cuando piso tierra, cuento una isla y la hundo entera».

1. Recorre todas las casillas con `for row` / `for col`.
2. Si la casilla es `"1"`: `count += 1` y llama a `sink(matrix, row, col)`.
3. `sink` (truco 3 + truco 2):
   - `pending = [(row, col)]`.
   - Mientras haya pendientes: saca una con `pop()`.
   - Si está fuera → `continue`. Si no es `"1"` → `continue`.
   - Ponla a `"0"` y añade sus 4 vecinas: abajo, arriba, derecha, izquierda.

**Trampas:**
- Las casillas son **strings**: `"1"` y `"0"`, no `1` y `0`.
- Añadir vecinas sin comprobarlas está bien: la comprobación se hace al sacarlas.
- Se usa una lista de pendientes y no recursión porque en una isla grande la recursión da `RecursionError`.

---

# Nivel 3

## py_prism_detector

**Enunciado:** busca todas las veces que aparece una palabra (`pattern`) en una rejilla de caracteres (`grid`), en las 8 direcciones.

Cada dirección es un vector `(dx, dy)` con su código:

| Vector | Código | Nombre en el enunciado |
|---|---|---|
| `(1, 0)` | `"H"` | horizontal a la derecha |
| `(-1, 0)` | `"H-"` | horizontal a la izquierda |
| `(0, 1)` | `"V"` | vertical hacia abajo |
| `(0, -1)` | `"V-"` | vertical hacia arriba |
| `(1, 1)` | `"D1"` | diagonal abajo-derecha |
| `(-1, -1)` | `"D1-"` | diagonal arriba-izquierda |
| `(-1, 1)` | `"D2"` | diagonal arriba-derecha |
| `(1, -1)` | `"D2-"` | diagonal abajo-izquierda |

- `grid` es una lista de strings (cada string es una fila).
- Devuelve una lista de tuplas `(x, y, código)` por cada coincidencia: `x` es la columna e `y` la fila de la **primera letra**.
- Si `grid` o `pattern` están vacíos, devuelve `[]`.

```python
def prism_detector(grid: list[str], pattern: str):

prism_detector(["CAT", "A..", "T.."], "CAT")    # [(0, 0, "H"), (0, 0, "V")]
prism_detector([], "CAT")                       # []
```

**Frase para recordar:** «En cada casilla pruebo las 8 flechas, y cada flecha la compruebo letra a letra».

1. Copia la lista `DIRECTIONS` con tuplas `(dx, dy, code)` **en el orden del enunciado**: H, H-, V, V-, D1, D1-, D2, D2-.
2. Si `grid` o `pattern` están vacíos → `[]`.
3. Tres bucles: `for y` (filas), `for x` (columnas), `for dx, dy, code in DIRECTIONS`. Si `matches(...)` → añade `(x, y, code)`.
4. `matches(grid, pattern, x, y, dx, dy)`: para `i` en `range(len(pattern))`:
   - `cx = x + dx * i`, `cy = y + dy * i`.
   - Si está fuera (truco 2) → `False`. Si `grid[cy][cx] != pattern[i]` → `False`.
   - Al final → `True`.

**Trampas:**
- Aquí `x` es la **columna** y `y` la **fila**: se accede con `grid[cy][cx]` (primero la fila).
- Fíate de los vectores del enunciado, no de los nombres: `(-1, 1)` se llama «up-right», pero con `y` hacia abajo en realidad va abajo-izquierda. Copia los números tal cual.
- El resultado es una tupla `(x, y, code)`: primero `x`.

## py_word_ladder

**Enunciado:** calcula la longitud de la escalera de palabras más corta para ir de `start` a `end`, usando las palabras permitidas de la lista `sentence`.

- En cada paso se cambia exactamente un carácter.
- Todas las palabras intermedias tienen que estar en `sentence`.
- Devuelve el número total de palabras de la escalera más corta, contando `start` y `end`.
- Si no se puede llegar, devuelve `0`.

```python
def word_ladder(start: str, end: str, sentence: list[str]) -> int:

word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])    # 5
word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"])           # 0
```
(En el primer ejemplo: `hit → hot → dot → dog → cog`, 5 palabras.)

**Frase para recordar:** «Voy saltando a palabras que se diferencian en una letra; el primero que entra es el primero que sale».

1. Función `differ_by_one(a, b)`: si las longitudes son distintas → `False`; cuenta las posiciones distintas; devuelve `differences == 1`.
2. `pending = [(start, 1)]` (palabra y número de palabras usadas hasta ahora), `visited = [start]`.
3. Mientras haya pendientes: `word, steps = pending.pop(0)`.
   - Si `word == end` → devuelve `steps`.
   - Para cada `candidate` de `sentence`: si no está en `visited` y `differ_by_one(word, candidate)` → añádelo a `visited` y a `pending` con `steps + 1`.
4. Si se acaba la lista → `0`.

**Trampas:**
- `pop(0)` y **no** `pop()`: sacar el más antiguo garantiza que la primera vez que llegas a `end` es por el camino más corto.
- Se empieza en `1`, no en `0`: se cuentan palabras, incluida `start`.
- Marca como visitada al **añadir** a pendientes, no al sacar, para no meter la misma palabra dos veces.

---

## Cómo practicar

1. Lee la «frase para recordar» y los pasos de un ejercicio.
2. Cierra la guía y escribe la solución en un fichero nuevo, de memoria.
3. Guárdala en `practica/` con el nombre del ejercicio (por ejemplo `practica/py_word_ladder.py`) y ejecuta `python3 practica/comprobar.py py_word_ladder`.
4. Si fallas, apunta qué paso olvidaste y repite ese ejercicio otro día.
