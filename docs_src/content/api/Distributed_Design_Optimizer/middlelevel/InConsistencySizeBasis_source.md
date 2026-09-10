---
title: InConsistencySizeBasis (Source)
---

← Back to [InConsistencySizeBasis documentation](InConsistencySizeBasis.md)

# InConsistencySizeBasis - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\InConsistencySizeBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Inconsistency size basis module.

This module provides the base class for computing inconsistency sizes
between coupled variables in distributed optimization.
"""

from typing import List, Tuple
import copy
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print


class InConsistencySizeBasis(InConsistencySizeInterface):
    """Base class for storing inconsistency size measurements between subsystems.

    Tracks coupling inconsistencies between subsystems at various
    coupling points (mapped-response, coupling-variable, shared, target design variables).
    """

    _DDO_PRINT_LABEL_WIDTH: int = 55

    def __init__(self,
                 id: str) -> None:
        """Initialize the inconsistency size storage.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        
        self._id: str = id  # identifier of the neighboring subsystem
        
        self._mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._copymappedresponse_minus_couplingvariable: List[float] | None = None
        self._shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        self._copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None
        
        self._mappedresponse_minus_copycouplingvariable_infynorm: float | None = None
        self._copymappedresponse_minus_couplingvariable_infynorm: float | None = None
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynorm: float | None = None
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynorm: float | None = None
        
        self._mappedresponse_minus_copycouplingvariable_infynormID: int | None = None
        self._copymappedresponse_minus_couplingvariable_infynormID: int | None = None
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynormID: int | None = None
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynormID: int | None = None
        
        self._oscillationindex_mappedresponse_minus_copycouplingvariable: List[float | None] | None = None
        self._oscillationindex_copymappedresponse_minus_couplingvariable: List[float | None] | None = None        
        self._oscillationindex_shareddesignvariable_minus_copytargetshareddesignvariable: List[float | None] | None = None
        self._oscillationindex_copyshareddesignvariable_minus_targetshareddesignvariable: List[float | None] | None = None   
        
        self._maxinconsistencyvalue: float | None = None
        self._maxinconsistencytype: str | None = None        
    
    def get_ID(self) -> str:
        """Get the identifier of the neighboring subsystem.

        Returns:
            The neighbor subsystem identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._id
    
    def evaluate_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse: List[float], copycouplingvariable: List[float]) -> None:
        """Set the inconsistency on the mapped-response side of the coupling circle.

        Args:
            mappedresponse: Mapped response values.
            copycouplingvariable: Copy of the coupling variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._mappedresponse_minus_copycouplingvariable = [s - d for s, d in zip(mappedresponse, copycouplingvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._mappedresponse_minus_copycouplingvariable), key=lambda x: abs(x[1]))
        self._mappedresponse_minus_copycouplingvariable_infynorm = abs(max_val)
        self._mappedresponse_minus_copycouplingvariable_infynormID = max_idx
        
    def get_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Get the inconsistency on the mapped-response side of the coupling circle.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponse_minus_copycouplingvariable)
        
    def get_MappedResponse_Minus_CopyCouplingVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency on the mapped-response side.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._mappedresponse_minus_copycouplingvariable_infynorm
    
    def get_MappedResponse_Minus_CopyCouplingVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency on the mapped-response side.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._mappedresponse_minus_copycouplingvariable_infynormID
    
    def evaluate_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse: List[float], couplingvariable: List[float]) -> None:
        """Set the inconsistency on the coupling-variable side of the coupling circle.

        Args:
            copymappedresponse: Copy of the mapped response values.
            couplingvariable: Coupling variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._copymappedresponse_minus_couplingvariable = [s - d for s, d in zip(copymappedresponse, couplingvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._copymappedresponse_minus_couplingvariable), key=lambda x: abs(x[1]))
        self._copymappedresponse_minus_couplingvariable_infynorm = abs(max_val)
        self._copymappedresponse_minus_couplingvariable_infynormID = max_idx
        
    def get_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the inconsistency on the coupling-variable side of the coupling circle.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copymappedresponse_minus_couplingvariable)
        
    def get_CopyMappedResponse_Minus_CouplingVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency on the coupling-variable side.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._copymappedresponse_minus_couplingvariable_infynorm
    
    def get_CopyMappedResponse_Minus_CouplingVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency on the coupling-variable side.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._copymappedresponse_minus_couplingvariable_infynormID
    
    def evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable: List[float], copytargetshareddesignvariable: List[float]) -> None:
        """Set the inconsistency for shared design variables.

        Args:
            shareddesignvariable: Shared design variable values.
            copytargetshareddesignvariable: Copy of the target shared design variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._shareddesignvariable_minus_copytargetshareddesignvariable = [s - d for s, d in zip(shareddesignvariable, copytargetshareddesignvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._shareddesignvariable_minus_copytargetshareddesignvariable), key=lambda x: abs(x[1]))
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynorm = abs(max_val)
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynormID = max_idx
    
    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for shared design variables.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariable_minus_copytargetshareddesignvariable)
        
    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNorm(self) -> float | None:
        """Get the maximum shared design variables inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._shareddesignvariable_minus_copytargetshareddesignvariable_infynorm

    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNormID(self) -> int | None:
        """Get the index of the maximum shared design variables inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._shareddesignvariable_minus_copytargetshareddesignvariable_infynormID

    def evaluate_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable: List[float], targetshareddesignvariable: List[float]) -> None:
        """Set the inconsistency for target shared design variables.

        Args:
            copyshareddesignvariable: Copy of the shared design variable values.
            targetshareddesignvariable: Target shared design variable values.
        """
        # No copy.copy() needed - list comprehension creates a new list with no reference
        # to the input lists, so modifications in the caller cannot affect the class attribute.
        # element-wise difference using list comprehension (faster than np.array conversion)
        self._copyshareddesignvariable_minus_targetshareddesignvariable = [s - d for s, d in zip(copyshareddesignvariable, targetshareddesignvariable)]
        # Single-pass computation of infinity norm and its index
        max_idx, max_val = max(enumerate(self._copyshareddesignvariable_minus_targetshareddesignvariable), key=lambda x: abs(x[1]))
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynorm = abs(max_val)
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynormID = max_idx
    
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for target shared design variables.

        Returns:
            List of inconsistency values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copyshareddesignvariable_minus_targetshareddesignvariable)
        
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency for target shared design variables.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._copyshareddesignvariable_minus_targetshareddesignvariable_infynorm
    
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency for target shared design variables.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._copyshareddesignvariable_minus_targetshareddesignvariable_infynormID
    
    def evaluate_MaxInconsistency(self) -> None:
        """Evaluate the maximum inconsistency value across all inconsistency types.
        """
        inconsistency_values = {
            "max_mappedresponse_minus_copycouplingvariable": self._mappedresponse_minus_copycouplingvariable_infynorm,
            "max_copymappedresponse_minus_couplingvariable": self._copymappedresponse_minus_couplingvariable_infynorm,
            "max_shareddesignvariable_minus_copytargetshareddesignvariable": self._shareddesignvariable_minus_copytargetshareddesignvariable_infynorm,
            "max_copyshareddesignvariable_minus_targetshareddesignvariable": self._copyshareddesignvariable_minus_targetshareddesignvariable_infynorm
        }
        
        # Filter out None values
        filtered_inconsistency_values = {key: value for key, value in inconsistency_values.items() if value is not None}    
        
        # Check if there are any valid values left
        if filtered_inconsistency_values:
            # Find the maximum value and its corresponding key
            self._maxinconsistencytype, self._maxinconsistencyvalue = max(filtered_inconsistency_values.items(), key=lambda x: x[1])
            
        else:
            # If all values are None, set the attributes to None
            self._maxinconsistencytype, self._maxinconsistencyvalue = None, None
        
    def get_maxInconsistencyValue(self) -> float | None:
        """Return the max inconsistency value.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._maxinconsistencyvalue
    
    def get_maxInconsistencyType(self) -> str | None:
        """Return the type of the max inconsistency value.

        Returns:
            Type identifier of the maximum inconsistency or None if not set.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._maxinconsistencytype
    
    def set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for mapped-response side.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_mappedresponse_minus_copycouplingvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float | None] | None:
        """Get oscillation index for mapped-response side.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_mappedresponse_minus_copycouplingvariable)
    
    def set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for coupling-variable side.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_copymappedresponse_minus_couplingvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float | None] | None:
        """Get oscillation index for coupling-variable side.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_copymappedresponse_minus_couplingvariable)
    
    def set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for shared design variables.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for shared design variables.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_shareddesignvariable_minus_copytargetshareddesignvariable)
    
    def set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for target shared design variables.

        Args:
            oscillationindex: List of oscillation index values.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._oscillationindex_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(oscillationindex)
        
    def get_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for target shared design variables.

        Returns:
            List of oscillation index values or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._oscillationindex_copyshareddesignvariable_minus_targetshareddesignvariable)
    
