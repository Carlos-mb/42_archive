from src.constants import Consts
import pygame
from typing import Callable, cast
import sys
from src.functions import get_cell
import time

PEOPLE_SIZE = Consts.PEOPLE_SIZE


class Person():
    """Base moving entity shared by the player and ghosts."""

    def __init__(self, x: int, y: int):
        """Create a person at the given pixel position.

        Args:
            x: Initial x coordinate.
            y: Initial y coordinate.
        """
        self.x = x
        self.y = y
        self.width = PEOPLE_SIZE
        self.height = PEOPLE_SIZE
        self.rect: pygame.rect.Rect
        self.speed = Consts.SPEED
        self.color: tuple[int, int, int] = (0, 0, 0)
        self.direction: int = 1
        self.animation: int = 0
        self.images: list
        self.id: int
        self.last_cell: tuple[int, int] = get_cell(x, y)
        self.start_x: int = self.x
        self.start_y: int = self.y

        self.subpixel_x: int = 0
        self.subpixel_y: int = 0

        self.speed_percent: int = 100
        self.move_charge: int = 0
        self.time_to_respawn: float = Consts.TIME_TO_GHOST_RESPAWN

        try:
            self.sprite_sheet = pygame.image.load(
                Consts.SPRITE_SHEET,
            ).convert_alpha()
        except Exception as error:
            print(f"Error loading sprite sheet {error}")
            pygame.quit()
            sys.exit(1)

    def should_move(self) -> bool:
        """Return True when the ghost can move this frame."""
        self.move_charge += self.speed_percent

        if self.move_charge < 100:
            return False

        self.move_charge -= 100
        return True

    def move(self, x: int, y: int) -> None:
        """Move the entity to a new pixel position.

        Args:
            x: Target x coordinate.
            y: Target y coordinate.
        """
        if self.time_to_respawn < time.time():
            if not self.should_move():
                return

            start_cell = get_cell(x, y)

            if x != self.x:
                self.direction = 1 if x > self.x else 0
            elif y != self.y:
                self.direction = 2 if y > self.y else 3

            self.x = x
            self.y = y
            self.rect.center = (self.x, self.y)

            if start_cell != get_cell(self.x, self.y):
                self.last_cell = start_cell

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draw the entity on the given screen surface.

        Args:
            screen: Target surface to draw on.
        """
        pass


class Player(Person):
    """Pac-Man controlled by the keyboard."""

    def __init__(self, x: int, y: int, lives: int):
        """Create the player entity.

        Args:
            x: Initial x coordinate.
            y: Initial y coordinate.
            lives: Starting number of lives.
        """
        super().__init__(x, y)

        self.lives = lives
        self.images = []
        s = Consts.SPRITE_SIZE

        # transparent key, 1st pixel of sprite
        key = self.sprite_sheet.get_at((0, 0))
        self.id = 0

        for i in range(4):
            n = 32 * i
            self.images.append([
                pygame.Surface((s, s), pygame.SRCALPHA),
                pygame.Surface((s, s), pygame.SRCALPHA),
            ])

            self.images[i][0].blit(
                self.sprite_sheet,
                (0, 0),
                (n, 0, Consts.SPRITE_SIZE, Consts.SPRITE_SIZE),
            )
            self.images[i][1].blit(
                self.sprite_sheet,
                (0, 0),
                (n, s, Consts.SPRITE_SIZE, Consts.SPRITE_SIZE),
            )

            # scale frame to game size
            self.images[i][0] = pygame.transform.scale(
                self.images[i][0],
                (PEOPLE_SIZE, PEOPLE_SIZE),
            )
            self.images[i][1] = pygame.transform.scale(
                self.images[i][1],
                (PEOPLE_SIZE, PEOPLE_SIZE),
            )

            self.images[i][0].set_colorkey((key[0], key[1], key[2]))
            self.images[i][1].set_colorkey((key[0], key[1], key[2]))

        self.animation = 0
        self.rect = self.images[1][self.animation].get_rect(
            center=(self.x, self.y),
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draw the player animation on the screen.

        Args:
            screen: Target surface to draw on.
        """
        ratio = Consts.FPS / 10
        if self.animation <= self.speed * ratio / 2:
            animation = 1
        else:
            animation = 0

        self.animation = (
            self.animation + 1
            if self.animation < self.speed * ratio
            else 0
        )
        screen.blit(self.images[self.direction][animation], self.rect)


