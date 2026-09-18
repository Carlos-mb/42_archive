def generate_spiral(n: int) -> list[list[int]]:
    matrix = []
    for _ in range(n):
        matrix.append([0] * n)

    # derecha, abajo, izquierda, arriba
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d = 0
    row = 0
    col = 0
    for number in range(1, n * n + 1):
        matrix[row][col] = number
        next_row = row + moves[d][0]
        next_col = col + moves[d][1]
        if (next_row < 0 or next_row >= n or next_col < 0 or next_col >= n
                or matrix[next_row][next_col] != 0):
            d = (d + 1) % 4
            next_row = row + moves[d][0]
            next_col = col + moves[d][1]
        row = next_row
        col = next_col
    return matrix
