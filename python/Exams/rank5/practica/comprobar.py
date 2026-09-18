"""Comprueba tus ejercicios de práctica con los ejemplos del enunciado.

Uso (desde la carpeta practica/):
    python3 comprobar.py py_word_ladder     comprueba un ejercicio
    python3 comprobar.py                    comprueba todos los que existan
"""
import importlib
import os
import signal
import sys
import traceback

SEGUNDOS_MAXIMOS = 2

# Cada caso: (llamada que se muestra, función que la ejecuta, resultado
# esperado).
# Las entradas se crean dentro de la lambda para que cada caso reciba datos
# nuevos (island_matrix_counter modifica la matriz que recibe).
CASOS = {
    "py_compress_decompress": [
        ('compress("aabcccccaaa")',
         lambda m: m.compress("aabcccccaaa"), "a2bc5a3"),
        ('decompress("a2bc5a3")',
         lambda m: m.decompress("a2bc5a3"), "aabcccccaaa"),
        ('compress("")', lambda m: m.compress(""), ""),
        ('decompress("")', lambda m: m.decompress(""), ""),
        ('compress("abc")', lambda m: m.compress("abc"), "abc"),
        ('decompress("a12")', lambda m: m.decompress("a12"), "a" * 12),
        ('compress("aaaaaaaaaaaab")',
         lambda m: m.compress("aaaaaaaaaaaab"), "a12b"),
    ],
    "py_spiral_matrix": [
        ("generate_spiral(3)", lambda m: m.generate_spiral(3),
         [[1, 2, 3], [8, 9, 4], [7, 6, 5]]),
        ("generate_spiral(1)", lambda m: m.generate_spiral(1), [[1]]),
        ("generate_spiral(2)", lambda m: m.generate_spiral(2),
         [[1, 2], [4, 3]]),
        ("generate_spiral(4)", lambda m: m.generate_spiral(4),
         [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]),
    ],
    "py_graph_cycle_detector": [
        ("{0: [1], 1: [2], 2: [0]}",
         lambda m: m.py_graph_cycle_detector({0: [1], 1: [2], 2: [0]}),
         True),
        ("{0: [1], 1: [2], 2: []}",
         lambda m: m.py_graph_cycle_detector({0: [1], 1: [2], 2: []}),
         False),
        ("{}", lambda m: m.py_graph_cycle_detector({}), False),
        ("{0: [0]}  (un nodo que apunta a sí mismo)",
         lambda m: m.py_graph_cycle_detector({0: [0]}), True),
        ("{0: [1], 1: [], 2: [3], 3: [2]}  (ciclo en la segunda parte)",
         lambda m: m.py_graph_cycle_detector(
             {0: [1], 1: [], 2: [3], 3: [2]}), True),
        ("{0: [1, 2], 1: [3], 2: [3], 3: []}  (rombo, sin ciclo)",
         lambda m: m.py_graph_cycle_detector(
             {0: [1, 2], 1: [3], 2: [3], 3: []}), False),
        ("{0: [5]}  (vecino que no es clave)",
         lambda m: m.py_graph_cycle_detector({0: [5]}), False),
    ],
    "py_room_scheduler": [
        ("[[0, 30], [5, 10], [15, 20]]",
         lambda m: m.py_room_scheduler([[0, 30], [5, 10], [15, 20]]),
         {"total_rooms": 2, "schedule": [[[0, 30]], [[5, 10], [15, 20]]]}),
        ("[]", lambda m: m.py_room_scheduler([]),
         {"total_rooms": 0, "schedule": []}),
        ("[[5, 10], [0, 5]]  (desordenadas; acaba a las 5 y empieza a las 5)",
         lambda m: m.py_room_scheduler([[5, 10], [0, 5]]),
         {"total_rooms": 1, "schedule": [[[0, 5], [5, 10]]]}),
        ("[[1, 4], [2, 5], [3, 6]]  (todas se solapan)",
         lambda m: m.py_room_scheduler([[1, 4], [2, 5], [3, 6]]),
         {"total_rooms": 3, "schedule": [[[1, 4]], [[2, 5]], [[3, 6]]]}),
    ],
    "py_island_matrix_counter": [
        ("ejemplo 1 del enunciado",
         lambda m: m.island_matrix_counter([
             ["1", "1", "1", "1", "0"], ["1", "1", "1", "0", "0"],
             ["1", "1", "1", "1", "0"], ["0", "0", "0", "0", "0"]]), 1),
        ("ejemplo 2 del enunciado",
         lambda m: m.island_matrix_counter([
             ["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
             ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]), 3),
        ("[]", lambda m: m.island_matrix_counter([]), 0),
        ("[[\"1\", \"0\"], [\"0\", \"1\"]]  (diagonales no cuentan)",
         lambda m: m.island_matrix_counter([["1", "0"], ["0", "1"]]), 2),
        ("rejilla 60x60 toda de tierra",
         lambda m: m.island_matrix_counter(
             [["1"] * 60 for _ in range(60)]), 1),
    ],
    "py_prism_detector": [
        ('["CAT", "A..", "T.."], "CAT"',
         lambda m: m.prism_detector(["CAT", "A..", "T.."], "CAT"),
         [(0, 0, "H"), (0, 0, "V")]),
        ('[], "CAT"', lambda m: m.prism_detector([], "CAT"), []),
        ('["CAT"], ""', lambda m: m.prism_detector(["CAT"], ""), []),
        ('["TAC"], "CAT"  (hacia la izquierda)',
         lambda m: m.prism_detector(["TAC"], "CAT"), [(2, 0, "H-")]),
        ('["C..", ".A.", "..T"], "CAT"  (diagonal)',
         lambda m: m.prism_detector(["C..", ".A.", "..T"], "CAT"),
         [(0, 0, "D1")]),
        ('["..C", ".A.", "T.."], "CAT"  (código D2)',
         lambda m: m.prism_detector(["..C", ".A.", "T.."], "CAT"),
         [(2, 0, "D2")]),
    ],
    "py_word_ladder": [
        ('"hit", "cog", [..., "cog"]',
         lambda m: m.word_ladder(
             "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
        ('"hit", "cog", [...] sin "cog"',
         lambda m: m.word_ladder(
             "hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
        ('"a", "c", ["a", "b", "c"]',
         lambda m: m.word_ladder("a", "c", ["a", "b", "c"]), 2),
        ('"hit", "hot", ["hot"]',
         lambda m: m.word_ladder("hit", "hot", ["hot"]), 2),
    ],
}


def demasiado_tiempo(signum, frame):
    raise TimeoutError(
        f"tardó más de {SEGUNDOS_MAXIMOS} s (¿bucle infinito? "
        "¿se te olvidó avanzar el índice?)")


def comprobar(nombre):
    print(f"\n=== {nombre} ===")
    if not os.path.exists(nombre + ".py"):
        print(f"  No existe {nombre}.py en esta carpeta.")
        return False
    try:
        modulo = importlib.import_module(nombre)
    except Exception:
        print("  ERROR al cargar el fichero:")
        print(traceback.format_exc(limit=0))
        return False

    todo_bien = True
    for llamada, ejecutar, esperado in CASOS[nombre]:
        signal.alarm(SEGUNDOS_MAXIMOS)
        try:
            obtenido = ejecutar(modulo)
        except Exception as error:
            signal.alarm(0)
            print(f"  ERROR  {llamada}")
            print(f"         {type(error).__name__}: {error}")
            todo_bien = False
            continue
        signal.alarm(0)
        if obtenido == esperado and type(obtenido) is type(esperado):
            print(f"  OK     {llamada}")
        else:
            print(f"  FALLO  {llamada}")
            print(f"         esperado: {esperado!r}")
            print(f"         obtenido: {obtenido!r}")
            todo_bien = False
    return todo_bien


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.getcwd())
    signal.signal(signal.SIGALRM, demasiado_tiempo)

    if len(sys.argv) > 2:
        print("Uso: python3 comprobar.py [nombre_del_ejercicio]")
        return
    if len(sys.argv) == 2:
        nombre = sys.argv[1].removesuffix(".py")
        if nombre not in CASOS:
            print(f"No conozco '{nombre}'. Ejercicios válidos:")
            for valido in CASOS:
                print(f"  {valido}")
            return
        nombres = [nombre]
    else:
        nombres = [n for n in CASOS if os.path.exists(n + ".py")]
        if not nombres:
            print("Aún no hay ejercicios en practica/. Nombres válidos:")
            for valido in CASOS:
                print(f"  {valido}.py")
            return

    resultados = [comprobar(nombre) for nombre in nombres]
    print()
    if all(resultados):
        print("Todo correcto.")
    else:
        print("Hay fallos: revisa los pasos y trampas en GUIA.md.")


if __name__ == "__main__":
    main()
