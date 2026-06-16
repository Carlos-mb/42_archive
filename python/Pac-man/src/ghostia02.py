from typing import TYPE_CHECKING, Callable
from src.functions import get_cell
from src.constants import Consts
from src.people import Ghost, Player

if TYPE_CHECKING:
    from src.game import GameGenerator


class GhostIa02:
    """Choose ghost targets using a simple greedy chase strategy."""

    def __init__(
        self,
        ghost: Ghost,
        player: Player,
        game: "GameGenerator",
    ) -> None:
        """Create the ghost AI.

        Args:
            ghost: Ghost controlled by this AI.
            player: Player chased by the ghost.
            game: Current game instance.
        """
        self.ghost = ghost
        self.player = player
        self.game = game

        self.default_chase: Callable[[int, int], tuple[int, int]]
        self.default_chase = ghost.chase

        self.target: tuple[int, int]

        current_cell = get_cell(self.ghost.x, self.ghost.y)

        self.last_cell: tuple[int, int] | None = current_cell
        self.previous_cell: tuple[int, int] | None = None

        if current_cell is None:
            self.target = (player.x, player.y)
        else:
            self.target = self.cell_center(*current_cell)

    def chase(self, px: int, py: int) -> tuple[int, int]:
        """Return the movement needed to chase the player.

        Args:
            px: Player x coordinate.
            py: Player y coordinate.

        Returns:
            Suggested ghost movement as ``(movx, movy)``.
        """
        current_cell = get_cell(self.ghost.x, self.ghost.y)

        if current_cell is None:
            return 0, 0

        current_center = self.cell_center(*current_cell)

        if self.is_near(current_center):
            if current_cell != self.last_cell:
                self.previous_cell = self.last_cell
                self.last_cell = current_cell

            self.target = self.choose_best_target(
                current_cell,
                px,
                py,
            )

        return self.default_chase(*self.target)

    def choose_best_target(
        self,
        current_cell: tuple[int, int],
        px: int,
        py: int,
    ) -> tuple[int, int]:
        """Choose the next neighbour cell that gets closer to the player.

        Args:
            current_cell: Current ghost cell as ``(row, col)``.
            px: Player x coordinate.
            py: Player y coordinate.

        Returns:
            Center of the chosen neighbour cell.
        """
        exits = self.directions(current_cell)

        if len(exits) == 0:
            return self.cell_center(*current_cell)

        if len(exits) > 1 and self.previous_cell is not None:
            previous_center = self.cell_center(*self.previous_cell)

            if previous_center in exits:
                exits.remove(previous_center)

        return min(
            exits,
            key=lambda exit_pos: self.distance(exit_pos, (px, py)),
        )

    def directions(
        self,
        cell_pos: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return the reachable neighbour cell centers.

        Args:
            cell_pos: Current cell as ``(row, col)``.

        Returns:
            List of neighbour cell centers reachable without crossing a wall.
        """
        row_index, col_index = cell_pos

        if row_index < 0 or row_index >= len(self.game.maze.maze):
            return []

        if col_index < 0:
            return []

        if col_index >= len(self.game.maze.maze[row_index]):
            return []

        north = 1
        east = 2
        south = 4
        west = 8

        cell = self.game.maze.maze[row_index][col_index]
        row_count = len(self.game.maze.maze)
        col_count = len(self.game.maze.maze[row_index])

        destinations: list[tuple[int, int]] = []

        if col_index > 0 and (cell & west) == 0:
            destinations.append(
                self.cell_center(row_index, col_index - 1),
            )

        if col_index < col_count - 1 and (cell & east) == 0:
            destinations.append(
                self.cell_center(row_index, col_index + 1),
            )

        if row_index > 0 and (cell & north) == 0:
            destinations.append(
                self.cell_center(row_index - 1, col_index),
            )

        if row_index < row_count - 1 and (cell & south) == 0:
            destinations.append(
                self.cell_center(row_index + 1, col_index),
            )

        return destinations

    def cell_center(self, row: int, col: int) -> tuple[int, int]:
        """Return the pixel center of a maze cell.

        Args:
            row: Maze row.
            col: Maze column.

        Returns:
            Cell center as ``(x, y)``.
        """
        return (
            col * Consts.CELL_SIZE + Consts.CELL_SIZE // 2,
            row * Consts.CELL_SIZE + Consts.CELL_SIZE // 2,
        )

    def is_near(self, target: tuple[int, int]) -> bool:
        """Return True if the ghost is close enough to a target point.

        Args:
            target: Target position as ``(x, y)``.

        Returns:
            True if the ghost is close to the target.
        """
        return (
            abs(self.ghost.x - target[0]) <= self.ghost.speed
            and abs(self.ghost.y - target[1]) <= self.ghost.speed
        )

    def distance(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> int:
        """Return the Manhattan distance between two positions.

        Args:
            first: First position as ``(x, y)``.
            second: Second position as ``(x, y)``.

        Returns:
            Manhattan distance.
        """
        return abs(first[0] - second[0]) + abs(first[1] - second[1])
