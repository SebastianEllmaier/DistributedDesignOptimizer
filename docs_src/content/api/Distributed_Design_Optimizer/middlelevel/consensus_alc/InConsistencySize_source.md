---
title: InConsistencySize (Source)
---

← Back to [InConsistencySize documentation](InConsistencySize.md)

# InConsistencySize - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\consensus_alc\InConsistencySize.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Inconsistency size computation for consensus-based ALC.

This module provides functionality for computing inconsistency sizes
between coupled variables in consensus-based ALC.
"""

from typing import List
import copy
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class InConsistencySize(InConsistencySizeBasis):
    """Inconsistency size storage for consensus-based ALC.

    Stores and computes the size of inconsistencies between coupled
    variables in consensus-based ALC coordination.
    """

    def __init__(self,
                 id: str) -> None:
        """Initialize inconsistency size.

        Args:
            id: Identifier for this inconsistency measure.
        """
        # call __init__() of InConsistencySizeBasis
        super().__init__(id)
        
        # FOR CONSENSUS CONSTRAINTS:       
        self._auxiliary_minus_mappedresponse: List[float] | None = None
        self._auxiliary_minus_couplingvariable: List[float] | None = None
        self._auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
        self._auxiliary_minus_mappedresponse_infynorm: float | None = None
        self._auxiliary_minus_couplingvariable_infynorm: float | None = None
        self._auxiliary_minus_shareddesignvariable_infynorm: float | None = None
        self._auxiliary_minus_targetshareddesignvariable_infynorm: float | None = None 
        
        self._auxiliary_minus_mappedresponse_infynormID: int | None = None
        self._auxiliary_minus_couplingvariable_infynormID: int | None = None
        self._auxiliary_minus_shareddesignvariable_infynormID: int | None = None
        self._auxiliary_minus_targetshareddesignvariable_infynormID: int | None = None
        
        self._oscillationindex_auxiliary_minus_mappedresponse: List[float | None] | None = None
        self._oscillationindex_auxiliary_minus_couplingvariable: List[float | None] | None = None        
        self._oscillationindex_auxiliary_minus_shareddesignvariable: List[float | None] | None = None
        self._oscillationindex_auxiliary_minus_targetshareddesignvariable: List[float | None] | None = None     

    # Auxiliary minus mapped response
    def evaluate_Auxiliary_Minus_MappedResponse(self, auxiliary: List[float], mappedresponse: List[float]) -> None:
        """Set the inconsistency between the auxiliary variable and the mapped response for consensus constraints.

        Args:
            auxiliary: Auxiliary variable values.
            mappedresponse: Mapped response values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._auxiliary_minus_mappedresponse = [s - d for s, d in zip(auxiliary, mappedresponse)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._auxiliary_minus_mappedresponse), key=lambda x: abs(x[1]))
        self._auxiliary_minus_mappedresponse_infynorm = abs(max_val)
        self._auxiliary_minus_mappedresponse_infynormID = max_idx
        
    def get_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Get the inconsistency between the auxiliary variable and the mapped response for consensus constraints.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_minus_mappedresponse)
        
    def get_Auxiliary_Minus_MappedResponse_InfyNorm(self) -> float | None:
        """Get the maximum auxiliary-minus-mapped-response inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_mappedresponse_infynorm
    
    def get_Auxiliary_Minus_MappedResponse_InfyNormID(self) -> int | None:
        """Get the index of the maximum auxiliary-minus-mapped-response inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_mappedresponse_infynormID
    
    # Auxiliary minus coupling variable
    def evaluate_Auxiliary_Minus_CouplingVariable(self, auxiliary: List[float], couplingvariable: List[float]) -> None:
        """Set the inconsistency between the auxiliary variable and the coupling variable for consensus constraints.

        Args:
            auxiliary: Auxiliary variable values.
            couplingvariable: Coupling variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._auxiliary_minus_couplingvariable = [s - d for s, d in zip(auxiliary, couplingvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._auxiliary_minus_couplingvariable), key=lambda x: abs(x[1]))
        self._auxiliary_minus_couplingvariable_infynorm = abs(max_val)
        self._auxiliary_minus_couplingvariable_infynormID = max_idx
        
    def get_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the inconsistency between the auxiliary variable and the coupling variable for consensus constraints.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_minus_couplingvariable)
        
    def get_Auxiliary_Minus_CouplingVariable_InfyNorm(self) -> float | None:
        """Get the maximum auxiliary-minus-coupling-variable inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_couplingvariable_infynorm
    
    def get_Auxiliary_Minus_CouplingVariable_InfyNormID(self) -> int | None:
        """Get the index of the maximum auxiliary-minus-coupling-variable inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_couplingvariable_infynormID
    
    # Auxiliary minus shared design variable
    
    def evaluate_Auxiliary_Minus_SharedDesignVariable(self, auxiliary: List[float], shareddesignvariable: List[float]) -> None:
        """Set the inconsistency for shared design variables in consensus constraints.

        Args:
            auxiliary: Auxiliary variable values.
            shareddesignvariable: Shared design variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._auxiliary_minus_shareddesignvariable = [s - d for s, d in zip(auxiliary, shareddesignvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._auxiliary_minus_shareddesignvariable), key=lambda x: abs(x[1]))
        self._auxiliary_minus_shareddesignvariable_infynorm = abs(max_val)
        self._auxiliary_minus_shareddesignvariable_infynormID = max_idx
    
    def get_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for shared design variables in consensus constraints.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_minus_shareddesignvariable)
        
    def get_Auxiliary_Minus_SharedDesignVariable_InfyNorm(self) -> float | None:
        """Get the maximum shared design variables auxiliary inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_shareddesignvariable_infynorm

    def get_Auxiliary_Minus_SharedDesignVariable_InfyNormID(self) -> int | None:
        """Get the index of the maximum shared design variables auxiliary inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_shareddesignvariable_infynormID

    # Auxiliary minus target shared design variable
    
    def evaluate_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary: List[float], targetshareddesignvariable: List[float]) -> None:
        """Set the inconsistency for target shared design variables in consensus constraints.

        Args:
            auxiliary: Auxiliary variable values.
            targetshareddesignvariable: Target shared design variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._auxiliary_minus_targetshareddesignvariable = [s - d for s, d in zip(auxiliary, targetshareddesignvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._auxiliary_minus_targetshareddesignvariable), key=lambda x: abs(x[1]))
        self._auxiliary_minus_targetshareddesignvariable_infynorm = abs(max_val)
        self._auxiliary_minus_targetshareddesignvariable_infynormID = max_idx
    
    def get_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for target shared design variables in consensus constraints.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_minus_targetshareddesignvariable)
        
    def get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNorm(self) -> float | None:
        """Get the maximum target shared design variables auxiliary inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_targetshareddesignvariable_infynorm
    
    def get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNormID(self) -> int | None:
        """Get the index of the maximum target shared design variables auxiliary inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._auxiliary_minus_targetshareddesignvariable_infynormID

    # Auxiliary inconsistency oscillations
    def set_OscillationIndex_Auxiliary_Minus_MappedResponse(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for auxiliary-minus-mapped-response inconsistency.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_auxiliary_minus_mappedresponse = copy.copy(oscillationindex)
        
    def get_OscillationIndex_Auxiliary_Minus_MappedResponse(self) -> List[float | None] | None:
        """Get oscillation index for auxiliary-minus-mapped-response inconsistency.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_auxiliary_minus_mappedresponse)
    
    def set_OscillationIndex_Auxiliary_Minus_CouplingVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for auxiliary-minus-coupling-variable inconsistency.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_auxiliary_minus_couplingvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_Auxiliary_Minus_CouplingVariable(self) -> List[float | None] | None:
        """Get oscillation index for auxiliary-minus-coupling-variable inconsistency.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_auxiliary_minus_couplingvariable)
    
    def set_OscillationIndex_Auxiliary_Minus_SharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for shared design variables auxiliary inconsistency.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_auxiliary_minus_shareddesignvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_Auxiliary_Minus_SharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for shared design variables auxiliary inconsistency.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_auxiliary_minus_shareddesignvariable)
    
    def set_OscillationIndex_Auxiliary_Minus_TargetSharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for target shared design variables auxiliary inconsistency.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_auxiliary_minus_targetshareddesignvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for target shared design variables auxiliary inconsistency.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_auxiliary_minus_targetshareddesignvariable)

    # necessary method when running multiprocessing
    def update_state(self, other_inconsistency: 'InConsistencySize') -> None:
        """Update the state of this InConsistencySize with the state of another InConsistencySize.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.
        
        Args:
            other_inconsistency: The source instance to copy state from.
        """
        # Call the base class update_state to handle all non-auxiliary attributes
        super().update_state(other_inconsistency)
        
        # FOR CONSENSUS CONSTRAINTS (AUXILIARY):
        # Auxiliary inconsistency values - List[float] updated via utility function
        self._auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(self._auxiliary_minus_mappedresponse, other_inconsistency.get_Auxiliary_Minus_MappedResponse())
        self._auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._auxiliary_minus_couplingvariable, other_inconsistency.get_Auxiliary_Minus_CouplingVariable())
        self._auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(self._auxiliary_minus_shareddesignvariable, other_inconsistency.get_Auxiliary_Minus_SharedDesignVariable())
        self._auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._auxiliary_minus_targetshareddesignvariable, other_inconsistency.get_Auxiliary_Minus_TargetSharedDesignVariable())
        
        # Auxiliary infinity norms - float is immutable, no copy.copy() needed
        self._auxiliary_minus_mappedresponse_infynorm: float | None = other_inconsistency.get_Auxiliary_Minus_MappedResponse_InfyNorm()
        self._auxiliary_minus_couplingvariable_infynorm: float | None = other_inconsistency.get_Auxiliary_Minus_CouplingVariable_InfyNorm()
        self._auxiliary_minus_shareddesignvariable_infynorm: float | None = other_inconsistency.get_Auxiliary_Minus_SharedDesignVariable_InfyNorm()
        self._auxiliary_minus_targetshareddesignvariable_infynorm: float | None = other_inconsistency.get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNorm()
        
        # Auxiliary infinity norm IDs - int is immutable, no copy.copy() needed
        self._auxiliary_minus_mappedresponse_infynormID: int | None = other_inconsistency.get_Auxiliary_Minus_MappedResponse_InfyNormID()
        self._auxiliary_minus_couplingvariable_infynormID: int | None = other_inconsistency.get_Auxiliary_Minus_CouplingVariable_InfyNormID()
        self._auxiliary_minus_shareddesignvariable_infynormID: int | None = other_inconsistency.get_Auxiliary_Minus_SharedDesignVariable_InfyNormID()
        self._auxiliary_minus_targetshareddesignvariable_infynormID: int | None = other_inconsistency.get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNormID()
        
        # Auxiliary inconsistency oscillation indices - List[float | None] updated via utility function
        self._oscillationindex_auxiliary_minus_mappedresponse: List[float | None] | None = update_state_listprimitive(self._oscillationindex_auxiliary_minus_mappedresponse, other_inconsistency.get_OscillationIndex_Auxiliary_Minus_MappedResponse())
        self._oscillationindex_auxiliary_minus_couplingvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_auxiliary_minus_couplingvariable, other_inconsistency.get_OscillationIndex_Auxiliary_Minus_CouplingVariable())
        self._oscillationindex_auxiliary_minus_shareddesignvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_auxiliary_minus_shareddesignvariable, other_inconsistency.get_OscillationIndex_Auxiliary_Minus_SharedDesignVariable())
        self._oscillationindex_auxiliary_minus_targetshareddesignvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_auxiliary_minus_targetshareddesignvariable, other_inconsistency.get_OscillationIndex_Auxiliary_Minus_TargetSharedDesignVariable())

```
