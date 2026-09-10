---
title: ControllerToLocalCouplingParameters (Source)
---

← Back to [ControllerToLocalCouplingParameters documentation](ControllerToLocalCouplingParameters.md)

# ControllerToLocalCouplingParameters - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\ControllerToLocalCouplingParameters.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Controller to local coupling parameters module.

This module provides parameters for coupling from controller
to local subsystems in ALADIN.
"""
# TODO: Not needed anymore, since it is not used in non-slack variable approach


class ControllerToLocalCouplingParameters:
    """This class is a part of the controller mapping between controller and local subsystem.

    It handles the communicated data that has an assignment to i <-> j pairs.
    """
    
    def __init__(self, id: str) -> None:
        """Initialize controller to local coupling parameters.

        Args:
            id: Identifier of the local subsystem j to which subsystem i is coupled.
        """
        
        # Id of local subsystem j to which subsystem i is coupled to
        self._id: str = id
        
        # Provision: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
        
        # # Slack variables from controller w.r.t. i <-> j coupling
        # # from QP subproblem
        # self._tauleft: List[float] | None = None
        # self._tauright: List[float] | None = None
        # self._taushareddesignvar: List[float] | None = None
        # self._tautargetshareddesignvar: List[float] | None = None

    def get_ID(self) -> str:
        """Return the ID.

        Returns:
            The identifier of the coupled local subsystem.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._id
    
    # def get_TauLeft(self) -> List[float] | None:
    #     """Return the slack variables corresponding to the constraints of the QP where subsystem i's mapped responses appear.

    #     Returns:
    #         List[float] | None: The left slack variables, or None if not set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     return copy.copy(self._tauleft)
    
    # def set_TauLeft(self, tauleftin: List[float]) -> None:
    #     """Set the slack variables corresponding to the constraints of the QP where subsystem i's mapped responses appear.

    #     Args:
    #         tauleftin: The left slack variables to set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     self._tauleft = copy.copy(tauleftin)
        
    # def get_TauRight(self) -> List[float] | None:
    #     """Return the slack variables corresponding to the constraints of the QP where subsystem i's coupling variables appear.

    #     Returns:
    #         List[float] | None: The right slack variables, or None if not set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     return copy.copy(self._tauright)
    
    # def set_TauRight(self, taurightin: List[float]) -> None:
    #     """Set the slack variables corresponding to the constraints of the QP where subsystem i's coupling variables appear.

    #     Args:
    #         taurightin: The right slack variables to set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     self._tauright = copy.copy(taurightin)
    
    # def get_TauSharedDesignVariables(self) -> List[float] | None:
    #     """Return the slack variables corresponding to the constraints of the QP where subsystem i's shared design variables appear.

    #     Returns:
    #         List[float] | None: The shared design variable slack variables, or None if not set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     return copy.copy(self._taushareddesignvar)
    
    # def set_TauSharedDesignVariables(self, taushareddesignvarin: List[float]) -> None:
    #     """Set the slack variables corresponding to the constraints of the QP where subsystem i's shared design variables appear.

    #     Args:
    #         taushareddesignvarin: The shared design variable slack variables to set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     self._taushareddesignvar = copy.copy(taushareddesignvarin)
        
    # def get_TauTargetSharedDesignVariables(self) -> List[float] | None:
    #     """Return the slack variables corresponding to the constraints of the QP where subsystem i's target shared design variables appear.

    #     Returns:
    #         List[float] | None: The target shared design variable slack variables, or None if not set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     return copy.copy(self._tautargetshareddesignvar)
    
    # def set_TauTargetSharedDesignVariables(self, tautargetshareddesignvarin: List[float]) -> None:
    #     """Set the slack variables corresponding to the constraints of the QP where subsystem i's target shared design variables appear.

    #     Args:
    #         tautargetshareddesignvarin: The target shared design variable slack variables to set.
    #     """
    #     # copy.copy() used - List[float] is mutable. This prevents modifications
    #     # in the caller from being reflected back to the class attribute.
    #     self._tautargetshareddesignvar = copy.copy(tautargetshareddesignvarin)
        
            
    def update_state(self, other_coupling: 'ControllerToLocalCouplingParameters') -> None:
        """Update the state of this object from another ControllerToLocalCouplingParameters.

        This method is necessary for multiprocessing: when subsystems are executed
        in parallel via Parallel.py using multiprocessing.Pool, each process
        receives a copy of the data. After execution, the original objects must be
        updated with results from the executed copies. This method updates the
        numerical information stored in the class's attributes without changing
        the original memory address location, preserving object identity.

        Attributes are updated in the same order as defined in __init__().

        Args:
            other_coupling: Source instance to copy state from.
        """
        # _id: str - direct assignment (str is immutable, no copy.copy() needed)
        self._id: str = other_coupling.get_ID()
        
        # Provision: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
        
        # self._tauleft: List[float] | None = update_state_listprimitive(self._tauleft, other_coupling.get_TauLeft())        
        # self._tauright: List[float] | None = update_state_listprimitive(self._tauright, other_coupling.get_TauRight())        
        # self._taushareddesignvar: List[float] | None = update_state_listprimitive(self._taushareddesignvar, other_coupling.get_TauSharedDesignVariables())        
        # self._tautargetshareddesignvar: List[float] | None = update_state_listprimitive(self._tautargetshareddesignvar, other_coupling.get_TauTargetSharedDesignVariables())
```
