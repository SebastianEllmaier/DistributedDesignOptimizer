# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Subsystem coupling parameters basis module.

This module provides the base class for subsystem-level coupling
parameters in distributed optimization.
"""

import copy
from typing import List
import numpy as np
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class SubSysCouplingParametersBasis(CouplingParametersBasis):
    """Base class for subsystem-level coupling parameters between local subsystems.

    Stores the coupling variables, mapped responses, shared design variables,
    their copies from the neighboring subsystem, associated Jacobians, and
    index mappings into the subsystem's design variable vector. All scaled
    quantities use [0, 1] scaling.

    The storage is defined as follows::

                          subsystem 0
                      //                 \\

        mapped response 0 -> 1         coupling variable 1 -> 0


        coupling variable 0 -> 1         mapped response 1 -> 0

                      \\                  //
                          subsystem 1

    Consider that the responses are stored locally for subsystem 0. Then:
        - mapping responses from  0 -> 1 is called mappedresponses
        - coupling variables from 1 -> 0 is called couplingvariable
        - coupling responses from 0 -> 1 is called copy_couplingvariable
        - mapping responses from  1 -> 0 is called copy_mappedresponses
    """

    def __init__(self, id: str) -> None:
        """Initialize coupling parameters for a subsystem.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        super().__init__(id)
        
        self._couplingvariable: List[float] | None = None  # scaled01 values
        self._mappedresponses: List[float] | None = None  # scaled01 values
        self._couplingvariable_unscaled: List[float] | None = None  # unscaled values
        self._mappedresponses_unscaled: List[float] | None = None  # unscaled values
        self._copy_couplingvariable: List[float] | None = None  # scaled01 values
        self._copy_mappedresponses: List[float] | None = None  # scaled01 values
        
        # Jacobian of the mapped response
        self._jacobian_mappedresponse: List[List[float | None]] | None = None
        self._copy_jacobian_mappedresponse: List[List[float | None]] | None = None
        
        self._shareddesignvariables: List[float] | None = None  # scaled01 values
        self._shareddesignvariables_unscaled: List[float] | None = None  # unscaled values
        self._copy_shareddesignvariables: List[float] | None = None  # scaled01 values
        self._targetshareddesignvariables: List[float] | None = None  # scaled01 values
        self._targetshareddesignvariables_unscaled: List[float] | None = None  # unscaled values
        self._copy_targetshareddesignvariables: List[float] | None = None  # scaled01 values
                
        self._couplingstrength: float | None = None
        
        # Indices of the design variables vector of the subsystem i that stores this object
        # that correspond to the coupling, shared and target shared variables of the 
        # i <-> j coupling
        self._indices_couplingvariables_in_designvariables: List[int] | None = None
        self._indices_shareddesignvariables_in_designvariables: List[int] | None = None
        self._indices_targetshareddesignvariables_in_designvariables: List[int] | None = None

        # Warning flags for out-of-range values (one-time warnings)
        self._mappedresponses_lower_scaler_bound_warning_raised: bool = False
        self._mappedresponses_upper_scaler_bound_warning_raised: bool = False
        self._couplingvariable_lower_scaler_bound_warning_raised: bool = False
        self._couplingvariable_upper_scaler_bound_warning_raised: bool = False
        self._shareddesignvariables_lower_scaler_bound_warning_raised: bool = False
        self._shareddesignvariables_upper_scaler_bound_warning_raised: bool = False
        self._targetshareddesignvariables_lower_scaler_bound_warning_raised: bool = False
        self._targetshareddesignvariables_upper_scaler_bound_warning_raised: bool = False
    
    def get_CouplingVariable(self) -> List[float] | None:
        """Returns the coupling variables prescribed by the subsystem for a single neighboring subsystem.

        Returns:
            Vector of coupling variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._couplingvariable)

    def set_CouplingVariable(self, couplingvariable: List[float]) -> None:
        """Stores a new value of the coupling variables.

        Args:
            couplingvariable: Coupling variables as scaled01 values.
        """
        cv_array = np.array(couplingvariable)
        # Check lower bound
        if not np.all((cv_array >= 0.0) | np.isclose(cv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._couplingvariable_lower_scaler_bound_warning_raised:
                self._couplingvariable_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All couplingvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((cv_array <= 1.0) | np.isclose(cv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._couplingvariable_upper_scaler_bound_warning_raised:
                self._couplingvariable_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All couplingvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._couplingvariable = copy.copy(couplingvariable)
            
    def get_MappedResponses(self) -> List[float] | None:
        """Returns the physically mapped responses from the subsystem onto the neighboring subsystem.

        Returns:
            Mapped responses as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponses)

    def set_MappedResponses(self, varin: List[float]) -> None:
        """Stores the mapped responses from the subsystem onto the neighboring subsystem.

        Args:
            varin: Mapped responses as scaled01 values.
        """
        mr_array = np.array(varin)
        # Check lower bound
        if not np.all((mr_array >= 0.0) | np.isclose(mr_array, 0.0, atol=1e-8, rtol=0)):
            if not self._mappedresponses_lower_scaler_bound_warning_raised:
                self._mappedresponses_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All mappedresponses must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((mr_array <= 1.0) | np.isclose(mr_array, 1.0, atol=1e-8, rtol=0)):
            if not self._mappedresponses_upper_scaler_bound_warning_raised:
                self._mappedresponses_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All mappedresponses must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._mappedresponses = copy.copy(varin)
    
    def set_CouplingVariable_Unscaled(self, couplingvariable: List[float]) -> None:
        """Stores the unscaled coupling variables.

        Note: No getter method is provided for unscaled values to prevent coordination
        methods from using unscaled values for coordination. Coordination should always
        use scaled [0,1] values to ensure numerical stability and consistency.

        Args:
            couplingvariable: Coupling variables as unscaled values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._couplingvariable_unscaled = copy.copy(couplingvariable)    
        
    def set_MappedResponses_Unscaled(self, varin: List[float]) -> None:
        """Stores the unscaled mapped responses.
            
        Note: No getter method is provided for unscaled values to prevent coordination
        methods from using unscaled values for coordination. Coordination should always
        use scaled [0,1] values to ensure numerical stability and consistency.

        Args:
            varin: Mapped responses as unscaled values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._mappedresponses_unscaled = copy.copy(varin)
        
    def get_Copy_CouplingVariable(self) -> List[float] | None:
        """Gets the stored copy of the coupling variable of a neighboring subsystem.

        Returns:
            Copy of the coupling variable as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_couplingvariable)

    def set_Copy_CouplingVariable(self, varin: List[float]) -> None:
        """Stores a copy of the coupling variable representing the physical coupling required by a neighboring subsystem.

        Args:
            varin: Copy of coupling variable as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_couplingvariable = copy.copy(varin)
   
    def get_Copy_MappedResponses(self) -> List[float] | None:
        """Gets the stored copy of the physical responses mapped onto this subsystem.

        Returns:
            Copy of mapped responses as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_mappedresponses)

    def set_Copy_MappedResponses(self, varin: List[float]) -> None:
        """Stores a copy of the mapped physical responses of a neighboring subsystem onto this subsystem.

        Args:
            varin: Copy of mapped responses as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_mappedresponses = copy.copy(varin)
        
    def get_Jacobian_MappedResponse(self) -> List[List[float | None]] | None:
        """Returns the stored Jacobian of the mapped responses, possibly with missing values.

        Returns:
            The Jacobian matrix, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_mappedresponse)
    
    def set_Jacobian_MappedResponse(self, jacobian_mappedresponse_in: List[List[float] | None]) -> None:
        """Sets the Jacobian of the mapped response from this subsystem's coupling.

        The Jacobian should have no missing values
        (or does not exist, if there are no mapped responses).

        Args:
            jacobian_mappedresponse_in: The Jacobian matrix to set.
        """

        # Check if there exist mapped responses in this coupling
        if self.get_MappedResponses() is None:
            
            # Since there are no mapped responses, there should also be no Jacobian
            raise ValueError(f"{DDO_Color}There exist no mapped responses in the coupling associated with ID {self.get_ID()} that you provided; hence, no Jacobian of the mapped responses{Reset}")
        
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._jacobian_mappedresponse = copy.deepcopy(jacobian_mappedresponse_in)
        
    def set_Jacobian_MappedResponse_at_Position(self, i: int, j: int, jacobian_mappedresponse_point: float) -> None:
        """Sets value 'jacobian_mappedresponse_point' to the Jacobian at index (i,j).

        Args:
            i: Row index of the Jacobian matrix.
            j: Column index of the Jacobian matrix.
            jacobian_mappedresponse_point: The value to set at position (i,j).
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._jacobian_mappedresponse[i][j] = jacobian_mappedresponse_point
        
    def get_Copy_Jacobian_MappedResponse(self) -> List[List[float]] | None:
        """Returns the Jacobian of the mapped response from the other subsystem's coupling.

        The Jacobian should have no missing values
        (or does not exist, if there are no mapped responses).

        Returns:
            The copy Jacobian matrix, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_jacobian_mappedresponse)
    
    def set_Copy_Jacobian_MappedResponse(self, copy_jacobian_mappedresponse_in: List[List[float] | None]) -> None:
        """Sets the Jacobian of the mapped response from the neighboring subsystem's coupling.

        The Jacobian should have no missing values
        (or does not exist, if there are no mapped responses).

        Args:
            copy_jacobian_mappedresponse_in: The copy Jacobian matrix to set.
        """
        
        # Check if there exist copy mapped responses in this coupling
        if self.get_Copy_MappedResponses() is None:
            
            # Since there are no copy mapped responses, there should also be no Jacobian
            raise ValueError(f"{DDO_Color}There exist no copy mapped responses in the coupling associated with ID {self.get_ID()} that you provided; hence, no Jacobian of the mapped responses{Reset}")
        
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_jacobian_mappedresponse = copy.deepcopy(copy_jacobian_mappedresponse_in)

    def set_SharedDesignVariables(self, variablesin: List[float]) -> None:
        """Sets the shared design variables which are shared with the neighboring subsystem.

        Args:
            variablesin: Shared design variables as scaled01 values.
        """
        sdv_array = np.array(variablesin)
        # Check lower bound
        if not np.all((sdv_array >= 0.0) | np.isclose(sdv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._shareddesignvariables_lower_scaler_bound_warning_raised:
                self._shareddesignvariables_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All shareddesignvariables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((sdv_array <= 1.0) | np.isclose(sdv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._shareddesignvariables_upper_scaler_bound_warning_raised:
                self._shareddesignvariables_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All shareddesignvariables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariables = copy.copy(variablesin)
        
    def get_SharedDesignVariables(self) -> List[float] | None:
        """Gets the shared design variables.

        Returns:
            Shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariables)
    
    def set_SharedDesignVariables_Unscaled(self, variablesin: List[float]) -> None:
        """Stores the unscaled shared design variables.

        Note: No getter method is provided for unscaled values to prevent coordination
        methods from using unscaled values for coordination. Coordination should always
        use scaled [0,1] values to ensure numerical stability and consistency.

        Args:
            variablesin: Shared design variables as unscaled values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariables_unscaled = copy.copy(variablesin)

    def set_Copy_SharedDesignVariables(self, copy_ofvariablesin: List[float]) -> None:
        """Sets a copy of the shared design variable value of the neighboring subsystem.

        Args:
            copy_ofvariablesin: Copy of shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_shareddesignvariables = copy.copy(copy_ofvariablesin)
        
    def get_Copy_SharedDesignVariables(self) -> List[float] | None:
        """Gets the copy of the shared design variable of the neighboring subsystem.

        Returns:
            Copy of shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_shareddesignvariables)
    
    def set_TargetSharedDesignVariables(self, variablesin: List[float]) -> None:
        """Sets the target shared design variables which are shared with the neighboring subsystem.

        Args:
            variablesin: Target shared design variables as scaled01 values.
        """
        tsdv_array = np.array(variablesin)
        # Check lower bound
        if not np.all((tsdv_array >= 0.0) | np.isclose(tsdv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._targetshareddesignvariables_lower_scaler_bound_warning_raised:
                self._targetshareddesignvariables_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All targetshareddesignvariables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((tsdv_array <= 1.0) | np.isclose(tsdv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._targetshareddesignvariables_upper_scaler_bound_warning_raised:
                self._targetshareddesignvariables_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All targetshareddesignvariables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariables = copy.copy(variablesin)

    def get_TargetSharedDesignVariables(self) -> List[float] | None:
        """Gets the target shared design variables.

        Returns:
            Target shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._targetshareddesignvariables)
    
    def set_TargetSharedDesignVariables_Unscaled(self, variablesin: List[float]) -> None:
        """Stores the unscaled target shared design variables.

        Note: No getter method is provided for unscaled values to prevent coordination
        methods from using unscaled values for coordination. Coordination should always
        use scaled [0,1] values to ensure numerical stability and consistency.

        Args:
            variablesin: Target shared design variables as unscaled values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariables_unscaled = copy.copy(variablesin)

    def set_Copy_TargetSharedDesignVariables(self, copy_ofvariablesin: List[float]) -> None:
        """Sets a copy of the shared design variable value of the neighboring subsystem.

        Args:
            copy_ofvariablesin: Copy of target shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_targetshareddesignvariables = copy.copy(copy_ofvariablesin)
        
    def get_Copy_TargetSharedDesignVariables(self) -> List[float] | None:
        """Gets the copy of the shared design variable of the neighboring subsystem.

        Returns:
            Copy of target shared design variables as scaled01 values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_targetshareddesignvariables)
    
    def set_CouplingStrength(self, couplingstrengthIn: float) -> None:
        """Sets the coupling strength value.

        Args:
            couplingstrengthIn: The coupling strength value to set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._couplingstrength = couplingstrengthIn
        
    def get_CouplingStrength(self) -> float | None:
        """Gets the coupling strength value.

        Returns:
            The coupling strength value, or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._couplingstrength
    
    def set_Indices_CouplingVariables_In_DesignVariables(self, indices_couplingvariables_in_designvariables_in: List[int]) -> None:
        """Sets the indices of coupling variables within the design variables vector.

        Args:
            indices_couplingvariables_in_designvariables_in: Indices of the coupling variables
                in the designvariables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_couplingvariables_in_designvariables = copy.copy(indices_couplingvariables_in_designvariables_in)

    def get_Indices_CouplingVariables_In_DesignVariables(self) -> List[int] | None:
        """Gets the indices of coupling variables within the design variables vector.

        Returns:
            Indices of the coupling variables in the designvariables of subsystem i,
            or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_couplingvariables_in_designvariables)

    def set_Indices_SharedDesignVariables_In_DesignVariables(self, indices_shareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Sets the indices of shared design variables within the design variables vector.

        Args:
            indices_shareddesignvariables_in_designvariables_in: Indices of the shared design
                variables in the designvariables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_shareddesignvariables_in_designvariables = copy.copy(indices_shareddesignvariables_in_designvariables_in)

    def get_Indices_SharedDesignVariables_In_DesignVariables(self) -> List[int] | None:
        """Gets the indices of shared design variables within the design variables vector.

        Returns:
            Indices of the shared design variables in the designvariables of subsystem i,
            or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_shareddesignvariables_in_designvariables)

    def set_Indices_TargetSharedDesignVariables_In_DesignVariables(self, indices_targetshareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Sets the indices of target shared design variables within the design variables vector.

        Args:
            indices_targetshareddesignvariables_in_designvariables_in: Indices of the target shared
                design variables in the designvariables of subsystem i.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._indices_targetshareddesignvariables_in_designvariables = copy.copy(indices_targetshareddesignvariables_in_designvariables_in)

    def get_Indices_TargetSharedDesignVariables_In_DesignVariables(self) -> List[int] | None:
        """Gets the indices of target shared design variables within the design variables vector.

        Returns:
            Indices of the target shared design variables in the designvariables
            of subsystem i, or None if not set.
        """
        # copy.copy() used - List[int] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._indices_targetshareddesignvariables_in_designvariables)   

    def update_state(self, other_coupling: 'SubSysCouplingParametersBasis') -> None:
        """Update the state of this SubSysCouplingParametersBasis with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source SubSysCouplingParametersBasis containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes (_id from CouplingParametersBasis)
        super().update_state(other_coupling=other_coupling)

        # Coupling variables and mapped responses (scaled01)
        self._couplingvariable: List[float] | None = update_state_listprimitive(self._couplingvariable, other_coupling.get_CouplingVariable())
        self._mappedresponses: List[float] | None = update_state_listprimitive(self._mappedresponses, other_coupling.get_MappedResponses())

        # Coupling variables and mapped responses (unscaled)
        # Note: Since we dont define getter methods, we have to directly access the private variables from the other couplings
        self._couplingvariable_unscaled: List[float] | None = update_state_listprimitive(self._couplingvariable_unscaled, other_coupling._couplingvariable_unscaled)
        self._mappedresponses_unscaled: List[float] | None = update_state_listprimitive(self._mappedresponses_unscaled, other_coupling._mappedresponses_unscaled)

        # Copy coupling variables and mapped responses
        self._copy_couplingvariable: List[float] | None = update_state_listprimitive(self._copy_couplingvariable, other_coupling.get_Copy_CouplingVariable())
        self._copy_mappedresponses: List[float] | None = update_state_listprimitive(self._copy_mappedresponses, other_coupling.get_Copy_MappedResponses())

        # Handle List[List[float]] attributes - need to iterate and update each inner list
        other_jacobian_mappedresponse: List[List[float | None]] | None = (other_coupling.get_Jacobian_MappedResponse())
        if other_jacobian_mappedresponse is None:
            self._jacobian_mappedresponse: List[List[float | None]] | None = None
        else:
            if self._jacobian_mappedresponse is None:
                self._jacobian_mappedresponse = other_jacobian_mappedresponse
            else:
                for i in range(len(other_jacobian_mappedresponse)):
                    self._jacobian_mappedresponse[i] = update_state_listprimitive(self._jacobian_mappedresponse[i], other_jacobian_mappedresponse[i])

        other_copy_jacobian_mappedresponse: List[List[float | None]] | None = (other_coupling.get_Copy_Jacobian_MappedResponse())
        if other_copy_jacobian_mappedresponse is None:
            self._copy_jacobian_mappedresponse: List[List[float | None]] | None = None
        else:
            if self._copy_jacobian_mappedresponse is None:
                self._copy_jacobian_mappedresponse = other_copy_jacobian_mappedresponse
            else:
                for i in range(len(other_copy_jacobian_mappedresponse)):
                    self._copy_jacobian_mappedresponse[i] = update_state_listprimitive(self._copy_jacobian_mappedresponse[i], other_copy_jacobian_mappedresponse[i])

        # Shared design variables (scaled01, unscaled, copy)
        self._shareddesignvariables: List[float] | None = update_state_listprimitive(self._shareddesignvariables, other_coupling.get_SharedDesignVariables())
        self._shareddesignvariables_unscaled = update_state_listprimitive(self._shareddesignvariables_unscaled, other_coupling._shareddesignvariables_unscaled)
        self._copy_shareddesignvariables: List[float] | None = update_state_listprimitive(self._copy_shareddesignvariables, other_coupling.get_Copy_SharedDesignVariables())

        # Target shared design variables (scaled01, unscaled, copy)
        self._targetshareddesignvariables: List[float] | None = update_state_listprimitive(self._targetshareddesignvariables, other_coupling.get_TargetSharedDesignVariables())
        self._targetshareddesignvariables_unscaled = update_state_listprimitive(self._targetshareddesignvariables_unscaled, other_coupling._targetshareddesignvariables_unscaled)
        self._copy_targetshareddesignvariables: List[float] | None = update_state_listprimitive(self._copy_targetshareddesignvariables, other_coupling.get_Copy_TargetSharedDesignVariables())
        
        # Coupling strength (float - primitive, direct assignment)
        self._couplingstrength: float | None = other_coupling.get_CouplingStrength()
        
        # Indices
        self._indices_couplingvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_couplingvariables_in_designvariables, 
                                                                                                          other_coupling.get_Indices_CouplingVariables_In_DesignVariables())
        self._indices_shareddesignvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_shareddesignvariables_in_designvariables, 
                                                                                                              other_coupling.get_Indices_SharedDesignVariables_In_DesignVariables())
        self._indices_targetshareddesignvariables_in_designvariables: List[int] | None = update_state_listprimitive(self._indices_targetshareddesignvariables_in_designvariables, 
                                                                                                                    other_coupling.get_Indices_TargetSharedDesignVariables_In_DesignVariables())

        # Warning flags (bool primitives - direct assignment)
        self._mappedresponses_lower_scaler_bound_warning_raised: bool = other_coupling._mappedresponses_lower_scaler_bound_warning_raised
        self._mappedresponses_upper_scaler_bound_warning_raised: bool = other_coupling._mappedresponses_upper_scaler_bound_warning_raised
        self._couplingvariable_lower_scaler_bound_warning_raised: bool = other_coupling._couplingvariable_lower_scaler_bound_warning_raised
        self._couplingvariable_upper_scaler_bound_warning_raised: bool = other_coupling._couplingvariable_upper_scaler_bound_warning_raised
        self._shareddesignvariables_lower_scaler_bound_warning_raised: bool = other_coupling._shareddesignvariables_lower_scaler_bound_warning_raised
        self._shareddesignvariables_upper_scaler_bound_warning_raised: bool = other_coupling._shareddesignvariables_upper_scaler_bound_warning_raised
        self._targetshareddesignvariables_lower_scaler_bound_warning_raised: bool = other_coupling._targetshareddesignvariables_lower_scaler_bound_warning_raised
        self._targetshareddesignvariables_upper_scaler_bound_warning_raised: bool = other_coupling._targetshareddesignvariables_upper_scaler_bound_warning_raised
