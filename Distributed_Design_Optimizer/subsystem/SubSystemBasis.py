# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Subsystem basis module.

This module provides the base class for all subsystems in the
distributed design optimization framework.
"""

import copy
import os
from collections import deque
from typing import List, Deque, Tuple
import numpy as np
import dill
from scipy.optimize import linprog, OptimizeResult
from scipy.sparse import csc_matrix
from qpsolvers import solve_qp
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis
from Distributed_Design_Optimizer.subsystem.historyentry import SubSystemHistoryEntry
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationInterface
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Local_ConvergenceIndicator_Outerloop_Interface
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import UpdateCouplingParameterMethodInterface
from Distributed_Design_Optimizer.middlelevel import (MiddleLevelCouplingInterface,
                                                      MiddleLevelDataStorageInterface,
                                                      MiddleLevelDataStorageProxy
                                                      )


class SubSystemBasis(SubSystemInterface):
    """A SubSystemBasis object contains a general structure of methods to optimize the subsystem and to couple it to neighboring subsystems."""

    _DDO_PRINT_LABEL_WIDTH: int = 24

    def __init__(self,
                 id: str,
                 neighborid: List[str],
                 ) -> None:
        """Create a new instance of SubSystemBasis with neighbors/controller.

        Args:
            id: Identifier for the subsystem.
            neighborid: Identifiers for the neighbors.
        """

        self._SUBSYSTEMID: str = id

        self._neighborid: List[str] = neighborid

        self._name: str | None = None  # use-case name, set by the Coordinator

        self._historyfolderpath: str | None = None  # historyfiles folder path, set by the Coordinator

        self._optimdata: OptimDataBasis | None = None
        self._couplingparameters: List[CouplingParametersInterface]  # to be initialized in child-class of SubSystemBasis

        self._local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_Interface  # to be initialized in child-class of SubSystemBasis
        self._local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_Interface  # to be initialized in child-class of SubSystemBasis
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface  # to be initialized in child-class of SubSystemBasis
        self._convinnerloop: bool = False
        self._convouterloop: bool = False

        self._middlelevels: List[MiddleLevelDataStorageInterface] = []

        self._outerloop_itr: int | None = None
        self._innerloop_itr: int | None = None

        self._innerloop_itr_runtime: float | None = None
        self._innerloop_itr_numberofdesignvariableevaluations: int | None = None

        self._subsystemhistory: Deque[SubSystemHistoryEntry] = deque()

        # Defined in subclass
        # Local subsystems: Get as input parameters to __init__
        # Controller: Set directly in __init__
        self._optimization: OptimizationInterface

        self._lowerbounds_unscaled: List[float] | None = None  # unscaled values
        self._upperbounds_unscaled: List[float] | None = None  # unscaled values

        self._designvariables: List[float] | None = None  # scaled01 values
        self._designvariables_unscaled: List[float] | None = None  # unscaled values
        self._designvariables_granularity: List[float] | None = None  # 0.0 means continuous

        # Warning flags for out-of-range design variables (one-time warnings)
        self._designvariables_lower_scaler_bound_warning_raised: bool = False
        self._designvariables_upper_scaler_bound_warning_raised: bool = False

        self._coordinationobjectivevalue: float | None = None  # stores the inconsistency value
        self._coordinationequalityconstraintvalue: List[float] | None = None
        self._coordinationinequalityconstraintvalue: List[float] | None = None

        self._totalobjectivevalue: float | None = None  # stores the value after the computation of TotalObjective Class
        self._totalconstrainteqvalue: List[float] | None = None  # stores the equality constraint value after the computation of TotalConstraint class
        self._totalconstraintineqvalue: List[float] | None = None  # stores the inequality constraint value after the computation of TotalConstraint class

########################################################################################################################
#   Basics of the subsystem
########################################################################################################################

    def get_SUBSYSTEMID(self) -> str:
        """Get the identifier of the subsystem.

        Returns:
            The subsystem identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._SUBSYSTEMID

    def get_NeighborId(self) -> List[str]:
        """Get the neighbor IDs.

        Returns:
            List of neighbor identifiers.
        """
        # copy.copy() used - List[str] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._neighborid)

    def set_Name(self, name: str) -> None:
        """Set the use-case name used when saving the subsystem history.

        Args:
            name: The use-case name identifier.
        """
        # No copy needed - str is a primitive/immutable type.
        self._name = name

    def get_Name(self) -> str:
        """Return the use-case name used when saving the subsystem history.

        Returns:
            The use-case name identifier.
        """
        # No copy needed - str is a primitive/immutable type.
        return self._name

    def set_HistoryFolderPath(self, history_folder_path: str) -> None:
        """Set the folder path used when saving the subsystem history.

        Args:
            history_folder_path: The absolute path to the historyfiles folder.
        """
        # No copy needed - str is a primitive/immutable type.
        self._historyfolderpath = history_folder_path

    def get_MiddleLevels(self) -> List[MiddleLevelDataStorageInterface] | List[MiddleLevelDataStorageProxy]:
        """Return the middle-level data storage interfaces.

        Returns:
            List of middle-level data storage interfaces or proxies.
        """
        # No copy - MiddleLevel objects are shared by reference intentionally (coordinator reads/writes same instances)
        return self._middlelevels

    def set_MiddleLevels(self, middlelevels: List[MiddleLevelDataStorageInterface] | List[MiddleLevelDataStorageProxy]) -> None:
        """Set the middle-level data storage interfaces.

        Args:
            middlelevels: List of middle-level data storage interfaces or proxies.
        """
        # No copy - MiddleLevel objects are shared by reference intentionally (coordinator reads/writes same instances)
        self._middlelevels = middlelevels

    def get_OuterLoop_Itr(self) -> int:
        """Return the current outer loop iteration number.

        Returns:
            The current outer loop iteration number.
        """
        return self._outerloop_itr

    def get_InnerLoop_Itr(self) -> int:
        """Return the current inner loop iteration number.

        Returns:
            The current inner loop iteration number.
        """
        return self._innerloop_itr

    def get_InnerLoop_Itr_Runtime(self) -> float | None:
        """Return the inner loop iteration runtime.

        Returns:
            The inner loop iteration runtime.
        """
        return self._innerloop_itr_runtime

    def get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self) -> int | None:
        """Return the number of design variable evaluations.

        Returns:
            The number of design variable evaluations.
        """
        return self._innerloop_itr_numberofdesignvariableevaluations

    def set_OuterLoop_Itr(self, outerloop_itr_in: int) -> None:
        """Set the outer loop iteration number.

        Args:
            outerloop_itr_in: The outer loop iteration number to set.
        """
        self._outerloop_itr = outerloop_itr_in

    def set_InnerLoop_Itr(self, innerloop_itr_in: int) -> None:
        """Set the inner loop iteration number.

        Args:
            innerloop_itr_in: The inner loop iteration number to set.
        """
        self._innerloop_itr = innerloop_itr_in

    def set_InnerLoop_Itr_Runtime(self, innerloop_itr_runtime_in: float) -> None:
        """Set the inner loop iteration runtime.

        Args:
            innerloop_itr_runtime_in: The inner loop iteration runtime to set.
        """
        self._innerloop_itr_runtime = innerloop_itr_runtime_in

    def set_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self, innerloop_itr_numberofdesignvariableevaluations_in: int) -> None:
        """Set the number of design variable evaluations.

        Args:
            innerloop_itr_numberofdesignvariableevaluations_in: The number of design variable evaluations to set.
        """
        self._innerloop_itr_numberofdesignvariableevaluations = innerloop_itr_numberofdesignvariableevaluations_in

    def get_SubsystemHistory(self) -> Deque[SubSystemHistoryEntry]:
        """Return the subsystem history.

        Returns:
            The subsystem history.
        """
        # No copy - returns by reference intentionally (history is only read externally for postprocessing)
        return self._subsystemhistory

    def CopyToMiddleLevel(self) -> None:
        """Copy coupling parameters to the shared middle-level data storage.

        For each MiddleLevelDataStorage, determines which neighbor it
        connects to, finds the matching local CouplingParameter, and
        writes it to shared storage (lock-safe via set_Coupling).
        """
        idsubsystem: str = self.get_SUBSYSTEMID()

        for ml in self.get_MiddleLevels():
            id_ml: List[str] = ml.get_ID()
            # Determine neighbor ID (the one that isn't this subsystem)
            if id_ml[0] == idsubsystem:
                neighbor_id = id_ml[1]
            elif id_ml[1] == idsubsystem:
                neighbor_id = id_ml[0]
            else:
                continue
            # Find the matching coupling parameter and write it
            for cp in self._couplingparameters:
                if cp.get_ID() == neighbor_id:
                    ml.set_Coupling(cp)  # lock acquired inside
                    break

    def CopyFromMiddleLevel(self) -> None:
        """Copy coupling data from the shared middle-level data storage.

        For each MiddleLevelDataStorage, determines which neighbor it
        connects to, retrieves the stored coupling data, and applies it
        to the matching local CouplingParameter.

        NOTE ON ASYMMETRY WITH CopyToMiddleLevel:
            CopyToMiddleLevel passes the CouplingParameter directly to
            ml.set_Coupling(cp), which internally calls
            cp.CopyToMiddleLevelCoupling(slot) — the data flows from the
            caller's object INTO shared storage via argument.

            CopyFromMiddleLevel cannot mirror this pattern because of
            multiprocessing proxies: arguments sent through a BaseProxy
            are pickled to the manager process. Mutations of the argument
            inside the manager are applied to a deserialized copy and
            discarded — the caller's original is never modified. Only
            return values travel back across process boundaries.

            Therefore we use get_StoredCoupling(neighbor_id) which RETURNS
            the data, then apply it locally via
            cp.CopyFromMiddleLevelCoupling(storedcoupling).
        """
        idsubsystem: str = self.get_SUBSYSTEMID()

        for ml in self.get_MiddleLevels():
            id_ml: List[str] = ml.get_ID()
            # Determine neighbor ID (the one that isn't this subsystem)
            if id_ml[0] == idsubsystem:
                neighbor_id = id_ml[1]
            elif id_ml[1] == idsubsystem:
                neighbor_id = id_ml[0]
            else:
                continue
            # Retrieve stored data and apply locally
            storedcoupling: MiddleLevelCouplingInterface = ml.get_StoredCoupling(neighbor_id)
            self.CopyFromMiddleLevelCoupling(neighbor_id, storedcoupling)

    def run_innerloop_job(self) -> None:
        """Execute the inner loop job: copy from middle level, optimize, copy back."""
        self.CopyFromMiddleLevel()
        self.prepare_OptimizationProblem()
        self.run_IterativeOptimization()
        self.postprocess_Optimization()
        self.CopyToMiddleLevel()

    def run_updateCouplingParameters_innerLoop_job(self) -> None:
        """Update coupling parameters in the inner loop after optimization."""
        self.set_DesignVariables(self.get_OptimData().get_DesignVariables())
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
        self.CopyFromMiddleLevel()
        self.updateCouplingParameters_innerLoop()
        self.CopyToMiddleLevel()

    def savesubsystemhistory(self) -> None:
        """Save the subsystem history to a dill file.

        The use-case name is read from the subsystem's own state (set via
        set_Name by the Coordinator). The target folder is the use-case's
        historyfiles folder (stored as self._historyfolderpath via
        set_HistoryFolderPath by the Coordinator).
        """
        filename: str = f"historyfile_{self.get_Name()}_subsystem_{self.get_SUBSYSTEMID()}.dill"

        # Create the folder if it doesn't exist
        os.makedirs(self._historyfolderpath, exist_ok=True)
        history_file_path: str = os.path.join(self._historyfolderpath, filename)

        # Serialize the object to a binary format
        with open(history_file_path, 'wb') as file:
            dill.dump(self._subsystemhistory, file)

    def set_LowerBounds_Unscaled(self, lowerbounds: List[float]) -> None:
        """Set the lower bounds for the design variables (unscaled values).

        Args:
            lowerbounds: Lower bound values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._lowerbounds_unscaled = copy.copy(lowerbounds)

    def get_LowerBounds_Unscaled(self) -> List[float] | None:
        """Get the lower bounds of the design variables.

        Returns:
            Lower bound values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._lowerbounds_unscaled)

    def set_UpperBounds_Unscaled(self, upperbounds: List[float]) -> None:
        """Set the upper bounds of the design variables (unscaled values).

        Args:
            upperbounds: Upper bound values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._upperbounds_unscaled = copy.copy(upperbounds)

    def get_UpperBounds_Unscaled(self) -> List[float] | None:
        """Get the upper bounds of the design variables.

        Returns:
            Upper bound values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._upperbounds_unscaled)

    def updateSubsystemfromOptimdata(self, optimdata: OptimDataBasis) -> None:
        """Update subsystem state from optimization data.

        Updates the subsystem's design variables, objective values, and
        constraint values from the provided optimization data.

        Args:
            optimdata: Optimization data containing updated values.
        """
        # update design variables
        if optimdata.get_DesignVariables() is not None:
            self.set_DesignVariables(optimdata.get_DesignVariables())

        # update the total objective function value
        if optimdata.get_TotalObjectiveValue() is not None:
            self.set_TotalObjectiveValue(optimdata.get_TotalObjectiveValue())

        # update the total equality constraint function value
        if optimdata.get_TotalConstraintEqValue() is not None:
            self.set_TotalConstraintEqValue(optimdata.get_TotalConstraintEqValue())

        # update the total inequality constraint function value
        if optimdata.get_TotalConstraintIneqValue() is not None:
            self.set_TotalConstraintIneqValue(optimdata.get_TotalConstraintIneqValue())

        # update the objective inconsistency value
        if optimdata.get_CoordinationObjectiveValue() is not None:
            self.set_CoordinationObjectiveValue(optimdata.get_CoordinationObjectiveValue())

        # update the constraint inconsistency value
        if optimdata.get_CoordinationEqualityConstraintValue() is not None:
            self.set_CoordinationEqualityConstraintValue(optimdata.get_CoordinationEqualityConstraintValue())

        # update the coordination inequality constraint value
        if optimdata.get_CoordinationInequalityConstraintValue() is not None:
            self.set_CoordinationInequalityConstraintValue(optimdata.get_CoordinationInequalityConstraintValue())

        # update the history of the optimization
        self.set_OptimData(optimdata)

        # update the coupling information to neighbors
        self.mapToCouplingParameters()

    def updateOptimdatafromSubsystem(self) -> None:
        """Update self._optimdata from the current subsystem information.

        Raises:
            ValueError: If design variables are incompatible with optimdata.
            ValueError: If design variables (unscaled) are incompatible with optimdata.
            ValueError: If total objective value is incompatible with optimdata.
            ValueError: If total equality constraint values are incompatible with optimdata.
            ValueError: If total inequality constraint values are incompatible with optimdata.
            ValueError: If coordination objective value is incompatible with optimdata.
            ValueError: If coordination equality constraint values are incompatible with optimdata.
            ValueError: If lower bounds are incompatible with optimdata.
            ValueError: If upper bounds are incompatible with optimdata.
        """

        if self.get_DesignVariables() is not None:
            self._optimdata.set_DesignVariables(self.get_DesignVariables())

        if self.get_DesignVariables_Unscaled() is not None:
            self._optimdata.set_DesignVariables_Unscaled(self.get_DesignVariables_Unscaled())

        # update the total objective function value
        if self.get_TotalObjectiveValue() is not None:
            self._optimdata.set_TotalObjectiveValue(self.get_TotalObjectiveValue())

        # update the total equality constraint function value
        if self.get_TotalConstraintEqValue() is not None:
            self._optimdata.set_TotalConstraintEqValue(self.get_TotalConstraintEqValue())

        # update the total inequality constraint function value
        if self.get_TotalConstraintIneqValue() is not None:
            self._optimdata.set_TotalConstraintIneqValue(self.get_TotalConstraintIneqValue())

            # Compute number of active inequality constraints
            numberofactiveinequalityconstraints: int = int(np.sum(np.isclose(np.array(self.get_TotalConstraintIneqValue()), 0.0, atol=1e-8)))
            self._optimdata.set_NumberofActiveInequalityConstraints(numberofactiveinequalityconstraints)

        # update the objective inconsistency value
        if self.get_CoordinationObjectiveValue() is not None:
            self._optimdata.set_CoordinationObjectiveValue(self.get_CoordinationObjectiveValue())

        # update the constraint inconsistency value
        if self.get_CoordinationEqualityConstraintValue() is not None:
            self._optimdata.set_CoordinationEqualityConstraintValue(self.get_CoordinationEqualityConstraintValue())

        # update the coordination inequality constraint value
        if self.get_CoordinationInequalityConstraintValue() is not None:
            self._optimdata.set_CoordinationInequalityConstraintValue(self.get_CoordinationInequalityConstraintValue())

    
