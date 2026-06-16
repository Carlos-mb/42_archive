# Acceptance Test Plan

## Test Categories

### 1. Configuration Loading

| ID | Test Case |
|----|-----------|
| CFG-01 | Valid config file |
| CFG-02 | Missing config file |
| CFG-03 | Invalid JSON |
| CFG-04 | Missing keys |
| CFG-05 | Invalid value type |
| CFG-06 | Value below minimum |
| CFG-07 | Comments in JSON |
| CFG-08 | Unknown keys |
| CFG-09 | Wrong argument count |
| CFG-10 | Non-JSON file |

### 2. Game Loop & Mechanics

| ID | Test Case |
|----|-----------|
| GM-01 | Player movement |
| GM-02 | Wall collision |
| GM-03 | Pacgum collection | 
| GM-04 | Super-pacgum collection |
| GM-05 | Edible ghost eating | 
| GM-06 | Ghost collision (normal) |
| GM-07 | Life decrement ||
| GM-08 | Win level |
| GM-09 | Time limit |
| GM-10 | Level progression | 
| GM-11 | Pause game |
| GM-12 | Resume from pause | 
| GM-13 | Quit to menu from pause |

### 3. Ghost AI

| ID | Test Case |
|----|-----------|
| AI-01 | Ghost movement |
| AI-02 | Ghost chase |
| AI-03 | Ghost flee |
| AI-04 | Ghost respawn |
| AI-05 | No wall clipping |
| AI-06 | Ghost speed |

### 4. Highscore System

| ID | Test Case |
|----|-----------|
| HS-01 | Display highscores |
| HS-02 | New highscore |
| HS-03 | Name entry |
| HS-04 | Name validation |
| HS-05 | Name length |
| HS-06 | Empty highscore file |
| HS-07 | Corrupt highscore file |
| HS-08 | Top 10 limit |
| HS-09 | Score persistence |
| HS-10 | Negative score |

### 5. Cheat Mode

| ID | Test Case |
|----|-----------|
| CH-01 | Level skip |
| CH-02 | Invincibility |
| CH-03 | Laberinth without walls |

### 6. UI / UX

| ID | Test Case |
|----|-----------|
| UI-01 | Main menu display |
| UI-02 | Start game |
| UI-03 | HUD elements |
| UI-04 | Time display |
| UI-05 | Game over screen |
| UI-06 | Victory screen |
| UI-07 | Window resize |
| UI-08 | Blinking text |

### 7. Error Handling & Robustness

| ID | Test Case |
|----|-----------|
| ERR-01 | Missing sprite sheet |
| ERR-02 | Missing font file |
| ERR-03 | Maze generator failure |
| ERR-04 | Invalid maze dimensions |
| ERR-05 | Keyboard interrupt |

---

## Bug Log

| ID | Description |
|----|-------------|
| BUG-01 | `get_highscores` crashes if file doesn't exist |
| BUG-02 | `update_highscore` keeps 11 entries instead of 10 |
| BUG-03 | Player-ghost collision never detected |
| BUG-04 | Win condition (all pacgums eaten) not checked |
| BUG-05 | Time limit not enforced |
| BUG-06 | Pause menu not implemented |
| BUG-07 | `is_valid_char` returns method object instead of bool |
| BUG-08 | Ghosts don't respawn after being eaten |
| BUG-09 | Level loop in `start_level` doesn't regenerate properly |
| BUG-10 | `col -= 1` in player spawn can go negative |
| BUG-11 | WASD controls not implemented (only arrows) |
| BUG-12 | `GameGenerator` attributes not declared in `__init__` |
| BUG-13  | `visual.py` color type hints use `Tuple[int]` instead of `Tuple[int,int,int]` |

---