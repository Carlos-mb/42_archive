"""Configuration loading utilities for the Pac-Man project."""

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.config_models import (
    Defaults,
    Mins,
    GameConfig,
    LevelConfig,
    create_default_levels,
)


def print_warning(message: str) -> None:
    """Print a warning message to standard error.

    Args:
        message: Warning text to display.
    """
    print(f"Warning: {message}", file=sys.stderr)


def remove_json_comments(content: str) -> str:
    """Remove comment lines from JSON-like configuration content.

    Args:
        content: Raw configuration file content.

    Returns:
        The content without lines that start with ``#``.
    """
    lines: list[str] = []

    for line in content.splitlines():
        stripped_line = line.lstrip()

        if stripped_line.startswith("#"):
            continue

        lines.append(line)

    return "\n".join(lines)


def get_int_value(
    data: dict[str, Any],
    key: str,
    default: int,
    min_value: int | None = None,
    label: str | None = None,
) -> int:
    """Read and validate an integer field from configuration data.

    Args:
        data: Raw configuration dictionary.
        key: Field name to read.
        default: Value used when the field is missing or invalid.
        min_value: Optional lower bound for the value.
        label: Optional display name used in warnings.

    Returns:
        A validated integer value.
    """

    if label is None:
        field_name = key
    else:
        field_name = label

    if key not in data:
        print_warning(
            f"missing '{field_name}'. Using default value: {default}."
        )
        return default

    value = data[key]

    # # in python, bool is also int
    # if isinstance(value, bool) or not isinstance(value, int):
    if type(value) is not int:
        print_warning(
            f"invalid '{field_name}'. Using default value: {default}."
        )
        return default

    if min_value is not None and value < min_value:
        print_warning(
            f"'{field_name}' is too small. "
            f"Using default value: {default}."
        )
        return default

    return value


def get_path_value(
    data: dict[str, Any],
    key: str,
    default: str,
) -> Path:
    """Read and validate a path field from configuration data.

    Args:
        data: Raw configuration dictionary.
        key: Field name to read.
        default: Default filename used when the field is missing or invalid.

    Returns:
        A validated path value.
    """
    if key not in data:
        print_warning(
            f"missing '{key}'. Using default value: {default}."
        )
        return Path(default)

    value = data[key]

    if not isinstance(value, str) or value.strip() == "":
        print_warning(
            f"invalid '{key}'. Using default value: {default}."
        )
        return Path(default)

    return Path(value)


def get_level_config(raw_level: Any, level_index: int) -> LevelConfig:
    """Build one validated level configuration.

    Args:
        raw_level: Raw level data from the configuration file.
        level_index: Zero-based index used in warning messages.

    Returns:
        A validated level configuration.
    """
    if not isinstance(raw_level, dict):
        print_warning(
            f"invalid 'levels[{level_index}]'. Using default level."
        )
        return LevelConfig()

    level_data: dict[str, Any] = raw_level

    width = get_int_value(
        level_data,
        "width",
        Defaults.LEVEL_WIDTH,
        Mins.LEVEL_SIZE,
        f"levels[{level_index}].width",
    )
    height = get_int_value(
        level_data,
        "height",
        Defaults.LEVEL_HEIGHT,
        Mins.LEVEL_SIZE,
        f"levels[{level_index}].height",
    )

    return LevelConfig(width=width, height=height)


def get_levels_value(data: dict[str, Any]) -> list[LevelConfig]:
    """Read and normalize the levels list from configuration data.

    Args:
        data: Raw configuration dictionary.

    Returns:
        A list of validated level configurations.
    """
    if "levels" not in data:
        print_warning("missing 'levels'. Using default levels.")
        return create_default_levels()

    raw_levels = data["levels"]

    if not isinstance(raw_levels, list):
        print_warning("invalid 'levels'. Using default levels.")
        return create_default_levels()

    levels: list[LevelConfig] = []

    for index, raw_level in enumerate(raw_levels):
        level = get_level_config(raw_level, index)
        levels.append(level)

    if len(levels) < Defaults.LEVEL_COUNT:
        print_warning(
            f"only {len(levels)} level(s) found. "
            f"Adding default levels up to {Defaults.LEVEL_COUNT}."
        )

    while len(levels) < Defaults.LEVEL_COUNT:
        levels.append(LevelConfig())

    return levels


def build_config_data(raw_config: dict[str, Any]) -> dict[str, Any]:
    """Build a sanitized configuration dictionary field by field.

    Args:
        raw_config: Raw configuration dictionary loaded from JSON.

    Returns:
        A dictionary that is safe to validate with ``GameConfig``.
    """
    config_data: dict[str, Any] = {
        "highscore_filename": get_path_value(
            raw_config,
            "highscore_filename",
            Defaults.HIGHSCORE_FILENAME,
        ),
        "lives": get_int_value(
            raw_config,
            "lives",
            Defaults.LIVES,
            Mins.LIVES,
        ),
        "points_per_pacgum": get_int_value(
            raw_config,
            "points_per_pacgum",
            Defaults.POINTS_PER_PACGUM,
            Mins.SCORE_VALUE,
        ),
        "points_per_super_pacgum": get_int_value(
            raw_config,
            "points_per_super_pacgum",
            Defaults.POINTS_PER_SUPER_PACGUM,
            Mins.SCORE_VALUE,
        ),
        "points_per_ghost": get_int_value(
            raw_config,
            "points_per_ghost",
            Defaults.POINTS_PER_GHOST,
            Mins.SCORE_VALUE,
        ),
        "level_max_time": get_int_value(
            raw_config,
            "level_max_time",
            Defaults.LEVEL_MAX_TIME,
            Mins.LEVEL_TIME,
        ),
        "levels": get_levels_value(raw_config),
    }

    if "seed" in raw_config:
        config_data["seed"] = get_int_value(
            raw_config,
            "seed",
            42,
        )

    return config_data


def load_config(config_path: Path) -> GameConfig:
    """Load, sanitize, and validate the game configuration file.

    Args:
        config_path: Path to the JSON configuration file.

    Returns:
        A validated game configuration.
    """
    if not config_path.exists():
        print_warning(
            f"configuration file not found: {config_path}. "
            "Using default configuration."
        )
        return GameConfig()

    if not config_path.is_file():
        print_warning(
            f"configuration path is not a file: {config_path}. "
            "Using default configuration."
        )
        return GameConfig()

    try:
        content = config_path.read_text(encoding="utf-8")
        content = remove_json_comments(content)
        raw_config = json.loads(content)
    except OSError as error:
        print_warning(
            f"could not read configuration file: {error}. "
            "Using default configuration."
        )
        return GameConfig()
    except json.JSONDecodeError as error:
        print_warning(
            f"invalid JSON configuration file: {error}. "
            "Using default configuration."
        )
        return GameConfig()

    if not isinstance(raw_config, dict):
        print_warning(
            "configuration root must be a JSON object. "
            "Using default configuration."
        )
        return GameConfig()

    config_data = build_config_data(raw_config)

    try:
        return GameConfig.model_validate(config_data)
    except ValidationError:
        print_warning(
            "configuration validation failed. "
            "Using default configuration."
        )
        return GameConfig()
