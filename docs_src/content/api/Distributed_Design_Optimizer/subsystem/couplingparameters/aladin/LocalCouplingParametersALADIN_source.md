---
title: LocalCouplingParametersALADIN (Source)
---

← Back to [LocalCouplingParametersALADIN documentation](LocalCouplingParametersALADIN.md)

# LocalCouplingParametersALADIN - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\LocalCouplingParametersALADIN.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""ALADIN local coupling parameters module.

This module provides coupling parameters for local subsystems
in the ALADIN coordination method.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.middlelevel.aladin import LocalToLocal_MiddleLevelCouplingALADIN


class LocalCouplingParametersALADIN(SubSysCouplingParametersBasis):
    """Coupling parameters for ALADIN local subsystems.

    Extends SubSysCouplingParametersBasis with penalty weight vectors,
    Lagrange multiplier vectors, and d_hat quantities (coupling values
    evaluated at the controller-proposed design point) for left/right
    sides of the coupling circle and shared/target design variables.
    """

    def __init__(self, id: str) -> None:
        """Initialize LocalCouplingParametersALADIN.

        Args:
            id: Identifier for this coupling.
        """
        super().__init__(id)

        self._weights_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._weights_copymappedresponse_minus_couplingvariable: List[float] | None = None
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = None
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None
        
        # d_hat quantities: coupling quantities evaluated at the controller-proposed d_hat
        self._mappedresponses_d_hat: List[float] | None = None
        self._couplingvariable_d_hat: List[float] | None = None
        self._shareddesignvariables_d_hat: List[float] | None = None
        self._targetshareddesignvariables_d_hat: List[float] | None = None
        
        # copy d_hat quantities: neighbor's coupling quantities evaluated at the neighbor's d_hat
        self._copy_mappedresponses_d_hat: List[float] | None = None
        self._copy_couplingvariable_d_hat: List[float] | None = None
        self._copy_shareddesignvariables_d_hat: List[float] | None = None
        self._copy_targetshareddesignvariables_d_hat: List[float] | None = None

    def set_Weights_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) -> None:
        """Set the penalty weights for the mapped-response part of the coupling circle.

        Args:
            mappedresponse_minus_copycouplingvariable_in: Vector of penalty weights for mapped-response side.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_mappedresponse_minus_copycouplingvariable = copy.copy(mappedresponse_minus_copycouplingvariable_in)

    def get_Weights_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Get the penalty weights for the mapped-response part of the coupling circle.

        Returns:
            Vector of penalty weights for mapped-response side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_mappedresponse_minus_copycouplingvariable)

    def set_Weights_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) -> None:
        """Set the penalty weights for the coupling-variable part of the coupling circle.

        Args:
            copymappedresponse_minus_couplingvariable_in: Vector of penalty weights for coupling-variable side.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_copymappedresponse_minus_couplingvariable = copy.copy(copymappedresponse_minus_couplingvariable_in)

    def get_Weights_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the penalty weights for the coupling-variable part of the coupling circle.

        Returns:
            Vector of penalty weights for coupling-variable side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_copymappedresponse_minus_couplingvariable)

    def set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) -> None:
        """Set the weights for coordination of the consistency constraint between shared design variables.

        Args:
            shareddesignvariable_minus_copytargetshareddesignvariable_in: Vector of weights for shared design variables.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(shareddesignvariable_minus_copytargetshareddesignvariable_in)
    
    def get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Get the weights for coordination of the consistency constraints for shared design variables.

        Returns:
            Vector of weights for shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_shareddesignvariable_minus_copytargetshareddesignvariable)

    def set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the weights for coordination of the consistency constraint between target shared design variables.

        Args:
            copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of weights for target design variables.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(copyshareddesignvariable_minus_targetshareddesignvariable_in)

    def get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the weights for coordination of the consistency constraints for target shared design variables.

        Returns:
            Vector of weights for target design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_copyshareddesignvariable_minus_targetshareddesignvariable)

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
        """Set the Lagrange multipliers for the target shared design variables.

        Args:
            copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of multipliers for target design variables.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(copyshareddesignvariable_minus_targetshareddesignvariable_in)    

    def get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Obtain the Lagrange multipliers from the target shared design variables.

        Returns:
            Vector of multipliers for target design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable)

    def set_MappedResponses_D_Hat(self, mappedresponses_d_hat_in: List[float]) -> None:
        """Set mapped response variables evaluated at the controller-proposed d_hat.

        Args:
            mappedresponses_d_hat_in: Mapped response variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._mappedresponses_d_hat = copy.copy(mappedresponses_d_hat_in)

    def get_MappedResponses_D_Hat(self) -> List[float] | None:
        """Get mapped response variables evaluated at the controller-proposed d_hat.

        Returns:
            Mapped response variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponses_d_hat)

    def set_CouplingVariable_D_Hat(self, couplingvariable_d_hat_in: List[float]) -> None:
        """Set coupling variable evaluated at the controller-proposed d_hat.

        Args:
            couplingvariable_d_hat_in: Coupling variable at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._couplingvariable_d_hat = copy.copy(couplingvariable_d_hat_in)

    def get_CouplingVariable_D_Hat(self) -> List[float] | None:
        """Get coupling variable evaluated at the controller-proposed d_hat.

        Returns:
            Coupling variable at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._couplingvariable_d_hat)

    def set_SharedDesignVariables_D_Hat(self, shareddesignvariables_d_hat_in: List[float]) -> None:
        """Set shared design variables evaluated at the controller-proposed d_hat.

        Args:
            shareddesignvariables_d_hat_in: Shared design variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariables_d_hat = copy.copy(shareddesignvariables_d_hat_in)

    def get_SharedDesignVariables_D_Hat(self) -> List[float] | None:
        """Get shared design variables evaluated at the controller-proposed d_hat.

        Returns:
            Shared design variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariables_d_hat)

    def set_TargetSharedDesignVariables_D_Hat(self, targetshareddesignvariables_d_hat_in: List[float]) -> None:
        """Set target shared design variables evaluated at the controller-proposed d_hat.

        Args:
            targetshareddesignvariables_d_hat_in: Target shared design variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariables_d_hat = copy.copy(targetshareddesignvariables_d_hat_in)

    def get_TargetSharedDesignVariables_D_Hat(self) -> List[float] | None:
        """Get target shared design variables evaluated at the controller-proposed d_hat.

        Returns:
            Target shared design variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._targetshareddesignvariables_d_hat)

    def set_Copy_MappedResponses_D_Hat(self, copy_mappedresponses_d_hat_in: List[float]) -> None:
        """Set copy of neighbor's mapped response variables evaluated at neighbor's d_hat.

        Args:
            copy_mappedresponses_d_hat_in: Neighbor's mapped response variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_mappedresponses_d_hat = copy.copy(copy_mappedresponses_d_hat_in)

    def get_Copy_MappedResponses_D_Hat(self) -> List[float] | None:
        """Get copy of neighbor's mapped response variables evaluated at neighbor's d_hat.

        Returns:
            Neighbor's mapped response variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_mappedresponses_d_hat)

    def set_Copy_CouplingVariable_D_Hat(self, copy_couplingvariable_d_hat_in: List[float]) -> None:
        """Set copy of neighbor's coupling variable evaluated at neighbor's d_hat.

        Args:
            copy_couplingvariable_d_hat_in: Neighbor's coupling variable at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_couplingvariable_d_hat = copy.copy(copy_couplingvariable_d_hat_in)

    def get_Copy_CouplingVariable_D_Hat(self) -> List[float] | None:
        """Get copy of neighbor's coupling variable evaluated at neighbor's d_hat.

        Returns:
            Neighbor's coupling variable at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_couplingvariable_d_hat)

    def set_Copy_SharedDesignVariables_D_Hat(self, copy_shareddesignvariables_d_hat_in: List[float]) -> None:
        """Set copy of neighbor's shared design variables evaluated at neighbor's d_hat.

        Args:
            copy_shareddesignvariables_d_hat_in: Neighbor's shared design variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_shareddesignvariables_d_hat = copy.copy(copy_shareddesignvariables_d_hat_in)

    def get_Copy_SharedDesignVariables_D_Hat(self) -> List[float] | None:
        """Get copy of neighbor's shared design variables evaluated at neighbor's d_hat.

        Returns:
            Neighbor's shared design variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_shareddesignvariables_d_hat)

    def set_Copy_TargetSharedDesignVariables_D_Hat(self, copy_targetshareddesignvariables_d_hat_in: List[float]) -> None:
        """Set copy of neighbor's target shared design variables evaluated at neighbor's d_hat.

        Args:
            copy_targetshareddesignvariables_d_hat_in: Neighbor's target shared design variables at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_targetshareddesignvariables_d_hat = copy.copy(copy_targetshareddesignvariables_d_hat_in)

    def get_Copy_TargetSharedDesignVariables_D_Hat(self) -> List[float] | None:
        """Get copy of neighbor's target shared design variables evaluated at neighbor's d_hat.

        Returns:
            Neighbor's target shared design variables at d_hat, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_targetshareddesignvariables_d_hat)
    
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: LocalToLocal_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters from the middle level.

        Args:
            middlelevelcouplingIn: Middle level coupling to copy from.

        Raises:
            ValueError: If middlelevelcouplingIn is not a LocalToLocal_MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, LocalToLocal_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}Error in LocalCouplingParametersALADIN.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")

        if middlelevelcouplingIn.get_MappedResponses() is not None:
            self.set_Copy_MappedResponses(middlelevelcouplingIn.get_MappedResponses())
            
        if middlelevelcouplingIn.get_CouplingVariable() is not None:
            self.set_Copy_CouplingVariable(middlelevelcouplingIn.get_CouplingVariable())
            
        if middlelevelcouplingIn.get_SharedDesignVariable() is not None:
            self.set_Copy_SharedDesignVariables(middlelevelcouplingIn.get_SharedDesignVariable())
            
        if middlelevelcouplingIn.get_TargetSharedDesignVariable() is not None:
            self.set_Copy_TargetSharedDesignVariables(middlelevelcouplingIn.get_TargetSharedDesignVariable())
            
        if middlelevelcouplingIn.get_MappedResponses_D_Hat() is not None:
            self.set_Copy_MappedResponses_D_Hat(middlelevelcouplingIn.get_MappedResponses_D_Hat())
            
        if middlelevelcouplingIn.get_CouplingVariable_D_Hat() is not None:
            self.set_Copy_CouplingVariable_D_Hat(middlelevelcouplingIn.get_CouplingVariable_D_Hat())
            
        if middlelevelcouplingIn.get_SharedDesignVariable_D_Hat() is not None:
            self.set_Copy_SharedDesignVariables_D_Hat(middlelevelcouplingIn.get_SharedDesignVariable_D_Hat())
            
        if middlelevelcouplingIn.get_TargetSharedDesignVariable_D_Hat() is not None:
            self.set_Copy_TargetSharedDesignVariables_D_Hat(middlelevelcouplingIn.get_TargetSharedDesignVariable_D_Hat())
            
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: LocalToLocal_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters to the middle level.

        Args:
            middlelevelcouplingIn: Middle level coupling to copy to.

        Raises:
            ValueError: If middlelevelcouplingIn is not a LocalToLocal_MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, LocalToLocal_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}Error in LocalCouplingParametersALADIN.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
        
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
            
        if self.get_MappedResponses_D_Hat() is not None:
            middlelevelcouplingIn.set_MappedResponses_D_Hat(self.get_MappedResponses_D_Hat())
        
        if self.get_CouplingVariable_D_Hat() is not None:
            middlelevelcouplingIn.set_CouplingVariable_D_Hat(self.get_CouplingVariable_D_Hat())
        
        if self.get_SharedDesignVariables_D_Hat() is not None:
            middlelevelcouplingIn.set_SharedDesignVariable_D_Hat(self.get_SharedDesignVariables_D_Hat())
        
        if self.get_TargetSharedDesignVariables_D_Hat() is not None:
            middlelevelcouplingIn.set_TargetSharedDesignVariable_D_Hat(self.get_TargetSharedDesignVariables_D_Hat())
    
    def update_state(self, other_coupling: 'LocalCouplingParametersALADIN') -> None:
        """Update the state of this LocalCouplingParametersALADIN with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source LocalCouplingParametersALADIN containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)
        
        self._weights_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._weights_mappedresponse_minus_copycouplingvariable, other_coupling.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
        self._weights_copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._weights_copymappedresponse_minus_couplingvariable, other_coupling.get_Weights_CopyMappedResponse_Minus_CouplingVariable())
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_copyshareddesignvariable_minus_targetshareddesignvariable, other_coupling.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_mappedresponse_minus_copycouplingvariable, other_coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_copymappedresponse_minus_couplingvariable, other_coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable, other_coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())

        self._mappedresponses_d_hat: List[float] | None = update_state_listprimitive(self._mappedresponses_d_hat, other_coupling.get_MappedResponses_D_Hat())
        self._couplingvariable_d_hat: List[float] | None = update_state_listprimitive(self._couplingvariable_d_hat, other_coupling.get_CouplingVariable_D_Hat())
        self._shareddesignvariables_d_hat: List[float] | None = update_state_listprimitive(self._shareddesignvariables_d_hat, other_coupling.get_SharedDesignVariables_D_Hat())
        self._targetshareddesignvariables_d_hat: List[float] | None = update_state_listprimitive(self._targetshareddesignvariables_d_hat, other_coupling.get_TargetSharedDesignVariables_D_Hat())
        
        self._copy_mappedresponses_d_hat: List[float] | None = update_state_listprimitive(self._copy_mappedresponses_d_hat, other_coupling.get_Copy_MappedResponses_D_Hat())
        self._copy_couplingvariable_d_hat: List[float] | None = update_state_listprimitive(self._copy_couplingvariable_d_hat, other_coupling.get_Copy_CouplingVariable_D_Hat())
        self._copy_shareddesignvariables_d_hat: List[float] | None = update_state_listprimitive(self._copy_shareddesignvariables_d_hat, other_coupling.get_Copy_SharedDesignVariables_D_Hat())
        self._copy_targetshareddesignvariables_d_hat: List[float] | None = update_state_listprimitive(self._copy_targetshareddesignvariables_d_hat, other_coupling.get_Copy_TargetSharedDesignVariables_D_Hat())

```
