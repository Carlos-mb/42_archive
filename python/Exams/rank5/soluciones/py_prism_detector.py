DIRECTIONS = [
    (1, 0, "H"), (-1, 0, "H-"),
    (0, 1, "V"), (0, -1, "V-"),
    (1, 1, "D1"), (-1, -1, "D1-"),
    (-1, 1, "D2"), (1, -1, "D2-"),
]


def prism_detector(grid: list[str], pattern: str):
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
        cx = x + dx * i
        cy = y + dy * i
        if cy < 0 or cy >= len(grid) or cx < 0 or cx >= len(grid[cy]):
            return False
        if grid[cy][cx] != pattern[i]:
            return False
    return True
