---
title: main
---

← Back to [SSBJ](index.md)

# main

**Source:** [userfiles\SSBJ\main.py](main_source.md)

Entry point for running the Supersonic Business Jet (SSBJ) distributed optimization.

This module sets up and executes a distributed design optimization using a
hierarchical decomposition with continuous variables for the Supersonic
Business Jet (SSBJ) multidisciplinary problem. It initializes subsystems
from an input file and coordinates them.

## Functions

??? abstract "main() → None"
    Run the distributed optimization for the Supersonic Business Jet (SSBJ) problem.

    Initializes the input file configuration, creates subsystems, sets up
    the coordinator, and executes the distributed optimization algorithm.
    Prints the completion timestamp upon success or error details upon failure.


    **Raises:**
    > Exception: Any exception that occurs during optimization is caught  
    > and printed with a traceback.  

