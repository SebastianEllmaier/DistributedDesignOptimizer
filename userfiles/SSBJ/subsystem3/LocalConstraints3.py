# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.

This module defines the LocalConstraints3 class which implements the local
equality and inequality constraints specific to Subsystem 3 in the distributed
design optimization framework.
"""
import numpy as np
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints3(LocalConstraintsInterface):
    """Local constraints class for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints3 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 3.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        equality_unscaled = []        
        # append any equality Local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        
        # no Equality Local constraints exist:
        equality = None
       
        # equality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################        
        subsystem.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 3.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()

        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints                ###
        ################################################################

        # Unpack flattened response arrays (each variable covers 3 panels)
        # sig_1..sig_6: bending stresses, indices 0:18 [lb/ft^2]
        sig_1   = np.array(responses[0:3])
        sig_2   = np.array(responses[3:6])
        sig_3   = np.array(responses[6:9])
        sig_4   = np.array(responses[9:12])
        sig_5   = np.array(responses[12:15])
        sig_6   = np.array(responses[15:18])
        # sig_cr/tau_cr: critical buckling normal/shear stresses, indices 18:42 [lb/ft^2]
        sig_cr1 = np.array(responses[18:21])
        tau_cr1 = np.array(responses[21:24])
        sig_cr2 = np.array(responses[24:27])
        tau_cr2 = np.array(responses[27:30])
        sig_cr3 = np.array(responses[30:33])
        tau_cr3 = np.array(responses[33:36])
        sig_cr5 = np.array(responses[36:39])
        tau_cr5 = np.array(responses[39:42])
        # tau/sig_eq: shear stresses & von Mises equivalent stresses, indices 42:72 [lb/ft^2]
        tau1    = np.array(responses[42:45])
        sig_eq1 = np.array(responses[45:48])
        tau2    = np.array(responses[48:51])
        sig_eq2 = np.array(responses[51:54])
        tau3    = np.array(responses[54:57])
        sig_eq3 = np.array(responses[57:60])
        sig_eq4 = np.array(responses[60:63])
        tau5    = np.array(responses[63:66])
        sig_eq5 = np.array(responses[66:69])
        sig_eq6 = np.array(responses[69:72])
        # h_spar at index 72:75 [ft], thickness arrays: indices 75:93 [ft]
        h_spar = np.array(responses[72:75])
        t1  = np.array(responses[75:78])
        t2  = np.array(responses[78:81])
        t3  = np.array(responses[81:84])
        ts1 = np.array(responses[84:87])
        ts2 = np.array(responses[87:90])
        ts3 = np.array(responses[90:93])
        # Sig_C / Sig_T as constants
        Sig_C = 65000.0 * 144.0  # allowable compressive stress [lb/ft^2] (65000 psi * 144)
        Sig_T = 65000.0 * 144.0  # allowable tensile stress [lb/ft^2] (65000 psi * 144)

        k = 6.09375

        # ------------------------------------------------------------------------------------------
        # REFORMULATION (magnitude-compressed ratio constraints, scalers[28:88]): every stress and
        # buckling constraint below has the canonical form  EXPR - 1 <= 0  where EXPR is a
        # dimensionless (a/b) ratio. At infeasible designs EXPR can reach extreme magnitudes
        # (O(1e17) and beyond), pushing the *scaled* constraint value far outside the
        # ScalerConstraint([-1, 1]) range. We replace the raw ratio EXPR by its power image
        #     EXPR  ->  sign(EXPR) * |EXPR|**exponent
        # so the constraint becomes  sign(EXPR)*|EXPR|**exponent - 1 <= 0. This map is strictly
        # increasing in EXPR, preserves the zero-crossing (|EXPR| = 1 -> 0) and the sign of EXPR - 1,
        # hence the FEASIBLE SET IS UNCHANGED while the constraint magnitude (and its scaled value)
        # is strongly compressed. The exponent is supplied per constraint at each call site below
        # (all 1/4, the original quarter-power).
        # (Per the warning-handling rule: abs(value) > 1E-4, bounds kept.)
        # ------------------------------------------------------------------------------------------
        def power_ratio(expr: np.ndarray, exponent: float) -> np.ndarray:
            """Return sign(expr)*|expr|**exponent: magnitude-compressed, sign/zero-crossing preserving."""
            expr = np.asarray(expr, dtype=float)
            return np.sign(expr) * np.abs(expr)**exponent

        # G1[0:3]   – compressive stress point 1
        inequality_unscaled.extend((power_ratio((k * sig_eq1) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[3:6]   – buckling point 1 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_1 / sig_cr1 + (tau1 / tau_cr1)**2), 1.0 / 4.0) - 1).tolist())
        # G1[6:9]   – buckling point 1 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_1 / sig_cr1 + (tau1 / tau_cr1)**2), 1.0 / 4.0) - 1).tolist())
        # G1[9:12]  – compressive stress point 2
        inequality_unscaled.extend((power_ratio((k * sig_eq2) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[12:15] – buckling point 2 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_2 / sig_cr2 + (tau2 / tau_cr2)**2), 1.0 / 8.0) - 1).tolist())
        # G1[15:18] – buckling point 2 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_2 / sig_cr2 + (tau2 / tau_cr2)**2), 1.0 / 8.0) - 1).tolist())
        # G1[18:21] – compressive stress point 3
        inequality_unscaled.extend((power_ratio((k * sig_eq3) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[21:24] – buckling point 3 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_3 / sig_cr3 + (tau3 / tau_cr3)**2), 1.0 / 4.0) - 1).tolist())
        # G1[24:27] – buckling point 3 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_3 / sig_cr3 + (tau3 / tau_cr3)**2), 1.0 / 4.0) - 1).tolist())
        # G1[27:30] – tensile stress point 4
        inequality_unscaled.extend((power_ratio((k * sig_eq4) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[30:33] – tensile stress point 5
        inequality_unscaled.extend((power_ratio((k * sig_eq5) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[33:36] – buckling point 5 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_5 / sig_cr5 + (tau5 / tau_cr5)**2), 1.0 / 8.0) - 1).tolist())
        # G1[36:39] – buckling point 5 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_5 / sig_cr5 + (tau5 / tau_cr5)**2), 1.0 / 8.0) - 1).tolist())
        # G1[39:42] – tensile stress point 6
        inequality_unscaled.extend((power_ratio((k * sig_eq6) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # ------------------------------------------------------------------------------------------
        # REFORMULATION (see SubSystem3_Reformulation.md): the two division-based families
        # G1[42:45] (0.5(ts1+ts3)/h_spar - 1) and G1[45:54] (t/(ts - 0.1 t) - 1) are REMOVED here.
        # They are reproduced, division-free, by the depth-relative parametrization: the t/ts core
        # ratio becomes the box bound rho <= 1/1.1, and the h_spar margin becomes the linear
        # constraint appended below. The sign-flip stress block that previously followed at G1[54:72]
        # now immediately follows G1[39:42], so the kept stress/buckling scalers stay positionally
        # aligned once the matching 12 scalers are removed in InputFile.py.
        # ------------------------------------------------------------------------------------------
        # Sign-flip stress families (scalers[70:88]) share the same EXPR - 1 <= 0 structure, so the
        # same magnitude-compressing power map is applied (feasible set unchanged).
        # G1[54:57] – tensile stress point 1 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq1) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[57:60] – tensile stress point 2 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq2) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[60:63] – tensile stress point 3 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq3) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[63:66] – compressive stress point 4 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq4) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[66:69] – compressive stress point 5 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq5) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[69:72] – compressive stress point 6 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq6) / Sig_T, 1.0 / 4.0) - 1).tolist())

        # ------------------------------------------------------------------------------------------
        # REFORMULATION: constraints appended at the END of the inequality list (see
        # SubSystem3_Reformulation.md §4/§6.4). Appending keeps the positional scaler mapping of all
        # the kept stress/buckling constraints undisturbed; the matching scalers are appended in the
        # same order in InputFile.py.
        #
        # (a) h_spar margin (replaces division-based G1[42:45]) -- one per spanwise station:
        #         alpha1_i + alpha3_i - 0.5 <= 0   <=>   ts1_i + ts3_i <= D_i   <=>   0.5(ts1+ts3) <= h_spar
        #     computed in calculate_structural_responses and read here from responses[93:96].
        hspar_margin = np.array(responses[93:96])
        inequality_unscaled.extend(hspar_margin.tolist())

        # (b) Absolute-gauge inequalities. Because ts1/ts3/t1..t3 are now depth-relative, the original
        #     box gauges (ts in [0.1,9] in, t in [0.1,4] in) are re-imposed as lower AND upper
        #     inequalities. ts2 keeps its hard box bound (still an absolute design variable), so only
        #     its skin t2 needs a gauge pair. t/ts in `responses[75:93]` are in FEET, so the gauges
        #     are compared in feet: 0.1 in = 0.1/12 ft, 9 in = 9/12 ft, 4 in = 4/12 ft.
        ts_lo = 0.1 / 12.0   # 0.1 in in feet
        ts_hi = 9.0 / 12.0   # 9.0 in in feet
        t_lo  = 0.1 / 12.0   # 0.1 in in feet
        t_hi  = 4.0 / 12.0   # 4.0 in in feet
        # top sandwich ts1: lower then upper
        inequality_unscaled.extend((ts_lo - ts1).tolist())
        inequality_unscaled.extend((ts1 - ts_hi).tolist())
        # bottom sandwich ts3: lower then upper
        inequality_unscaled.extend((ts_lo - ts3).tolist())
        inequality_unscaled.extend((ts3 - ts_hi).tolist())
        # skin t1: lower then upper
        inequality_unscaled.extend((t_lo - t1).tolist())
        inequality_unscaled.extend((t1 - t_hi).tolist())
        # skin t2: lower then upper
        inequality_unscaled.extend((t_lo - t2).tolist())
        inequality_unscaled.extend((t2 - t_hi).tolist())
        # skin t3: lower then upper
        inequality_unscaled.extend((t_lo - t3).tolist())
        inequality_unscaled.extend((t3 - t_hi).tolist())
        # ------------------------------------------------------------------------------------------

        # scale the inequality Local constraint evaluation
        # 93 inequality constraints (72 - 12 removed + 33 added) -> scalers[28:121]
        scl: List[ScalerConstraint] = scalers[28:121]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # inequality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None