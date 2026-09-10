---
title: ControllerSubSystemBasis (Source)
---

← Back to [ControllerSubSystemBasis documentation](ControllerSubSystemBasis.md)

# ControllerSubSystemBasis - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\ControllerSubSystemBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Controller subsystem basis module.

This module provides the base class for controller subsystems in
hierarchical distributed optimization.
"""

import copy
from typing import List, Tuple
from Distributed_Design_Optimizer.subsystem import SubSystemBasis
from Distributed_Design_Optimizer.subsystem.historyentry import ControllerSubSystemHistoryEntry
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import ControllerOptimData
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationController
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print
from Distributed_Design_Optimizer.subsystem.couplingparameters import ControllerCouplingParametersBasis


class ControllerSubSystemBasis(SubSystemBasis):
    """A ControllerSubSystemBasis object with id = "C" contains all necessary data for a controller.

    It includes methods to optimize the subsystem and to couple it to
    neighboring subsystems.
    """

    def __init__(self,
                 neighborid: List[str]
                 ) -> None:
        """Create a new instance of ControllerSubSystemBasis.

        Args:
            neighborid: List of identifiers for neighboring subsystems.
        """

        # Call init of super, id is "C", since this is a class for the controller
        super().__init__(id="C", neighborid=neighborid)

        # 'optimization: OptimizationInterface' is set in specific subclass, e.g. ControllerSubSystemALADIN
        self._optimization: OptimizationController

        self._optimdata: ControllerOptimData = self.initialize_Initial_Optimdata_at_Beginning()
        self._couplingparameters: List[ControllerCouplingParametersBasis]  # to be initialized in child-class of ControllerSubSystemBasis


    def initialize_Initial_Optimdata_at_Beginning(self) -> ControllerOptimData:
        """Return a ControllerOptimData object based on the subsystem's current state.

        Returns:
            A ControllerOptimData with all fields set to None.
        """

        return ControllerOptimData(optimizer_type=None,
                                   designvariables=None,
                                   designvariables_unscaled=None,
                                   lowerbounds=None,
                                   lowerbounds_scaled=None,
                                   upperbounds=None,
                                   upperbounds_scaled=None,
                                   totalobjectivevalue=None,
                                   coordinationobjectivevalue=None,
                                   totalconstrainteqvalue=None,
                                   totalconstraintineqvalue=None,
                                   coordinationequalityconstraintvalue=None,
                                   coordinationinequalityconstraintvalue=None,
                                   gradient_coordinationobjective=None,
                                   gradient_totalobjective=None,
                                   jacobian_coordinationequalityconstraints=None,
                                   jacobian_totalequalityconstraints=None,
                                   jacobian_coordinationinequalityconstraints=None,
                                   jacobian_totalinequalityconstraints=None,
                                   jacobian_lowerbounds=None,
                                   jacobian_upperbounds=None,
                                   multipliers_lowerbounds=None,  # placeholders if solver computes multipliers
                                   multipliers_upperbounds=None,  # placeholders if solver computes multipliers
                                   multipliers_coordination_equality_constraints=None,  # placeholders if solver computes multipliers
                                   multipliers_coordination_inequality_constraints=None,  # placeholders if solver computes multipliers
                                   activecoordinationinequalityconstraints=None,
                                   activelowerbounds=None,
                                   activeupperbounds=None,
                                   exitflag=None,
                                   message=None,
                                   optimization_numberofdesignvariableevaluations=None,
                                   optimization_runtime=None,
                                   numberofactiveinequalityconstraints=None,
                                   numberofactivebounds=None
                                   )

########################################################################################################################
#   Basics of the subsystem
########################################################################################################################

########################################################################################################################
#   Functions to obtain past values from self._subsystemhistory
########################################################################################################################

########################################################################################################################
#   Functions to evaluate the auxiliary variables of the controller and map them onto coupling parameters (see Analysis class)
########################################################################################################################

    def mapToController(self) -> None:
        """Controller does not map to itself."""

########################################################################################################################
#   Functions to handle coordination parameters
########################################################################################################################

    def run_updateCouplingParameters_outerLoop_job(self) -> None:
        """Update coupling parameters in the outer loop after the inner loop."""
        self.set_DesignVariables(self.get_OptimData().get_DesignVariables())
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
        self.CopyFromMiddleLevel()
        self.updateCouplingParameters_outerLoop()
        self.CopyToMiddleLevel()

    def run_prepare_updateCouplingParameters_job(self) -> None:
        """Prepare coupling parameters update after inner loop is finished."""
        self.set_DesignVariables(self.get_OptimData().get_DesignVariables())
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
        self.CopyFromMiddleLevel()
        self.prepare_updateCouplingParameters()
        self.CopyToMiddleLevel()

    def appendtohistory(self) -> None:
        """Append the current controller state to the history."""
        self._subsystemhistory.append(ControllerSubSystemHistoryEntry(subsystem_id=self.get_SUBSYSTEMID(),
                                                                      outerloop_itr=self.get_OuterLoop_Itr(),
                                                                      innerloop_itr=self.get_InnerLoop_Itr(),
                                                                      innerloop_itr_runtime=self.get_InnerLoop_Itr_Runtime(),
                                                                      innerloop_itr_numberofdesignvariableevaluations=self.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(),
                                                                      optimdata=copy.deepcopy(self.get_OptimData()),
                                                                      convinnerloop=self.get_ConvInnerLoop(),
                                                                      convouterloop=self.get_ConvOuterLoop(),
                                                                      ))

########################################################################################################################
#   Functions to evaluate a controller's optimization objective and constraints for given responses
########################################################################################################################

    def evaluateTotalObjective(self) -> None:
        """Evaluate the total objective function (coordination only, no local objective)."""

        # execute mapping
        self.mapToCouplingParameters()

        # No local objective, hence, only coordination objective
        # compute any objective term due to the coordination method handling of controller
        self.evaluateCoordinationObjective()

        f: float | None = self.get_CoordinationObjectiveValue()

        # Check if there exists a cooridnation objective
        self.set_TotalObjectiveValue(f)

    def evaluateTotalConstraint(self) -> None:
        """Evaluate the total constraints (coordination only, no local constraints)."""

        # execute mapping
        self.mapToCouplingParameters()

        # No local constraints, hence, only coordination constraints
        # compute any constraint due to the coordination method handling of controller
        self.evaluateCoordinationEqualityConstraint()
        self.evaluateCoordinationInequalityConstraint()

        equality_coordinationcons: List[float] | None = self.get_CoordinationEqualityConstraintValue()
        inequality_coordinationcons: List[float] | None = self.get_CoordinationInequalityConstraintValue()

        # set the equality, inequality constraint values to the subsystem
        self.set_TotalConstraintEqValue(equality_coordinationcons)
        self.set_TotalConstraintIneqValue(inequality_coordinationcons)

    def evaluateTotalObjectiveAndTotalConstraint(self) -> None:
        """Evaluate both total objective and total constraint in a single call.

        This method combines evaluateTotalObjective() and evaluateTotalConstraint()
        to avoid redundant mapping operations when both values are needed.
        """
        # execute mapping once
        self.mapToCouplingParameters()

        # No local objective, hence, only coordination objective
        self.evaluateCoordinationObjective()
        f: float | None = self.get_CoordinationObjectiveValue()
        self.set_TotalObjectiveValue(f)

        # No local constraints, hence, only coordination constraints
        self.evaluateCoordinationEqualityConstraint()
        self.evaluateCoordinationInequalityConstraint()
        equality_coordinationcons: List[float] | None = self.get_CoordinationEqualityConstraintValue()
        inequality_coordinationcons: List[float] | None = self.get_CoordinationInequalityConstraintValue()
        self.set_TotalConstraintEqValue(equality_coordinationcons)
        self.set_TotalConstraintIneqValue(inequality_coordinationcons)


########################################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
#   This only works on auxiliary variables (which the controller sends) and coupling information from the subsystems.
#   Nothing related to coordination parameters
#
#   Workflow: In subclasses of ControllerSubSystemBasis for each distributed optimization algorithm, setters and
#   getters are implemented
########################################################################################################################

########################################################################################################################
#   Compute local KKT multipliers
########################################################################################################################

    def compute_KKT_system_matrix_and_bounds(self) -> List[List[List[float]] | List[Tuple[float | None, float | None]]]:
        """Return the total linear KKT system matrix.

        Returns:
            A list containing the constraint matrix and bounds for the KKT system.
        """

        # Define the KKT system constraint equality matrix
        # Form: ( coordination eq. | coordination ineq. | lower bounds | upper bounds)
        constraint_matrix = []
        bounds: List[List[float]] = []

        primal_dimension: int = len(self.get_DesignVariables())

        # If coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None:

            # Get the Jacobian of the coordination equality constraints
            jacobian_coordinationequalityconstraints: List[List[float]] = self._optimdata.get_Jacobian_CoordinationEqualityConstraints()

            # Append the Jacobian w.r.t the coordination equality constraint rowwise
            for component_jacobian in jacobian_coordinationequalityconstraints:

                # Append the specific row
                constraint_matrix.append(component_jacobian)

                # Indicate no bound for dual multiplier w.r.t
                # this specific coordination equality constraint
                bounds.append((None, None))

        # If coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the Jacobian and indicators of the (active) coordination inequality constraints
            jacobian_coordinationinequalityconstraints: List[List[float | None]] = self._optimdata.get_Jacobian_CoordinationInequalityConstraints()
            activecoordinationinequalityconstraints: List[bool] = self._optimdata.get_ActiveCoordinationInequalityConstraints()

            # Iterate over the Jacobians of each component function
            for i in range(len(jacobian_coordinationinequalityconstraints)):

                # Initialize the component gradient
                component_jacobian: List[float] = [0.0] * primal_dimension

                # Check if the constraint is inactive
                if activecoordinationinequalityconstraints[i] is not True:

                    # Do not change the Jacobian from the zeros vector,
                    # since the constraint is inactive

                    # Indicate no bound for dual multiplier w.r.t.
                    # inactive coordination inequality constraints, since they
                    # have no impact in KKT system
                    bounds.append((None, None))

                # Active coordination inequality constraint
                else:

                    # Set the Jacobian approximation
                    component_jacobian = jacobian_coordinationinequalityconstraints[i]

                    # Indicate nonnegativity bound for dual multiplier
                    # w.r.t. active coordination inequality constraints
                    bounds.append((0.0, None))

                # Add the component Jacobian
                constraint_matrix.append(component_jacobian)

        # For lower bounds

        # Get the Jacobian and indicators of the (active) lower bounds
        jacobian_activelowerbounds: List[List[float | None]] = self._optimdata.get_Jacobian_LowerBounds()
        activelowerbounds: List[bool] = self._optimdata.get_ActiveLowerBounds()

        # Iterate over the Jacobians of each component function
        for i in range(len(jacobian_activelowerbounds)):

            # Initialize the component gradient
            component_jacobian: List[float] = [0.0] * primal_dimension

            # Check if the constraint is inactive
            if activelowerbounds[i] is not True:

                # Do not change the Jacobian from the zeros vector,
                # since the bound is inactive

                # Indicate no bound for dual multiplier w.r.t.
                # inactive lower bound constraints, since they
                # have no impact in KKT system
                bounds.append((None, None))

            # Active lower bound constraint
            else:

                # Set the Jacobian approximation
                component_jacobian = jacobian_activelowerbounds[i]

                # Indicate nonnegativity bound for dual multiplier
                # w.r.t. active lower bound constraints
                bounds.append((0.0, None))

            # Add the component Jacobian
            constraint_matrix.append(component_jacobian)

        # For upper bounds

        # Get the Jacobian and indicators of the (active) upper bounds
        jacobian_activeupperbounds: List[List[float | None]] = self._optimdata.get_Jacobian_UpperBounds()
        activeupperbounds: List[bool] = self._optimdata.get_ActiveUpperBounds()

        # Iterate over the Jacobians of each component function
        for i in range(len(jacobian_activeupperbounds)):

            # Initialize the component gradient
            component_jacobian: List[float] = [0.0] * primal_dimension

            # Check if the constraint is inactive
            if activeupperbounds[i] is not True:

                # Do not change the Jacobian from the zeros vector,
                # since the bound is inactive

                # Indicate no bound for dual multiplier w.r.t.
                # inactive upper bound constraints, since they
                # have no impact in KKT system
                bounds.append((None, None))

            # Active upper bound constraint
            else:

                # Set the Jacobian approximation
                component_jacobian = jacobian_activeupperbounds[i]

                # Indicate nonnegativity bound for dual multiplier
                # w.r.t. active upper bound constraints
                bounds.append((0.0, None))

            # Add the component Jacobian
            constraint_matrix.append(component_jacobian)

        # Return the KKT system matrix
        return [constraint_matrix, bounds]

    def decompose_KKT_multipliers(self, all_multipliers: List[float]) -> None:
        """Decompose the KKT system solution into individual multiplier groups.

        The solution stored in optimization_result is separated into different
        parts (e.g. local inequality constraints) and stored in self._optimdata.

        Args:
            all_multipliers: Total accumulation of all multipliers (only for constraints, not for objective)
        """

        # Form of all_multipliers by definition:
        # ( coordination eq. | coordination ineq. | lower bounds | upper bounds)

        # Define a pointer for the indices of all_multipliers
        index_pointer: int = 0

        # Coordination equality constraint

        # If coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None:

            # Get the number of coordination equality constraints
            number_coordinationequalityconstraints: int = len(self.get_CoordinationEqualityConstraintValue())

            # Store the corresponding multipliers
            self._optimdata.set_Multipliers_Coordination_Equality_Constraints(all_multipliers[index_pointer:index_pointer + number_coordinationequalityconstraints])

            # Update the index pointer
            index_pointer += number_coordinationequalityconstraints


        # Coordination inequality constraint

        # If coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the indicators of the (active) coordination inequality constraints
            activecoordinationinequalityconstraints: List[bool] = self._optimdata.get_ActiveCoordinationInequalityConstraints()
            multipliers_coordinationinequalityconstraints: List[float | None] = []

            # Iterate over each coordination inequality constraint
            for i in range(len(activecoordinationinequalityconstraints)):

                # Check if the constraint is inactive
                if activecoordinationinequalityconstraints[i] is False:

                    # Append a None field, since constraint is inactive
                    multipliers_coordinationinequalityconstraints.append(None)

                # Active coordination inequality constraint
                else:

                    # Add the corresponding multiplier
                    multipliers_coordinationinequalityconstraints.append(all_multipliers[index_pointer])

                # Move the index pointer to next component
                index_pointer += 1

            # Store the corresponding multipliers
            self._optimdata.set_Multipliers_Coordination_Inequality_Constraints(multipliers_coordinationinequalityconstraints)

        # Lower bounds, upper bounds

        # For lower bounds

        # Get the Jacobian and indicators of the (active) lower bounds
        activelowerbounds: List[bool] = self._optimdata.get_ActiveLowerBounds()
        multipliers_lowerbounds: List[float] = []

        # Iterate over the Jacobians of each component function
        for i in range(len(activelowerbounds)):

            # Check if the constraint is inactive
            if activelowerbounds[i] is False:

                # Append a None field, since constraint is inactive
                multipliers_lowerbounds.append(None)

            # Active lower bound constraint
            else:

                # Add the component Jacobian
                multipliers_lowerbounds.append(all_multipliers[index_pointer])

            # Move the index pointer to next component
            index_pointer += 1

        # Set the multiplier of the lower bounds
        self._optimdata.set_Multipliers_LowerBounds(multipliers_lowerbounds)

        # For upper bounds

        # Get the Jacobian and indicators of the (active) upper bounds
        activeupperbounds: List[bool] = self._optimdata.get_ActiveUpperBounds()
        multipliers_upperbounds: List[float] = []

        # Iterate over the Jacobians of each component function
        for i in range(len(activeupperbounds)):

            # Check if the constraint is inactive
            if activeupperbounds[i] is False:

                # Append a None field, since constraint is inactive
                multipliers_upperbounds.append(None)

            # Active upper bound constraint
            else:

                # Add the component Jacobian
                multipliers_upperbounds.append(all_multipliers[index_pointer])

            # Move the index pointer to next component
            index_pointer += 1

        # Set the multiplier of the upper bounds
        self._optimdata.set_Multipliers_UpperBounds(multipliers_upperbounds)

    def evaluate_Gradient_TotalObjective(self) -> None:
        """
        Evaluate the gradient of the total objective (coordination only, if it exists).

        Returns:
            None. The total objective gradient is stored in self._optimdata.
        """

        # Check if a coordination objective exists
        if self.get_CoordinationObjectiveValue() is not None:

            # Store the gradient of the coordination objective
            # No copy.copy() wrapper needed - getter returns defensive copy and setter creates its own copy
            self._optimdata.set_Gradient_TotalObjective(self._optimdata.get_Gradient_CoordinationObjective())


    def evaluate_Jacobian_TotalEqualityConstraints(self) -> None:
        """
        Evaluate the Jacobian of the total equality constraints if it exists.

        Returns:
            None. The Jacobian is stored in self._optimdata.
        """

        # Check if coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None:

            # Get the Jacobian of the coordination equality constraints
            # No copy.deepcopy() wrapper needed - getter returns defensive copy and setter creates its own copy
            self._optimdata.set_Jacobian_TotalEqualityConstraints(self._optimdata.get_Jacobian_CoordinationEqualityConstraints())


    def evaluate_Jacobian_TotalInEqualityConstraints(self) -> None:
        """
        Evaluate the Jacobian of the total inequality constraints if it exists.

        Returns:
            None. The Jacobian is stored in self._optimdata.
        """

        # Check if coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the Jacobian of the coordination inequality constraints
            # No copy.deepcopy() wrapper needed - getter returns defensive copy and setter creates its own copy
            self._optimdata.set_Jacobian_TotalInequalityConstraints(self._optimdata.get_Jacobian_CoordinationInequalityConstraints())

########################################################################################################################
#   Print methods for terminal output
########################################################################################################################

    def print_startup_summary(self) -> None:
        """Print controller subsystem info at startup."""
        ddo_print(f"   SubSystem {self.get_SUBSYSTEMID()} (Controller)")

    def print_end_of_innerloop_iteration(self) -> None:
        """Print controller subsystem results at the end of an inner loop iteration."""
        self._print_subsystem_header()
        self.get_OptimData().print_results()
        ddo_print("")

    def print_termination_summary(self) -> None:
        """Print controller subsystem results at the end of the optimization run."""
        self._print_subsystem_header()
        self.get_OptimData().print_results()
        ddo_print("")

########################################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################################
    def update_state(self, other_subsystem: 'ControllerSubSystemBasis') -> None:
        """Update the state of this ControllerSubSystemBasis instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source ControllerSubSystemBasis containing updated values
                from parallel execution.
        """
        # Update attributes inherited from SubSystemBasis
        super().update_state(other_subsystem=other_subsystem)

        # Update ControllerSubSystemBasis-specific attributes (in __init__ order)

        # 1. _optimization: OptimizationController
        # No update needed - serves as a strategy object whose state is not changed

        # 2. _optimdata: ControllerOptimData
        # Handled by parent class (SubSystemBasis) with copy.deepcopy

        # 3. _couplingparameters: List[ControllerCouplingParametersBasis]
        # Handled by parent class (SubSystemBasis) via in-place update_state calls

```