################################################################################################################
#   Print methods for terminal output
################################################################################################################

    def _print_inconsistencies(self) -> None:
        """Print inconsistency details for all inconsistency types of this inconsistency."""
        ddo_print(f"          Inconsistencies with SubSystem {self.get_ID()}:")
        inconsistency_types: List[Tuple[str, List[float] | None]] = [
            ("MappedResponse - CopyCouplingVariable",                 self.get_MappedResponse_Minus_CopyCouplingVariable()),
            ("CopyMappedResponse - CouplingVariable",                 self.get_CopyMappedResponse_Minus_CouplingVariable()),
            ("SharedDesignVariable - CopyTargetSharedDesignVariable", self.get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()),
            ("CopySharedDesignVariable - TargetSharedDesignVariable", self.get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()),
        ]
        for label, inconsistency in inconsistency_types:
            padded_label = f"{label}:".ljust(self._DDO_PRINT_LABEL_WIDTH)
            if inconsistency is None:
                ddo_print(f"              {padded_label} None")
            else:
                index_width = len(f"[{len(inconsistency) - 1}]")
                ddo_print(f"              {padded_label} {'[0]'.ljust(index_width)} {inconsistency[0]}")
                for i, v in enumerate(inconsistency[1:], start=1):
                    ddo_print(f"              {' ' * self._DDO_PRINT_LABEL_WIDTH} {f'[{i}]'.ljust(index_width)} {v}")

    def print_end_of_innerloop_iteration(self) -> None:
        """Print inconsistency details for this inconsistency at the end of an inner loop iteration."""
        self._print_inconsistencies()

    def print_termination_summary(self) -> None:
        """Print inconsistency details for this inconsistency at the end of the optimization run."""
        self._print_inconsistencies()

