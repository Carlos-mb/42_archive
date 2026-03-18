# Validation tools for Fly-in

This repository includes two helper scripts to test and validate Fly-in simulation outputs:

- `validate_simulation.py`
- `run_all.sh`

These tools are intended to verify that a generated solution is **valid according to the project rules**.  
They do **not** check whether the solution is optimal.

---

## Files

### `validate_simulation.py`

Validates a solution file against a map file.

It checks:

- graph topology
- valid zone-to-zone movement
- valid restricted-zone transit
- connection capacities
- zone capacities
- that drones in transit arrive on the next turn
- that drones do not move after reaching `goal`
- that all drones eventually reach `goal`

It does **not** evaluate performance or turn optimality.

### `run_all.sh`

Runs `fly-in.py` on all `.txt` maps found in:

- `../maps/easy`
- `../maps/medium`
- `../maps/hard`
- `../maps/challenger`

For each map, it:

1. executes `python3 ./fly-in.py <mapfile>`
2. saves the output into `./soluciones/`
3. validates that output with `validate_simulation.py`

---

## Requirements

- Linux
- Python 3
- Bash

---

## How to use `validate_simulation.py`

### Syntax

```bash
python3 validate_simulation.py MAP_FILE SOLUTION_FILE
````

### Example

```bash
python3 validate_simulation.py ../maps/hard/01_maze_nightmare.txt salida
```

### Output

If the simulation is valid:

```text
VALID
```

If the simulation is invalid:

```text
INVALID: <reason>
```

### Notes

* The validator checks correctness only.
* It accepts solution lines with or without prefixes such as `T1:`.
* It supports outputs containing ANSI color codes, because those are stripped before validation.
* Restricted-zone moves must be represented using the connection name on the first turn, and the restricted zone name on the following turn.

Example:

```text
T3: D1-maze_a2-trap_loop1
T4: D1-trap_loop1
```

---

## How to use `run_all.sh`

### Syntax

```bash
./run_all.sh
```

### Example

```bash
chmod +x run_all.sh
./run_all.sh
```

### What it does

For every `.txt` file inside the map directories, the script:

* runs `fly-in.py`
* stores the generated output in `./soluciones/`
* validates that output using `validate_simulation.py`

Generated solution files are named like this:

```text
easy__example_map.out
hard__01_maze_nightmare.out
```

This avoids filename collisions between directories.

---

## Expected project structure

Example:

```text
.
├── fly-in.py
├── validate_simulation.py
├── run_all.sh
├── soluciones/
└── ../maps/
    ├── easy/
    ├── medium/
    ├── hard/
    └── challenger/
```

`run_all.sh` assumes:

* `fly-in.py` is in the current directory
* `validate_simulation.py` is in the current directory
* the maps are in `../maps/...`

---

## Typical workflow

Validate a single solution manually:

```bash
python3 fly-in.py ../maps/hard/01_maze_nightmare.txt > salida
python3 validate_simulation.py ../maps/hard/01_maze_nightmare.txt salida
```

Validate all maps automatically:

```bash
./run_all.sh
```

---

## Important limitation

These tools only answer this question:

> Is the simulation valid according to the project rules?

They do **not** answer:

> Is this simulation the fastest or best possible one?

A valid solution may still be suboptimal.

---

## Troubleshooting

### Error: `destination '...' is neither zone nor connection`

Possible causes:

* typo in the output
* hidden characters in the solution file
* ANSI color codes not removed in an older validator version
* wrong map file used during validation

### Error: `invalid move A->B`

Possible causes:

* no connection exists between `A` and `B`
* trying to enter a restricted zone directly instead of using its connection id
* drone position tracking is inconsistent because of an earlier invalid move

### Error: drone in transit must arrive

Cause:

* a drone entered a restricted transit on one turn
* but did not arrive at the restricted zone on the next turn

This is invalid according to the project rules.

---

## Summary

* Use `validate_simulation.py` to check one map/output pair
* Use `run_all.sh` to generate and validate all map outputs automatically
* These tools validate correctness, not optimality

```
```
