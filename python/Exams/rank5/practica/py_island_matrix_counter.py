def island_matrix_counter(matrix: list[list[str]]):

    count=0
    
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == "1": # ¡Ojo! es un string
                count += 1        
                hundir(matrix,row, col)
    return count

def hundir(matrix, row, col):
    try:
        if matrix[row + 1][col] == "1":
            hundir(matrix, row + 1, col)
    except:
        pass

    try:
        if matrix[row][col + 1] == "1":
            hundir(matrix, row, col + 1)
    except:
        pass

    matrix[row][col] = "0"



print(
    island_matrix_counter([["1", "1", "1", "1", "0"],
                       ["1", "1", "1", "0", "0"],
                       ["1", "1", "1", "1", "0"],
                       ["0", "0", "0", "0", "0"]])    # 1
)

print(
    island_matrix_counter([["1", "1", "0", "0", "0"],
                       ["1", "1", "0", "0", "0"],
                       ["0", "0", "1", "0", "0"],
                       ["0", "0", "0", "1", "1"]])    # 3
                       )
print(
    island_matrix_counter([])                             # 0
    )