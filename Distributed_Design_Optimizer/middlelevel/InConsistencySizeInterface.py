# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for inconsistency size computation.

This module defines the abstract interface for computing inconsistency
sizes between coupled variables.
"""

from abc import ABC, abstractmethod
from typing import List


class InConsistencySizeInterface(ABC):
    """Abstract interface for inconsistency size storage.

    Defines the contract for classes that store and manage inconsistency
    measurements between subsystems in distributed optimization.
    """
    
    @abstractmethod
    def get_ID(self) -> str:
        """Get the identifier of the neighboring subsystem.

        Returns:
            The neighbor subsystem identifier.
        """
    
    @abstractmethod
    def evaluate_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse: List[float], copycouplingvariable: List[float]) -> None:
        """Set the inconsistency on the mapped-response side of the coupling circle.

        Args:
            mappedresponse: Mapped response values.
            copycouplingvariable: Copy of the coupling variable values.
        """ 
        
    @abstractmethod
    def get_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Get the inconsistency on the mapped-response side of the coupling circle.

        Returns:
            List of inconsistency values or None if not set.
        """

    @abstractmethod
    def get_MappedResponse_Minus_CopyCouplingVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency on the mapped-response side.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        
    @abstractmethod
    def get_MappedResponse_Minus_CopyCouplingVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency on the mapped-response side.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        
    @abstractmethod
    def evaluate_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse: List[float], couplingvariable: List[float]) -> None:
        """Set the inconsistency on the coupling-variable side of the coupling circle.

        Args:
            copymappedresponse: Copy of the mapped response values.
            couplingvariable: Coupling variable values.
        """
        
    @abstractmethod
    def get_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the inconsistency on the coupling-variable side of the coupling circle.

        Returns:
            List of inconsistency values or None if not set.
        """
        
    @abstractmethod
    def get_CopyMappedResponse_Minus_CouplingVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency on the coupling-variable side.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        
    @abstractmethod
    def get_CopyMappedResponse_Minus_CouplingVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency on the coupling-variable side.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        
    @abstractmethod
    def evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable: List[float], copytargetshareddesignvariable: List[float]) -> None:
        """Set the inconsistency for shared design variables.

        Args:
            shareddesignvariable: Shared design variable values.
            copytargetshareddesignvariable: Copy of the target shared design variable values.
        """
        
    @abstractmethod
    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for shared design variables.

        Returns:
            List of inconsistency values or None if not set.
        """
        
    @abstractmethod
    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNorm(self) -> float | None:
        """Get the maximum shared design variables inconsistency (infinity norm).

        Returns:
            Maximum inconsistency value or None if not set.
        """
        
    @abstractmethod
    def get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNormID(self) -> int | None:
        """Get the index of the maximum shared design variables inconsistency.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        
    @abstractmethod
    def evaluate_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable: List[float], targetshareddesignvariable: List[float]) -> None:
        """Set the inconsistency for target shared design variables.

        Args:
            copyshareddesignvariable: Copy of the shared design variable values.
            targetshareddesignvariable: Target shared design variable values.
        """
        
    @abstractmethod
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the inconsistency for target shared design variables.

        Returns:
            List of inconsistency values or None if not set.
        """
        
    @abstractmethod
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNorm(self) -> float | None:
        """Return the maximum inconsistency for target shared design variables.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        
    @abstractmethod
    def get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable_InfyNormID(self) -> int | None:
        """Return the index of the maximum inconsistency for target shared design variables.

        Returns:
            Index of maximum inconsistency or None if not set.
        """
        
    @abstractmethod
    def evaluate_MaxInconsistency(self) -> None:
        """Evaluate the max inconsistency value across all inconsistency types."""
        
    @abstractmethod
    def get_maxInconsistencyValue(self) -> float | None:
        """Return the max inconsistency value.

        Returns:
            Maximum inconsistency value or None if not set.
        """
        
    @abstractmethod
    def get_maxInconsistencyType(self) -> str | None:
        """Return the type of the max inconsistency value.

        Returns:
            Type identifier of the maximum inconsistency or None if not set.
        """
        
    @abstractmethod
    def set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for mapped-response side.

        Args:
            oscillationindex: List of oscillation index values.
        """
        
    @abstractmethod
    def get_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float | None] | None:
        """Get oscillation index for mapped-response side.

        Returns:
            List of oscillation index values or None if not set.
        """
        
    @abstractmethod
    def set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for coupling-variable side.

        Args:
            oscillationindex: List of oscillation index values.
        """
        
    @abstractmethod
    def get_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float | None] | None:
        """Get oscillation index for coupling-variable side.

        Returns:
            List of oscillation index values or None if not set.
        """
        
    @abstractmethod
    def set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for shared design variables.

        Args:
            oscillationindex: List of oscillation index values.
        """
        
    @abstractmethod
    def get_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for shared design variables.

        Returns:
            List of oscillation index values or None if not set.
        """
        
    @abstractmethod
    def set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, oscillationindex: List[float | None]) -> None:
        """Set oscillation index for target shared design variables.

        Args:
            oscillationindex: List of oscillation index values.
        """
    
    @abstractmethod
    def get_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float | None] | None:
        """Get oscillation index for target shared design variables.

        Returns:
            List of oscillation index values or None if not set.
        """      
    
    @abstractmethod
    def print_end_of_innerloop_iteration(self) -> None:
        """Print inconsistency details for this inconsistency at the end of an inner loop iteration."""
        
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print inconsistency details for this inconsistency at the end of the optimization run."""

    @abstractmethod
    def update_state(self, other_inconsistency: 'InConsistencySizeInterface') -> None:
        """Update the state of this InConsistencySizeInterface from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. Implementations must
        preserve the memory address of the object's attributes while updating
        their values.

        Args:
            other_inconsistency: The source instance containing updated values to copy from.
        
        """
    