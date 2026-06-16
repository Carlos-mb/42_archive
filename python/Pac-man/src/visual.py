from typing import List, Tuple

import pygame

from src.constants import Colors, Consts, Defaults, ProgramState, GameStates
from src.game import GameConfig
from src.highscore import get_highscores, get_idx_score, update_highscore

Surface = pygame.surface.Surface
Font = pygame.font.Font


def get_screen_size(x: int = 0, y: int = 0) -> Tuple[int, int]:
    """Return the current screen size with an optional offset.

    Args:
        x: Extra width to add.
        y: Extra height to add.

    Returns:
        The current screen size as ``(width, height)``.
    """
    current_x = pygame.display.Info().current_w
    current_y = pygame.display.Info().current_h
    return (current_x + x, current_y + y)


def get_font_size(surface: Surface, percentage: int) -> int:
    """Compute a font size from the surface dimensions.

    Args:
        surface: Target surface used for sizing.
        percentage: Percentage of the smaller surface dimension.

    Returns:
        A font size in pixels.
    """
    width, height = surface.get_size()
    return int(min(width, height) * (percentage / 100))


def create_font(name: str, size: int) -> Font:
    """Create a font, falling back to the default font when needed.

    Args:
        name: Font file path.
        size: Requested font size.

    Returns:
        A loaded ``pygame.font.Font`` instance.
    """
    try:
        font = pygame.font.Font(name, size)
    except FileNotFoundError:
        font = pygame.font.Font(None, size)
    return font


def draw_text(
    text: str,
    font: Font,
    color: Tuple[int, int, int],
    surface: Surface,
    x: int,
    y: int,
) -> None:
    """Render centered text on a surface.

    Args:
        text: Text to render.
        font: Font used for rendering.
        color: RGB text color.
        surface: Target surface.
        x: Center x coordinate.
        y: Center y coordinate.
    """
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, text_rect)


