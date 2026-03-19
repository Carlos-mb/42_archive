*This project has been created as part of the 42 curriculum by cmelero-.*

# Fly-in

## Description

This project implements a drone routing simulation system.
The goal is to move a fleet of drones from a start zone to an end zone in the fewest possible simulation turns while respecting movement rules, zone capacities and connection constraints.

The simulation operates on a graph of connected zones.
Each drone moves turn by turn according to zone type rules (normal, restricted, priority, blocked).

The implementation includes:

- Input parser for map files
- Simulation engine respecting all movement constraints
- Pathfinding strategy to reduce total turns
- Terminal-based visual representation
- Output formatted according to subject requirements

---

## Instructions

### Install

make install

### Run

make run CONFIG=<map_file>

Example:

make run CONFIG=01_linear_path.txt

### Debug

make debug CONFIG=<map_file>

### Verbose debug

Create a file named `debug` to see debug output

Create a file named `nocolor` to remove colors from output

### Clean

make clean

### Lint

make lint

---

## Example Input and Expected Output

Example input file (`test.txt`):

```txt
nb_drones: 6

start_hub: start 0 0 [color=green max_drones=6]
hub: loop_a 1 0 [zone=restricted color=orange]
hub: loop_b 2 0 [zone=restricted color=orange]
hub: loop_c 2 1 [zone=restricted color=orange]
hub: loop_d 1 1 [zone=restricted color=orange]
hub: exit_point 3 0 [color=blue]
end_hub: goal 4 0 [color=red max_drones=6]

connection: start-loop_a
connection: loop_a-loop_b
connection: loop_b-loop_c
connection: loop_c-loop_d
connection: loop_d-loop_a
connection: loop_b-exit_point
connection: exit_point-goal
```

Command:

```bash
python3 fly-in.py test.txt
```

Expected output (colors are not visibles here):

```txt
T1: D1-start-loop_a
T2: D1-loop_a
T3: D1-loop_a-loop_b D2-start-loop_a
T4: D1-loop_b D2-loop_a
T5: D1-exit_point D2-loop_a-loop_b D3-start-loop_a
T6: D1-goal D2-loop_b D3-loop_a
T7: D2-exit_point D3-loop_a-loop_b D4-start-loop_a
T8: D2-goal D3-loop_b D4-loop_a
T9: D3-exit_point D4-loop_a-loop_b D5-start-loop_a
T10: D3-goal D4-loop_b D5-loop_a
T11: D4-exit_point D5-loop_a-loop_b D6-start-loop_a
T12: D4-goal D5-loop_b D6-loop_a
T13: D5-exit_point D6-loop_a-loop_b
T14: D5-goal D6-loop_b
T15: D6-exit_point
T16: D6-goal
```

---

## Algorithm and Strategy

The simulation uses a greedy pathfinding approach based on distance estimation toward the goal.

At each turn:

- Drones attempt to move to the neighbour zone with the smallest estimated distance.
- Zone capacity and connection capacity constraints are respected.
- Restricted zones are handled as multi-turn movements.
- Drones may wait if movement is not possible.
- The simulation iterates until all drones reach the end zone.
- The simulation incraease the "cost" of move to a hub each time the drone has visited the hub
- All hub without exit are removed from the map before simulation

This approach focuses on:

- Conflict avoidance
- Turn scheduling
- Simple throughput optimisation

The algorithm does not compute global optimal paths or flow distribution.

---

## Visual Representation

The simulation provides terminal-based visual feedback using colored output.

Zone colors from the map metadata are used to improve readability and help understand drone movement and congestion during execution.

---

## Results (Benchmarks)

Test results obtained on provided maps:

Easy maps

- Linear path → 4 turns
- Simple fork → 5 turns
- Basic capacity → 6 turns

Medium maps

- Dead end trap → 8 turns
- Circular loop → 16 turns
- Priority puzzle → 8 turns

Hard maps

- Maze nightmare → 14 turns
- Capacity hell → 18 turns
- Ultimate challenge → 35 turns 

	<sub>Ultimate callenge has 2 nodes with same coordinates. I had to change it to make it playable.</sub>


Challenger
- The impossible dream → 65 turns

All simulations validated successfully.

---

## Limitations

- The algorithm is based on the concept of traffic in a city. Vehicles start moving and make decisions based on the results.
- The algorithm does not guarantee optimal solutions.
- It does not perform global route planning or flow optimization.
- Some complex maps may result in suboptimal performance.
- Route recalculation is based on the number of times a drone passes through an area.
---

## Resources

- Python official documentation
- 42 subject documentation

AI tools were used to:

- Understand Python concepts
- Define extreme use cases
- Clarify the interpretation of the subject requirements

All generated content was reviewed and fully understood before integration.