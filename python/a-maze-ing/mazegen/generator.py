"""
MazeGenerator reusable module.

Example usage:

    from mazegen.generator import MazeGenerator

    gen = MazeGenerator(rows=20, cols=20, seed=42)
    maze = gen.generate()

    path = gen.solve()

Access structure:

    maze.matrix
"""

from enum import IntFlag
import random
import collections
from typing import Callable


class Wall(IntFlag):
    """Bitmask flags representing walls of a maze cell.

    Values:
        N: North wall.
        E: East wall.
        S: South wall.
        W: West wall.
    """
    N = 1
    E = 2
    S = 4
    W = 8


class Cell:
    """Represent a single maze cell.

    Attributes:
        row (int): Row index.
        col (int): Column index.
        maze (Maze): Parent maze.
        visited (bool): Traversal state.
        walls (int): Bitmask of closed walls.
    """

    # Relative position of a cell according to N/E/S/W
    relative: dict[Wall, tuple[int, int]] = {
        Wall.N: (-1, 0),
        Wall.E: (0, +1),
        Wall.S: (+1, 0),
        Wall.W: (0, -1)
    }

    # List of oposite walls to simplify open neighbor's walls
    oposite_wall: dict[Wall, Wall] = {
        Wall.N: Wall.S,
        Wall.E: Wall.W,
        Wall.S: Wall.N,
        Wall.W: Wall.E
    }

    def __init__(self, row: int, col: int, maze: "MazeGenerator") -> None:
        """Initialize a cell.

        Args:
            row (int): Row index.
            col (int): Column index.
            maze (Maze): Parent maze reference.

        Returns:
            None
        """
        self.maze: MazeGenerator = maze
        self.row: int = row
        self.col: int = col

        self.visited: bool = False

        # Walls. Byte OR of 0001, 0010, 0100 and 1000
        self.walls: int = Wall.N | Wall.E | Wall.S | Wall.W

    def _notvisited(self) -> list["Cell"]:
        """Return unvisited neighbor cells excluding blocked pattern cells.

        Returns:
            list[Cell]: Unvisited adjacent cells.
        """
        neighbors: list[Cell] = []
        matrix: list[list[Cell]] = self.maze.matrix
        blocked = self.maze.coords42

        if self.row > 0:
            if (not matrix[self.row - 1][self.col].visited and
                    matrix[self.row - 1][self.col] not in blocked):
                neighbors.append(matrix[self.row - 1][self.col])
        if self.row < self.maze.rows - 1:
            if (not matrix[self.row + 1][self.col].visited and
                    matrix[self.row + 1][self.col] not in blocked):
                neighbors.append(matrix[self.row + 1][self.col])
        if self.col > 0:
            if (not matrix[self.row][self.col - 1].visited and
                    matrix[self.row][self.col - 1] not in blocked):
                neighbors.append(matrix[self.row][self.col - 1])
        if self.col < self.maze.cols - 1:
            if (not matrix[self.row][self.col + 1].visited and
                    matrix[self.row][self.col + 1] not in blocked):
                neighbors.append(matrix[self.row][self.col + 1])

        return (neighbors)

    def _open_wall(self, wall: Wall) -> None:
        """Open one wall in this cell and opposite wall in adjacent cell.

        Args:
            wall (Wall): Wall direction to open.

        Returns:
            None
        """
        # Get the neighbor coordinates using the wall position
        neighbor_row: int = self.row + Cell.relative[wall][0]
        neighbor_col: int = self.col + Cell.relative[wall][1]

        # If there is a valid neighbor
        if (self.maze._cell_exist(neighbor_row, neighbor_col)):

            # Open my wall
            self.walls &= ~wall  # Open the wall doing "and not wall.X"

            # Open neighbor's wall
            self.maze.matrix[neighbor_row][neighbor_col].walls\
                &= ~self.oposite_wall[wall]

    def _able_neighbors(self) -> list["Cell"]:
        """Return traversable unvisited neighbors via open walls.

        Returns:
            list[Cell]: Reachable adjacent cells.
        """
        neighbors: list[Cell] = []
        matrix: list[list[Cell]] = self.maze.matrix

        # walls = 0101
        # N     = 0001
        # walls & N == wall exist

        if ((self.row > 0) and not (self.walls & Wall.N) and
            not matrix[self.row - 1][self.col].visited and
                matrix[self.row - 1][self.col] not in self.maze.coords42):
            neighbors.append(matrix[self.row - 1][self.col])
        if ((self.row < self.maze.rows - 1) and not (self.walls & Wall.S) and
            not matrix[self.row + 1][self.col].visited and
                matrix[self.row + 1][self.col] not in self.maze.coords42):
            neighbors.append(matrix[self.row + 1][self.col])
        if ((self.col > 0) and not (self.walls & Wall.W) and
            not matrix[self.row][self.col - 1].visited and
                matrix[self.row][self.col - 1] not in self.maze.coords42):
            neighbors.append(matrix[self.row][self.col - 1])
        if ((self.col < self.maze.cols - 1) and not (self.walls & Wall.E) and
            not matrix[self.row][self.col + 1].visited and
                matrix[self.row][self.col + 1] not in self.maze.coords42):
            neighbors.append(matrix[self.row][self.col + 1])

        return neighbors

    def to_hex(self) -> str:
        return format(int(self.walls), "X")


