*This project has been created as part of the 42 curriculum by cagil, cmelero-*

# Pac-Man 
---
## Description

### Graphical Library Choice

This project uses `pygame-ce` as its graphical library.

The subject requires the game to be written in Python and to use a simple graphical library, such as MLX or a similar alternative. We chose `pygame-ce` because it provides a direct and practical API for building a 2D arcade game while keeping the implementation understandable and maintainable.

Pac-Man is mainly based on a grid, keyboard input, simple 2D rendering, text display, timing, menus, and collision checks. `pygame-ce` supports these needs without requiring a complex game engine or low-level graphics programming. This makes it suitable for a project where the priority is to deliver a complete, playable game with a clear object-oriented architecture.

We considered using MLX because it is commonly used in 42 projects, but we decided not to use it for this project. The subject allows “MLX or similar”, and `pygame-ce` offers a better fit for a Python game that must include a polished UI, menus, highscores, a game-over screen, and packaging for a public gaming platform. It also reduces the risk of spending too much time on platform-specific graphical setup instead of implementing the actual game logic.

The project architecture keeps the game logic separated from the graphical layer. Classes such as the maze, player, ghosts, score, levels, configuration, and highscores do not depend directly on `pygame-ce`. The library is mainly used for window management, input handling, rendering, fonts, timing, and optional sound. This separation makes the code easier to test, maintain, and explain during peer review.

Using `pygame-ce` also helps with packaging, because it is widely used for Python games and can be bundled with tools such as PyInstaller. The goal is to provide a minimal, functional package for Linux that can be uploaded to a platform such as Itch.io, as required by the subject.

---

## Instructions
### Requirements

- **Python** 3.10 or later
- **pip**
- **pygame**
- **pydantic**
- An external **A-Maze-ing** package (assigned by the 42 curriculum)

### Installation
1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies (**A-Maze-ing** package provided separately):

```bash
make install
```

### Running the Game

Launch the game from the command line with a configuration file:

```bash
python3 pac-man.py <config-file.json> | make run
```

The program takes **exactly one argument**: a JSON configuration file. If the file is missing, invalid, or contains errors, the game will fall back to safe default values and log a warning message — **never crashing with a traceback**.

### Controls

| Action | Key |
|--------|-----|
| Move Up | ↑ Arrow|
| Move Down | ↓ Arrow|
| Move Left | ← Arrow|
| Move Right | → Arrow|
| Pause | P |
| Level Skip (Cheat) | Hold Down Right Shift |

### Cheat Mode

For peer review and testing purposes, the following cheat features are available:

- **Invincibility**: Pac-Man does not lose lives when touched by ghosts.
- **Level Skip**: Press `R` during gameplay to immediately win the current level.
- **Ghost Freeze**: Ghosts stop moving (can be toggled via code modification).
- **Extra Lives**: Additional lives can be granted.
- **Increased Speed**: Player moves faster.

> [!IMPORTANT]
> Cheat mode is intended to facilitate testing of all game features during peer review.

---

## Configuration

The game reads its settings from a **JSON file with comments** (lines starting with `#` are ignored). The exact structure is flexible — missing or invalid values are clamped to safe defaults with a warning logged to stderr. Unknown keys are ignored.

### Example `config.json`

```json
# Pac-Man Configuration File
# Lines starting with # are ignored

{
  "highscore_filename": "highscores.json",
  "lives": 3,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 21,
  "level_max_time": 90,
  "levels": [
    {
      "width": 5,
      "height": 11
    },
    {
      "width": 14,
      "height": 18
    }
	...
  ]
}
```

### Configuration Keys

