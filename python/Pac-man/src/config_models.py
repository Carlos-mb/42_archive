"""Configuration models for the Pac-Man project."""

from src.constants import (
    Defaults,
    Mins,
)
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class LevelConfig(BaseModel):
    """Validated configuration for one maze level."""

    model_config = ConfigDict(extra="ignore")

    width: int = Field(default=Defaults.LEVEL_WIDTH, ge=Mins.LEVEL_SIZE)
    height: int = Field(default=Defaults.LEVEL_HEIGHT, ge=Mins.LEVEL_SIZE)


def create_default_levels() -> list[LevelConfig]:
    """Create the default list of level configurations.

    Returns:
        A list containing the default number of level configurations.
    """
    levels = []

    for _ in range(Defaults.LEVEL_COUNT):
        levels.append(LevelConfig())

    return levels


class GameConfig(BaseModel):
    """Validated top-level configuration for the game."""

    model_config = ConfigDict(extra="ignore")

    highscore_filename: Path = Path(Defaults.HIGHSCORE_FILENAME)

    lives: int = Field(default=Defaults.LIVES, ge=Mins.LIVES)

    points_per_pacgum: int = Field(
        default=Defaults.POINTS_PER_PACGUM,
        ge=Mins.SCORE_VALUE,
    )
    points_per_super_pacgum: int = Field(
        default=Defaults.POINTS_PER_SUPER_PACGUM,
        ge=Mins.SCORE_VALUE,
    )
    points_per_ghost: int = Field(
        default=Defaults.POINTS_PER_GHOST,
        ge=Mins.SCORE_VALUE,
    )

    seed: int = Defaults.SEED
    level_max_time: int = Field(
        default=Defaults.LEVEL_MAX_TIME,
        ge=Mins.LEVEL_TIME,
    )

    levels: list[LevelConfig] = Field(
        default_factory=create_default_levels,
        min_length=Defaults.LEVEL_COUNT,
    )
