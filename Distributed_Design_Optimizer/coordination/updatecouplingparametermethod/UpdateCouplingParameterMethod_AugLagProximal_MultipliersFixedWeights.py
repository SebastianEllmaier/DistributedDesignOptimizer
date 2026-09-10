# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""ALADIN coupling parameter update method.

This module implements the user-specified initialization strategy for all
ALADIN coupling parameters:

- Augmented Lagrangian multipliers and penalty weights (``initialweight``,
  ``initialmultiplier``): multipliers are updated via the augmented Lagrangian
  rule λ_new = λ_old + 2·w²·c(x); weights are held fixed.
- Proximal term parameters ν and Σ^i (``initial_nu``, ``initial_sigma_i``):
  the proximal matrix is initialized as ``initial_sigma_i * I`` and the
  penalty parameter as ``initial_nu``; both are held fixed across iterations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border, DDO_Color, Reset

from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface

if TYPE_CHECKING:
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemALADIN import LocalSubSystemALADIN


class UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights(UpdateCouplingParameterMethodInterface):
    """User-specified coupling parameter initialization for ALADIN.

    Combines the augmented Lagrangian multiplier/weight update rule with the
    user-specified initialization of the ALADIN proximal term parameters.

    Multiplier update rule: λ_new = λ_old + 2·w²·c(x)
    Weights: no update (ALADIN does not modify penalty weights)
    Proximal matrix: Σ^i = initial_sigma_i · I (fixed across iterations)
    Proximal penalty: ν = initial_nu (fixed across iterations)

    Attributes:
        _initialweight: Initial value for penalty weights (must be >= 0).
        _initialmultiplier: Initial value for Lagrange multipliers.
        _initial_nu: Initial value of the proximal penalty parameter ν
            (must be > 0).
        _initial_sigma_i: Diagonal entry for the initial proximal matrix Σ^i
            (must be > 0).  The full matrix is ``initial_sigma_i * I``.
    """

    def __init__(self,
                 initialweight: float,
                 initialmultiplier: float,
                 initial_nu: float,
                 initial_sigma_i: float) -> None:
        """Initialize the ALADIN coupling parameter method.

        Args:
            initialweight: Initial value for penalty weights.
                Must be >= 0.
            initialmultiplier: Initial value for Lagrange multipliers.
            initial_nu: Initial value of the proximal penalty parameter ν.
                Must be strictly positive.
            initial_sigma_i: Diagonal entry of the initial proximal matrix
                Σ^i = initial_sigma_i · I.  Must be strictly positive so
                that Σ^i is positive definite.
        """
        # Hyperparameter validation bounds:

        # initialweight: must be >= 0, should be in (0, 0.1]
        self._initialweight_allowed_min: float = 0.0                   # inclusive (>=)
        self._initialweight_allowed_max: float = float('inf')          # strict (<), inf bounds are always exclusive
        self._initialweight_rec_min: float = 0.0                       # strict (>)
        self._initialweight_rec_max: float = 0.1                       # inclusive (<=)

        # initialmultiplier: can be anything, should be 0
        self._initialmultiplier_allowed_min: float = float('-inf')     # strict (>), inf bounds are always exclusive
        self._initialmultiplier_allowed_max: float = float('inf')      # strict (<), inf bounds are always exclusive
        self._initialmultiplier_rec_min: float = 0.0                   # inclusive (>=)
        self._initialmultiplier_rec_max: float = 0.0                   # inclusive (<=)

        # initial_nu: must be > 0
        self._initial_nu_allowed_min: float = 0.0   # strict (>)
        self._initial_nu_allowed_max: float = float('inf')  # strict (<), inf always exclusive
        self._initial_nu_rec_min: float = 0.0                          # strict (>)
        self._initial_nu_rec_max: float = float('inf')                 # strict (<), inf bounds are always exclusive

        # initial_sigma_i: must be > 0
        self._initial_sigma_i_allowed_min: float = 0.0   # strict (>)
        self._initial_sigma_i_allowed_max: float = float('inf')  # strict (<)
        self._initial_sigma_i_rec_min: float = 0.0                     # strict (>)
        self._initial_sigma_i_rec_max: float = float('inf')            # strict (<), inf bounds are always exclusive

        # Set inputs
        self._initialweight: float = initialweight
        self._initialmultiplier: float = initialmultiplier
        self._initial_nu: float = initial_nu
        self._initial_sigma_i: float = initial_sigma_i

        # Validate inputs
        self.validate_inputs()

    ###########################################################################
    #   Validation
    ###########################################################################

    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== initialweight Validation =====
        # Allowed: >= 0 (inclusive), Recommended: (0, 0.1] (strict left, inclusive right)
        if not (self._initialweight_allowed_min <= self._initialweight < self._initialweight_allowed_max):
            raise ValueError(
                f"{DDO_Color}initialweight must be in [{self._initialweight_allowed_min}, "
                f"{self._initialweight_allowed_max}), but got {self._initialweight}.{Reset}"
            )
        elif not (self._initialweight_rec_min < self._initialweight <= self._initialweight_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: initialweight={self._initialweight} is outside the recommended range "
                      f"({self._initialweight_rec_min}, {self._initialweight_rec_max}].")
            ddo_print_border()

        # ===== initialmultiplier Validation =====
        # Allowed: all values, Recommended: 0
        if not (self._initialmultiplier_rec_min <= self._initialmultiplier <= self._initialmultiplier_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: initialmultiplier={self._initialmultiplier} is not the recommended value "
                      f"({self._initialmultiplier_rec_min}).")
            ddo_print_border()

        # ===== initial_nu Validation =====
        # Allowed: strictly positive
        if not (self._initial_nu_allowed_min < self._initial_nu < self._initial_nu_allowed_max):
            raise ValueError(
                f"{DDO_Color}initial_nu must be in ({self._initial_nu_allowed_min}, "
                f"{self._initial_nu_allowed_max}), but got {self._initial_nu}.{Reset}"
            )

        # ===== initial_sigma_i Validation =====
        # Allowed: strictly positive (ensures Σ^i = initial_sigma_i · I is positive definite)
        if not (self._initial_sigma_i_allowed_min < self._initial_sigma_i < self._initial_sigma_i_allowed_max):
            raise ValueError(
                f"{DDO_Color}initial_sigma_i must be in ({self._initial_sigma_i_allowed_min}, "
                f"{self._initial_sigma_i_allowed_max}), but got {self._initial_sigma_i}.{Reset}"
            )

    ###########################################################################
    #   Getters
    ###########################################################################

    def get_InitialWeight(self) -> float:
        """Get the initial penalty weight value.

        Returns:
            The initial penalty weight value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        return self._initialweight

    def get_InitialMultiplier(self) -> float:
        """Get the initial Lagrange multiplier value.

        Returns:
            The initial Lagrange multiplier value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        return self._initialmultiplier

    def get_Initial_Nu(self) -> float:
        """Get the initial value of the proximal penalty parameter ν.

        Returns:
            The initial ν value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        return self._initial_nu

    def get_Initial_Sigma_i(self) -> float:
        """Get the diagonal entry of the initial proximal matrix Σ^i.

        The full matrix used during initialization is ``initial_sigma_i * I``.

        Returns:
            The scalar diagonal entry of the initial proximal matrix.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        return self._initial_sigma_i

    ###########################################################################
    #   Initialization
    ###########################################################################

    def initialize_ProximalParameters(self, subsystem: 'Distributed_Design_Optimizer.subsystem.LocalSubSystemALADIN.LocalSubSystemALADIN') -> None:
        """Push the initial ν and Σ^i onto the subsystem.

        Called once inside
        ``LocalSubSystemALADIN.initializeCouplingParameters_before_CopyToMiddleLevel``
        to replace the hardcoded identity default with the user-specified values.

        Args:
            subsystem: The ALADIN local subsystem to initialize.
        """
        n: int = len(subsystem.get_DesignVariables())

        # Build Σ^i = initial_sigma_i * I
        sigma_i: List[List[float]] = [[self._initial_sigma_i if i == j else 0.0
                                       for j in range(n)]
                                      for i in range(n)]

        subsystem.set_Nu(self._initial_nu)
        subsystem.set_Sigma_i(sigma_i)

    ###########################################################################
    #   Multiplier / weight update
    ###########################################################################

    def update_CoordinationMultipliers(self,
                                       multiplierin: List[float],
                                       weightsin: List[float],
                                       inconsistencyin: List[float]) -> None:
        """Update Lagrange multipliers using the augmented Lagrangian rule.

        Update formula: λ_new = λ_old + 2 · w² · c(x)

        Args:
            multiplierin: Current multiplier values to update in place.
            weightsin: Current penalty weight values.
            inconsistencyin: Current inconsistency values.
        """
        for i in range(len(multiplierin)):
            multiplierin[i] = multiplierin[i] + 2 * weightsin[i] * weightsin[i] * inconsistencyin[i]

    def update_CoordinationWeights(self,
                                   weightin: List[float]) -> None:
        """ALADIN does not update penalty weights.

        Args:
            weightin: Current penalty weights.
        """
        # ALADIN does not update penalty weights
        pass

    def update_Proximal_nu(self) -> None:
        """Proximal penalty parameter ν is held fixed across iterations."""
        # ν = initial_nu (fixed across iterations)
        pass

    def update_Proximal_Sigma_i(self) -> None:
        """Proximal matrix Σ^i is held fixed across iterations."""
        # Σ^i = initial_sigma_i · I (fixed across iterations)
        pass

    ###########################################################################
    #   Interface methods
    ###########################################################################

    def print_startup_summary(self) -> None:
        """Print the coupling parameter configuration at startup."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     initialweight:       {self._initialweight}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)
        ddo_print(f"{pad}     initial_nu:          {self._initial_nu}", indent=1)
        ddo_print(f"{pad}     initial_sigma_i:     {self._initial_sigma_i}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the coupling parameter configuration at the end."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     initialweight:       {self._initialweight}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)
        ddo_print(f"{pad}     initial_nu:          {self._initial_nu}", indent=1)
        ddo_print(f"{pad}     initial_sigma_i:     {self._initial_sigma_i}", indent=1)

    def update_state(self, other: 'UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights') -> None:
        """Update the state of this instance with values from another instance.

        This method is necessary for multiprocessing.  When subsystems are
        executed in parallel using ``multiprocessing.Pool``, they are
        serialized and deserialized, creating new objects in separate memory
        spaces.  After parallel execution completes, this method updates the
        original object's attribute values.

        Args:
            other: The source instance containing updated values from
                parallel execution.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        self._initialweight = other._initialweight
        self._initialmultiplier = other._initialmultiplier
        self._initial_nu = other._initial_nu
        self._initial_sigma_i = other._initial_sigma_i
