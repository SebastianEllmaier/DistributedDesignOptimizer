---
title: update_state_listprimitive (Source)
---

← Back to [update_state_listprimitive documentation](update_state_listprimitive.md)

# update_state_listprimitive - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\tools\update_state_listprimitive.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""State update utilities module.

This module provides utilities for updating state lists with
primitive values.
"""

from typing import List, Union

# Define a type alias for primitive types
PrimitiveType = Union[float, int, str, bool, None]


def update_state_listprimitive(self_list: List[PrimitiveType] | None, other_list: List[PrimitiveType] | None) -> List[PrimitiveType] | None:
    """
    Update the state of a list of primitive values with the state of another list.
    This operation is meant to preserve the memory address of the list when possible.
    Works with lists of primitive types (float, int, str, bool) and None values.
    
    Args:
        self_list: The list to be updated
        other_list: The list containing the source values
        
    Returns:
        The updated list, or None if other_list is None
    
    Raises:
        TypeError: Automatically raised by beartype if non-primitive types are detected
    
    Note:
        No copy.copy() is needed for primitive types (float, int, str, bool, None)
        since they are immutable in Python. Assigning directly is safe.
    """
    # If source is None, return None to preserve semantic equivalence
    # (None means "not set", which is different from [] meaning "empty list")
    if other_list is None:
        return None
    
    # If both have values, update in-place to preserve memory address
    elif self_list is not None and other_list is not None:
        # Update values in-place - no copy needed for immutable primitives
        for i in range(len(other_list)):
            if i < len(self_list):
                self_list[i] = other_list[i]
            else:
                self_list.append(other_list[i])
        
        # Trim if needed
        if len(self_list) > len(other_list):
            del self_list[len(other_list):]
        
        return self_list
        
    # If target is None but source has a value, create a new list
    else:  # self_list is None and other_list is not None
        return list(other_list)

```
