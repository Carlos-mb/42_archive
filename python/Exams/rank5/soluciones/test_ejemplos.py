from py_compress_decompress import compress, decompress
from py_spiral_matrix import generate_spiral
from py_graph_cycle_detector import py_graph_cycle_detector
from py_room_scheduler import py_room_scheduler
from py_island_matrix_counter import island_matrix_counter
from py_prism_detector import prism_detector
from py_word_ladder import word_ladder

# Ejemplos de subjects.md
assert compress("aabcccccaaa") == "a2bc5a3"
assert decompress("a2bc5a3") == "aabcccccaaa"
assert compress("") == ""
assert generate_spiral(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
assert generate_spiral(1) == [[1]]
assert py_graph_cycle_detector({0: [1], 1: [2], 2: [0]}) is True
assert py_graph_cycle_detector({0: [1], 1: [2], 2: []}) is False
assert py_graph_cycle_detector({}) is False
assert py_room_scheduler([[0, 30], [5, 10], [15, 20]]) == {
    "total_rooms": 2, "schedule": [[[0, 30]], [[5, 10], [15, 20]]]}
assert py_room_scheduler([]) == {"total_rooms": 0, "schedule": []}
assert island_matrix_counter([["1", "1", "1", "1", "0"], ["1", "1", "1", "0", "0"],
                              ["1", "1", "1", "1", "0"], ["0", "0", "0", "0", "0"]]) == 1
assert island_matrix_counter([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
                              ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]) == 3
assert island_matrix_counter([]) == 0
assert prism_detector(["CAT", "A..", "T.."], "CAT") == [(0, 0, "H"), (0, 0, "V")]
assert prism_detector([], "CAT") == []
assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0

# Casos extra
assert decompress("a12") == "a" * 12
assert compress(decompress("x10yz3")) == "x10yz3"
assert generate_spiral(4) == [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]
assert generate_spiral(0) == []
assert py_graph_cycle_detector({0: [0]}) is True
assert py_graph_cycle_detector({0: [1], 1: [], 2: [3], 3: [2]}) is True
assert py_graph_cycle_detector({0: [1, 2], 1: [3], 2: [3], 3: []}) is False
assert py_room_scheduler([[5, 10], [0, 5]]) == {"total_rooms": 1, "schedule": [[[0, 5], [5, 10]]]}
assert island_matrix_counter([["1"] * 60 for _ in range(60)]) == 1
assert prism_detector(["TAC"], "CAT") == [(2, 0, "H-")]
print("OK: todos los ejemplos pasan")
