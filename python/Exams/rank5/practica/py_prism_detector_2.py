def prism_detector(grid: list[str], pattern: str):
    DIRECTIONS = [
        (1, 0, "H"), (-1, 0, "H-"),
        (0, 1, "V"), (0, -1, "V-"),
        (1, 1, "D1"), (-1, -1, "D1-"),
        (-1, 1, "D2"), (1, -1, "D2-"),
]

    result = []
    if not grid or not pattern:
        return result
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            for dx, dy, code in DIRECTIONS:
                if matches(grid, pattern, x, y, dx, dy):
                    result.append((x, y, code))
    return result


def matches(grid: list[str], pattern: str, x: int, y: int,
            dx: int, dy: int) -> bool:
    for i in range(len(pattern)):
        cx = x + (dx * i)
        cy = y + (dy * i)
        try:
            if grid[cy][cx] != pattern[i]:
                return False
        except:
            return False
    return True


prism_detector(["CAT", "A..", "T.."], "CAT")    # [(0, 0, "H"), (0, 0, "V")]
prism_detector([], "CAT")                       # []

try:
    resultado = prism_detector(["CAT", "A..", "T.."], "CAT")
    print("OK #1" if resultado == [(0, 0, "H"), (0, 0, "V")] else "ERROR #1")
except Exception:
    print("ERROR #1")

try:
    resultado = prism_detector([], "CAT")
    print("OK #2" if resultado == [] else "ERROR #2")
except Exception:
    print("ERROR #2")

try:
    resultado = prism_detector(["CAT"], "")
    print("OK #3" if resultado == [] else "ERROR #3")
except Exception:
    print("ERROR #3")

try:
    resultado = prism_detector(["TAC"], "CAT")
    print("OK #4" if resultado == [(2, 0, "H-")] else "ERROR #4")
except Exception:
    print("ERROR #4")

try:
    resultado = prism_detector(["C..", ".A.", "..T"], "CAT")
    print("OK #5" if resultado == [(0, 0, "D1")] else "ERROR #5")
except Exception:
    print("ERROR #5")

try:
    resultado = prism_detector(["T", "A", "C"], "CAT")
    print("OK #6" if resultado == [(0, 2, "V-")] else "ERROR #6")
except Exception:
    print("ERROR #6")

try:
    resultado = prism_detector(["AB", "C"], "XYZ")
    print("OK #7" if resultado == [] else "ERROR #7")
except Exception:
    print("ERROR #7")

try:
    resultado = prism_detector(["." * 100 for _ in range(100)], "CAT")
    print("OK #8" if resultado == [] else "ERROR #8")
except Exception:
    print("ERROR #8")

try:
    resultado = prism_detector(["CAT"], "CATS")
    print("OK #9" if resultado == [] else "ERROR #9")
except Exception:
    print("ERROR #9")