class MazeGenerator:
    """Generate, mutate, and solve a maze.

    Attributes:
        rows (int): Number of rows.
        cols (int): Number of columns.
        matrix (list[list[Cell]]): Grid of cells.
        entry (tuple[int, int]): Start coordinate.
        exit (tuple[int, int]): End coordinate.
    """

    def __init__(
        self,
        rows: int = 10,
        cols: int = 10,
        seed: int = 94,
        perfect: bool = True,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] | None = None
    ) -> None:
        """Initialize maze grid and generation options.

        Args:
            rows (int): Row count.
            cols (int): Column count.
            seed (int): RNG seed.
            perfect (bool): Whether maze remains perfect.
            entry (tuple[int, int]): Entry coordinate.
            exit (tuple[int, int] | None): Exit coordinate or
                                            default bottom-right.

        Returns:
            None
        """
        if cols < 2:
            raise ValueError("Cols must be >= 2")
        if rows < 2:
            raise ValueError("Rows must be >= 2")
        self.__rows: int = rows
        self.__cols: int = cols
        self.rnd: random.Random = random.Random(seed)
        self.perfect: bool = perfect
        self.matrix: list[list[Cell]] = (
            [[Cell(row=row, col=col, maze=self)
              for col in range(cols)]
                for row in range(rows)])
        self.showdraw: Callable | None = None
        self.shortest_path: list[Cell] = []
        self.__coords42: list[Cell] = []
        self.__entry: tuple[int, int] = entry
        if exit is None:
            self.__exit: tuple[int, int] = (rows - 1, cols - 1)
        else:
            self.__exit = exit
        self.directions: str = ""

        self.pattern: list[tuple[int, int]] = [
            (-2, -2),           (-2, +1), (-2, +2),
            (-1, -2),                     (-1, +2),
            (+0, -2), (+0, -1), (+0, +1), (+0, +2),
                      (+1, -1), (+1, +1),
                      (+2, -1), (+2, +1), (+2, +2)
        ]

    @property
    def entry(self) -> tuple[int, int]:
        return self.__entry

    @entry.setter
    def entry(self, entry: tuple[int, int]) -> None:

        row, col = entry
        if (self._cell_exist(row, col)) and entry != self.__exit:
            self.__entry = entry
        else:
            raise ValueError("Entry not asignable in those coordinates")

    @property
    def exit(self) -> tuple[int, int]:
        return self.__exit

    @exit.setter
    def exit(self, exit: tuple[int, int]) -> None:

        row, col = exit
        if (self._cell_exist(row, col)) and exit != self.__entry:
            self.__exit = exit
        else:
            raise ValueError("Exit not asignable in those coordinates")

    @property
    def coords42(self) -> list[Cell]:
        return self.__coords42

    @property
    def rows(self) -> int:
        return self.__rows

    @rows.setter
    def rows(self, rows: int) -> None:
        if rows < 2:
            raise ValueError("Rows must be >= 2")
        if self.entry[0] >= rows or self.exit[0] >= rows:
            raise ValueError("Entry/exit point is outside new maze bounds")
        if self.__rows != rows:
            self.__rows = rows
            self._resize()

    @property
    def cols(self) -> int:
        return self.__cols

    @cols.setter
    def cols(self, cols: int) -> None:
        if cols < 2:
            raise ValueError("Cols must be >= 2")
        if self.entry[1] >= cols or self.exit[1] >= cols:
            raise ValueError("Entry/exit point is outside new maze bounds")
        if self.cols != cols:
            self.__cols = cols
            self._resize()

    def _resize(self) -> None:
        """Resize the maze matrix based on current rows and cols.

        Returns:
            None
        """
        self.matrix = (
            [[Cell(row=row, col=col, maze=self)
              for col in range(self.__cols)]
                for row in range(self.__rows)])
        self.__coords42 = []
        self.shortest_path = []
        self.directions = ""

        self._do_perfect()
        if not self.perfect:
            self._unperfect()

    def _cell_exist(self, row: int, col: int) -> bool:
        """Check whether a coordinate is inside bounds and not blocked.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: `True` if the coordinate is valid.
        """
        return (row >= 0 and col >= 0 and
                row < self.__rows and col < self.__cols
                and self.matrix[row][col] not in self.__coords42)

    def _connect(self, origin: Cell, destination: Cell) -> None:
        """Open wall between two adjacent cells.

        Args:
            origin (Cell): Source cell.
            destination (Cell): Adjacent destination cell.

        Returns:
            None
        """
        if destination.row > origin.row:
            origin._open_wall(Wall.S)
        elif destination.row < origin.row:
            origin._open_wall(Wall.N)
        elif destination.col > origin.col:
            origin._open_wall(Wall.E)
        elif destination.col < origin.col:
            origin._open_wall(Wall.W)
        else:
            raise ValueError("Cells are not adjacent")

    def _tunnel(self, cell: Cell) -> None:
        """Recursively carve maze passages from a cell.

        Args:
            cell (Cell): Current cell.

        Returns:
            None
        """
        cell.visited = True
        neighbors: list[Cell] = cell._notvisited()

        if self.showdraw:
            self.showdraw()

        if len(neighbors) > 0:
            dest: Cell = self.rnd.choice(neighbors)
            self._connect(cell, dest)
            self._tunnel(dest)

    def _pending_neighbors(self) -> list[Cell]:
        """Collect visited cells that still have unvisited neighbors.

        Returns:
            list[Cell]: Candidate cells to continue carving.
        """
        notvisited: list[Cell] = []
        for row in self.matrix:
            for cell in row:
                # If cell exist, is visited and had no visited neighbors
                if cell.visited and cell not in self.__coords42:
                    if len(cell._notvisited()) > 0:
                        if cell not in self.__coords42:
                            notvisited.append(cell)
        return list(notvisited)

    def _unperfect(self) -> None:
        """Open extra walls to make the maze imperfect.

        Returns:
            None
        """

        changed: bool = False

        # Enumarete generates a tupla of pairs [0, value1], [1, value2]
        for i, row in enumerate(self.matrix):  # [1:-1]
            if i % 2 == 0:
                cell: Cell = self.rnd.choice(row)  # [1:-1]
                while cell in self.__coords42:
                    cell = self.rnd.choice(row)  # [1:-1]
                closed: list[Wall] = [
                    wall for wall in Wall if cell.walls & wall]
                if closed:
                    # cell._open_wall(self.rnd.choice(closed))
                    walls = cell.walls
                    cell._open_wall(self.rnd.choice(closed))
                    changed = walls != cell.walls

        if not changed:  # Extreme situations
            for row in self.matrix:
                for cell in row:
                    if cell not in self.__coords42:
                        walls = cell.walls
                        cell._open_wall(Wall.N)
                        cell._open_wall(Wall.E)
                        cell._open_wall(Wall.S)
                        cell._open_wall(Wall.W)
                        changed = walls != cell.walls
                        if changed:
                            return

    def _do_perfect(self) -> None:
        """Generate a perfect maze.

        Returns:
            None
        """

        self._draw42(((self.__rows - 1) // 2, (self.__cols - 1) // 2))

        start: Cell = self.rnd.choice(
            [cell for row in self.matrix for cell in row
             if cell not in self.coords42])

        self._tunnel(start)

        # while any(not cell.visited for row in self.matrix for cell in row):
        pendings: list[Cell] = self._pending_neighbors()
        while pendings:
            self._tunnel(self.rnd.choice(pendings))
            pendings = self._pending_neighbors()

    def generate(self) -> "MazeGenerator":
        """Regenerate maze with current dimensions/options.

        Returns:
            None
        """
        # self.rnd = random.Random()
        self.matrix = (
            [[Cell(row=row, col=col, maze=self)
              for col in range(self.__cols)]
                for row in range(self.__rows)])
        self._do_perfect()
        if not self.perfect:
            self._unperfect()

        return self

    def solve(self) -> None:
        """Calculate shortest path from entry to exit.

        Returns:
            None
        """
        for row in self.matrix:
            for cell in row:
                cell.visited = False

        current: Cell = self.matrix[self.entry[0]][self.entry[1]]

        parents: dict[Cell, Cell] = {}
        queue: collections.deque[Cell] = collections.deque()

        queue.append(current)
        current.visited = True
        if current == self.matrix[self.exit[0]][self.exit[1]]:
            queue.clear()

        while queue:
            if self.showdraw:
                path: list[Cell] = [current]
                while parents.get(current, False):
                    path.append(parents[current])
                    current = parents[current]
                self.showdraw(current, path=path)

            current = queue.popleft()
            neighbors: list[Cell] = current._able_neighbors()
            if neighbors:
                for next in neighbors:
                    queue.append(next)
                    next.visited = True
                    parents[next] = current
                    if next == self.matrix[self.exit[0]][self.exit[1]]:
                        current = next
                        queue.clear()
                        break

        # create and draw path
        path = [current]
        while parents.get(current, False):
            path.append(parents[current])
            current = parents[current]

        # self.draw(path=path)

        # Create directions from path
        directions: str = ""
        for i in range(len(path) - 1, 0, -1):  # reverse range: start,stop,step
            a: Cell = path[i]
            b: Cell = path[i - 1]

            diff: tuple[int, int] = (b.row - a.row, b.col - a.col)

            for wall, rel in Cell.relative.items():
                if rel == diff:
                    wall_name: str | None = wall.name
                    if wall_name:
                        directions += (wall_name)
                    break

        self.directions = directions
        self.shortest_path = path

    def _try_to_draw42(self, center: tuple[int, int]) -> None:
        """Try placing the 42-pattern obstacle centered at given coordinates.

        Args:
            center (tuple[int, int]): Candidate center coordinate.

        Returns:
            None
        """

        pattern = self.pattern

        r: int
        c: int
        r, c = center
        if (self.__cols - c < 4 or
                self.__rows - r < 4):
            return
        self.__coords42 = []
        for dr, dc in pattern:
            rr: int = r + dr
            cc: int = c + dc
            if self._cell_exist(rr, cc):
                self.__coords42.append(self.matrix[rr][cc])
            else:
                self.__coords42 = []
                break

    def _draw42(self, center: tuple[int, int]) -> None:
        """Place a valid 42-pattern obstacle while preserving entry/exit.

        Args:
            center (tuple[int, int]): Preferred center coordinate.

        Returns:
            None
        """
        self._try_to_draw42(center)

        for coord in self.__coords42:  # only enter if 42 has been drawed
            if ((coord.row, coord.col) == self.entry or
                    (coord.row, coord.col) == self.exit):
                self.__coords42 = []

                for row in self.matrix:  # no [3:] -> Good for any pattern size
                    for cell in row:
                        self._try_to_draw42((cell.row, cell.col))

                        for coord in self.__coords42:
                            if ((coord.row, coord.col) == self.entry or
                                    (coord.row, coord.col) == self.exit):
                                self.__coords42 = []
                                break

                        if len(self.__coords42) > 0:
                            break
                    if len(self.__coords42) > 0:
                        break
                break
        for cell in self.__coords42:
            cell.visited = True