class Ghost(Person):
    """Enemy entity driven by a pluggable chasing strategy."""

    def __init__(
        self,
        x: int,
        y: int,
        number: int,
        chaser: Callable[[int, int], tuple[int, int]] | None = None,
    ):
        """Create a ghost entity.

        Args:
            x: Initial x coordinate.
            y: Initial y coordinate.
            number: Ghost index used to pick its sprite.
            chaser: Optional movement strategy used for chasing.
        """
        super().__init__(x, y)

        self.chaser: Callable[[int, int], tuple[int, int]] = (
            chaser or self.chase
        )
        self.id = number + 1
        self.destination: tuple[int, int]

        self.images: list[pygame.Surface] = []

        key = self.sprite_sheet.get_at((0, 0))
        self.speed_percent: int = 80

        ghostn: int = 0
        self.is_live: bool = True
        self.eating_until: float = 0.0

        self.images_scared: list[pygame.Surface] = []

        for i in [2, 3, 1, 0]:
            n = (Consts.SPRITE_SIZE * 2) + Consts.SPRITE_SIZE * i
            self.images.append(
                pygame.Surface(
                    (Consts.SPRITE_SIZE, Consts.SPRITE_SIZE),
                    pygame.SRCALPHA,
                )
            )

            self.images[ghostn].blit(
                self.sprite_sheet,
                (0, 0),
                (
                    number * Consts.SPRITE_SIZE,
                    n,
                    Consts.SPRITE_SIZE,
                    Consts.SPRITE_SIZE,
                ),
            )
            self.images[ghostn] = cast(
                pygame.Surface,
                pygame.transform.scale(
                    self.images[ghostn],
                    (PEOPLE_SIZE, PEOPLE_SIZE),
                ),
            )
            self.images[ghostn].set_colorkey((key[0], key[1], key[2]))
            ghostn += 1

            self.images_scared.append(
                pygame.Surface(
                    (Consts.SPRITE_SIZE, Consts.SPRITE_SIZE),
                    pygame.SRCALPHA,
                )
            )
            self.images_scared[0].blit(
                self.sprite_sheet,
                (0, 0),
                (
                    5 * Consts.SPRITE_SIZE,
                    2 * Consts.SPRITE_SIZE,
                    Consts.SPRITE_SIZE,
                    Consts.SPRITE_SIZE,
                ),
            )
            self.images_scared[0] = cast(
                pygame.Surface,
                pygame.transform.scale(
                    self.images_scared[0],
                    (PEOPLE_SIZE, PEOPLE_SIZE),
                ),
            )
            self.images_scared[0].set_colorkey((key[0], key[1], key[2]))

            self.images_scared.append(
                pygame.Surface(
                    (Consts.SPRITE_SIZE, Consts.SPRITE_SIZE),
                    pygame.SRCALPHA,
                )
            )
            self.images_scared[1].blit(
                self.sprite_sheet,
                (0, 0),
                (
                    5 * Consts.SPRITE_SIZE,
                    3 * Consts.SPRITE_SIZE,
                    Consts.SPRITE_SIZE,
                    Consts.SPRITE_SIZE,
                ),
            )
            self.images_scared[1] = cast(
                pygame.Surface,
                pygame.transform.scale(
                    self.images_scared[1],
                    (PEOPLE_SIZE, PEOPLE_SIZE),
                ),
            )
            self.images_scared[1].set_colorkey((key[0], key[1], key[2]))

        self.animation = 0
        self.rect = self.images[0].get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draw the ghost on the given screen surface.

        Args:
            screen: Target surface to draw on.
        """
        screen.blit(self.images[self.direction], self.rect)

    def draw_scared(
        self,
        screen: pygame.surface.Surface,
        limit_time: float,
    ) -> None:
        """Draw the scared ghost animation while the power-up lasts.

        Args:
            screen: Target surface to draw on.
            limit_time: Absolute timestamp when the scared state ends.
        """
        if self.time_to_respawn < time.time():
            if limit_time - time.time() > 2:
                screen.blit(self.images_scared[0], self.rect)
            elif int(limit_time * 10 - time.time() * 10) % 4 == 0:
                screen.blit(self.images_scared[1], self.rect)
            else:
                screen.blit(self.images_scared[0], self.rect)

    def chase(self, px: int, py: int) -> tuple[int, int]:
        """Return a movement vector that heads toward the target point.

        Args:
            px: Target x coordinate.
            py: Target y coordinate.

        Returns:
            A movement vector as ``(movx, movy)``.
        """
        movx: int = 0
        movy: int = 0

        if px < self.x:
            movx = -min(self.speed, abs(px - self.x))
        elif px > self.x:
            movx = min(self.speed, abs(px - self.x))

        if py < self.y:
            movy = -min(self.speed, abs(py - self.y))
        elif py > self.y:
            movy = min(self.speed, abs(py - self.y))

        return movx, movy
