---
title: main
---

← Back to [TwoBarTruss](index.md)

# main

**Source:** [userfiles\TwoBarTruss\main.py](main_source.md)

Entry point for running the Two-Bar Truss Non-Hierarchic distributed optimization.

This module sets up and executes a distributed design optimization using a
non-hierarchic decomposition with Augmented Lagrangian Coordination for the
Two-Bar Truss structural problem. It initializes subsystems from an input
file and coordinates them.

## Functions

??? abstract "main() → None"
    Run the distributed optimization for the Two-Bar Truss problem.

    Initializes the input file configuration, creates subsystems, sets up
    the coordinator, and executes the distributed optimization algorithm.
    Prints the completion timestamp upon success or error details upon failure.


    **Raises:**
    > Exception: Any exception that occurs during optimization is caught  
    > and printed with a traceback.  

