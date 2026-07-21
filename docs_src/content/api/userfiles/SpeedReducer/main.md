---
title: main
---

← Back to [SpeedReducer](index.md)

# main

**Source:** [userfiles\SpeedReducer\main.py](main_source.md)

Entry point for running the Speed Reducer Non-Hierarchic distributed optimization.

This module sets up and executes a distributed design optimization using a
non-hierarchic decomposition with Augmented Lagrangian Coordination for the
Speed Reducer gearbox problem. It initializes subsystems from an input file
and coordinates them.

## Functions

??? abstract "main() → None"
    Run the distributed optimization for the Speed Reducer problem.

    Initializes the input file configuration, creates subsystems, sets up
    the coordinator, and executes the distributed optimization algorithm.
    Prints the completion timestamp upon success or error details upon failure.


    **Raises:**
    > Exception: Any exception that occurs during optimization is caught  
    > and printed with a traceback.  

