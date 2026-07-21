---
title: update_state_listprimitive
---

← Back to [tools](index.md)

# update_state_listprimitive

**Source:** [Distributed_Design_Optimizer\subsystem\tools\update_state_listprimitive.py](update_state_listprimitive_source.md)

State update utilities module.

This module provides utilities for updating state lists with
primitive values.

## Functions

??? abstract "update_state_listprimitive(self_list: List[PrimitiveType] | None, other_list: List[PrimitiveType] | None) → List[PrimitiveType] | None"
    Update the state of a list of primitive values with the state of another list.
    This operation is meant to preserve the memory address of the list when possible.
    Works with lists of primitive types (float, int, str, bool) and None values.


    **Args:**
    > self_list: The list to be updated  
    > other_list: The list containing the source values  


    **Returns:**
    > The updated list, or None if other_list is None  


    **Raises:**
    > TypeError: Automatically raised by beartype if non-primitive types are detected  


    **Note:**
    > No copy.copy() is needed for primitive types (float, int, str, bool, None)  
    > since they are immutable in Python. Assigning directly is safe.  

