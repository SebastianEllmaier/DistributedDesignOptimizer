# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local middle-level coupling basis module.

This module provides the base class for local-side middle-level coupling
parameters in distributed optimization.
"""

from typing import List
import copy
import numpy as np
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.middlelevel import MiddleLevelCouplingBasis


class SubSysMiddleLevelCouplingBasis(MiddleLevelCouplingBasis):
    
    """
    A LocalMiddleLevelCoupling object holds the coupling parameters between a subsystem and a single neighbor. 
    It stores the identifier of the neighbor and stores the couplingvariables

    The storage is defined as follows:
    Consider two coupled subsystems

                             subsystem 0
                        //                 \\

         mapped response 0 -> 1         expected response 1 -> 0


         expected response 0 -> 1       mapped response 1 -> 0

                        \\                  //
                             subsystem 1

    Consider that the reponses are stored locally for subsystem 0. Then: 
    mapped response 0 -> 1   is called mappedresponses
    expected response 1 -> 0 is called couplingvariable
    and
    expected response 0 -> 1 is called couplingvariable
    mapped response 1 -> 0   is called mappedresponses
    """
    
    def __init__(self, id: str) -> None:
        """Initialize the local middle level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        
        super().__init__(id=id) 
        
        # Variables of MiddleLevel between local subsystems
        self._couplingvariable: List[float] | None = None  # scaled01 values
        self._mappedresponses: List[float] | None = None  # scaled01 values
        self._shareddesignvariable: List[float] | None = None  # scaled01 values
        self._targetshareddesignvariable: List[float] | None = None  # scaled01 values
        
        # Warning flags for out-of-range values (one-time warnings)
        self._couplingvariable_lower_scaler_bound_warning_raised: bool = False
        self._couplingvariable_upper_scaler_bound_warning_raised: bool = False
        self._mappedresponses_lower_scaler_bound_warning_raised: bool = False
        self._mappedresponses_upper_scaler_bound_warning_raised: bool = False
        self._shareddesignvariable_lower_scaler_bound_warning_raised: bool = False
        self._shareddesignvariable_upper_scaler_bound_warning_raised: bool = False
        self._targetshareddesignvariable_lower_scaler_bound_warning_raised: bool = False
        self._targetshareddesignvariable_upper_scaler_bound_warning_raised: bool = False
    
    def set_CouplingVariable(self, couplingvariable: List[float]) -> None:
        """Set the coupling variable values (scaled01).

        Args:
            couplingvariable: Scaled [0,1] coupling variable values.
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
    
    def get_CouplingVariable(self) -> List[float] | None:
        """Get the coupling variable values (scaled01).

        Returns:
            Scaled [0,1] coupling variable values or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._couplingvariable)
    
    def set_MappedResponses(self, varin: List[float]) -> None:
        """Set the mapped response variable values (scaled01).

        Args:
            varin: Scaled [0,1] mapped response values.
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
    
    def get_MappedResponses(self) -> List[float] | None:
        """Get the mapped response variable values (scaled01).

        Returns:
            Scaled [0,1] mapped response values or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponses)
    
    def set_SharedDesignVariable(self, variablesin: List[float]) -> None:
        """Set the shared design variable values (scaled01).

        Args:
            variablesin: Scaled [0,1] shared design variable values.
        """
        sdv_array = np.array(variablesin)
        # Check lower bound
        if not np.all((sdv_array >= 0.0) | np.isclose(sdv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._shareddesignvariable_lower_scaler_bound_warning_raised:
                self._shareddesignvariable_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All shareddesignvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((sdv_array <= 1.0) | np.isclose(sdv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._shareddesignvariable_upper_scaler_bound_warning_raised:
                self._shareddesignvariable_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All shareddesignvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariable = copy.copy(variablesin)
        
    def get_SharedDesignVariable(self) -> List[float] | None:
        """Get the shared design variable values (scaled01).

        Returns:
            Scaled [0,1] shared design variable values or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariable)
        
    def set_TargetSharedDesignVariable(self, variablesin: List[float]) -> None:
        """Set the target shared design variable values (scaled01).

        Args:
            variablesin: Scaled [0,1] target shared design variable values.
        """
        tsdv_array = np.array(variablesin)
        # Check lower bound
        if not np.all((tsdv_array >= 0.0) | np.isclose(tsdv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._targetshareddesignvariable_lower_scaler_bound_warning_raised:
                self._targetshareddesignvariable_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All targetshareddesignvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((tsdv_array <= 1.0) | np.isclose(tsdv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._targetshareddesignvariable_upper_scaler_bound_warning_raised:
                self._targetshareddesignvariable_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All targetshareddesignvariable must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariable = copy.copy(variablesin)
        
    def get_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the target shared design variable values (scaled01).

        Returns:
            Scaled [0,1] target shared design variable values or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._targetshareddesignvariable)
    
    def update_state(self, other_middlelevelcoupling: 'SubSysMiddleLevelCouplingBasis') -> None:
        """Update the state of this SubSysMiddleLevelCouplingBasis from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. This method preserves
        the memory address of the object's attributes while updating their values.

        Args:
            other_middlelevelcoupling: The source instance containing updated values to copy from.
        
        Note on copy operations:
            - Base class attribute (_id): Handled by super().update_state()
            - List[float] attributes: Use update_state_listprimitive() which updates in-place
              to preserve memory address. The getter methods already return copy.copy()
              of the lists, providing the necessary isolation from the source.
        """
        # Base class attribute (_id: str) - handled by parent class
        super().update_state(other_middlelevelcoupling=other_middlelevelcoupling)
        
        self._couplingvariable: List[float] | None = update_state_listprimitive(self._couplingvariable, other_middlelevelcoupling.get_CouplingVariable())
        self._mappedresponses: List[float] | None = update_state_listprimitive(self._mappedresponses, other_middlelevelcoupling.get_MappedResponses())
        self._shareddesignvariable: List[float] | None = update_state_listprimitive(self._shareddesignvariable, other_middlelevelcoupling.get_SharedDesignVariable())
        self._targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._targetshareddesignvariable, other_middlelevelcoupling.get_TargetSharedDesignVariable())
        
        # Warning flags (bool primitives - direct assignment)
        self._couplingvariable_lower_scaler_bound_warning_raised: bool = other_middlelevelcoupling._couplingvariable_lower_scaler_bound_warning_raised
        self._couplingvariable_upper_scaler_bound_warning_raised: bool = other_middlelevelcoupling._couplingvariable_upper_scaler_bound_warning_raised
        self._mappedresponses_lower_scaler_bound_warning_raised: bool = other_middlelevelcoupling._mappedresponses_lower_scaler_bound_warning_raised
        self._mappedresponses_upper_scaler_bound_warning_raised: bool = other_middlelevelcoupling._mappedresponses_upper_scaler_bound_warning_raised
        self._shareddesignvariable_lower_scaler_bound_warning_raised: bool = other_middlelevelcoupling._shareddesignvariable_lower_scaler_bound_warning_raised
        self._shareddesignvariable_upper_scaler_bound_warning_raised: bool = other_middlelevelcoupling._shareddesignvariable_upper_scaler_bound_warning_raised
        self._targetshareddesignvariable_lower_scaler_bound_warning_raised: bool = other_middlelevelcoupling._targetshareddesignvariable_lower_scaler_bound_warning_raised
        self._targetshareddesignvariable_upper_scaler_bound_warning_raised: bool = other_middlelevelcoupling._targetshareddesignvariable_upper_scaler_bound_warning_raised
        