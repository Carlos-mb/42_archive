# Level 1
## py_compress_decompress

Write two functions: `compress` and `decompress`.

`compress(s: str) -> str`:
- Takes a string and compresses consecutive repeated characters by appending the count after the character.
- If a character appears only once consecutively, omit the number '1'.
- If the input string is empty, return an empty string.

`decompress(s: str) -> str`:
- Takes a compressed string and expands it back to its uncompressed form.
- Handles multi-digit counts (e.g., "a12" -> 12 'a's).
- If no count follows a character, it counts as 1.

Function signature

def compress(s: str) -> str:

Examples
Input
compress("aabcccccaaa")
Output
"a2bc5a3"
Input
decompress("a2bc5a3")
Output
"aabcccccaaa"
Input
compress("")
Output
""

## py_spiral_matrix

Write a function that generates an `n x n` 2D matrix filled with numbers from 1 to `n^2` in clockwise spiral order.

The spiral starts at the top-left cell (0, 0) moving right, then down, then left, then up, continuing inwards.

Function signature

def generate_spiral(n: int) -> list[list[int]]:

Examples
Input
generate_spiral(3)
Output
[[1, 2, 3], [8, 9, 4], [7, 6, 5]]
Input
generate_spiral(1)
Output
[[1]]

# Level 2
## py_graph_cycle_detector

Write a function that determines whether a directed graph contains at least one cycle.

The function takes a dictionary representing an adjacency list where keys are integer node IDs and values are lists of integer neighbor node IDs.

The function should:
- Return True if the directed graph contains a cycle.
- Return False if the graph is acyclic or if the input graph dictionary is empty.
- Correctly handle graphs with multiple disconnected components.

Function signature

def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:

Examples
Input
py_graph_cycle_detector({0: [1], 1: [2], 2: [0]})
Output
True
Input
py_graph_cycle_detector({0: [1], 1: [2], 2: []})
Output
False
Input
py_graph_cycle_detector({})
Output
False

## py_room_scheduler

Each meeting is represented as a list of two integers `[start_time, end_time]`.

The function should:
- Sort meetings by start time and assign them to available rooms sequentially.
- Return a dictionary containing:
  - `"total_rooms"`: the integer count of rooms required.
  - `"schedule"`: a list of lists containing the scheduled intervals for each room.
- If the input list is empty, return `{"total_rooms": 0, "schedule": []}`.

Function signature

def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:

Examples
Input
py_room_scheduler([[0, 30], [5, 10], [15, 20]])
Output
{"total_rooms": 2, "schedule": [[[0, 30]], [[5, 10], [15, 20]]]}
Input
py_room_scheduler([])
Output
{"total_rooms": 0, "schedule": []}

## py_island_matrix_counter

Write a function island_matrix_counter(matrix) that receives a 2D matrix containing "1" and "0" string values and returns the total number of islands.

An island is a group of connected "1" cells. Cells are considered connected only when they are directly adjacent horizontally (left, right) or vertically (up, down). Diagonal cells do not count as connected.

Requirements:
- "1" represents land.
- "0" represents water.
- Count each separate island exactly once.
- An empty matrix (or matrix with no rows) should return 0.
- DFS/BFS traversal or matrix mutation can be used to explore each complete island.

Function signature

def island_matrix_counter(matrix: list[list[str]]) -> int:

Examples
Input
island_matrix_counter([["1", "1", "1", "1", "0"], ["1", "1", "1", "0", "0"], ["1", "1", "1", "1", "0"], ["0", "0", "0", "0", "0"]])
Output
1
Input
island_matrix_counter([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]])
Output
3
Input
island_matrix_counter([])
Output
0

# Level 3

## py_prism_detector

Write a function that searches for all occurrences of a target word pattern within a 2D grid of characters in all 8 cardinal and diagonal directions.

The directions and their codes are:
- (1, 0) -> "H" (Horizontal right)
- (-1, 0) -> "H-" (Horizontal left)
- (0, 1) -> "V" (Vertical down)
- (0, -1) -> "V-" (Vertical up)
- (1, 1) -> "D1" (Diagonal down-right)
- (-1, -1) -> "D1-" (Diagonal up-left)
- (-1, 1) -> "D2" (Diagonal up-right)
- (1, -1) -> "D2-" (Diagonal down-left)

The function should:
- Take a grid of strings `grid` and a target string `pattern`.
- Return a list of tuples `(x, y, direction_code)` for each match, where `x` is the column index and `y` is the row index of the first character.
- Return an empty list `[]` if either `grid` or `pattern` is empty.

Function signature

def prism_detector(grid: list[str], pattern: str):

Examples
Input
prism_detector(["CAT", "A..", "T.."], "CAT")
Output
[(0, 0, "H"), (0, 0, "V")]
Input
prism_detector([], "CAT")
Output
[]

## py_word_ladder

Write a function that computes the length of the shortest transformation sequence from a `start` word to an `end` word using a dictionary list of allowed words `sentence`.

Each transformation step must change exactly one single character. All intermediate words must exist in `sentence`.

The function should:
- Return the total number of words in the shortest ladder (including `start` and `end`).
- Return 0 if no transformation sequence is possible.

Function signature

def word_ladder(start: str, end: str, sentence: list[str]) -> int:

Examples
Input
word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
Output
5
Input
word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"])
Output
0