########################################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
########################################################################################################################
    # TODO: Uncomment after modularisation via checkDesignVariables -> see MS Teams task
    # def set_DesignVariables(self, designvariables: List[float]) -> None:
    #     """Set the scaled design variables.

    #     Args:
    #         designvariables: Scaled design variable values in [0, 1].
    #     """
    #     dv_array = np.array(designvariables)
    #     # Check lower bound
    #     if not np.all((dv_array >= 0.0) | np.isclose(dv_array, 0.0, atol=1e-8, rtol=0)):
    #         if not self._designvariables_lower_scaler_bound_warning_raised:
    #             self._designvariables_lower_scaler_bound_warning_raised = True
    #             ddo_print("WARNING: All design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
    #     # Check upper bound
    #     if not np.all((dv_array <= 1.0) | np.isclose(dv_array, 1.0, atol=1e-8, rtol=0)):
    #         if not self._designvariables_upper_scaler_bound_warning_raised:
    #             self._designvariables_upper_scaler_bound_warning_raised = True
    #             ddo_print("WARNING: All design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
    #     if len(designvariables) != len(self._designvariables_granularity):
    #         raise ValueError(f"{DDO_Color}Length of Design Variables doesn't match with Length of DesignVariables Granularity{Reset}")
    #     # Check whether the to-be-set designvariables fit with the specified granularity
    #     if self._designvariables_granularity is not None:
    #         for i in range(len(designvariables)):
    #             if self._designvariables_granularity[i] == 0.0:
    #                 # 0.0 means continuous - no granularity check needed
    #                 pass
    #             elif self._designvariables_granularity[i] > 0.0:
    #                 # Check if design variable is a multiple of the granularity using modulo
    #                 remainder = np.mod(designvariables[i], self._designvariables_granularity[i])
    #                 if np.isclose(remainder, 0.0) or np.isclose(remainder, self._designvariables_granularity[i]):
    #                     pass
    #                 else:
    #                     raise ValueError(f"{DDO_Color}Design variable at index {i} with value {designvariables[i]} does not match the required granularity of {self._designvariables_granularity[i]}{Reset}")
    #             else:
    #                 raise ValueError(f"{DDO_Color}Invalid granularity value at index {i}: {self._designvariables_granularity[i]}. Must be >= 0.0{Reset}")
    #     else:
    #         raise ValueError(f"{DDO_Color}DesignVariable Granularity must be defined before setting any design variables{Reset}")
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     self._designvariables = copy.copy(designvariables)  # scaled01 values

    #     # No additional copy.copy() needed as list comprehension already creates new list object
    #     designvariables_unscaled = [self.get_Scalers()[i].inverse_transform(designvariables[i]) for i in range(len(designvariables))]
    #     # Check unscaled design variables against bounds
    #     if self._lowerbounds_unscaled is not None:
    #         dv_unscaled_array = np.array(designvariables_unscaled)
    #         lb_array = np.array(self._lowerbounds_unscaled)
    #         if not np.all((dv_unscaled_array >= lb_array) | np.isclose(dv_unscaled_array, lb_array, atol=1e-8, rtol=0)):
    #             violating_indices = np.where(~((dv_unscaled_array >= lb_array) | np.isclose(dv_unscaled_array, lb_array, atol=1e-8, rtol=0)))[0]
    #             raise ValueError(f"{DDO_Color}Unscaled design variables at indices {violating_indices.tolist()} are below their lower bounds (with tolerance 1e-8){Reset}")
    #     else:
    #         raise ValueError(f"{DDO_Color}Lower bounds must be defined before setting any design variables{Reset}")
    #     if self._upperbounds_unscaled is not None:
    #         dv_unscaled_array = np.array(designvariables_unscaled)
    #         ub_array = np.array(self._upperbounds_unscaled)
    #         if not np.all((dv_unscaled_array <= ub_array) | np.isclose(dv_unscaled_array, ub_array, atol=1e-8, rtol=0)):
    #             violating_indices = np.where(~((dv_unscaled_array <= ub_array) | np.isclose(dv_unscaled_array, ub_array, atol=1e-8, rtol=0)))[0]
    #             raise ValueError(f"{DDO_Color}Unscaled design variables at indices {violating_indices.tolist()} exceed their upper bounds (with tolerance 1e-8){Reset}")
    #     else:
    #         raise ValueError(f"{DDO_Color}Upper bounds must be defined before setting any design variables{Reset}")
    #     self._designvariables_unscaled = designvariables_unscaled

    def get_DesignVariables(self) -> List[float] | None:
        """Get the scaled design variables.

        Returns:
            Scaled design variable values in [0, 1].
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._designvariables)

    def get_DesignVariables_Unscaled(self) -> List[float] | None:
        """Get the unscaled design variables.

        Returns:
            Unscaled design variable values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._designvariables_unscaled)

    def set_DesignVariables_Granularity(self, designvariables_granularity: List[float]) -> None:
        """Set the granularity of the design variables.

        Args:
            designvariables_granularity: Granularity values where 0.0 means continuous.
        """
        for i in range(len(designvariables_granularity)):
            if designvariables_granularity[i] < 0.0:
                raise ValueError(f"{DDO_Color}Element at index {i} in DesignVariables Granularity must be >= 0.0 (0.0 means continuous){Reset}")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._designvariables_granularity = copy.copy(designvariables_granularity)

    def get_DesignVariables_Granularity(self) -> List[float] | None:
        """Get the granularity of the design variables.

        Returns:
            Granularity values where 0.0 means continuous.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._designvariables_granularity)

########################################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
########################################################################################################################

    def set_TotalObjectiveValue(self, totalobjectivevalue: float | None) -> None:
        """Store the total objective value after the computation of the TotalObjective Class.

        Args:
            totalobjectivevalue: The total objective value to store.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._totalobjectivevalue = totalobjectivevalue

    def get_TotalObjectiveValue(self) -> float | None:
        """Return the total objective value after the computation of the TotalObjective Class.

        Returns:
            The total objective value, or None if not yet computed.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._totalobjectivevalue

    def set_CoordinationObjectiveValue(self, coordinationobjectivevalue: float | None) -> None:
        """Store the objective inconsistency results.

        Args:
            coordinationobjectivevalue: The coordination objective value to store.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._coordinationobjectivevalue = coordinationobjectivevalue

    def get_CoordinationObjectiveValue(self) -> float | None:
        """Get the objective inconsistency function value.

        Returns:
            The coordination objective value, or None if not yet computed.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._coordinationobjectivevalue

    def set_TotalConstraintEqValue(self, ceq: List[float] | None) -> None:
        """Store the equality constraint value after the computation of the TotalConstraint Class.

        Args:
            ceq: The equality constraint values to store.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._totalconstrainteqvalue = copy.copy(ceq) if ceq is not None else None

    def get_TotalConstraintEqValue(self) -> List[float] | None:
        """Return the equality constraint value after the computation of the TotalConstraint Class.

        Returns:
            The equality constraint values, or None if not yet computed.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._totalconstrainteqvalue)

    def set_TotalConstraintIneqValue(self, cineq: List[float] | None) -> None:
        """Store the inequality constraint value after the computation of the TotalConstraint Class.

        Args:
            cineq: The inequality constraint values to store.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._totalconstraintineqvalue = copy.copy(cineq) if cineq is not None else None

    def get_TotalConstraintIneqValue(self) -> List[float] | None:
        """Return the inequality constraint value after the computation of the TotalConstraint Class.

        Returns:
            The inequality constraint values, or None if not yet computed.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._totalconstraintineqvalue)

    def set_CoordinationEqualityConstraintValue(self, coordinationequalityconstraintvalue: List[float] | None) -> None:
        """Store the constraint inconsistency results.

        Args:
            coordinationequalityconstraintvalue: The coordination equality constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._coordinationequalityconstraintvalue = copy.copy(coordinationequalityconstraintvalue)

    def get_CoordinationEqualityConstraintValue(self) -> List[float] | None:
        """Get the constraint inconsistency function value.

        Returns:
            The coordination equality constraint values, or None if not yet computed.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._coordinationequalityconstraintvalue)

    def set_CoordinationInequalityConstraintValue(self, coordinationinequalityconstraintvalue: List[float] | None) -> None:
        """Store the coordination inequality constraint results.

        Args:
            coordinationinequalityconstraintvalue: The coordination inequality constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._coordinationinequalityconstraintvalue = copy.copy(coordinationinequalityconstraintvalue)

    def get_CoordinationInequalityConstraintValue(self) -> List[float] | None:
        """Get the coordination inequality constraint function value.

        Returns:
            The coordination inequality constraint values, or None if not yet computed.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._coordinationinequalityconstraintvalue)

########################################################################################################################
#   Functions to obtain past values from self._subsystemhistory
########################################################################################################################

    def copy_Coupling_Past_outerloop_itr(self, outerloop_itr_before: int) -> List[CouplingParametersInterface]:
        """Copy the coupling from a past outer loop iteration.

        Args:
            outerloop_itr_before: Number of iterations to go back.

        Returns:
            List of coupling parameters from the specified past iteration.
        """
        previous_itr = self._outerloop_itr - outerloop_itr_before
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: List[CouplingParametersInterface] = result_optimdata.get_CouplingParameters()
                else:
                    result = None
                found_result = True
                break
        if not found_result:
            # There exist no List of CouplingParametersInterface with fitting self._outerloop_itr, so just return a List of initialized CouplingParametersInterface
            # result = CreateCouplingParameters.createCouplingParameters(self._subsystem)
            result = self.return_initialized_CouplingParameters()

        return result

    def copy_Coupling_Previous_outerloop_itr(self) -> List[CouplingParametersInterface]:
        """Copy the coupling from the previous outer loop iteration.

        Returns:
            List of coupling parameters from the previous iteration.
        """
        return self.copy_Coupling_Past_outerloop_itr(outerloop_itr_before=1)

    def copy_TotalObjective_Previous_outer_or_innerloop_itr(self) -> float | None:
        """Copy the total objective from a previous iteration.

        Returns:
            Total objective value from the previous iteration, or None if not found.
        """
        found_result = False
        # Search the self._subsystemhistory backwards for the most recent iteration strictly before the current one
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if (self._subsystemhistory[i].get_OuterLoop_Itr() < self._outerloop_itr) or (self._subsystemhistory[i].get_OuterLoop_Itr() == self._outerloop_itr and self._subsystemhistory[i].get_InnerLoop_Itr() < self._innerloop_itr):
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: float = result_optimdata.get_TotalObjectiveValue()
                else:
                    result = None
                found_result = True
                break
        if not found_result:
            # There exist no OptimDataBasis._totalobjectivevalue with fitting self._outerloop_itr or self._innerloop_itr, so just return a None
            result = None

        return result

    def copy_DesignVariablesUnscaled_Previous_outerloop_itr(self) -> List[float] | None:
        """Copy the unscaled design variables from the previous outer loop iteration.

        Returns:
            Unscaled design variables from the previous iteration, or None if not found.
        """
        previous_itr = self._outerloop_itr - 1
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: List[float] = result_optimdata.get_DesignVariables_Unscaled()
                else:
                    result = None
                found_result = True
                break
        if not found_result:
            # There exist no OptimDataBasis._totalobjectivevalue with fitting self._outerloop_itr or self._innerloop_itr, so just return a None
            result = None

        return result

    def copy_DesignVariables_Previous_outerloop_itr(self) -> List[float] | None:
        """Copy the scaled design variables from the previous outer loop iteration.

        Returns:
            Scaled design variables from the previous iteration, or None if not found.
        """
        previous_itr = self._outerloop_itr - 1
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: List[float] = result_optimdata.get_DesignVariables()
                else:
                    result = None
                found_result = True
                break
        if not found_result:
            # There exist no OptimDataBasis._totalobjectivevalue with fitting self._outerloop_itr or self._innerloop_itr, so just return a None
            result = None

        return result

    def copy_DesignVariables_Previous_innerloop_itr(self) -> List[float] | None:
        """Copy the scaled design variables from the previous inner loop iteration.

        Returns:
            Scaled design variables from the previous inner iteration, or None if not found.
        """
        previous_inner_itr = self._innerloop_itr - 1
        found_result = False

        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            history_entry = self._subsystemhistory[i]
            # Match same outer loop but previous inner loop
            if (history_entry.get_OuterLoop_Itr() == self._outerloop_itr and
                    history_entry.get_InnerLoop_Itr() == previous_inner_itr):
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: List[float] = result_optimdata.get_DesignVariables()
                else:
                    result = None
                found_result = True
                break

        if found_result is False:
            result = None

        return result

    def copy_DesignVariablesUnscaled_Previous_innerloop_itr(self) -> List[float] | None:
        """Copy the unscaled design variables from the previous inner loop iteration.

        Returns:
            Unscaled design variables from the previous inner iteration, or None if not found.
        """
        previous_inner_itr = self._innerloop_itr - 1
        found_result = False

        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            history_entry = self._subsystemhistory[i]
            # Match same outer loop but previous inner loop
            if (history_entry.get_OuterLoop_Itr() == self._outerloop_itr and
                    history_entry.get_InnerLoop_Itr() == previous_inner_itr):
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                result_optimdata: OptimDataBasis | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: List[float] = result_optimdata.get_DesignVariables_Unscaled()
                else:
                    result = None
                found_result = True
                break

        if found_result is False:
            result = None

        return result

########################################################################################################################
#   Functions to prepare, solve and postprocess a subsystem's optimization problem
########################################################################################################################

    def run_IterativeOptimization(self) -> None:
        """Execute the local optimization of the subsystem."""
        optimdata = self._optimization.callOptimizer(self)
        self.updateSubsystemfromOptimdata(optimdata=optimdata)

    def set_OptimData(self, optimdataIn: OptimDataBasis) -> None:
        """Store the information from the optimization run.

        Args:
            optimdataIn: The optimization data to store.
        """
        # No copy.copy() used - OptimDataBasis is a class object assigned by reference intentionally.
        # This allows the caller to continue interacting with the actual object.
        # If isolation is needed, the caller should explicitly copy.
        self._optimdata = optimdataIn

    def get_OptimData(self) -> OptimDataBasis:
        """Get information from the last optimization run.

        Returns:
            The optimization data, or None if not set.
        """
        # No copy.copy() used - OptimDataBasis is a class object returned by reference intentionally.
        # This allows the caller to interact with the actual object. If isolation is needed,
        # the caller should explicitly copy.
        return self._optimdata

    def get_Local_ConvergenceIndicator_Innerloop(self) -> Local_ConvergenceIndicator_Innerloop_Interface:
        """Get the local convergence indicator for the inner loop.

        Returns:
            The local inner loop convergence indicator.
        """
        return self._local_convergenceindicator_innerloop

    def get_Local_ConvergenceIndicator_Outerloop(self) -> Local_ConvergenceIndicator_Outerloop_Interface:
        """Get the local convergence indicator for the outer loop.

        Returns:
            The local outer loop convergence indicator.
        """
        return self._local_convergenceindicator_outerloop

    def evaluate_InnerLoopConvergenceIndicator(self) -> None:
        """Evaluate the inner loop convergence indicator.

        The local convergence indicator retrieves the data it needs from self.
        This allows different convergence criteria to access different data
        (e.g., total objective, primal/dual residuals, etc.).
        """
        self._convinnerloop: bool = self._local_convergenceindicator_innerloop.evaluate(self)

    def get_ConvInnerLoop(self) -> bool:
        """Check if the subsystem is locally converged in the inner loop.

        Returns:
            True if converged, False otherwise.
        """
        # No copy.copy() needed - bool is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._convinnerloop

    def evaluate_OuterLoopConvergenceIndicator(self) -> None:
        """Evaluate the outer loop convergence indicator.

        Same design rationale as evaluate_InnerLoopConvergenceIndicator:
        the local convergence indicator retrieves the data it needs from self.
        """
        self._convouterloop: bool = self._local_convergenceindicator_outerloop.evaluate(self)

    def get_ConvOuterLoop(self) -> bool:
        """Get the outer loop convergence indicator.

        Returns:
            True if converged, False otherwise.
        """
        # No copy.copy() needed - bool is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._convouterloop

########################################################################################################################
#   Functions to handle and update coupling parameters related to modelling a distributed optimization problem.
#   The details depend on the type of system: Local subsystem or controller.
#   Nothing related to coordination parameters
########################################################################################################################

    def CopyFromMiddleLevelCoupling(self, idIn: str, couplingIn: MiddleLevelCouplingInterface) -> None:
        """Apply stored middle-level coupling data to the matching local CouplingParameter.

        Args:
            idIn: Identifier of the neighbor subsystem.
            couplingIn: The MiddleLevelCouplingInterface data retrieved from storage.
        """
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == idIn:
                couplingparameter.CopyFromMiddleLevelCoupling(couplingIn)
                break

    def get_CouplingParameters(self) -> List[CouplingParametersInterface]:
        """Get the coupling parameters.

        Returns:
            List of coupling parameters for all neighbors.
        """
        # copy.copy() used - List[CouplingParametersInterface] is a list of class objects.
        # The list container is copied to prevent modifications to the list structure,
        # but the objects themselves are returned by reference intentionally.
        return copy.copy(self._couplingparameters)

    def get_CouplingParameter_with_ID(self, id: str) -> CouplingParametersInterface:
        """Return the coupling parameter from self._couplingparameters with the provided ID.

        Args:
            id: Identifier of the neighbor subsystem.

        Raises:
            ValueError: If no coupling parameter with the given ID exists.

        Returns:
            The coupling parameter matching the provided ID.
        """

        # Get all couplingparamters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Iterate over all coupling parameters
        for couplingparameter in couplingparameters:

            # Check if the coupling parameter has the provided ID
            if couplingparameter.get_ID() == id:

                # No copy.copy() used - CouplingParametersInterface is a class object returned by reference intentionally.
                # This allows the caller to interact with the actual object. If isolation is needed,
                # the caller should explicitly copy.
                # Return the corresponding coupling parameter
                return couplingparameter

        # If the coupling parameter with the provided ID could not be found
        raise ValueError(f"{DDO_Color}There does not exist a coupling parameters w.r.t subsystem {id}.{Reset}")

########################################################################################################################
#   Compute local KKT multipliers
########################################################################################################################

    def compute_KKT_multipliers(self) -> None:
        """If a coordination method needs multipliers of local constraints (incl. bound constraints), but the used solver does not provide such, then a globally defined procedure is called to set them in the OptimDataBasis object.

        The KKT multipliers are computed with respect to the current state
        of the subsystem, i.e. based on the Jacobians/gradients and design
        variable values currently stored in self._optimdata; updates of these 
        quantities have to be done separately.
        Therefore, before calling this method, one should typically call
        evaluateAllJacobians() and updateSubsystemfromOptimdata()
        to ensure that the subsystem state and the stored Jacobians/gradients
        are consistent and up to date.
        """
        
        # Computation of KKT multipliers of local constraints
        # including bound constraints by using current optimal data
        # and update optimdata

        # Primal dimension
        primal_dimension = len(self.get_DesignVariables())

        # Get the matrix of the KKT system
        result: List[List[List[float]] | List[Tuple[float | None, float | None]]] = self.compute_KKT_system_matrix_and_bounds()

        # Get the KKT system matrix of linear KKT system
        # If no constraints exist, constraint_matrix is an empty List
        constraint_matrix: List[List[float]] = result[0]

        # If there exist no constraints, use a vector of zeros in KKT system
        if len(constraint_matrix) == 0:

            # Use a zeros vector
            constraint_matrix = [0.0] * primal_dimension


        # Get the bounds on dual multipliers w.r.t. non-coupling, local constraints
        # Nonnegativity of KKT multipliers for active inequality constraints / bounds
        # Zero else
        bounds: List[Tuple[float | None, float | None]] = result[1]

        # Get the dimension of the dual KKT system multipliers
        # I.e., number of columns of the KKT system
        dual_dimension: int = len(constraint_matrix)

        # Transpose the KKT system matrix
        constraint_matrix: np.typing.ArrayLike = np.array(constraint_matrix).T

        # Initialize the right hand side of the KKT system (- gradient of total objective)
        b: List[float] = [0.0] * primal_dimension

        # Get the gradient of total objective
        gradient_totalobjective: List[float] | None = self._optimdata.get_Gradient_TotalObjective()

        # If the total objective exists, i.e. gradient_totalobjective is not None,
        # set b to the negative gradient of the total objective
        # else, let it be the zeros vector
        if gradient_totalobjective is not None:

            # Flip the sign to get the right side of the KKT system
            b: List[float] = [- gradient_totalobjective[i] for i in range(len(gradient_totalobjective))]

        # Define a constraint satisfaction problem by defining a
        # LP with cost = 0.0
        c: List[float] = [0.0] * dual_dimension

        # Initialize List for all multipliers
        all_multipliers: List[float] | None = None

        # Solve the KKT system linear system of equations and inequalities
        optimization_result: OptimizeResult = linprog(c=c, A_eq=constraint_matrix, b_eq=b, bounds=bounds)
        # Check if a solution could be found by scip.optimize

        # Success (status = 0)
        if optimization_result.status == 0:

            # Since the computation was successfull
            # Continue out of the status handling
            all_multipliers = optimization_result.x.tolist()

        # Iteration limit is hit
        elif optimization_result.status == 1:

            # Raise an error indicating to increase the number of iterations
            raise ValueError(f"{DDO_Color}The solver failed to find a solution with the status code {optimization_result.status}. The reason is: "
                             f"{optimization_result.message}. You should manually increase the iteration count limit as a parameter of "
                             f"scipy.optimize.linprog{Reset}")

        # Infeasible KKT system
        elif optimization_result.status == 2:

            # Raise a warning explaining that the KKT system is unsolveable,
            # as either the solution provided to the primal subsystem
            # is not optimal, or the problem is nonsmooth such that no multipliers
            # exist
            # Bilevel Mitigation: Compute approximate KKT multipliers that tries to minimize KKT system violation

            # no 'raise Warning', since it would terminate the code instantly;
            # this warning should only inform the user, hence print in Terminal
            ddo_print(f"WARNING: "
                  f"The solver failed to find a solution with the status code {optimization_result.status}. The reason is: "
                  f"{optimization_result.message}. This means that either the solution you provided to the primal subproblem "
                  f"of the subsystem with ID {self.get_SUBSYSTEMID()} is not optimal, or the problem does not satisfy constraint qualifications "
                  f"such that the KKT condition does not hold for any solution. "
                  f"Please check the problem function and the primal solutions. For now, we use the multipliers that minimize "
                  f"the violation of the KKT-system while satisfying nonnegativity of multipliers corresponding to active constraints "
                  f"or bounds.")

            # Compute approximate 'multipliers' that minimize the violation of the KKT-system
            # in the squared l2-norm using the package 'qpsolvers' and the solver 'clarabel'
            all_multipliers = self.compute_ApproximateKKT_multipliers(constraint_matrix, b, bounds)

        # "Unbounded" problem
        elif optimization_result.status == 3:

            # This case should never be attained, since our cost function is the zeros-vector
            # Hence, the cost function is always zero

            raise ValueError(f"{DDO_Color}The solver failed to find a solution with the status code {optimization_result.status}. The reason is: "
                             f"{optimization_result.message}. This case can never occur in our use of scipy.optimize.linprog, "
                             f"hence please check the gradients and Jacobians you provide.{Reset}")

        # If the status code differs for some reason:
        else:

            # Raise an error
            raise ValueError(f"{DDO_Color}The solver failed to find a solution with the unknown status code {optimization_result.status}. The reason is: "
                             f"{optimization_result.message}.{Reset}")

        # If the solution could be found successfully, decompose the raw accumulation
        # of all multipliers into the parts from their semantic mapping (e.g. local
        # inequality constraints)

        self.decompose_KKT_multipliers(all_multipliers)


    def compute_ApproximateKKT_multipliers(self, matrix_KKT_system: np.typing.ArrayLike, negative_gradient_totalobjective: List[float],
                                           bounds: List[Tuple[float | None, float | None]]) -> List[float]:
        """Compute approximate KKT multipliers when the solver does not provide them.

        If a coordination method needs multipliers
        of local constraints (incl. bound constraints),
        but the used solver does not provide such, then
        a globally defined procedure is called to set them
        in the OptimDataBasis object.

        This function should only be called if the solver
        does not obtain a solution for the exact KKT-system;
        then, as a mitigation for algorithms that need multipliers
        to work, we compute the 'multipliers' that minimize the
        violation of the KKT system w.r.t. the squared l2-error.

        Args:
            matrix_KKT_system: The KKT system matrix.
            negative_gradient_totalobjective: Negative gradient of the total objective.
            bounds: List of (lower, upper) bound tuples for each dual variable.

        Returns:
            The computed approximate KKT multipliers as a list.
        """

        # KKT-matrix has zero-columns for inactive inequality constraints / bounds
        # -> Hence, can disregard the multipliers

        # Bring the minimization of the squared l2-norm of the KKT system
        # into standard QP form of 'qpsolvers' packages
        # Please refer to the form description: https://qpsolvers.github.io/qpsolvers/index.html

        # Numpy does matrix-vector-multiplications in a correct way already internally
        P_qpmatrix_helper: np.typing.ArrayLike = 2 * matrix_KKT_system.T @ matrix_KKT_system
        P_qpmatrix: np.typing.ArrayLike = 0.5 * (P_qpmatrix_helper.T + P_qpmatrix_helper)
        q_qpmatrix: np.typing.ArrayLike = -2 * matrix_KKT_system.T @ negative_gradient_totalobjective

        # Infer lower bounds arrays encoding from input bounds
        # For each (dual variable) component, the corresponding bounds are
        # either (None, None) or (0.0, None)
        lowerbounds: np.typing.ArrayLike = np.array([0.0] * len(bounds))

        # Loop over every bounds from input and encode nonnegativity of multipliers w.r.t.
        # active constraints via lowerbound entry 0.0
        for i in range(len(bounds)):

            # If there is a lower bounds
            if bounds[i][0] == 0.0:

                # Insert the same lower bound to variable lowerbounds
                lowerbounds[i] = 0.0

            # If there is no lower bound
            else:

                # Insert -np.inf as lower bound (see reference for usage: https://qpsolvers.github.io/qpsolvers/quadratic-programming.html)
                lowerbounds[i] = -np.inf

        # Use solver 'clarabel' from 'qpsolvers'
        P_csc = csc_matrix(P_qpmatrix)
        multipliers: np.typing.ArrayLike = solve_qp(P=P_csc, q=q_qpmatrix, lb=lowerbounds, solver="clarabel")

        # Transform the multipliers into an accumulated list
        return multipliers.tolist()

    def check_MultipliersNotSet(self) -> bool:
        """Return True if any existing constraint is missing its corresponding multiplier in optimdata.

        Returns:
            True if at least one constraint has no corresponding multiplier set.
        """
        # Get optimdata
        # Check if in self._optimdatabasis, multipliers are set; else, execute compute_KKT_system
        # compute_KKT_multipliers is defined in SubSystemBasis.py
        optimdata: OptimDataBasis = self.get_OptimData()

        # TODO: Also include coordination inequality constraints, after they are included in SubSystemBasis
        return (self.get_LowerBounds_Unscaled() is not None and optimdata.get_Multipliers_LowerBounds() is None) or \
            (self.get_UpperBounds_Unscaled() is not None and optimdata.get_Multipliers_UpperBounds() is None) or \
            (self.get_InequalityLocalConstraintsValue() is not None and optimdata.get_Multipliers_Local_Inequality_Constraints() is None) or \
            (self.get_EqualityLocalConstraintsValue() is not None and optimdata.get_Multipliers_Local_Equality_Constraints() is None) or \
            (self.get_CoordinationEqualityConstraintValue() is not None and optimdata.get_Multipliers_Coordination_Equality_Constraints() is None)


########################################################################################################################
#   Print methods for terminal output
########################################################################################################################

    def _print_subsystem_header(self) -> None:
        """Print the subsystem results header with ID and iteration info."""
        ddo_print(f"   SubSystem {self.get_SUBSYSTEMID()}:")
        ddo_print(f"       {'Outerloop Iteration:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_OuterLoop_Itr()}")
        ddo_print(f"       {'Innerloop Iteration:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_InnerLoop_Itr()}")

########################################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################################
    def update_state(self, other_subsystem: 'SubSystemBasis') -> None:
        """Update the state of this SubSystemBasis instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source SubSystemBasis containing updated values
                from parallel execution.
        """
        # Update SubSystemBasis attributes (in __init__ order)

        # 1. _SUBSYSTEMID: str
        # No copy.copy() needed - str is a primitive/immutable type
        self._SUBSYSTEMID: str = other_subsystem.get_SUBSYSTEMID()

        # 2. _neighborid: List[str]
        # Update list in-place to preserve memory address
        other_neighborid: List[str] = other_subsystem.get_NeighborId()
        for i in range(len(other_neighborid)):
            # No copy.copy() needed - str is immutable; assignment creates a new binding
            self._neighborid[i] = other_neighborid[i]

        # 3. _name: str | None
        # No copy.copy() needed - str is a primitive/immutable type
        self._name: str | None = other_subsystem.get_Name()

        # 3b. _historyfolderpath: str | None
        # No copy.copy() needed - str is a primitive/immutable type
        self._historyfolderpath: str | None = other_subsystem._historyfolderpath

        # 4. _optimdata: OptimDataBasis | None
        # copy.deepcopy() used - OptimDataBasis contains mutable nested structures
        self._optimdata: OptimDataBasis | None = copy.deepcopy(other_subsystem.get_OptimData())

        # 5. _couplingparameters: List[CouplingParametersInterface]
        # Update each coupling parameter object in-place to preserve memory addresses
        other_couplingparameters: List[CouplingParametersInterface] = other_subsystem.get_CouplingParameters()
        for i in range(len(other_couplingparameters)):
            self._couplingparameters[i].update_state(other_couplingparameters[i])

        # 6. _local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_Interface
        # Update via its own update_state method to preserve memory address
        self._local_convergenceindicator_innerloop.update_state(other_subsystem.get_Local_ConvergenceIndicator_Innerloop())

        # 7. _local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_Interface
        # Update via its own update_state method to preserve memory address
        self._local_convergenceindicator_outerloop.update_state(other_subsystem.get_Local_ConvergenceIndicator_Outerloop())

        # 8. _updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface
        # Update via its own update_state method to preserve memory address
        self._updatecouplingparametermethod_outerloop.update_state(other_subsystem._updatecouplingparametermethod_outerloop)

        # 9. _convinnerloop: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._convinnerloop: bool = other_subsystem.get_ConvInnerLoop()

        # 10. _convouterloop: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._convouterloop: bool = other_subsystem.get_ConvOuterLoop()

        # 11. _middlelevels: List[MiddleLevelDataStorageInterface]
        # Update via nested update_state() calls to preserve memory addresses
        for i in range(len(other_subsystem.get_MiddleLevels())):
            self._middlelevels[i].update_state(other_subsystem.get_MiddleLevels()[i])

        # 12. _outerloop_itr: int | None
        # No copy.copy() needed - int is a primitive/immutable type
        self._outerloop_itr: int | None = other_subsystem.get_OuterLoop_Itr()

        # 13. _innerloop_itr: int | None
        # No copy.copy() needed - int is a primitive/immutable type
        self._innerloop_itr: int | None = other_subsystem.get_InnerLoop_Itr()

        # 14. _innerloop_itr_runtime: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._innerloop_itr_runtime: float | None = other_subsystem.get_InnerLoop_Itr_Runtime()

        # 15. _innerloop_itr_numberofdesignvariableevaluations: int | None
        # No copy.copy() needed - int is a primitive/immutable type
        self._innerloop_itr_numberofdesignvariableevaluations: int | None = other_subsystem.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations()

        # 16. _subsystemhistory: Deque
        # Update in-place to preserve memory address
        other_history: Deque = other_subsystem.get_SubsystemHistory()
        self._subsystemhistory.clear()
        self._subsystemhistory.extend(copy.deepcopy(other_history))

        # 17. _optimization: OptimizationInterface
        # No update needed - serves as a strategy object whose state is not changed

        # 18. _lowerbounds_unscaled: List[float] | None
        self._lowerbounds_unscaled: List[float] | None = update_state_listprimitive(self._lowerbounds_unscaled, other_subsystem.get_LowerBounds_Unscaled())

        # 19. _upperbounds_unscaled: List[float] | None
        self._upperbounds_unscaled: List[float] | None = update_state_listprimitive(self._upperbounds_unscaled, other_subsystem.get_UpperBounds_Unscaled())

        # 20. _designvariables: List[float] | None
        self._designvariables: List[float] | None = update_state_listprimitive(self._designvariables, other_subsystem.get_DesignVariables())

        # 21. _designvariables_unscaled: List[float] | None
        self._designvariables_unscaled: List[float] | None = update_state_listprimitive(self._designvariables_unscaled, other_subsystem.get_DesignVariables_Unscaled())

        # 22. _designvariables_granularity: List[float] | None (0.0 means continuous)
        self._designvariables_granularity: List[float] | None = update_state_listprimitive(self._designvariables_granularity, other_subsystem.get_DesignVariables_Granularity())

        # 23. _designvariables_lower_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._designvariables_lower_scaler_bound_warning_raised: bool = other_subsystem._designvariables_lower_scaler_bound_warning_raised

        # 24. _designvariables_upper_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._designvariables_upper_scaler_bound_warning_raised: bool = other_subsystem._designvariables_upper_scaler_bound_warning_raised

        # 25. _coordinationobjectivevalue: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._coordinationobjectivevalue: float | None = other_subsystem.get_CoordinationObjectiveValue()

        # 26. _coordinationequalityconstraintvalue: List[float] | None
        self._coordinationequalityconstraintvalue: List[float] | None = update_state_listprimitive(self._coordinationequalityconstraintvalue, other_subsystem.get_CoordinationEqualityConstraintValue())

        # 26b. _coordinationinequalityconstraintvalue: List[float] | None
        self._coordinationinequalityconstraintvalue: List[float] | None = update_state_listprimitive(self._coordinationinequalityconstraintvalue, other_subsystem.get_CoordinationInequalityConstraintValue())

        # 27. _totalobjectivevalue: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._totalobjectivevalue: float | None = other_subsystem.get_TotalObjectiveValue()

        # 28. _totalconstrainteqvalue: List[float] | None
        self._totalconstrainteqvalue: List[float] | None = update_state_listprimitive(self._totalconstrainteqvalue, other_subsystem.get_TotalConstraintEqValue())

        # 29. _totalconstraintineqvalue: List[float] | None
        self._totalconstraintineqvalue: List[float] | None = update_state_listprimitive(self._totalconstraintineqvalue, other_subsystem.get_TotalConstraintIneqValue())