| Key | Type | Default | Description |
|-----|:----:|:-------:|-------------|
| `highscore_filename` | string | `"highscores.json"` | Path to the highscore JSON file |
| `lives` | int | `3` | Starting lives (minimum: 1) |
| `points_per_pacgum` | int | `10` | Score for eating a regular pacgum (minimum: 0) |
| `points_per_super_pacgum` | int | `50` | Score for eating a super-pacgum (minimum: 0) |
| `points_per_ghost` | int | `200` | Score for eating an edible ghost (minimum: 0) |
| `seed` | int | `42` | Random seed for the first level's maze generation |
| `level_max_time` | int | `90` | Time limit per level in seconds (minimum: 1) |
| `levels` | array | 10 default levels | List of level configurations, each with `width` and `height` (minimum: 5) |

---

## Highscore

The highscore system persists the top 10 scores across game sessions in a **JSON file** (default: `highscores.json`).

JSON was chosen for its simplicity, human readability, and native Python support. It requires no external database and makes debugging and manual inspection straightforward. The file is small (maximum 10 entries), so performance is never a concern.

### Highscore File Format

```json
[
    ["AAA", 1500],
    ["BBB", 1200],
    ["CCC", 900]
]
```

### Features

- **Persistent storage**: Scores are saved to disk and loaded at game start.
- **Robust error handling**: Missing files, permission errors, or invalid JSON are handled gracefully — the system initializes an empty leaderboard rather than crashing.
- **Player name validation**: Names are limited to **10 characters**, allowing only alphanumeric characters and spaces.
- **Score validation**: Only non-negative integers are accepted.
- **Top 10 display**: The main menu shows the top 10 scores with color-coded rankings.
- **Name entry**: After winning or losing, the player is prompted to enter their name to save their score.

---

## Maze Generation

This project **does not implement its own maze generator**. Instead, it integrates an assigned **A-Maze-ing** package from another 42 team, adapting to its interface rather than modifying it.

### Integration

The game uses the `MazeGenerator` class from the external package:

```python
from mazegenerator import MazeGenerator

maze = MazeGenerator(
    size=(width, height),
    perfect=False,  # Imperfect maze for Pac-Man-compatible corridors
    seed=seed
)
```

- **`perfect=False`**: Produces imperfect mazes with loops, which are necessary for Pac-Man-style gameplay where the player can circle around.
- **Seed**: The first level uses a fixed seed (`42` by default) for reproducibility. Subsequent levels use an incremented seed for random generation.
- **Error handling**: If the generator fails (e.g., invalid dimensions), the error is caught and the game falls back to safe defaults or exits cleanly with a message.

### Maze Grid Format

The maze is represented as a 2D list of integers where each cell encodes walls as a 4-bit bitmask:

| Bit | Value | Wall |
|-----|-------|------|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A cell with value `15` has all walls intact (a solid block). Value `0` means no walls.

---
## Implementation

### Game Loop

```
Main Menu → Start Game → Play Level → Win/Lose/Time Out
                                    ↓
                        Enter Name for Highscore
                                    ↓
                            Back to Main Menu
```

### Key Mechanics

- **Movement**: The player moves at a base speed of 2 pixels per frame. Diagonal movement is allowed but speed is reduced by `√2` to maintain consistent velocity.
- **Collision Detection**: Pixel-perfect collision against the maze background surface. The player's bounding box is checked against wall pixels before each movement step.
- **Pacgum Collection**: Front-facing pixels are checked against the transparent pacgum surface. When a pacgum is eaten, it is erased from the surface and the score is updated.
- **Super-Pacgums**: Four large dots placed in the maze corners. Eating one makes ghosts edible for 10 seconds (`EATING_TIME`).
- **Ghost AI**: Two distinct AI behaviors:
  - **GhostIa01**: Smart pathfinding with backtracking avoidance, random exploration at intersections, and periodic refocusing on the player.
  - **GhostIa02**: Greedy chase using Manhattan distance to select the best neighbor cell at each intersection.
- **Edible Ghosts**: When a super-pacgum is active, ghosts turn blue and run away from the player. Eating an edible ghost awards bonus points.
- **Ghost Respawn**: Ghosts respawn at their original corner positions after being eaten.
- **Level Progression**: The game consists of at least 10 levels. The player keeps their score and remaining lives between levels. Each new level generates a larger or differently-sized random maze.
- **Time Limit**: Each level has a time limit (default: 90 seconds). When time runs out, the level ends.
- **Pause**: Pressing Escape pauses the game, showing options to resume or return to the main menu.

