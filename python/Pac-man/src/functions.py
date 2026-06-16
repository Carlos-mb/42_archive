from src.constants import Consts


def get_cell(x: int, y: int) -> tuple[int, int]:
    """Return the maze cell containing a pixel position.

    Args:
        x: Pixel x coordinate.
        y: Pixel y coordinate.

    Returns:
        The corresponding ``(row, col)`` cell indices.
    """

    col_index = x // Consts.CELL_SIZE
    row_index = y // Consts.CELL_SIZE

    return row_index, col_index


def get_cell_center(x: int, y: int) -> tuple[int, int]:
    """Return the pixel center of the cell containing a position.

    Args:
        x: Pixel x coordinate.
        y: Pixel y coordinate.

    Returns:
        The center of the corresponding cell as ``(x, y)``.
    """

    cell = get_cell(x, y)

    row_index, col_index = cell

    center_x = col_index * Consts.CELL_SIZE + Consts.CELL_SIZE // 2
    center_y = row_index * Consts.CELL_SIZE + Consts.CELL_SIZE // 2

    return center_x, center_y
