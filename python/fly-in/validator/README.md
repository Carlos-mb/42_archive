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

## 1. How to use `validate_simulation.py`

### Syntax

```bash
python3 validate_simulation.py MAP_FILE SOLUTION_FILE
