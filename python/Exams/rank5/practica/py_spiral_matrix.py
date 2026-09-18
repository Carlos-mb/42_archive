def generate_spiral(n: int) -> list[list[int]]:

    matrix = []

    for _ in range(n):
        matrix.append([0]*n)

    fin = n * n
    fin += 1

    row = 0
    col = 0
    moves = [(0,1), (1,0), (0,-1), (-1, 0)]
    d = 0

    i = 1
    while i < fin:
        matrix[row][col] = i
        nextr = row + moves[d][0]
        nextc = col + moves[d][1]
        if (nextr < 0 or
            nextc < 0 or
            nextr >= n or
            nextc >= n or
            matrix[nextr][nextc] != 0):
            d = d + 1 if d < 3 else 0
            nextr = row + moves[d][0]
            nextc = col + moves[d][1]
        row = nextr
        col = nextc
        i += 1

    return matrix