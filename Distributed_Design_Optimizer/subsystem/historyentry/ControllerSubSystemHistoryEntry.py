# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Controller subsystem history entry module.

This module provides the history log entry for the controller subsystem. The
controller holds the shared subsystem state only (no scalers or inconsistencies).
"""

from Distributed_Design_Optimizer.subsystem.historyentry import SubSystemHistoryEntry
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import ControllerOptimData


class ControllerSubSystemHistoryEntry(SubSystemHistoryEntry):
    """History log entry for the controller subsystem.

    Carries the same fields as SubSystemHistoryEntry; the dedicated type keeps
    the controller optimization data type explicit and distinguishes controller
    snapshots from local subsystem snapshots.
    """

    def __init__(self,
                 subsystem_id: str,
                 outerloop_itr: int,
                 innerloop_itr: int,
                 innerloop_itr_runtime: float | None,
                 innerloop_itr_numberofdesignvariableevaluations: int | None,
                 optimdata: ControllerOptimData,
                 convinnerloop: bool,
                 convouterloop: bool
                 ) -> None:
        """Create a new ControllerSubSystemHistoryEntry.

        Args:
            subsystem_id: Identifier of the controller subsystem.
            outerloop_itr: Outer loop iteration number of this snapshot.
            innerloop_itr: Inner loop iteration number of this snapshot.
            innerloop_itr_runtime: Runtime of the inner loop iteration.
            innerloop_itr_numberofdesignvariableevaluations: Number of design
                variable evaluations of the inner loop iteration.
            optimdata: Snapshot of the controller's optimization data.
            convinnerloop: Inner loop convergence flag.
            convouterloop: Outer loop convergence flag.
        """
        super().__init__(subsystem_id=subsystem_id,
                         outerloop_itr=outerloop_itr,
                         innerloop_itr=innerloop_itr,
                         innerloop_itr_runtime=innerloop_itr_runtime,
                         innerloop_itr_numberofdesignvariableevaluations=innerloop_itr_numberofdesignvariableevaluations,
                         optimdata=optimdata,
                         convinnerloop=convinnerloop,
                         convouterloop=convouterloop)

    def get_OptimData(self) -> ControllerOptimData:
        """Return the snapshot of the controller's optimization data.

        Returns:
            The controller optimization data of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._optimdata
