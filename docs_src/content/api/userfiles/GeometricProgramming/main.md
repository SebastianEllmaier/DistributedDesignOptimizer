---
title: main
---

← Back to [GeometricProgramming](index.md)

# main

**Source:** [userfiles\GeometricProgramming\main.py](main_source.md)

Entry point for running the Geometric Programming Top-Down Hierarchic continuous optimization.

This module sets up and executes a distributed design optimization using a
hierarchical top-down approach with continuous variables for a geometric
programming problem. It initializes subsystems from an input file and
coordinates them.

## Functions

??? abstract "main() → None"
    Run the distributed optimization for the Geometric Programming problem.

    Initializes the input file configuration, creates subsystems, sets up
    the coordinator, and executes the distributed optimization algorithm.
    Prints the completion timestamp upon success or error details upon failure.


    **Raises:**
    > Exception: Any exception that occurs during optimization is caught  
    > and printed with a traceback.  

