# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Coupling Lagrange multipliers module.

This module provides Lagrange multiplier parameters for the
Lagrangian Coordination method.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.middlelevel.lc import MiddleLevelCouplingLC


class CouplingParametersLC(SubSysCouplingParametersBasis):
    """Coupling multipliers for Lagrangian coordination.

    Extends SubSysCouplingParametersBasis with Lagrange multiplier vectors for
    mapped-response/coupling-variable sides of the coupling circle and shared/target design variables.
    """

    def __init__(self, id: str) -> None:
        """Initialize CouplingParametersLC.

        Args:
            id: Unique identifier for this coupling.
        """
        super().__init__(id)

        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = None
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None

    def set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the mapped-response side of the coupling circle.

        Args:
            mappedresponse_minus_copycouplingvariable_in: Vector of Lagrange multipliers for mapped-response side.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_mappedresponse_minus_copycouplingvariable = copy.copy(mappedresponse_minus_copycouplingvariable_in)

    def get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Obtain the Lagrange multipliers from the mapped-response side of the coupling circle.

        Returns:
            Vector of Lagrange multipliers for mapped-response side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_mappedresponse_minus_copycouplingvariable)
    
    def set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the coupling-variable side of the coupling circle.

        Args:
            copymappedresponse_minus_couplingvariable_in: Vector of Lagrange multipliers for coupling-variable side.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_copymappedresponse_minus_couplingvariable = copy.copy(copymappedresponse_minus_couplingvariable_in)

    def get_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Obtain the Lagrange multipliers from the coupling-variable side of the coupling circle.

        Returns:
            Vector of Lagrange multipliers for coupling-variable side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_copymappedresponse_minus_couplingvariable)

    def set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the shared design variables.

        Args:
            shareddesignvariable_minus_copytargetshareddesignvariable_in: Vector of multipliers for shared design variables.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(shareddesignvariable_minus_copytargetshareddesignvariable_in)
        
    def get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Obtain the Lagrange multipliers from the shared design variables.

        Returns:
            Vector of multipliers for shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable)

    def set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the target design variables.

        Args:
            copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of multipliers for target design variables.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(copyshareddesignvariable_minus_targetshareddesignvariable_in)    

    def get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Obtain the Lagrange multipliers from the target design variables.

        Returns:
            Vector of multipliers for target design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable)
    
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingLC) -> None:
        """Copy coupling data from a MiddleLevelCoupling object.

        Args:
            middlelevelcouplingIn: The MiddleLevelCoupling object to copy data from.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingLC):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersLC.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")

        if middlelevelcouplingIn.get_MappedResponses() is not None:
            self.set_Copy_MappedResponses(middlelevelcouplingIn.get_MappedResponses())
            
        if middlelevelcouplingIn.get_CouplingVariable() is not None:
            self.set_Copy_CouplingVariable(middlelevelcouplingIn.get_CouplingVariable())
            
        if middlelevelcouplingIn.get_SharedDesignVariable() is not None:
            self.set_Copy_SharedDesignVariables(middlelevelcouplingIn.get_SharedDesignVariable())
            
        if middlelevelcouplingIn.get_TargetSharedDesignVariable() is not None:
            self.set_Copy_TargetSharedDesignVariables(middlelevelcouplingIn.get_TargetSharedDesignVariable())
            
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingLC) -> None:
        """Copy coupling data to a MiddleLevelCoupling object.

        Args:
            middlelevelcouplingIn: The MiddleLevelCoupling object to copy data to.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingLC):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersLC.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
        
        # No copy.copy() wrapper needed - the getter methods already return defensive copies,
        # and the setter methods also create defensive copies of the input.
        if self.get_MappedResponses() is not None:
            middlelevelcouplingIn.set_MappedResponses(self.get_MappedResponses())
    
        if self.get_CouplingVariable() is not None:
            middlelevelcouplingIn.set_CouplingVariable(self.get_CouplingVariable())
        
        if self.get_SharedDesignVariables() is not None:
            middlelevelcouplingIn.set_SharedDesignVariable(self.get_SharedDesignVariables())
            
        if self.get_TargetSharedDesignVariables() is not None:
            middlelevelcouplingIn.set_TargetSharedDesignVariable(self.get_TargetSharedDesignVariables())
    
    def update_state(self, other_coupling: 'CouplingParametersLC') -> None:
        """Update the state of this CouplingParametersLC with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source CouplingParametersLC containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)

        # Update all List[float] | None attributes using update_state_listprimitive
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_mappedresponse_minus_copycouplingvariable, other_coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_copymappedresponse_minus_couplingvariable, other_coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable, other_coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
