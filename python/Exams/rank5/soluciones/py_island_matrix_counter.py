def island_matrix_counter(matrix: list[list[str]]) -> int:
    count = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == "1":
                count += 1
                sink(matrix, row, col)
    return count


def sink(matrix: list[list[str]], row: int, col: int) -> None:
    pending = [(row, col)]
    while pending:
        row, col = pending.pop()
        if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[row]):
            continue
        if matrix[row][col] != "1":
            continue
        matrix[row][col] = "0"
        pending.append((row + 1, col))
        pending.append((row - 1, col))
        pending.append((row, col + 1))
        pending.append((row, col - 1))
