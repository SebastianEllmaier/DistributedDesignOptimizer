# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local to controller coupling parameters module.

This module provides parameters for coupling from local
subsystems to controller in ALADIN.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class LocalToLocalForController_CouplingParameters:
    """This class is meant to be a part of the controller mapping.

    Maps between controller and local subsystem, since that part of
    the communicated data has an assignment to i <-> j pairs.
    """
    
    def __init__(self, id: str) -> None:
        """Initialize local to controller coupling parameters.

        Args:
            id: Identifier for the coupled subsystem.
        """
        
        # Id of local subsystem j to which subsystem i is coupled to
        self._id: str = id

        # Mapped responses
        self._mappedresponses: List[float] | None = None
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._weights_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        
        # If self._jacobian_mappedresponses is None, then mapped responses do not exist
        # If self._jacobian_mappedresponses is List[List[float | None]], then the entries that 
        # are None are precisely the derivatives the user could not provide in his Analysis_xxx.py
        # In total: Non-complete Jacobians are stored intermediately
        # If the Jacobian is needed in computations, one needs to ensure that no 'None'-entries exist
        self._jacobian_mappedresponses: List[List[float | None]] | None = None
        self._hessians_mappedresponses: List[List[List[float]]] | None = None
        
        # Coupling variables
        self._couplingvariables: List[float] | None = None
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = None
        self._weights_copymappedresponse_minus_couplingvariable: List[float] | None = None
        
        # Shared design variables
        self._shareddesignvariables: List[float] | None = None
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None
        
        # Target shared design variables
        self._targetshareddesignvariables: List[float] | None = None
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = None
        
        # Indices of the design variables vector of the subsystem i that stores this object
        # that correspond to the coupling, shared and target shared variables of the 
        # i <-> j coupling
        # In ALADIN import for building the QP
        self._indices_couplingvariables_in_designvariables: List[int] | None = None
        self._indices_shareddesignvariables_in_designvariables: List[int] | None = None
        self._indices_targetshareddesignvariables_in_designvariables: List[int] | None = None

    def get_ID(self) -> str:
        """Return the ID.

        Returns:
            Identifier for the coupled subsystem.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._id
    
    def set_MappedResponses(self, mappedresponsesin: List[float]) -> None:
        """Set mapped responses.

        Args:
            mappedresponsesin: Mapped responses to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._mappedresponses = copy.copy(mappedresponsesin)

    def get_MappedResponses(self) -> List[float] | None:
        """Return mapped responses.

        Returns:
            Mapped responses, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponses)
    
    def set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) -> None:
        """Set multipliers corresponding to constraint with subsystem i's mapped responses.

        Args:
            mappedresponse_minus_copycouplingvariable_in: Multipliers for the mapped response minus copied coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_mappedresponse_minus_copycouplingvariable = copy.copy(mappedresponse_minus_copycouplingvariable_in)

    def get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Return multipliers corresponding to constraint with subsystem i's mapped responses.

        Returns:
            Left multipliers, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_mappedresponse_minus_copycouplingvariable)
    
    def set_Weights_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) -> None:
        """Set weights corresponding to constraint with subsystem i's mapped responses.

        Args:
            mappedresponse_minus_copycouplingvariable_in: Weights for the mapped response minus copied coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_mappedresponse_minus_copycouplingvariable = copy.copy(mappedresponse_minus_copycouplingvariable_in)

    def get_Weights_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Return weights corresponding to constraint with subsystem i's mapped responses.

        Returns:
            Left weights, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_mappedresponse_minus_copycouplingvariable)
    
    def set_JacobianMappedResponses(self, jacobianmappedresponsesin: List[List[float | None]]) -> None:
        """Set the Jacobians of subsystem i's mapped responses.

        Args:
            jacobianmappedresponsesin: Jacobian of mapped responses to set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_mappedresponses = copy.deepcopy(jacobianmappedresponsesin)

    def get_JacobianMappedResponses(self) -> List[List[float | None]] | None:
        """Return the Jacobians of subsystem i's mapped responses.

        If it is None, the user does not know the Jacobians.
        If it is a List[List[float | None]], the entries with None
        indicate the derivatives the user does not provide, i.e. need
        to be approximated ('intermediate storage').
        It needs to be ensured that if the Jacobian
        is used, it should have no 'None'-fields.

        Returns:
            Jacobian of mapped responses, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_mappedresponses)
        
    def set_HessiansMappedResponses(self, hessiansmappedresponsesin: List[List[List[float]]]) -> None:
        """Set the Hessians of subsystem i's mapped responses.

        Args:
            hessiansmappedresponsesin: Hessians of mapped responses to set.
        """
        # copy.deepcopy() used - List[List[List[float]]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._hessians_mappedresponses = copy.deepcopy(hessiansmappedresponsesin)

    def get_HessiansMappedResponses(self) -> List[List[List[float]]] | None:
        """Get the Hessians of subsystem i's mapped responses.

        Returns:
            Hessians of mapped responses, or None if not set.
        """
        # copy.deepcopy() used - List[List[List[float]]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._hessians_mappedresponses)
        
    def set_Jacobian_MappedResponses_at_Position(self, i: int, j: int, value: float) -> None:
        """Update the Jacobian at position (i,j) with the input value.

        Args:
            i: Row index.
            j: Column index.
            value: Value to set at position (i, j).
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._jacobian_mappedresponses[i][j] = value
    
    def set_CouplingVariables(self, couplingvariablesin: List[float]) -> None:
        """Set subsystem i's coupling variables.

        Args:
            couplingvariablesin: Coupling variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._couplingvariables = copy.copy(couplingvariablesin)

    def get_CouplingVariables(self) -> List[float] | None:
        """Return subsystem i's coupling variables.

        Returns:
            Coupling variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._couplingvariables)
    
    def set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) -> None:
        """Set the multipliers corresponding to the constraints where subsystem i's coupling variables appear.

        Args:
            copymappedresponse_minus_couplingvariable_in: Multipliers for the copied mapped response minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_copymappedresponse_minus_couplingvariable = copy.copy(copymappedresponse_minus_couplingvariable_in)

    def get_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Return the multipliers corresponding to the constraints where subsystem i's coupling variables appear.

        Returns:
            Right multipliers, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_copymappedresponse_minus_couplingvariable)
    
    def set_Weights_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) -> None:
        """Set the weights corresponding to the constraints where subsystem i's coupling variables appear.

        Args:
            copymappedresponse_minus_couplingvariable_in: Weights for the copied mapped response minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_copymappedresponse_minus_couplingvariable = copy.copy(copymappedresponse_minus_couplingvariable_in)

    def get_Weights_CopyMappedResponse_Minus_CouplingVariable(self) -> List[float] | None:
        """Return the weights corresponding to the constraints where subsystem i's coupling variables appear.

        Returns:
            Right weights, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_copymappedresponse_minus_couplingvariable)
    
    def set_SharedDesignVariables(self, shareddesignvariablesin: List[float]) -> None:
        """Set the shared design variables of subsystem i.

        Args:
            shareddesignvariablesin: Shared design variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariables = copy.copy(shareddesignvariablesin)

    def get_SharedDesignVariables(self) -> List[float] | None:
        """Return the shared design variables of subsystem i.

        Returns:
            Shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariables)
    
    def set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) -> None:
        """Set multipliers w.r.t constraints where subsystem i's shared design vars appear.

        Args:
            shareddesignvariable_minus_copytargetshareddesignvariable_in: Multipliers for the shared design variable minus copied target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(shareddesignvariable_minus_copytargetshareddesignvariable_in)

    def get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Return multipliers w.r.t constraints where subsystem i's shared design vars appear.

        Returns:
            Multipliers for shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable)
    
    def set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) -> None:
        """Set weights w.r.t. constraints where subsystem i's shared design vars appear.

        Args:
            shareddesignvariable_minus_copytargetshareddesignvariable_in: Weights for the shared design variable minus copied target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(shareddesignvariable_minus_copytargetshareddesignvariable_in)

    def get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Return weights w.r.t. constraints where subsystem i's shared design vars appear.

        Returns:
            Weights for shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_shareddesignvariable_minus_copytargetshareddesignvariable)
    
    def set_TargetSharedDesignVariables(self, targetshareddesignvariablesin: List[float]) -> None:
        """Set the target shared design variables of subsystem i.

        Args:
            targetshareddesignvariablesin: Target shared design variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariables = copy.copy(targetshareddesignvariablesin)

    def get_TargetSharedDesignVariables(self) -> List[float] | None:
        """Return the target shared design variables of subsystem i.

        Returns:
            Target shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._targetshareddesignvariables)
    
    def set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set multipliers w.r.t constraints where subsystem i's target shared design vars appear.

        Args:
            copyshareddesignvariable_minus_targetshareddesignvariable_in: Multipliers for the copied shared design variable minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(copyshareddesignvariable_minus_targetshareddesignvariable_in)

    def get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Return multipliers w.r.t constraints where subsystem i's target shared design vars appear.

        Returns:
            Multipliers for target shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable)
    
    def set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set weights w.r.t. constraints where subsystem i's target shared design vars appear.

        Args:
            copyshareddesignvariable_minus_targetshareddesignvariable_in: Weights for the copied shared design variable minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable = copy.copy(copyshareddesignvariable_minus_targetshareddesignvariable_in)

    def get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Return weights w.r.t. constraints where subsystem i's target shared design vars appear.

        Returns:
            Weights for target shared design variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_copyshareddesignvariable_minus_targetshareddesignvariable)
        
    def set_Indices_CouplingVariables_In_DesignVariables(self, indices_couplingvariables_in_designvariables_in: List[int]) -> None:
        """Set the indices of the design variables of subsystem i that correspond to the coupling variables of the i <-> j coupling.

        Args:
            indices_couplingvariables_in_designvariables_in: Indices of the coupling variables
                in the design variables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_couplingvariables_in_designvariables = copy.copy(indices_couplingvariables_in_designvariables_in)

    def get_Indices_CouplingVariables_In_DesignVariables(self) -> List[int] | None:
        """Get the indices of the design variables of subsystem i that correspond to the coupling variables of the i <-> j coupling.

        Returns:
            Indices of the coupling variables in the design variables of subsystem i,
            or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_couplingvariables_in_designvariables)

    def set_Indices_SharedDesignVariables_In_DesignVariables(self, indices_shareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Set the indices of the design variables of subsystem i that correspond to the shared design variables of the i <-> j coupling.

        Args:
            indices_shareddesignvariables_in_designvariables_in: Indices of the shared design
                variables in the design variables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_shareddesignvariables_in_designvariables = copy.copy(indices_shareddesignvariables_in_designvariables_in)

    def get_Indices_SharedDesignVariables_In_DesignVariables(self) -> List[int] | None:
        """Get the indices of the design variables of subsystem i that correspond to the shared design variables of the i <-> j coupling.

        Returns:
            Indices of the shared design variables in the design variables of subsystem i,
            or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_shareddesignvariables_in_designvariables)

    def set_Indices_TargetSharedDesignVariables_In_DesignVariables(self, indices_targetshareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Set the indices of the design variables of subsystem i that correspond to the target shared design variables of the i <-> j coupling.

        Args:
            indices_targetshareddesignvariables_in_designvariables_in: Indices of the target shared
                design variables in the design variables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_targetshareddesignvariables_in_designvariables = copy.copy(indices_targetshareddesignvariables_in_designvariables_in)

    def get_Indices_TargetSharedDesignVariables_In_DesignVariables(self) -> List[int] | None:
        """Get the indices of the design variables of subsystem i that correspond to the target shared design variables of the i <-> j coupling.

        Returns:
            Indices of the target shared design variables in the design variables
            of subsystem i, or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_targetshareddesignvariables_in_designvariables)    
    
    def update_state(self, other_coupling: 'LocalToLocalForController_CouplingParameters') -> None:
        """Update the state of this object from another LocalToLocalForController_CouplingParameters.

        This method is necessary for multiprocessing: when subsystems are executed
        in parallel via Parallel.py using multiprocessing.Pool, each process
        receives a copy of the data. After execution, the original objects must be
        updated with results from the executed copies. This method updates the
        numerical information stored in the class's attributes without changing
        the original memory address location, preserving object identity.

        Attributes are updated in the same order as defined in __init__().

        Args:
            other_coupling: The source LocalToLocalForController_CouplingParameters containing updated values
                from parallel execution.
        """
        # _id: str - direct assignment (str is immutable, no copy.copy() needed)
        self._id: str = other_coupling.get_ID()
        
        self._mappedresponses: List[float] | None = update_state_listprimitive(self._mappedresponses, other_coupling.get_MappedResponses())
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_mappedresponse_minus_copycouplingvariable, other_coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        self._weights_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(self._weights_mappedresponse_minus_copycouplingvariable, other_coupling.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
        
        # Nested list - iterate and use update_state_listprimitive per inner list
        other_jacobian_mappedresponses: List[List[float | None]] | None = other_coupling.get_JacobianMappedResponses()
        if other_jacobian_mappedresponses is None:
            self._jacobian_mappedresponses = None
        elif self._jacobian_mappedresponses is None:
            self._jacobian_mappedresponses = other_jacobian_mappedresponses
        else:
            for i in range(len(other_jacobian_mappedresponses)):
                self._jacobian_mappedresponses[i] = update_state_listprimitive(
                    self._jacobian_mappedresponses[i], other_jacobian_mappedresponses[i])
                
        # Hessian of mapped responses is List[List[List[float]]], call update_state_listprimitive on each inner list
        other_hessians_mappedresponses: List[List[List[float]]] | None = other_coupling.get_HessiansMappedResponses()

        if other_hessians_mappedresponses is None:
            self._hessians_mappedresponses = None
        else:
            if self._hessians_mappedresponses is None:
                self._hessians_mappedresponses = copy.deepcopy(other_hessians_mappedresponses)
            else:
                for i in range(len(other_hessians_mappedresponses)):
                    for j in range(len(other_hessians_mappedresponses[i])):
                        self._hessians_mappedresponses[i][j] = update_state_listprimitive(self._hessians_mappedresponses[i][j], other_hessians_mappedresponses[i][j])
        
        self._couplingvariables: List[float] | None = update_state_listprimitive(self._couplingvariables, other_coupling.get_CouplingVariables())
        self._multipliers_copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_copymappedresponse_minus_couplingvariable, other_coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        self._weights_copymappedresponse_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._weights_copymappedresponse_minus_couplingvariable, other_coupling.get_Weights_CopyMappedResponse_Minus_CouplingVariable())
        
        self._shareddesignvariables: List[float] | None = update_state_listprimitive(self._shareddesignvariables, other_coupling.get_SharedDesignVariables())
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._weights_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        
        self._targetshareddesignvariables: List[float] | None = update_state_listprimitive(self._targetshareddesignvariables, other_coupling.get_TargetSharedDesignVariables())
        self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_copyshareddesignvariable_minus_targetshareddesignvariable, other_coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        self._weights_copyshareddesignvariable_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_copyshareddesignvariable_minus_targetshareddesignvariable, other_coupling.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())

        self._indices_couplingvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_couplingvariables_in_designvariables, other_coupling.get_Indices_CouplingVariables_In_DesignVariables())
        self._indices_shareddesignvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_shareddesignvariables_in_designvariables, other_coupling.get_Indices_SharedDesignVariables_In_DesignVariables())
        self._indices_targetshareddesignvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_targetshareddesignvariables_in_designvariables, other_coupling.get_Indices_TargetSharedDesignVariables_In_DesignVariables())