### Scoring

| Action | Points |
|--------|--------|
| Eat Pacgum | `points_per_pacgum` (default: 10) |
| Eat Super-Pacgum | `points_per_super_pacgum` (default: 50) |
| Eat Edible Ghost | `points_per_ghost` (default: 200) |

### Window & Rendering

- The game window is resizable. The internal game surface is scaled to fit while maintaining aspect ratio.
- A HUD (10% of game height) displays score, lives, level, and remaining time.
- All rendering uses pygame surfaces: a static maze background, a dynamic pacgum overlay, and entity sprites.
- Sprite animation is frame-based, cycling through mouth-open/closed states for Pac-Man.

---
## General Software Architecture

### Module Overview

```
pac-man.py          # Entry point: argument parsing, main state machine
game.py             # GameGenerator: level generation, game loop, rendering
people.py           # Person, Player, Ghost: entity logic, sprites, movement
ghostia01.py        # GhostIa01: advanced ghost AI with pathfinding
ghostia02.py        # GhostIa02: greedy distance-based ghost AI
config_loader.py    # JSON config parsing with comment removal and validation
config_models.py    # Pydantic models for type-safe configuration
constants.py        # Game constants: sizes, colors, defaults, states
functions.py        # Utility functions: cell coordinate conversions
highscore.py        # Persistent highscore loading, validation, and updating
visual.py           # UI rendering: main menu, highscore display, name entry
```

### Class Relationships

```
GameGenerator
├── Player (from people.py)
├── Ghost[0..3] (from people.py)
│   ├── GhostIa01 (ghostia01.py)  # Ghosts 0 & 2
│   └── GhostIa02 (ghostia02.py)  # Ghosts 1 & 3
├── MazeGenerator (external: A-Maze-ing package)
├── GameConfig (from config_models.py)
└── Surfaces (maze, pacgums, HUD, world)

Person (abstract base)
├── Player
└── Ghost

GameConfig (Pydantic BaseModel)
└── LevelConfig[]
```

### State Machine

The game uses two state enums:

- **`GameStates`** (in-game): `EXIT`, `PLAYING`, `STOP`, `NEXT`, `NONE`
- **`ProgramState`** (application): `MENU`, `PLAY`, `NEW_SCORE`, `WIN`, `DEAD`, `QUIT`

The main loop in `pac-man.py` uses a `match` statement to transition between program states based on user actions and game outcomes.

### Data Flow

1. **Config loading**: `config_loader.py` reads and validates the JSON file, producing a `GameConfig` object.
2. **Level generation**: `GameGenerator.generate()` creates the maze, places pacgums, and spawns entities.
3. **Game loop**: `handle_events()` → `update()` (movement, collision, scoring) → `draw()` (rendering).
4. **Highscore**: At game end, `highscore.py` loads existing scores, inserts the new one if it qualifies, sorts, trims to top 10, and writes back to disk.
---

## Resources



## References

- [pacman in python](https://www.youtube.com/watch?&v=hebtgq99sBg)
- [pacman in python](https://www.youtube.com/watch?v=9H27CimgPsQ)
- [pygame Documentation](https://www.pygame.org/docs/)

AI assistance was used for:
- Docstring formatting and PEP 257 compliance.
- Debugging edge cases in ghost AI pathfinding and collision detection.
- Structuring the README and project documentation.

## Explanations

The game takes into account screen pixels, not cells. That's why gums can only be eaten if they are encountered head-on. The gum in the exit cell isn't eaten until Pac-Man touches it with his mouth. If the corridors are large enough, Pac-Man and ghosts can move diagonally.



Si no se puede mover en diagonal, debería ir más rápido recto. No se debe dividir la velocidad.

Revisa que se usan todos los valores de constansts.py para algo y que los defaults no se usan, excepto para cargar la configuración

Tecla de pausa (no ESC)