def draw_blink_text(
    text: str,
    font: Font,
    color: Tuple[int, int, int],
    surface: Surface,
    x: int,
    y: int,
    speed: int = 500,
) -> None:
    """Draw centered text that blinks at a fixed interval.

    Args:
        text: Text to render.
        font: Font used for rendering.
        color: RGB text color.
        surface: Target surface.
        x: Center x coordinate.
        y: Center y coordinate.
        speed: Blink period in milliseconds.
    """
    ticks = pygame.time.get_ticks()
    if (ticks // speed) % 2 == 0:
        draw_text(text, font, color, surface, x, y)


def draw_lines(
    surface: Surface,
    text: str,
    percentage: int,
    pos_x: int,
    pos_y: int,
    header: str = "",
) -> None:
    """Draw a titled multiline text block.

    Args:
        surface: Target surface.
        text: Multiline body text.
        percentage: Font size percentage of the surface.
        pos_x: Center x coordinate.
        pos_y: Starting y coordinate.
        header: Optional heading displayed above the text.
    """
    lines = text.split("\n")

    text_size = get_font_size(surface, percentage)
    text_font = create_font(Consts.FONT_PATH, text_size)
    header_size = get_font_size(surface, percentage + 2)
    header_font = create_font(Consts.FONT_PATH, header_size)

    if header != "":
        draw_text(
            f"- {header} -",
            header_font,
            (255, 255, 255),
            surface,
            pos_x,
            pos_y,
        )
        pos_y += int(header_size + (header_size / 2))

    for line in lines:
        draw_text(line, text_font, (255, 255, 255), surface, pos_x, pos_y)
        pos_y += int(text_size + (text_size / 2))


def get_highscore_text(idx: int, name: str, score: int) -> str:
    """Format a single highscore entry for display.

    Args:
        idx: Zero-based leaderboard index.
        name: Player name.
        score: Stored score.

    Returns:
        A formatted leaderboard line.
    """
    sufix = "th"
    if idx == 0:
        sufix = "st"
    elif idx == 2:
        sufix = "nd"
    elif idx == 3:
        sufix = "rd"
    return f"{idx + 1}{sufix}. {name} - {score} pts"


def draw_highscore(
    scores: List[Tuple[str, int]],
    surface: Surface,
    pos_x: int,
    pos_y: int,
) -> None:
    """Draw the top 10 highscore table.

    Args:
        scores: Highscore entries to display.
        surface: Target surface.
        pos_x: Center x coordinate.
        pos_y: Starting y coordinate.
    """
    font = create_font(Consts.FONT_PATH, get_font_size(surface, 3))
    title = create_font(Consts.FONT_PATH, get_font_size(surface, 5))

    offset = get_font_size(surface, 3)

    draw_text("- HIGH SCORES -", title, (255, 255, 255), surface, pos_x, pos_y)

    pos_y += int(offset + offset / 2)
    for n in range(1, 11):
        sufix = "th"
        if n == 1:
            sufix = "st"
        elif n == 2:
            sufix = "nd"
        elif n == 3:
            sufix = "rd"

        try:
            data = scores[n - 1]
            text = f"{n}{sufix}. {data[0]} - {data[1]} pts"
        except IndexError:
            text = f"{n}{sufix}."

        draw_text(
            text,
            font,
            Colors.HIGHSCOREBOARD[n - 1],
            surface,
            pos_x,
            pos_y,
        )
        pos_y += offset


def main_menu(
    config: GameConfig,
    window: pygame.window.Window,
) -> ProgramState:
    """Run the main menu and return the next program state.

    Args:
        config: Loaded game configuration.
        window: Active game window.

    Returns:
        The next program state selected by the user.
    """
    window.size = (Defaults.MAX_WINDOW_WIDTH, Defaults.MAX_WINDOW_HEIGHT)
    screen: Surface = window.get_surface()
    current_size = (0, 0)
    scores = get_highscores(config.highscore_filename)
    title = create_font(Consts.FONT_PATH, 1)
    text = create_font(Consts.FONT_PATH, 1)

    while True:
        screen.fill(Colors.BACKGROUND)
        if window.size != current_size:
            screen = window.get_surface()
            current_size = window.size
            title = create_font(Consts.FONT_PATH, get_font_size(screen, 20))
            text = create_font(Consts.FONT_PATH, get_font_size(screen, 5))

        w, h = current_size
        draw_text(
            "Pac-Man",
            title,
            (255, 255, 0),
            screen,
            int(w / 2),
            int(h * 0.15),
        )
        draw_blink_text(
            "Press SPACE to play",
            text,
            (255, 255, 255),
            screen,
            int(w / 2),
            int(h * 0.35),
        )

        draw_highscore(scores, screen, int(w / 3), int(h * 0.5))

        help_text = "MOVE: Arrows\nPAUSE: P"
        draw_lines(
            screen,
            help_text,
            3,
            int(w / 3 * 2),
            int(h * 0.5),
            header="INSTRUCTIONS",
        )
        window.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ProgramState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return ProgramState.PLAY
                if event.key == pygame.K_ESCAPE:
                    return ProgramState.QUIT
                if event.key == pygame.K_p:
                    return ProgramState.NEW_SCORE


def new_score_menu(
    config: GameConfig,
    window: pygame.window.Window,
    score: int,
    status: int,
) -> ProgramState:
    """Run the highscore name-entry menu.

    Args:
        config: Loaded game configuration.
        window: Active game window.
        score: Score to store if the player confirms.
        status: The last state of the play.

    Returns:
        The next program state selected by the user.
    """
    print(status)
    window.size = (Defaults.MAX_WINDOW_WIDTH, Defaults.MAX_WINDOW_HEIGHT)
    screen: Surface = window.get_surface()
    current_size = (0, 0)
    user_text = "[]"
    title = create_font(Consts.FONT_PATH, 1)
    text = create_font(Consts.FONT_PATH, 1)

    scores = get_highscores(config.highscore_filename)
    score_idx = get_idx_score(scores, score)
    while True:
        screen.fill(Colors.BACKGROUND)
        if window.size != current_size:
            screen = window.get_surface()
            current_size = window.size
            title = create_font(Consts.FONT_PATH, get_font_size(screen, 10))
            text = create_font(Consts.FONT_PATH, get_font_size(screen, 5))

        for event in pygame.event.get():
            screen.fill(Colors.BACKGROUND)

            if event.type == pygame.QUIT:
                return ProgramState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(user_text) > 2:
                    user_text = user_text[:-2]
                    user_text += "]"
                else:
                    if event.key == pygame.K_RETURN:
                        update_highscore(
                            config.highscore_filename,
                            user_text[1:-1],
                            score,
                        )
                        return ProgramState.MENU
                    if (
                        (event.unicode.isalnum() or event.unicode == " ")
                        and len(user_text) < 12
                    ):
                        user_text = user_text[:-1]
                        user_text += event.unicode
                        user_text += "]"

        w, h = current_size
        if status == GameStates.NEXT:
            draw_text(
                "YOU WIN!",
                title,
                (255, 255, 0),
                screen,
                int(w / 2),
                int(h * 0.20),
            )
        else:
            draw_text(
                "GAME OVER",
                title,
                (255, 0, 0),
                screen,
                int(w / 2),
                int(h * 0.20),
            )
        draw_blink_text(
            "New Hi-Score register!",
            text,
            (255, 255, 0),
            screen,
            int(w / 2),
            int(h * 0.27),
        )
        draw_text(
            "Enter your name:",
            text,
            (255, 255, 255),
            screen,
            int(w / 2),
            int(h * 0.45),
        )
        score_text = get_highscore_text(score_idx, user_text, score)
        draw_text(
            score_text,
            text,
            Colors.HIGHSCOREBOARD[score_idx],
            screen,
            int(w / 2),
            int(h * 0.50),
        )

        window.flip()


def score_menu(
    window: pygame.window.Window,
    score: int,
    status: int
) -> ProgramState:
    """Run the highscore name-entry menu.

    Args:
        config: Loaded game configuration.
        window: Active game window.
        score: Score to store if the player confirms.
        status: The last state of the play.

    Returns:
        The next program state selected by the user.
    """
    window.size = (Defaults.MAX_WINDOW_WIDTH, Defaults.MAX_WINDOW_HEIGHT)
    screen: Surface = window.get_surface()
    current_size = (0, 0)

    title = create_font(Consts.FONT_PATH, 1)
    text = create_font(Consts.FONT_PATH, 1)

    while True:
        screen.fill(Colors.BACKGROUND)
        if window.size != current_size:
            screen = window.get_surface()
            current_size = window.size
            title = create_font(Consts.FONT_PATH, get_font_size(screen, 10))
            text = create_font(Consts.FONT_PATH, get_font_size(screen, 5))

        for event in pygame.event.get():
            screen.fill(Colors.BACKGROUND)

            if event.type == pygame.QUIT:
                return ProgramState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return ProgramState.MENU

        w, h = current_size
        if status == GameStates.NEXT:
            draw_text(
                "YOU WIN!",
                title,
                (255, 255, 0),
                screen,
                int(w / 2),
                int(h * 0.20),
            )
        else:
            draw_text(
                "GAME OVER",
                title,
                (255, 0, 0),
                screen,
                int(w / 2),
                int(h * 0.20),
            )
        draw_text(
            f"Your score is : {score}",
            text,
            (255, 255, 0),
            screen,
            int(w / 2),
            int(h * 0.50),
        )
        draw_blink_text(
            "Press SPACE to return menu",
            text,
            (255, 255, 255),
            screen,
            int(w / 2),
            int(h * 0.75),
        )

        window.flip()


def pause_menu(
    window: pygame.window.Window,
) -> GameStates:
    """Run the pause menu and return the next game state.

    Args:
        window: Active game window.

    Returns:
        The next program state selected by the user.
    """
    screen: Surface = window.get_surface()
    current_size = (0, 0)
    title = create_font(Consts.FONT_PATH, 1)

    while True:
        screen.fill(Colors.BACKGROUND)
        if window.size != current_size:
            screen = window.get_surface()
            current_size = window.size
            title = create_font(Consts.FONT_PATH, get_font_size(screen, 20))

        w, h = current_size

        draw_text(
            "PAUSE",
            title,
            (255, 255, 255),
            screen,
            int(w / 2),
            int(h * 0.35),
        )

        help_text = "CONTINUE: P\nMENU: ESC"
        draw_lines(
            screen,
            help_text,
            3,
            int(w / 2),
            int(h * 0.5),
        )
        window.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameStates.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return GameStates.PLAYING
                if event.key == pygame.K_ESCAPE:
                    return GameStates.STOP
