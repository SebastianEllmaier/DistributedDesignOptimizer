# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Coupling parameters basis module.

This module provides the base class for coupling parameters in
multilevel distributed optimization.
"""

from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface


class CouplingParametersBasis(CouplingParametersInterface):
    """Base implementation of coupling parameters storing the neighbor identifier.

    Provides the common ``_id`` attribute and its getter, shared by both
    subsystem-level and controller-level coupling parameter subclasses.
    """

    def __init__(self, id: str) -> None:
        """Initialize coupling parameters.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        self._id: str = id
        
    def get_ID(self) -> str:
        """Return the identifier of the neighboring subsystem.

        Returns:
            The neighbor identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._id

    def update_state(self, other_coupling: 'CouplingParametersBasis') -> None:
        """Update the state of this CouplingParametersBasis with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        For primitive/immutable types like str, direct assignment is safe since Python
        creates a new binding rather than modifying the original value.

        Args:
            other_coupling: The source CouplingParametersBasis containing updated values
                from parallel execution.
        """
        # Update _id (str) - direct assignment is safe for immutable types
        self._id: str = other_coupling.get_ID()
        
