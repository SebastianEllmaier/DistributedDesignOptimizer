# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""PyNomad BBO optimizer module.

This module provides optimization using PyNomad for
black-box optimization.
"""

from typing import List
import sys
import time
import copy
import numpy as np
import PyNomad
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print

from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemBasis, ControllerSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import (LocalSubSystemOptimData,
                                                                               ControllerOptimData,
                                                                               OptimDataBasis
                                                                               )
from Distributed_Design_Optimizer.subsystem.optimization.solver import SolverInterface


class Solver_PyNomadBBO(SolverInterface):
    """NOMAD Blackbox Optimization solver via PyNomad.

    Implements the MADS (Mesh Adaptive Direct Search) algorithm for derivative-free
    optimization. Supports both continuous and discrete (granular) design variables.
    Handles constraints using Progressive Barrier (PB) or Extreme Barrier (EB) methods.
    """
    
    def __init__(self,
                 maxevals: int | None,
                 constraint_handling_method: str,
                 seed: int,
                 vns_mads_search: bool,
                 quad_model_search: bool,
                 eqcon_as_ineqcon_tol: float  # 1E-8 as default
                 ) -> None:
        """Initialize the PyNomad optimizer.

        Args:
            maxevals: Maximum number of blackbox evaluations. None for unlimited.
            constraint_handling_method: Method for handling constraints.
                'PB' for Progressive Barrier or 'EB' for Extreme Barrier.
            seed: Random seed for reproducibility.
            vns_mads_search: Whether to enable Variable Neighborhood Search.
                Useful for escaping local minima but computationally expensive.
            quad_model_search: Whether to enable quadratic model search in the
                MADS search phase for proposing new candidate points.
            eqcon_as_ineqcon_tol: Tolerance for converting equality constraints
                to inequality constraints.
        """
        if isinstance(maxevals, int) and (maxevals > 0):
            self._maxevals = maxevals
        elif maxevals is None:
            self._maxevals = maxevals
        else:
            raise NotImplementedError(f"{DDO_Color}Unknown maxevals for Solver_PyNomadBBO{Reset}")
        
        if constraint_handling_method == "PB":  # Progressive Bound Handling
            self._constraint_handling_method = "PB"
        elif constraint_handling_method == "EB":  # Extreme Bound Handling
            self._constraint_handling_method = "EB"
        else:
            raise NotImplementedError(f"{DDO_Color}Unknown constraint handling method for NOMAD. Only PB (Progressive Bounds) or EB (Extreme Bounds) available{Reset}")
        
        self._seed = seed
        self._vns_mads_search: str = "true" if vns_mads_search else "false"  # This enforces a more global exploration by trying to escape local minimum. It is a costly strategy. But if you see that many evaluations are spent without improvements it could be an interesting strategy.
        self._quad_model_search: str = "yes" if quad_model_search else "no"  # The Search phase of the MADS algorithm can use models of the objectives and constraints that are constructed dynamically from all the evaluations made. By default, a quadratic model is used to propose new points to be evaluated with the blackbox.
        
        if isinstance(eqcon_as_ineqcon_tol, float) and (eqcon_as_ineqcon_tol > 0):
            self._eqcon_as_ineqcon_tol = eqcon_as_ineqcon_tol
        else:
            raise NotImplementedError(f"{DDO_Color}Unknown eqcon_as_ineqcon_tol for Solver_PyNomadBBO{Reset}")
        
    def execute(self, subsystem: SubSystemInterface) -> OptimDataBasis:
        """Execute the NOMAD MADS optimization algorithm.

        Args:
            subsystem: The subsystem to optimize containing design variables,
                bounds, objectives, and constraints.

        Returns:
            Optimization results containing optimal design variables and
            objective/constraint values.
        """
        # Helper function to retrieve and format all constraints for PyNomad.
        # This reads the already-computed constraint values from the subsystem
        # (must be called AFTER evaluateTotalObjectiveAndTotalConstraint()).
        def get_all_ineq_constraints() -> List[float]:
            """Get inequality constraints, converting equality constraints to inequality pairs.
            
            PyNomad only handles inequality constraints <= 0.
            Equality h(x) == 0 becomes: h(x) - tol <= 0 AND -h(x) - tol <= 0
            """
            # Retrieve cached constraint values (computed by evaluateTotalObjectiveAndTotalConstraint)
            eqcon: List[float] | None = subsystem.get_TotalConstraintEqValue()    # equality constraints h(x) == 0
            ineqcon: List[float] | None = subsystem.get_TotalConstraintIneqValue()  # inequality constraints g(x) <= 0
            # Transform each equality constraint h(x)==0 into two inequality constraints:
            #   h(x) - tol <= 0  (enforces h(x) <= tol)
            #  -h(x) - tol <= 0  (enforces h(x) >= -tol)
            # Together these enforce |h(x)| <= tol
            eq_as_ineq = []
            # Check if there exist any equality constraints
            if eqcon is not None:
                for eq in eqcon:
                    eq_as_ineq.append(eq - self._eqcon_as_ineqcon_tol)     # h(x) <= eps becomes h(x) - eps <= 0
                    eq_as_ineq.append(-eq - self._eqcon_as_ineqcon_tol)    # -h(x) <= eps becomes -h(x) - eps <= 0                
            
            # Combine all inequality constraints
            output = []
            
            # Concatenate the local inequality constraints and the local equality 
            # constraints that are transformed into two inequality constraints
            if ineqcon is not None:
                output += ineqcon
            if eq_as_ineq is not None:
                output += eq_as_ineq
            
            return output
        
        ub: List[float] = subsystem.get_UpperBounds_Unscaled()  # unscaled values
        ub_scaled01: List[float] = [subsystem.get_Scalers()[i].transform(ub[i]) for i in range(len(ub))]
        lb: List[float] = subsystem.get_LowerBounds_Unscaled()  # unscaled values
        lb_scaled01: List[float] = [subsystem.get_Scalers()[i].transform(lb[i]) for i in range(len(lb))]
        x0_scaled01: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        
        granularity_scaled01: List[float] = [float('nan')] * len(subsystem.get_DesignVariables_Granularity())
        for i in range(len(granularity_scaled01)):
            granularity = subsystem.get_DesignVariables_Granularity()[i]
            if granularity >= 0.0:  # 0.0 means continuous, > 0.0 means discrete
                granularity_scaled01[i] = granularity
            else:
                raise ValueError(f"{DDO_Color}Invalid granularity at index {i}: {granularity}. Must be >= 0.0{Reset}")
        
        # Check if any element of x0_scaled is outside the bounds and clip if necessary
        for i in range(len(x0_scaled01)):
            if x0_scaled01[i] < lb_scaled01[i]:
                ddo_print(f"x0_scaled01[{i}] = {x0_scaled01[i]} is below lower bound {lb_scaled01[i]}.")
                ddo_print("This may be because of numerical imprecisions in the scaling/unscaling transformation.")
                ddo_print("Clipping to lower bound.")
                x0_scaled01[i] = lb_scaled01[i]
            elif x0_scaled01[i] > ub_scaled01[i]:
                ddo_print(f"x0_scaled01[{i}] = {x0_scaled01[i]} is above upper bound {ub_scaled01[i]}.")
                ddo_print("This may be because of numerical imprecisions in the scaling/unscaling transformation.")
                ddo_print("Clipping to upper bound.")
                x0_scaled01[i] = ub_scaled01[i]
        
        # Define the blackbox evaluation function for PyNomad.
        # PyNomad (wrapping NOMAD's C++ implementation) calls this function repeatedly
        # during optimization. It must:
        #   1. Extract design variables from PyNomad's EvalPoint object (x)
        #   2. Evaluate objective and constraints
        #   3. Pack results into a UTF-8 encoded string via x.setBBO()
        #   4. Return 1 for success, 0 for failure
        def bb(x) -> int:
            bb.counter += 1  # Track number of blackbox evaluations
            try:
                # Extract design variables from PyNomad's EvalPoint object.
                # x.size() returns the number of design variables.
                # x.get_coord(i) returns the i-th coordinate value.
                # Wrap with float() to ensure pure Python floats, not numpy float types.
                des_var = [float(x.get_coord(i)) for i in range(x.size())]
                
                # Set design variables and evaluate BOTH objective and constraints
                # in a SINGLE call. This avoids redundant runAnalysis() and 
                # mapToCouplingParameters() calls that would occur if we called
                # evaluateTotalObjective() and evaluateTotalConstraint() separately.
                subsystem.set_DesignVariables(des_var)
                subsystem.evaluateTotalObjectiveAndTotalConstraint()
                
                # Retrieve the computed objective value
                f: float | None = subsystem.get_TotalObjectiveValue()                
                # If the total objective does not exist, return 0.0
                if f is None:
                    f = 0.0
                # Retrieve all inequality constraints (includes transformed equality constraints)
                g_all: List[float] = get_all_ineq_constraints()
                
                # Pack results for PyNomad: space-separated string "f g1 g2 g3 ..."
                # Must be UTF-8 encoded for the C++ backend
                rawBBO: str = str(f) + " " + " ".join(map(str, g_all))
                x.setBBO(rawBBO.encode("UTF-8"))
            except Exception as e:
                ddo_print(f"Unexpected eval error: {sys.exc_info()[0]} {e}")
                return 0  # Signal evaluation failure to NOMAD
            return 1  # Signal successful evaluation to NOMAD
        bb.counter = 0  # Initialize evaluation counter
        
        # Pre-evaluation: NOMAD requires knowing the number of constraints at initialization
        # to properly parse the BB_OUTPUT_TYPE parameter. We evaluate x0 once to determine
        # how many inequality constraints (original + transformed equalities) exist.
        # Ensure pure Python floats (clipping may have assigned numpy floats from scaled bounds).
        subsystem.set_DesignVariables([float(v) for v in x0_scaled01])
        subsystem.evaluateTotalObjectiveAndTotalConstraint()
        num_constraints: int = len(get_all_ineq_constraints())
        
        params = [f"DIMENSION {len(x0_scaled01)}",
                  "BB_OUTPUT_TYPE OBJ " + " ".join([self._constraint_handling_method] * num_constraints),  # OBJ objective function, EB/PB: inequality constraint handling
                  f"MAX_BB_EVAL {self._maxevals}",
                  "X0 (" + " ".join(map(str, x0_scaled01)) + ")",
                  f"LH_SEARCH {int(min(5 * len(x0_scaled01) * len(x0_scaled01), 0.1 * self._maxevals))} 0",
                  "LOWER_BOUND (" + " ".join(map(str, lb_scaled01)) + ")",
                  "UPPER_BOUND (" + " ".join(map(str, ub_scaled01)) + ")",
                  "GRANULARITY (" + " ".join(map(str, granularity_scaled01)) + ")",  # 0.0 for continuous, scaled01 discrete step size for integer variables...
                  "DISPLAY_DEGREE 2",
                  "DISPLAY_ALL_EVAL false",
                  "DISPLAY_STATS BBE OBJ",
                  "EVAL_OPPORTUNISTIC false",
                  f"SEED {self._seed}",
                  f"VNS_MADS_SEARCH {self._vns_mads_search}",
                  f"QUAD_MODEL_SEARCH {self._quad_model_search}"
                  ]
        if all([gran > 0.0 for gran in subsystem.get_DesignVariables_Granularity()]):  # all discrete
            params.append("DIRECTION_TYPE ORTHO 2N")  # These settings have worked better for us if all desing variables are discrete
        
        starttime = time.time()
        result = PyNomad.optimize(bb, x0_scaled01, lb_scaled01, ub_scaled01, params)
        finishtime = time.time()
        xopt_scaled01 = result['x_best']
            
        # evaluate the subsystem one more time with the determined optimal design variables
        # xopt_scaled01 is proposed by optimizer within scaled01 upper and lower bounds.
        # set_DesignVariables() recieves scaled01 values.
        # Check if any element of xopt_scaled01 is outside the scaled bounds and clip if necessary
        for i in range(len(xopt_scaled01)):
            if xopt_scaled01[i] < lb_scaled01[i]:
                ddo_print(f"xopt_scaled01[{i}] = {xopt_scaled01[i]} is below lower bound {lb_scaled01[i]}.")
                ddo_print("This may be because of numerical imprecisions in the scaling/unscaling transformation.")
                ddo_print("Clipping to lower bound.")
                xopt_scaled01[i] = lb_scaled01[i]
            elif xopt_scaled01[i] > ub_scaled01[i]:
                ddo_print(f"xopt_scaled01[{i}] = {xopt_scaled01[i]} is above upper bound {ub_scaled01[i]}.")
                ddo_print("This may be because of numerical imprecisions in the scaling/unscaling transformation.")
                ddo_print("Clipping to upper bound.")
                xopt_scaled01[i] = ub_scaled01[i]
        
        # Ensure pure Python floats (result['x_best'] and clipping may have numpy floats).
        subsystem.set_DesignVariables([float(v) for v in xopt_scaled01])
        subsystem.evaluateTotalObjectiveAndTotalConstraint()
        # validates the constraints
        # assigns exit flag if inequality violations detected
        # Define a tolerance for numerical precision
        # Check equality constraints with numpy.isclose
        if subsystem.get_TotalConstraintEqValue() is None:
            eq_msg = f"No equality TotalConstraints exist for Subsystem {subsystem.get_SUBSYSTEMID()}."
        elif np.all(np.isclose(np.array(subsystem.get_TotalConstraintEqValue()), 0.0, atol=self._eqcon_as_ineqcon_tol)):
            eq_msg = f"Equality TotalConstraints of Subsystem {subsystem.get_SUBSYSTEMID()} are VALIDATED!"
        else:
            eq_msg = f"Equality TotalConstraints of Subsystem {subsystem.get_SUBSYSTEMID()} are NOT VALIDATED!"
        # Check inequality constraints with tolerance
        if subsystem.get_TotalConstraintIneqValue() is None:
            ineq_msg = f"No inequality TotalConstraints exist for Subsystem {subsystem.get_SUBSYSTEMID()}."
            exitflag = 1
        elif np.all(np.logical_or(np.array(subsystem.get_TotalConstraintIneqValue()) <= 0.0, 
                                  np.isclose(np.array(subsystem.get_TotalConstraintIneqValue()), 0, atol=self._eqcon_as_ineqcon_tol))):
            ineq_msg = f"Inequality TotalConstraints of Subsystem {subsystem.get_SUBSYSTEMID()} are VALIDATED!"
            # mapping of exit flags
            # check the solver documentation for the results status of the solvers
            exitflag = 1
        else:
            ineq_msg = f"Inequality TotalConstraints of Subsystem {subsystem.get_SUBSYSTEMID()} are NOT VALIDATED!"
            exitflag = 0
            raise ValueError(f'{DDO_Color}TOTALCONSTRAINTS VIOLATIONS DETECTED!{Reset}')
        
        if 'stop_reason' in result:
            # If the solver returns any solution message, replace 'solver_result.message' with appropriate attribute
            message = result['stop_reason'] + "\n" + eq_msg + "\n" + ineq_msg
        else:
            message = eq_msg + "\n" + ineq_msg
            
        # create object to hold the read data
        
        # NOTE: For general optimizers that compute gradients
        # If multiplier would be computed by the solver, 
        # need to use subsystem.getLocalConstrs and subsystem.getCoordinationCons
        # to seperate corresponding multipliers of total multipliers
        
        # If it is a local subsystem, use OptimData for local subsystems
        # If it is the controller, use OptimData for controller
        if isinstance(subsystem, LocalSubSystemBasis):
            optimdata = LocalSubSystemOptimData(optimizer_type="Solver_PyNomadBBO", 
                                                designvariables=subsystem.get_DesignVariables(),
                                                designvariables_unscaled=subsystem.get_DesignVariables_Unscaled(),
                                                lowerbounds=lb,
                                                lowerbounds_scaled=lb_scaled01,
                                                upperbounds=ub,
                                                upperbounds_scaled=ub_scaled01,
                                                Responses_unscaled=subsystem.get_Responses_Unscaled(),
                                                localobjectivevalue=subsystem.get_LocalObjectiveValue(),
                                                localobjectivevalue_unscaled=subsystem.get_LocalObjectiveValue_Unscaled(),
                                                totalobjectivevalue=subsystem.get_TotalObjectiveValue(),
                                                coordinationobjectivevalue=subsystem.get_CoordinationObjectiveValue(),
                                                equalitylocalconstraintsvalue=subsystem.get_EqualityLocalConstraintsValue(),
                                                equalitylocalconstraintsvalue_unscaled=subsystem.get_EqualityLocalConstraintsValue_Unscaled(),
                                                inequalitylocalconstraintsvalue=subsystem.get_InequalityLocalConstraintsValue(),
                                                inequalitylocalconstraintsvalue_unscaled=subsystem.get_InequalityLocalConstraintsValue_Unscaled(),
                                                totalconstrainteqvalue=subsystem.get_TotalConstraintEqValue(),
                                                totalconstraintineqvalue=subsystem.get_TotalConstraintIneqValue(),
                                                coordinationequalityconstraintvalue=subsystem.get_CoordinationEqualityConstraintValue(),
                                                coordinationinequalityconstraintvalue=subsystem.get_CoordinationInequalityConstraintValue(),
                                                couplingparameters=copy.deepcopy(subsystem.get_CouplingParameters()),
                                                gradient_localobjective=None,
                                                gradient_coordinationobjective=None,
                                                gradient_totalobjective=None,
                                                jacobian_localequalityconstraints=None,
                                                jacobian_coordinationequalityconstraints=None,
                                                jacobian_totalequalityconstraints=None,
                                                jacobian_localinequalityconstraints=None,
                                                jacobian_coordinationinequalityconstraints=None,
                                                jacobian_totalinequalityconstraints=None,
                                                jacobian_lowerbounds=None,
                                                jacobian_upperbounds=None,
                                                multipliers_lowerbounds=None,  # placeholder if solver computes multipliers
                                                multipliers_upperbounds=None,  # placeholders if solver computes multipliers
                                                multipliers_local_inequality_constraints=None,  # placeholders if solver computes multipliers
                                                multipliers_local_equality_constraints=None,  # placeholders if solver computes multipliers
                                                multipliers_coordination_equality_constraints=None,  # placeholders if solver computes multipliers
                                                multipliers_coordination_inequality_constraints=None,  # Placeholders if solver computes multipliers
                                                activelocalinequalityconstraints=np.isclose(np.array(subsystem.get_InequalityLocalConstraintsValue()), 0.0, atol=1e-8).tolist() if subsystem.get_InequalityLocalConstraintsValue() is not None else None,
                                                activecoordinationinequalityconstraints=np.isclose(np.array(subsystem.get_CoordinationInequalityConstraintValue()), 0.0, atol=1e-8).tolist() if subsystem.get_CoordinationInequalityConstraintValue() is not None else None,
                                                activelowerbounds=np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), np.array(subsystem.get_LowerBounds_Unscaled()), atol=1e-8).tolist(),
                                                activeupperbounds=np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), np.array(subsystem.get_UpperBounds_Unscaled()), atol=1e-8).tolist(),
                                                exitflag=exitflag,
                                                message=message,
                                                optimization_numberofdesignvariableevaluations=bb.counter,
                                                optimization_runtime=finishtime - starttime,
                                                numberofactiveinequalityconstraints=int(np.sum(np.isclose(np.array(subsystem.get_InequalityLocalConstraintsValue()), 0.0, atol=1e-8))) if subsystem.get_InequalityLocalConstraintsValue() is not None else 0,
                                                numberofactivebounds=int(np.sum(np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()),
                                                                                           np.array(subsystem.get_LowerBounds_Unscaled()),
                                                                                           atol=1e-8)) + \
                                                                         np.sum(np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), 
                                                                                           np.array(subsystem.get_UpperBounds_Unscaled()), 
                                                                                           atol=1e-8)))
                                                )
            
        elif isinstance(subsystem, ControllerSubSystemBasis):
            optimdata = ControllerOptimData(optimizer_type="Solver_PyNomadBBO",
                                            designvariables=subsystem.get_DesignVariables(),
                                            designvariables_unscaled=subsystem.get_DesignVariables_Unscaled(),
                                            lowerbounds=lb,
                                            lowerbounds_scaled=lb_scaled01,
                                            upperbounds=ub,
                                            upperbounds_scaled=ub_scaled01,
                                            totalobjectivevalue=subsystem.get_TotalObjectiveValue(),
                                            coordinationobjectivevalue=subsystem.get_CoordinationObjectiveValue(),
                                            totalconstrainteqvalue=subsystem.get_TotalConstraintEqValue(),
                                            totalconstraintineqvalue=subsystem.get_TotalConstraintIneqValue(),
                                            coordinationequalityconstraintvalue=subsystem.get_CoordinationEqualityConstraintValue(),
                                            coordinationinequalityconstraintvalue=subsystem.get_CoordinationInequalityConstraintValue(),
                                            gradient_coordinationobjective=None,
                                            jacobian_coordinationequalityconstraints=None,
                                            jacobian_coordinationinequalityconstraints=None,
                                            gradient_totalobjective=None,
                                            jacobian_totalequalityconstraints=None,
                                            jacobian_totalinequalityconstraints=None,
                                            jacobian_lowerbounds=None,
                                            jacobian_upperbounds=None,
                                            multipliers_lowerbounds=None,  # placeholder if solver computes multipliers
                                            multipliers_upperbounds=None,  # placheolder if solver computes multipliers
                                            multipliers_coordination_equality_constraints=None,  # placeholder if solver computes multipliers
                                            multipliers_coordination_inequality_constraints=None,  # placeholder if solver computes multipliers
                                            activecoordinationinequalityconstraints=np.isclose(np.array(subsystem.get_CoordinationInequalityConstraintValue()), 0.0, atol=1e-8).tolist() if subsystem.get_CoordinationInequalityConstraintValue() is not None else None,
                                            activelowerbounds=np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), np.array(subsystem.get_LowerBounds_Unscaled()), atol=1e-8).tolist(),
                                            activeupperbounds=np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), np.array(subsystem.get_UpperBounds_Unscaled()), atol=1e-8).tolist(),
                                            exitflag=exitflag,
                                            message=message,
                                            optimization_numberofdesignvariableevaluations=bb.counter,
                                            optimization_runtime=finishtime - starttime,
                                            numberofactiveinequalityconstraints=int(np.sum(np.isclose(np.array(subsystem.get_TotalConstraintIneqValue()), 0.0, atol=1e-8))) if subsystem.get_TotalConstraintIneqValue() is not None else 0,
                                            numberofactivebounds=int(np.sum(np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()),
                                                                                       np.array(subsystem.get_LowerBounds_Unscaled()),
                                                                                       atol=1e-8)) + \
                                                                     np.sum(np.isclose(np.array(subsystem.get_DesignVariables_Unscaled()), 
                                                                                       np.array(subsystem.get_UpperBounds_Unscaled()), 
                                                                                       atol=1e-8)))
                                            )
        
        else: 
            raise TypeError(f"{DDO_Color}Unknown subsystem type: {type(subsystem).__name__}. Expected LocalSubSystemBasis or ControllerSubSystemBasis.{Reset}")
        
        return optimdata
