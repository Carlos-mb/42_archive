from typing import TYPE_CHECKING, Callable
import random

from src.constants import Consts
from src.functions import get_cell
from src.people import Ghost, Player

if TYPE_CHECKING:
    from src.game import GameGenerator


class GhostIa01():
    """Ghost AI that mixes target chasing with light random exploration."""

    def __init__(self, ghost: Ghost, player: Player, game: "GameGenerator"):
        """Create the AI controller.

        Args:
            ghost: Ghost controlled by this AI.
            player: Player used as the chase target.
            game: Active game instance.
        """
        self.ghost: Ghost = ghost
        self.player: Player = player
        self.game: GameGenerator = game
        self.default_chase: Callable = ghost.chase

        self.last_pos: tuple[int, int] = self.ghost.x, self.ghost.y
        self.target: tuple[int, int] = (player.x, player.y)

        self.focused: bool = True
        self.last_visited: list = []
        self.last_positions: list = []

    def chase(self, px: int, py: int) -> tuple[int, int]:
        """Return a movement vector toward the current ghost target.

        Args:
            px: Player x coordinate.
            py: Player y coordinate.

        Returns:
            A suggested movement vector as ``(movx, movy)``.
        """
        pos = (self.ghost.x, self.ghost.y)
        cur_cell = get_cell(*pos)

        exits = self.directions()

        if len(exits) == 1:
            self.target = exits[0]

        dx, dy = self.default_chase(*self.target)
        x, y = self.game.try_to_move(self.ghost, dx, dy)

        if x == self.ghost.x and y == self.ghost.y:
            exits = self.directions(True)
            if self.cell_center(*self.ghost.last_cell) in exits:
                exits.remove(self.cell_center(*self.ghost.last_cell))

            selected = False
            for target in exits:
                if get_cell(*target) not in self.last_visited:
                    self.target = target
                    selected = True
                    break
            if not selected:
                self.target = random.choice(exits)
                self.focused = True
                self.last_visited = []
                self.target = (px, py)

            dx, dy = self.default_chase(*self.target)
            return dx, dy

        ontarget = get_cell(pos[0], pos[1]) == get_cell(
            self.target[0],
            self.target[1],
        )

        if len(self.last_positions) >= 2 and pos == self.last_positions[0]:
            self.last_positions = []
            self.focused = False
            ontarget = True

        self.last_positions.append(pos)
        if len(self.last_positions) > 2:
            self.last_positions.pop(0)

        if not self.focused or ontarget:
            if ontarget or (
                self.ghost.last_cell != cur_cell and len(exits) > 2
            ):
                selected = False
                exits = self.directions(True)

                if int(random.random() * 3) == 0:
                    self.target = (px, py)
                    self.last_visited = []
                    self.focused = True
                    dx, dy = self.default_chase(*self.target)
                else:
                    tmp_target = self.target
                    for target in exits:
                        if get_cell(*target) not in self.last_visited:
                            tmp_target = target
                            selected = True
                            break
                    if not selected:
                        tmp_target = random.choice(exits)
                    if ontarget:
                        self.target = tmp_target
                    dx, dy = self.default_chase(*tmp_target)

        if cur_cell != self.ghost.last_cell:
            if len(self.last_visited) >= 15:
                self.last_visited.pop(0)
            self.last_visited.append(cur_cell)

        if int(random.random() * 1000) == 1:
            self.focused = not self.focused
            self.focused = True
            self.last_visited = []
            if self.focused:
                self.target = (px, py)

        return dx, dy

    def cell_center(self, row: int, col: int) -> tuple[int, int]:
        """Return the pixel center of a maze cell.

        Args:
            row: Maze row.
            col: Maze column.

        Returns:
            The cell center as ``(x, y)``.
        """
        return (
            col * Consts.CELL_SIZE + Consts.CELL_SIZE // 2,
            row * Consts.CELL_SIZE + Consts.CELL_SIZE // 2,
        )

    def directions(self, onecell: bool = False) -> list[tuple[int, int]]:
        """Return reachable target coordinates from the current cell.

        Args:
            onecell: When true, return only adjacent cell centers.

        Returns:
            A list of valid target cell centers.
        """
        cell_pos = get_cell(self.ghost.x, self.ghost.y)
        if cell_pos is None:
            return []

        row_index, col_index = cell_pos

        if row_index >= len(self.game.maze.maze):
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

        if onecell:
            if col_index > 0 and (cell & west) == 0:
                destinations.append(
                    self.cell_center(row_index, cell_pos[1] - 1),
                )
            if col_index < col_count - 1 and (cell & east) == 0:
                destinations.append(
                    self.cell_center(row_index, cell_pos[1] + 1),
                )
            if row_index > 0 and (cell & north) == 0:
                destinations.append(
                    self.cell_center(cell_pos[0] - 1, col_index),
                )
            if row_index < row_count - 1 and (cell & south) == 0:
                destinations.append(
                    self.cell_center(cell_pos[0] + 1, col_index),
                )
        else:
            if col_index > 0 and (cell & west) == 0:
                destinations.append(self.cell_center(row_index, 0))
            if col_index < col_count - 1 and (cell & east) == 0:
                destinations.append(
                    self.cell_center(row_index, col_count - 1),
                )
            if row_index > 0 and (cell & north) == 0:
                destinations.append(self.cell_center(0, col_index))
            if row_index < row_count - 1 and (cell & south) == 0:
                destinations.append(
                    self.cell_center(row_count - 1, col_index),
                )

        return destinations