########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_inconsistency: 'InConsistencySizeBasis') -> None:
        """Update the state of this InConsistencySizeBasis from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. This method preserves
        the memory address of the object's attributes while updating their values.

        Args:
            other_inconsistency: The source instance containing updated values to copy from.
        
        Note on copy operations:
            - Primitives (str, float, int, None): No copy.copy() needed because they are
              immutable in Python. Assigning creates a new binding; the original cannot
              be modified through the new reference.
            - List[float]: Uses update_state_listprimitive() which updates the list in-place
              to preserve the memory address. The getter methods already return copy.copy()
              of the lists, providing the necessary isolation from the source.
        """
        # Identifier (str is immutable - no copy.copy() needed)
        self._id: str = other_inconsistency.get_ID()
        
        # Inconsistency values - List[float] updated via utility function
        # update_state_listprimitive preserves memory address; getter returns copy.copy()
        self._mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._mappedresponse_minus_copycouplingvariable, other_inconsistency.get_MappedResponse_Minus_CopyCouplingVariable())
        self._copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._copymappedresponse_minus_couplingvariable, other_inconsistency.get_CopyMappedResponse_Minus_CouplingVariable())
        self._shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._shareddesignvariable_minus_copytargetshareddesignvariable, other_inconsistency.get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._copyshareddesignvariable_minus_targetshareddesignvariable, other_inconsistency.get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        # Infinity norms - float is immutable, no copy.copy() needed
        self._mappedresponse_minus_copycouplingvariable_infynorm: float | None = other_inconsistency.get_MappedResponse_Minus_CopyCouplingVariable_InfyNorm()
        self._copymappedresponse_minus_couplingvariable_infynorm: float | None = other_inconsistency.get_CopyMappedResponse_Minus_CouplingVariable_InfyNorm()
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynorm: float | None = other_inconsistency.get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNorm()
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynorm: float | None = other_inconsistency.get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNorm()
        
        # Infinity norm IDs - int is immutable, no copy.copy() needed
        self._mappedresponse_minus_copycouplingvariable_infynormID: int | None = other_inconsistency.get_MappedResponse_Minus_CopyCouplingVariable_InfyNormID()
        self._copymappedresponse_minus_couplingvariable_infynormID: int | None = other_inconsistency.get_CopyMappedResponse_Minus_CouplingVariable_InfyNormID()
        self._shareddesignvariable_minus_copytargetshareddesignvariable_infynormID: int | None = other_inconsistency.get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNormID()
        self._copyshareddesignvariable_minus_targetshareddesignvariable_infynormID: int | None = other_inconsistency.get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNormID()
        
        # Oscillation indices - List[float | None] updated via utility function
        self._oscillationindex_mappedresponse_minus_copycouplingvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_mappedresponse_minus_copycouplingvariable, other_inconsistency.get_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable())
        self._oscillationindex_copymappedresponse_minus_couplingvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_copymappedresponse_minus_couplingvariable, other_inconsistency.get_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable())
        self._oscillationindex_shareddesignvariable_minus_copytargetshareddesignvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_shareddesignvariable_minus_copytargetshareddesignvariable, other_inconsistency.get_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._oscillationindex_copyshareddesignvariable_minus_targetshareddesignvariable: List[float | None] | None = update_state_listprimitive(self._oscillationindex_copyshareddesignvariable_minus_targetshareddesignvariable, other_inconsistency.get_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        # Max inconsistency tracking - float and str are immutable, no copy.copy() needed
        self._maxinconsistencyvalue: float | None = other_inconsistency.get_maxInconsistencyValue()
        self._maxinconsistencytype: str | None = other_inconsistency.get_maxInconsistencyType()

```
