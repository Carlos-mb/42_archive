# Risk Analysis

## Risk Register

| ID | Risk | Mitigation Strategy |
|----|------|---------------------|
| R01 | **A-Maze-ing package incompatible** — The assigned maze generator may have an unexpected API, return format, or fail to install | Contact the other team early; read their documentation; implement adapter pattern; have a fallback simple maze generator for testing |
| R02 | **pygame performance issues** — Large mazes or many entities may cause frame drops below 60 FPS | Profile with `cProfile`; optimize rendering (only redraw changed regions); reduce FPS target if needed; use `convert()` on all surfaces |
| R03 | **JSON config corruption** — User may edit config file incorrectly, causing parse errors | Robust fallback to defaults; clear warning messages; validate with Pydantic; ignore unknown keys |
| R04 | **Ghost AI too easy or too hard** — Balancing chase behavior for fun gameplay is subjective | Implement multiple AI strategies; make ghost speed configurable; add cheat mode for testing; peer playtesting |
| R05 | **Highscore file permissions** — Game may not have write access to the highscore file location | Handle `PermissionError` gracefully; allow config to specify path; default to user-writable directory; test on restricted accounts |
| R06 | **Sprite assets missing** — The sprite sheet or font files may not be present on the evaluator's machine | Provide fallback rendering (colored rectangles/pygame default font); document asset requirements; bundle assets in package |
| R07 | **Python version incompatibility** — Evaluator may use Python < 3.10 | Document requirement clearly; use only 3.10+ features intentionally (match statements); test on 3.10, 3.11, 3.12 |
| R08 | **mypy strict mode failures** — Type hints may be incomplete or incorrect, causing CI failures | Run mypy frequently during development; use `pyproject.toml` to configure strictness; fix errors immediately rather than batching |
| R09 | **Peer review package reinstall** — The A-Maze-ing package will be reinstalled during defense; our code must work with the "official" version | Never modify the package; test with fresh install in clean venv; pin version in requirements if possible; document exact version used |
| R10 | **Packaging complexity** — Creating a distributable for Itch.io/Steam may be harder than expected | Start packaging early (Sprint 6); use `PyInstaller` or `cx_Freeze`; test the built executable; provide clear install instructions |
| R11 | **Time limit not fun** — 90 seconds per level may feel too short or too long | Make time limit configurable; gather playtest feedback; adjust default based on average completion time |

---

## Mitigation Details

### R01 — A-Maze-ing Package Incompatibility
**What happened**: The assigned package's `MazeGenerator` constructor expected `size=(width, height)` with `perfect=False`. Our initial assumption was `size=(height, width)`. We discovered this during Sprint 2 integration testing.
**Resolution**: Added an adapter layer in `game.py` that explicitly maps our coordinate system to the package's expected format. Added error handling for constructor failures.

### R06 — Sprite Assets Missing
**What happened**: During initial testing on a clean VM without the `src/sprites/` directory, the game crashed with `FileNotFoundError`.
**Resolution**: Added fallback rendering in `Player` and `Ghost` classes — if the sprite sheet is missing, entities are drawn as colored rectangles. Added fallback font loading in `visual.py`.

### R09 — Peer Review Package Reinstall
**What happened**: We initially considered patching the A-Maze-ing package locally to fix a minor bug.
**Resolution**: Team decision to never modify the package. We adapted our code to work around the issue. Added a compatibility test in our test suite.
