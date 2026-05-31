""" 
Write a function called draw_constellation that takes a list of coordinates (tuples) 
and an integer representing the size of a square grid. 
The function should return a list of strings representing a visual "map" of stars.

The grid is a square of size x size.

If a coordinate (y, x) exists in the stars list, that position in the grid should be represented by an asterisk (*).

If no star exists at that coordinate, the position should be represented by a period (.).

The function must return a list of strings, where each string represents one row of the grid.

Assume coordinates in the list are within the bounds of the grid size.


>>> draw_constellation([(0, 0), (1, 1), (2, 2)], 4)
['*...', '.*..', '..*.', '....']

>>> draw_constellation([(0, 1), (0, 2), (1, 1)], 3)
['.**', '.*.', '...']

>>> draw_constellation([], 2)
['..', '..']

 """


def draw_constellation(l: list[tuple[int, int]], gsize: int) -> list[str]:

    const = []
    for i in range(gsize):
        const.append(["."] * gsize)

    for x, y in l:
        const[x][y] = "*"

    out = []
    for row in const:
        out.append("".join(row))

    return out

def draw_constellation2(stars: list[tuple[int, int]], size: int) -> list[str]:
    """
    1. make a matrix
    2. for each row and colom in stars, if r and c are in range
    3. put a star there
    4. use join to add each row to the grid
    """
    grid = [['.' for _ in range(size)] for _ in range(size)]
    for r, c in stars:
        if size > r >= 0 and size > c >= 0:
            grid[r][c] = "*"
    result = ["".join(r) for r in grid]
    return result


print(draw_constellation([(0, 0), (1, 1), (2, 2)], 4))
print(draw_constellation2([(0, 0), (1, 1), (2, 2)], 4))
print("['*...', '.*..', '..*.', '....']")
print()

print(draw_constellation([(0, 1), (0, 2), (1, 1)], 3))
print(draw_constellation2([(0, 1), (0, 2), (1, 1)], 3))
print("['.**', '.*.', '...']")
print()

print(draw_constellation([], 2))
print(draw_constellation2([], 2))
print("['..', '..']")
