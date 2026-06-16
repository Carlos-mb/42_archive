import pygame
from src.constants import (
    Defaults,
    GameStates,
    Colors,
    Consts
)
from src.people import Player, Person, Ghost
import mazegenerator
from src.config_models import GameConfig
import time
from src.ghostia01 import GhostIa01
from src.ghostia02 import GhostIa02
from src.functions import get_cell
import random
from src.visual import pause_menu

PEOPLE_SIZE = Consts.PEOPLE_SIZE


class GameGenerator():
    """Create and run one Pac-Man game session."""

    def __init__(
        self,
        config: GameConfig,
        window: pygame.window.Window,
    ) -> None:
        """Create a game session controller.

        Args:
            config: Loaded game configuration.
            window: Active game window.
        """

        self.config: GameConfig = config
        self.seed = config.seed
        self.window = window

        self.window_max_width: int = Defaults.MAX_WINDOW_WIDTH
        self.window_max_height: int = Defaults.MAX_WINDOW_HEIGHT
        self.width: int
        self.height: int
        self.hud_base_height: int
        self.screen: pygame.surface.Surface
        self.game_scale: float = 1.0
        self.window_width: int = 0
        self.window_height: int = 0
        self.hud_window_height: int = 0
        self.resize_target_size: tuple[int, int] | None = None
        self.resize_apply_at: int = 0
        self.ignore_next_resize: bool = False

        self.pacgums: list[list[int]]

        self.pacgums_surface: pygame.surface.Surface
        self.world_surface: pygame.surface.Surface
        self.hud_surface: pygame.surface.Surface

        self.score: int = 0
        self.level: int
        self.time_remaining: int

        self.status = GameStates.NONE
        self.lives = config.lives

        self.cheat_mode = False

    def level_generator(
        self,
        cells_width: int,
        cells_height: int,
        level: int,
    ) -> None:
        """Create a new maze level and reset level-specific state.

        Args:
            cells_width: Maze width in cells.
            cells_height: Maze height in cells.
            level: One-based level number.
        """

        self.width = cells_width * Consts.CELL_SIZE
        self.height = cells_height * Consts.CELL_SIZE
        self.level = level
        self.time_remaining = self.config.level_max_time
        self.start_time = time.time()
        scale_x = self.window_max_width / self.width
        scale_y = self.window_max_height / self.height
        self.game_scale = min(scale_x, scale_y, 1.0)
        self.window_width = int(self.width * self.game_scale)
        self.window_height = int(self.height * self.game_scale)

        self.hud_base_height = self.height // 10
        self.hud_window_height = self.window_height // 10

        self.window.size = (self.window_width,
                            self.window_height + self.hud_window_height)

        self.screen = self.window.get_surface()

        self.world_surface = pygame.Surface(
                            (self.width, self.height)).convert()

        # Create and set transparent Surface
        self.pacgums_surface = pygame.Surface(
                              (self.width, self.height),
                              pygame.SRCALPHA).convert_alpha()
        self.pacgums_surface.fill((0, 0, 0, 0))

        self.hud_surface = pygame.Surface(
                          (self.width, self.hud_base_height)).convert()

        self.maze_surface: pygame.surface.Surface = pygame.Surface(
            (self.width, self.height)).convert()

        pygame.display.set_caption("Pac-man")

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.status = GameStates.PLAYING

        try:
            self.hud_font = pygame.font.Font("fonts/PixelOperator-Bold.ttf",
                                             int(self.height / 25))
        except FileNotFoundError:
            print("HUD font does not found. Using default font.")
            self.hud_font = pygame.font.Font(None, int(self.height / 25))
        try:
            self.maze = mazegenerator.MazeGenerator(size=(cells_width,
                                                          cells_height),
                                                    perfect=False,
                                                    seed=self.seed)
            self.seed += 1
            # self.maze.generate(seed=self.seed)
        except Exception as e:
            print(f"Error generating maze {e}")

        self.create_background_surface()
        self.create_pacgums()
        self.reborn()

    def create_pacgums(self) -> None:
        """Populate the maze with pacgums and super pacgums."""
        n: int = 0
        self.pacgums = []
        for row_index, row in enumerate(self.maze.maze):
            self.pacgums.append([])
            for col_index in range(len(row)):
                self.pacgums[n].append(0)
                super = False
                if (n == 0 or n == len(self.maze.maze) - 1) and \
                   (col_index == 0 or col_index == len(self.maze.maze[0]) - 1):
                    self.pacgums[row_index][col_index] =\
                        self.config.points_per_super_pacgum
                    super = True
                else:
                    self.pacgums[row_index][col_index] =\
                        self.config.points_per_pacgum
                self.draw_pacgum(
                    row_index,
                    col_index,
                    super=super
                )

            n += 1

    def draw_pacgum(self,
                    row_index: int,
                    col_index: int,
                    delete: bool = False,
                    super: bool = False,
                    ) -> None:
        """Draw or erase a pacgum at the given cell.

        Args:
            row_index: Maze row index.
            col_index: Maze column index.
            delete: When true, erase the gum instead of drawing it.
            super: When true, draw a super pacgum.
        """

        if super or delete:
            radius = Consts.SUPER_GUM_RADIUS
        else:
            radius = Consts.GUM_RADIUS

        if self.maze.maze[row_index][col_index] != 15:  # 42 figure
            x = col_index * Consts.CELL_SIZE + Consts.CELL_SIZE // 2
            y = row_index * Consts.CELL_SIZE + Consts.CELL_SIZE // 2

            pygame.draw.circle(
                surface=self.pacgums_surface,
                color=(Colors.GUM if not delete
                       else Colors.BACKGROUND),
                center=(x, y),
                radius=radius,
                )
        else:
            self.pacgums[row_index][col_index] = 0

    def create_background_surface(self) -> None:
        """Create the static background surface with the maze walls."""

        self.maze_surface.fill(Colors.BACKGROUND)

        pygame.draw.line(
                    self.maze_surface,
                    Consts.WALL_COLOR,
                    (0, 0),
                    (self.width, 0),
                    Consts.WALL_THICKNESS,
                    )

        pygame.draw.line(
                    self.maze_surface,
                    Consts.WALL_COLOR,
                    (0, 0),
                    (0, self.height),
                    Consts.WALL_THICKNESS,
                    )

        for row_index, row in enumerate(self.maze.maze):
            for col_index, cell in enumerate(row):
                self.draw_cell_walls(
                    cell,
                    row_index,
                    col_index,
                )

    def draw_cell_walls(self,
                        cell: int,
                        row_index: int,
                        col_index: int,
                        ) -> None:
        """Draw the walls of one maze cell."""

        # NORTH = 1
        EAST = 2
        SOUTH = 4
        # WEST = 8

        x = col_index * Consts.CELL_SIZE
        y = row_index * Consts.CELL_SIZE

        # top_left = (x, y)
        top_right = (x + Consts.CELL_SIZE, y)
        bottom_left = (x, y + Consts.CELL_SIZE)
        bottom_right = (x + Consts.CELL_SIZE, y + Consts.CELL_SIZE)

        # if cell & NORTH:
        #     pygame.draw.line(
        #         self.maze_surface,
        #         Consts.WALL_COLOR,
        #         top_left,
        #         top_right,
        #         Consts.WALL_THICKNESS,
        #     )

        if cell & EAST:
            pygame.draw.line(
                self.maze_surface,
                Consts.WALL_COLOR,
                (top_right[0], top_right[1] + 1 - Consts.WALL_THICKNESS // 2),
                (bottom_right[0],
                 bottom_right[1] + Consts.WALL_THICKNESS // 2),
                Consts.WALL_THICKNESS,
            )

        if cell & SOUTH:
            pygame.draw.line(
                self.maze_surface,
                Consts.WALL_COLOR,
                (bottom_left[0] + 1 - Consts.WALL_THICKNESS // 2,
                 bottom_left[1]),
                (bottom_right[0] +
                 Consts.WALL_THICKNESS // 2, bottom_right[1]),
                Consts.WALL_THICKNESS,
            )

        # if cell & WEST:
        #     pygame.draw.line(
        #         self.maze_surface,
        #         Consts.WALL_COLOR,
        #         top_left,
        #         bottom_left,
        #         Consts.WALL_THICKNESS,
        #     )

    def handle_events(self) -> None:
        """Process pending window and keyboard events."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.status = GameStates.EXIT
            if event.type == pygame.VIDEORESIZE:
                self.__resize(event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.status = GameStates.STOP
                elif event.key == pygame.K_r:
                    self.status = GameStates.NEXT
                elif event.key == pygame.K_p:
                    if self.status == GameStates.PAUSE:
                        self.status = GameStates.PLAYING
                    else:
                        self.status = GameStates.PAUSE
                elif event.key == pygame.K_o:
                    for row in range(len(self.maze.maze)):
                        for col in range(len(self.maze.maze[0])):
                            self.maze.maze[row][col] = 0
                    for g in self.ghosts:
                        g.time_to_respawn = 99999999
                    self.create_background_surface()
                    pygame.draw.line(
                                self.maze_surface,
                                Colors.BACKGROUND,
                                (0, 0),
                                (self.width, 0),
                                Consts.WALL_THICKNESS,
                                )

                    pygame.draw.line(
                                self.maze_surface,
                                Colors.BACKGROUND,
                                (0, 0),
                                (0, self.height),
                                Consts.WALL_THICKNESS,
                                )
                    self.reborn()

        self.__apply_pending_resize()

    def __resize(self, x: int, y: int) -> None:
        """Update the game layout after a window resize event."""

        if self.ignore_next_resize:
            self.ignore_next_resize = False
            self.screen = self.window.get_surface()
            return

        self.window_max_width = max(x, 100)

        # Total height = game height + HUD height.
        # HUD height is 10% of game height.
        # Therefore: total height = game height * 1.10
        self.window_max_height = max((y * 10) // 11, 100)

        scale_x = self.window_max_width / self.width
        scale_y = self.window_max_height / self.height
        self.game_scale = min(scale_x, scale_y)

        self.window_width = max(1, int(self.width * self.game_scale))
        self.window_height = max(1, int(self.height * self.game_scale))
        self.hud_window_height = max(1, self.window_height // 10)

        self.resize_target_size = (
            self.window_width,
            self.window_height + self.hud_window_height,
        )
        self.resize_apply_at = pygame.time.get_ticks() + 150

        self.screen = self.window.get_surface()

    def __apply_pending_resize(self) -> None:
        """Apply the corrected window size after resize events stop."""

        if self.resize_target_size is None:
            return

        if pygame.time.get_ticks() < self.resize_apply_at:
            return

        if self.window.size != self.resize_target_size:
            self.ignore_next_resize = True
            self.window.size = self.resize_target_size
            self.screen = self.window.get_surface()

        self.resize_target_size = None

    def update(self) -> None:
        """Advance player and ghost movement for one frame."""
        keys = pygame.key.get_pressed()

        self.cheat_mode = keys[pygame.K_LSHIFT]

        wanted_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        wanted_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP])

        wanted_x *= self.player.speed
        wanted_y *= self.player.speed

        movx, movy = self.__get_subpixel_move(
            self.player,
            wanted_x,
            wanted_y,
        )

        x, y = self.try_to_move(self.player, movx, movy)

        real_movx = x - self.player.x
        real_movy = y - self.player.y

        if movx != 0 and real_movx != movx:
            self.player.subpixel_x = 0

        if movy != 0 and real_movy != movy:
            self.player.subpixel_y = 0

        if real_movx != 0 or real_movy != 0:
            self.eat_gum(self.player, real_movx, real_movy)
            self.player.move(x, y)

        self.eat_ghost(self.player, movx, movy)

        corners = [(0, 0),
                   (0, len(self.maze.maze[0]) - 1),
                   (len(self.maze.maze) - 1, 0),
                   ((len(self.maze.maze) - 1, len(self.maze.maze[0]) - 1))]

        player_cell = get_cell(self.player.x, self.player.y)
        if player_cell in corners:
            corners.remove(player_cell)

        for ghost in self.ghosts:
            if ghost.eating_until < time.time():
                movx, movy = ghost.chaser(self.player.x, self.player.y)
            else:
                choice = random.choice(corners)
                movx, movy = ghost.chaser(*choice)

            if movx != 0 and movy != 0:
                diagonal_speed = max(1, round(ghost.speed / (2 ** 0.5)))
                movx = diagonal_speed if movx > 0 else -diagonal_speed
                movy = diagonal_speed if movy > 0 else -diagonal_speed
            x, y = self.try_to_move(ghost, movx, movy)
            ghost.move(x, y)

    def eat_ghost(self,
                  person: Person,
                  px: int,
                  py: int) -> None:
        """Resolve collisions between the player and ghosts.

        Args:
            person: Moving person to test against the ghosts.
            px: Horizontal movement applied this frame.
            py: Vertical movement applied this frame.
        """

        if self.cheat_mode:
            return

        for ghost in self.ghosts:
            g_left = 1 + Consts.SPEED + ghost.x - ghost.width // 2
            g_right = - 1 - Consts.SPEED + ghost.x + ghost.width // 2
            g_up = 1 + Consts.SPEED + ghost.y - ghost.width // 2
            g_down = -1 - Consts.SPEED + ghost.y + ghost.width // 2

            p_left = person.x - person.width // 2
            p_right = person.x + person.width // 2
            p_up = person.y - person.width // 2
            p_down = person.y + person.width // 2

            if (g_left >= p_left and g_left <= p_right or
                g_right >= p_left and g_right <= p_right) and \
                (g_up >= p_up and g_up <= p_down or
                 g_down >= p_up and g_down <= p_down):

                if ghost.eating_until > time.time():
                    if ghost.time_to_respawn < time.time():
                        self.score += self.config.points_per_ghost
                        ghost.x = ghost.start_x
                        ghost.y = ghost.start_y
                        ghost.move(ghost.x, ghost.y)
                        ghost.time_to_respawn = (time.time() +
                                                 Consts.TIME_TO_GHOST_RESPAWN)
                        ghost.eating_until = ghost.time_to_respawn
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.status = GameStates.EXIT
                    else:
                        time.sleep(2)
                        self.time_remaining += 2
                        self.start_time += 2
                        self.reborn()
                        self.player.time_to_respawn = time.time() + 2

    def reborn(self) -> None:
        """Reset the player and ghosts to their spawn positions."""

        row = len(self.maze.maze) // 2
        col = len(self.maze.maze[0]) // 2
        while self.maze.maze[row][col] == 15:
            col -= 1

        x = col * Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        y = row * Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        self.player = Player(x, y, self.lives)

        # Delete pacgum on pac-man cell
        pacr, pacc = get_cell(self.player.x, self.player.y)
        self.draw_pacgum(pacr, pacc, delete=True)
        self.pacgums[pacr][pacc] = 0

        self.ghosts: list[Ghost] = []

        x = Consts.CELL_SIZE // 2
        y = Consts.CELL_SIZE // 2
        self.ghosts.append(Ghost(x, y, 0))
        self.ghosts[0].chaser = GhostIa01(
            self.ghosts[0],
            self.player,
            self,
        ).chase

        x = (len(self.maze.maze[0]) - 1) *\
            Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        y = Consts.CELL_SIZE // 2
        self.ghosts.append(Ghost(x, y, 1))
        ia = GhostIa02(self.ghosts[1], self.player, self)
        self.ghosts[1].chaser = ia.chase

        x = Consts.CELL_SIZE // 2
        y = (len(self.maze.maze) - 1) *\
            Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        self.ghosts.append(Ghost(x, y, 2))
        self.ghosts[2].chaser = GhostIa01(
            self.ghosts[2],
            self.player,
            self,
        ).chase

        x = (len(self.maze.maze[0]) - 1) *\
            Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        y = (len(self.maze.maze) - 1) *\
            Consts.CELL_SIZE + Consts.CELL_SIZE // 2
        self.ghosts.append(Ghost(x, y, 3))
        self.ghosts[3].chaser = GhostIa02(
            self.ghosts[3],
            self.player,
            self,
        ).chase

    def eat_gum(self,
                person: Person,
                movx: int,
                movy: int) -> None:
        """Consume pacgums in front of a moving entity.

        Args:
            person: Moving person that may collect pacgums.
            movx: Horizontal movement applied this frame.
            movy: Vertical movement applied this frame.
        """

        gum = None

        if movx != 0:
            x_direction = 1 if movx > 0 else -1

            for step in range(1, abs(movx) + 1):
                next_x = person.x + step * x_direction

                left = next_x - person.width // 2
                right = next_x + person.width // 2 - 1
                top = person.y - person.height // 2
                bottom = person.y + person.height // 2 - 1

                if x_direction > 0:
                    front_x = right
                else:
                    front_x = left

                for py in range(top, bottom):
                    if self.is_gum_pixel(front_x, py):
                        gum = get_cell(front_x, py)
                        self.score += self.pacgums[gum[0]][gum[1]]
                        self.pacgums[gum[0]][gum[1]] = 0
                        self.draw_pacgum(gum[0], gum[1], True)
                        if ((gum[0] == 0 or gum[0] ==
                             len(self.maze.maze) - 1) and
                            (gum[1] == 0 or gum[1] ==
                             len(self.maze.maze[0]) - 1)):
                            for ghost in self.ghosts:
                                if ghost.time_to_respawn < time.time():
                                    ghost.eating_until = (time.time() +
                                                          Consts.EATING_TIME)
                        return

        if movy != 0:
            y_direction = 1 if movy > 0 else -1

            for step in range(1, abs(movy) + 1):
                next_y = person.y + step * y_direction

                left = person.x - person.width // 2
                right = person.x + person.width // 2 - 1
                top = next_y - person.height // 2
                bottom = next_y + person.height // 2 - 1

                if y_direction > 0:
                    front_y = bottom
                else:
                    front_y = top

                for px in range(left, right + 1):
                    if self.is_gum_pixel(px, front_y):
                        gum = get_cell(px, front_y)
                        self.score += self.pacgums[gum[0]][gum[1]]
                        self.pacgums[gum[0]][gum[1]] = 0
                        self.draw_pacgum(gum[0], gum[1], True)
                        if ((gum[0] == 0 or gum[0] ==
                             len(self.maze.maze) - 1) and
                            (gum[1] == 0 or gum[1] ==
                             len(self.maze.maze[0]) - 1)):
                            for ghost in self.ghosts:
                                if ghost.time_to_respawn < time.time():
                                    ghost.eating_until =\
                                        time.time() + Consts.EATING_TIME
                        return

        if all(all(value == 0 for value in row) for row in self.pacgums):
            self.status = GameStates.NEXT

    def ghosts_pixel(self, x: int, y: int) -> list[Ghost]:
        """Return ghosts currently occupying the cell containing a pixel.

        Args:
            x: Pixel x coordinate.
            y: Pixel y coordinate.

        Returns:
            Ghosts found in the corresponding cell.
        """

        cell = get_cell(x, y)
        ghost_found = []
        for ghost in self.ghosts:
            if get_cell(ghost.x, ghost.y) == cell:
                ghost_found.append(ghost)

        return ghost_found

    def is_gum_pixel(self, px: int, py: int) -> bool:
        """Return True if a pixel still contains a pacgum.

        Args:
            px: Pixel x coordinate.
            py: Pixel y coordinate.

        Returns:
            True when the pixel belongs to an uneaten pacgum.
        """

        if px < 0 or px >= self.width:
            return False
        if py < 0 or py >= self.height:
            return False

        pixel = self.pacgums_surface.get_at((px, py))

        return (pixel[0], pixel[1], pixel[2]) == Colors.GUM[:3]

    def try_to_move(self,
                    person: Person,
                    movx: int,
                    movy: int) -> tuple[int, int]:
        """Return the next valid position for a moving person."""

        x = person.x
        y = person.y
        x_direction = 0
        y_direction = 0

        if movx != 0:
            x_direction = 1 if movx > 0 else -1
            last_valid_x = person.x

            for step in range(1, abs(movx) + 1):
                next_x = person.x + step * x_direction

                left = next_x - person.width // 2
                right = next_x + person.width // 2 - 1
                top = person.y - person.height // 2
                bottom = person.y + person.height // 2 - 1

                if x_direction > 0:
                    front_x = right
                else:
                    front_x = left

                blocked = False

                for py in range(top, bottom):
                    if not self.is_background_pixel(front_x, py):
                        blocked = True
                        break

                if blocked:
                    x = last_valid_x
                    break

                last_valid_x = next_x
                x = last_valid_x

        if movy != 0:
            y_direction = 1 if movy > 0 else -1
            last_valid_y = person.y

            for step in range(1, abs(movy) + 1):
                next_y = person.y + step * y_direction

                left = x - person.width // 2
                right = x + person.width // 2 - 1
                top = next_y - person.height // 2
                bottom = next_y + person.height // 2 - 1

                if y_direction > 0:
                    front_y = bottom
                else:
                    front_y = top

                blocked = False

                for px in range(left, right + 1):
                    if not self.is_background_pixel(px, front_y):
                        blocked = True
                        break

                if blocked:
                    y = last_valid_y
                    break

                last_valid_y = next_y
                y = last_valid_y

        if (movx != 0 and x == movx + person.x) and\
           (movy != 0 and y != movy + person.y):

            x, y = self.try_to_move(person, movx + abs(movy) * x_direction, 0)

        elif (movy != 0 and y == movy + person.y) and\
             (movx != 0 and x != movx + person.x):
            x, y = self.try_to_move(person, 0, movy + abs(movx) * y_direction)

        return x, y

    def is_background_pixel(self, px: int, py: int) -> bool:
        """Return True if the pixel is inside the screen and walkable."""
        if px < 0 or px >= self.width:
            return False
        if py < 0 or py >= self.height:
            return False

        pixel = self.maze_surface.get_at((px, py))

        return (pixel[0], pixel[1], pixel[2]) == Colors.BACKGROUND[:3]

    def draw_hud(self) -> None:
        """Draw the current game information on the HUD surface."""

        # self.hud_font.set_point_size(self.width // 21)

        elapsed_time = int(time.time() - self.start_time)
        self.time_remaining = max(
            0,
            self.config.level_max_time - elapsed_time,
        )

        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60

        hud_items: list[str] = [
            f"Lives: {self.lives}",
            f"Level: {self.level}",
            f"Time: {minutes:02d}:{seconds:02d}",
        ]

        self.hud_surface.fill(Colors.HUD_BACKGROUND)

        section_width = self.width // len(hud_items)
        y = self.hud_base_height // 3

        text_surface = self.hud_font.render(
            f"Score: {self.score}",
            True,
            Colors.HUD_TEXT,
        )
        text_rect = text_surface.get_rect(
            center=(
                self.width // 2,
                y,
            ))
        self.hud_surface.blit(text_surface, text_rect)

        y *= 2

        for index, text in enumerate(hud_items):
            text_surface = self.hud_font.render(
                text,
                True,
                Colors.HUD_TEXT,
            )
            text_rect = text_surface.get_rect(
                center=(
                    index * section_width + section_width // 2,
                    y,
                )
            )
            self.hud_surface.blit(text_surface, text_rect)

    def draw(self) -> None:
        """Draw the game scaled down to fit inside the window limits."""

        # Internal clear of Surface, nothing shown
        self.world_surface.blit(self.maze_surface, (0, 0))
        self.world_surface.blit(self.pacgums_surface, (0, 0))

        self.player.draw(self.world_surface)

        for ghost in self.ghosts:
            if ghost.eating_until < time.time():
                ghost.draw(self.world_surface)
            else:
                ghost.draw_scared(self.world_surface, ghost.eating_until)

        self.draw_hud()

        screen_width, screen_height = self.screen.get_size()

        self.screen.fill(Colors.BACKGROUND)

        x_offset = max((screen_width - self.window_width) // 2, 0)
        y_offset = max(
            (screen_height -
             (self.window_height + self.hud_window_height)) // 2,
            0,
        )

        scaled_surface = pygame.transform.scale(
            self.world_surface,
            (self.window_width, self.window_height),
        )

        scaled_hud_surface = pygame.transform.scale(
            self.hud_surface,
            (self.window_width, self.hud_window_height),
        )

        self.screen.blit(scaled_surface, (x_offset, y_offset))
        self.screen.blit(
            scaled_hud_surface,
            (x_offset, y_offset + self.window_height),
        )

        self.window.flip()

    def __extract_pixels(self, units: int) -> tuple[int, int]:
        """Extract full pixels from fixed-point movement units."""
        sign = 1

        if units < 0:
            sign = -1
            units = -units

        pixels = units // Consts.SUBPIXEL_SCALE
        remainder = units % Consts.SUBPIXEL_SCALE

        return sign * pixels, sign * remainder

    def __get_subpixel_move(
        self,
        person: Person,
        movx: int,
        movy: int,
    ) -> tuple[int, int]:
        """Convert requested movement into integer pixels using subpixels."""
        movx_units = movx * Consts.SUBPIXEL_SCALE
        movy_units = movy * Consts.SUBPIXEL_SCALE

        if movx != 0 and movy != 0:
            movx_units = round(movx_units / (2 ** 0.5))
            movy_units = round(movy_units / (2 ** 0.5))

        person.subpixel_x += movx_units
        person.subpixel_y += movy_units

        pixel_x, person.subpixel_x = self.__extract_pixels(
            person.subpixel_x,
        )
        pixel_y, person.subpixel_y = self.__extract_pixels(
            person.subpixel_y,
        )

        return pixel_x, pixel_y

    def run(self) -> None:
        """Run the active level until it ends or the player pauses."""
        first = True
        pausetime = None
        timeremain = None
        while self.status == GameStates.PLAYING or \
                self.status == GameStates.PAUSE:

            self.handle_events()

            if self.status == GameStates.PAUSE:
                if pausetime is None:
                    pausetime = time.time()
                    timeremain = self.time_remaining
                    self.status = pause_menu(self.window)
                    w, h = self.window.size
                    self.__resize(w, h)
            else:
                if pausetime is not None and timeremain is not None:
                    self.time_remaining = timeremain
                    self.start_time += time.time() - pausetime
                    timeremain = None
                    pausetime = None

            if self.status != GameStates.PAUSE:
                self.update()
                self.draw()
                if first:
                    time.sleep(1)
                    self.start_time += + 1
                    self.time_remaining += 1

                    first = False

                started = time.time()
                timeremain = self.time_remaining
                while self.player.time_to_respawn > time.time():
                    pass
                self.start_time += time.time() - started
                self.time_remaining = timeremain

                if self.time_remaining <= 0:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.status = GameStates.EXIT
                    else:
                        time.sleep(2)
                        self.time_remaining = self.config.level_max_time
                        self.start_time = time.time()
                        self.reborn()

                self.clock.tick(Consts.FPS)  # 60 fps

        time.sleep(1)
        self.start_time += + 1
        self.time_remaining += 1
