

# Dynamic Pathfinding Agent

This project implements a Dynamic Pathfinding Agent capable of navigating a grid-based environment using informed search algorithms. The system supports real-time obstacle generation and intelligent re-planning, simulating realistic navigation scenarios where the environment changes while the agent is moving.

The application is built with Python and Tkinter, providing an interactive graphical interface for visualization and experimentation.

---

## Features

* Dynamic Grid Sizing (user-defined rows × columns)
* Manual Obstacle Editing via mouse interaction
* Random Maze Generation with configurable obstacle density
* Two Informed Search Algorithms:

  * A* Search
  * Greedy Best First Search (GBFS)
* Two Heuristic Functions:

  * Manhattan Distance
  * Euclidean Distance
* Dynamic Mode:

  * Random obstacle spawning during movement
  * Real-time path re-planning if the current path becomes blocked
* Real-Time Metrics Dashboard:

  * Nodes Visited
  * Path Cost
  * Execution Time
* Full GUI Visualization:

  * Frontier Nodes
  * Visited Nodes
  * Final Path

---

## Algorithms Implemented

### A* Search

Uses the evaluation function:

f(n) = g(n) + h(n)

Where:

* g(n) is the path cost from start to node n
* h(n) is the heuristic estimate to the goal

A* guarantees an optimal path when the heuristic is admissible.

### Greedy Best First Search (GBFS)

Uses the evaluation function:

f(n) = h(n)

It prioritizes nodes that appear closest to the goal but does not guarantee optimality.

---

## Dynamic Re-Planning Mechanism

When dynamic mode is enabled:

* Obstacles spawn randomly during agent movement.
* If a newly spawned obstacle blocks the remaining planned path, the agent:

  * Detects the obstruction
  * Re-runs the search from its current position
  * Computes a new valid path without resetting the entire environment

This simulates real-world navigation under changing conditions.

---

## Technologies Used

* Python 3
* Tkinter (GUI)
* Heapq (Priority Queue for search algorithms)
* Math & Time modules for heuristic and performance metrics

---

## Learning Outcomes

This project demonstrates:

* Implementation of informed search strategies
* Heuristic design and comparison
* Dynamic environment handling
* Real-time visualization of search behavior
* Performance analysis of algorithms

---

## How to Run

```bash
python dynamic_pathfinding.py
```

Make sure Python 3 is installed.

