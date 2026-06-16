import os
import json

from typing import Tuple, List
from pathlib import Path

from src.game import GameConfig


def get_highscores(path: Path) -> List[Tuple[str, int]]:
    """Load and sort the stored highscores.

    Args:
        path: Path to the highscore JSON file.

    Returns:
        Scores sorted from highest to lowest.
    """
    raw_score: List[Tuple[str, int]] = []
    try:
        with open(path, "r") as file:
            raw_score = json.load(file)
            for n, data in enumerate(raw_score, 1):
                text = f"Error in highscore nº{n}:"
                if not isinstance(data, list) or data == []:
                    raise ValueError(f"{text} Must be [name, pts]")
                if not isinstance(data[0], str):
                    raise ValueError(f"{text} The first value need"
                                     "to be a str")
                if not isinstance(data[1], int) or data[1] < 0:
                    raise ValueError(f"{text} The points value must be a "
                                     "positive number")
    except FileNotFoundError:
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
        except FileExistsError:
            pass
        with open(path, "w") as file:
            json.dump(raw_score, file, indent=4)
    except PermissionError:
        raise ValueError(f"Permission denied reading: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")

    try:
        highscores = [(name, score)
                      for name, score in raw_score]
        highscores = sorted(highscores, key=lambda val: val[1], reverse=True)
    except ValueError:
        raise ValueError("Invalid .json for highscore")
    return highscores


def get_idx_score(scores: List[Tuple[str, int]], score: int) -> int:
    """Return the zero-based display position for a score.

    Args:
        scores: Existing highscore entries.
        score: Score to place in the ranking.

    Returns:
        The score's rank index.
    """
    pts = [score[1]
           for score in scores]
    pts.append(score)
    pts = sorted(pts, reverse=True)
    idx = len(pts) - 1 - next(i
                              for i,
                              v in enumerate(reversed(pts)) if v == score)
    return idx


def update_highscore(path: Path, name: str, score: int) -> None:
    """Insert a score into the persistent leaderboard.

    Args:
        path: Path to the highscore JSON file.
        name: Player name to store.
        score: Score value to persist.
    """
    try:
        old_scores: List[Tuple[str, int]] = get_highscores(path)
        with open(path, "w") as file:
            old_scores.append((name, score))
            old_scores = sorted(old_scores, key=lambda val: val[1],
                                reverse=True)
            if len(old_scores) > 9:
                old_scores.pop()
            json.dump(old_scores, file, indent=4)

    except FileNotFoundError:
        raise ValueError(f"Input file not found {path}")
    except PermissionError:
        raise ValueError(f"Permission denied writting: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def check_new_highscore(config: GameConfig, score: int) -> bool:
    """Return True when a score belongs in the top 10.

    Args:
        config: Loaded game configuration.
        score: Score to evaluate.

    Returns:
        True when the score beats the leaderboard threshold.
    """
    h_scores: List[Tuple[str, int]] = get_highscores(config.highscore_filename)
    if len(h_scores) < 10:
        h_scores.append(("", 0))
    h_scores = sorted(h_scores, key=lambda val: val[1])
    lowest_score = h_scores[0][1]
    return score > lowest_score
