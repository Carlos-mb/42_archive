from dataclasses import dataclass
from enum import IntEnum
import os


@dataclass
class Consts():
    """Immutable constants used by the game runtime."""

    CELL_SIZE = 56  # Must be divisible by 4
    PEOPLE_SIZE = 30  # Must be divisible by 4
    SPEED = 2
    SPRITE_SHEET = (os.path.join("src", "sprites", "spritesheet.png"))
    SPRITE_SIZE = 32
    FPS = 120
    WALL_THICKNESS = 20
    WALL_COLOR = (0, 0, 255)
    GUM_RADIUS = CELL_SIZE / 8
    SUPER_GUM_RADIUS = CELL_SIZE / 4
    GUM_WIDTH = 1
    HUD_HEIGHT = 64
    GHOST_SPEED_PERCENT = 80
    EATING_TIME = 10
    FONT_PATH = "fonts/PixelOperator-Bold.ttf"
    TIME_TO_GHOST_RESPAWN = 5
    SUBPIXEL_SCALE = 1000


@dataclass
class Defaults():
    """Default values used when configuration data is missing or invalid."""

    HIGHSCORE_FILENAME = "highscores.json"
    LIVES = 3
    POINTS_PER_PACGUM = 1000
    POINTS_PER_SUPER_PACGUM = 50
    POINTS_PER_GHOST = 200
    SEED = 42
    LEVEL_MAX_TIME = 90
    LEVEL_COUNT = 10
    LEVEL_WIDTH = 5
    LEVEL_HEIGHT = 5
    MAX_WINDOW_WIDTH = 1920
    MAX_WINDOW_HEIGHT = 900  # Whithout HUD


@dataclass
class Mins():
    """Minimum accepted values for validated configuration fields."""

    LIVES = 1
    SCORE_VALUE = 0
    LEVEL_TIME = 1
    LEVEL_SIZE = 5


@dataclass
class Colors():
    """RGB color palettes used by the game and menus."""

    BACKGROUND = (0, 0, 0)
    PLAYER = (255, 255, 0)
    GHOST = [(255, 0, 128),
             (255, 64, 128),
             (255, 128, 128),
             (255, 255, 128)]
    GUM = (255, 255, 255)
    HUD_BACKGROUND = (8, 8, 24)
    HUD_TEXT = (255, 226, 64)
    HIGHSCOREBOARD = [(255, 127, 0),
                      (255, 255, 0),
                      (127, 255, 0),
                      (0, 255, 0),
                      (0, 255, 255),
                      (0, 127, 255),
                      (0, 0, 255),
                      (0, 0, 255),
                      (127, 0, 255),
                      (255, 0, 255)]


class GameStates(IntEnum):
    """In-game states used by the main game loop."""

    EXIT = 0
    PLAYING = 1
    STOP = 2
    NEXT = 3
    NONE = 4
    PAUSE = 5


class ProgramState(IntEnum):
    """Top-level program states used by the entrypoint."""

    MENU = 0
    PLAY = 1
    NEW_SCORE = 2
    END = 3
    QUIT = 4
