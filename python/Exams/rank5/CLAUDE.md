# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

Practice material for the 42 Python "rank05" exam. Right now it contains only `subjects.md`: the
statements of the exam exercises, grouped by level. There is no code, build system, test runner or
git repository yet.

## Exercises (`subjects.md`)

| Level | Exercise | Required signature |
|-------|----------|--------------------|
| 1 | `py_compress_decompress` | `compress(s: str) -> str`, `decompress(s: str) -> str` |
| 1 | `py_spiral_matrix` | `generate_spiral(n: int) -> list[list[int]]` |
| 2 | `py_graph_cycle_detector` | `py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool` |
| 2 | `py_room_scheduler` | `py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]` |
| 2 | `py_island_matrix_counter` | `island_matrix_counter(matrix: list[list[str]]) -> int` |
| 3 | `py_prism_detector` | `prism_detector(grid: list[str], pattern: str)` |
| 3 | `py_word_ladder` | `word_ladder(start: str, end: str, sentence: list[str]) -> int` |

`subjects.md` is the source of truth: function names, signatures, edge cases (empty input) and the
exact output format must match it, because grading compares outputs literally. Details that are easy
to get wrong:

- `py_room_scheduler`: meetings are sorted by start time and placed in the first room that is free;
  the result keeps the per-room list of intervals, not only the count.
- `py_prism_detector`: tuples are `(x, y, code)` with `x` = column and `y` = row; direction vectors
  are `(dx, dy)`. Match order in the example is `"H"` before `"V"` for the same cell.
- `py_word_ladder`: the result counts words (start and end included), and `0` means no ladder.

## Working here

- `soluciones/` holds one reference solution per exercise (`<exercise>.py`, standard library only) and
  `test_ejemplos.py` (plain asserts: the subject examples plus a few edge cases). Run it with
  `cd soluciones && python3 test_ejemplos.py`. The exam does not check style (no flake8), so never review practice code for PEP 8.
- `practica/` is where the user rewrites exercises from memory. `python3 practica/comprobar.py [exercise]`
  checks them against the subject examples plus edge cases (per-case OK/FALLO/ERROR, 2 s timeout).
  When reviewing a practice file, point to the missed step in `GUIA.md` instead of handing over the solution.
- `GUIA.md` is the study guide: four shared patterns (index `while`, bounds check, pending list,
  recursion carrying the path) and, per exercise, a memory phrase, numbered steps and traps. Keep it
  in sync with `soluciones/` when a solution changes.
- The goal is exam recall, not elegance: the user must be able to rewrite each solution from memory.
  Prefer explicit loops, flags and small helper functions over comprehensions, `for/else`,
  `collections` or clever idioms, and reuse the same patterns across exercises. Explain in Spanish.
