"""Pac-Man project entrypoint."""

import sys
import pygame
from pathlib import Path
import src.game
from src.config_models import GameConfig

from src.config_loader import load_config
from src.constants import ProgramState, GameStates, Defaults
from src.visual import main_menu, new_score_menu, score_menu
from src.highscore import check_new_highscore
import os
from typing import Tuple


def main() -> int:
    """Load the configuration file and start the program.

    Returns:
        Process exit code.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return 1

    config_path = Path(sys.argv[1])

    if config_path.suffix.lower() != ".json":
        print("Error: configuration file must be a .json file.")
        return 1

    config: GameConfig = load_config(config_path)

    pygame.init()
    state = ProgramState.MENU
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    window = pygame.Window(title="Pac-Man",
                           size=(Defaults.MAX_WINDOW_WIDTH,
                                 Defaults.MAX_WINDOW_HEIGHT),
                           resizable=True)

    while state != ProgramState.QUIT:
        try:
            match state:
                case (ProgramState.MENU):
                    state = main_menu(config, window)
                case (ProgramState.PLAY):
                    game = start_level(config, 0, window=window)
                    pygame.event.clear()
                    if check_new_highscore(config, game[1]):
                        state = ProgramState.NEW_SCORE
                    elif game[1] > -1:
                        state = ProgramState.END
                    else:
                        state = ProgramState.QUIT
                case (ProgramState.END):
                    state = score_menu(window, game[1], game[0])
                case (ProgramState.NEW_SCORE):
                    state = new_score_menu(config, window, game[1], game[0])
        except ValueError as e:
            print(e)
            sys.exit()
    return 0


def start_level(
    config: GameConfig,
    level: int,
    window: pygame.window.Window,
) -> Tuple[int, int]:
    """Run successive game levels and accumulate the score.

    Args:
        config: Loaded game configuration.
        level: Starting level index.
        window: Active game window.

    Returns:
        Total score for the played levels, or ``-1`` on failure.
    """

    exit = False
    game = src.game.GameGenerator(config, window)
    if game is None:
        print("Error: creating game.")
        return (ProgramState.QUIT, 0)

    while not exit:

        try:
            game.level_generator(config.levels[
                min(level,
                    len(config.levels) - 1)].width,
                        config.levels[min(level,
                                          len(config.levels) - 1)].height,
                        level + 1)
            game.run()

            level += 1

        except Exception as e:
            print(f"Error in start_level: {e}")
            return (GameStates.EXIT, -1)

        exit = (level == 10) or \
            game.status in [GameStates.EXIT, GameStates.STOP]

    return (game.status, game.score)


if __name__ == "__main__":
    raise SystemExit(main())
