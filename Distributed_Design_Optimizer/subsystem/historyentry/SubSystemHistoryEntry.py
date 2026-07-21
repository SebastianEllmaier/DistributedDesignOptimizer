# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Subsystem history entry module.

This module provides the base class for a single subsystem history log entry,
shared by local subsystems and the controller subsystem.
"""

from Distributed_Design_Optimizer.subsystem.historyentry import HistoryEntry
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis


class SubSystemHistoryEntry(HistoryEntry):
    """Base class for a single subsystem history log entry.

    Extends HistoryEntry with the state common to every subsystem snapshot
    (identifier, optimization data and convergence flags).
    """

    def __init__(self,
                 subsystem_id: str,
                 outerloop_itr: int,
                 innerloop_itr: int,
                 innerloop_itr_runtime: float | None,
                 innerloop_itr_numberofdesignvariableevaluations: int | None,
                 optimdata: OptimDataBasis,
                 convinnerloop: bool,
                 convouterloop: bool
                 ) -> None:
        """Create a new SubSystemHistoryEntry.

        Args:
            subsystem_id: Identifier of the subsystem this snapshot belongs to.
            outerloop_itr: Outer loop iteration number of this snapshot.
            innerloop_itr: Inner loop iteration number of this snapshot.
            innerloop_itr_runtime: Runtime of the inner loop iteration.
            innerloop_itr_numberofdesignvariableevaluations: Number of design
                variable evaluations of the inner loop iteration.
            optimdata: Snapshot of the subsystem's optimization data.
            convinnerloop: Inner loop convergence flag.
            convouterloop: Outer loop convergence flag.
        """
        super().__init__(outerloop_itr=outerloop_itr,
                         innerloop_itr=innerloop_itr,
                         innerloop_itr_runtime=innerloop_itr_runtime,
                         innerloop_itr_numberofdesignvariableevaluations=innerloop_itr_numberofdesignvariableevaluations)

        self._subsystem_id: str = subsystem_id
        self._optimdata: OptimDataBasis = optimdata
        self._convinnerloop: bool = convinnerloop
        self._convouterloop: bool = convouterloop

    def get_SUBSYSTEMID(self) -> str:
        """Return the identifier of the subsystem this snapshot belongs to.

        Returns:
            The subsystem identifier.
        """
        # No copy needed - str is a primitive/immutable type.
        return self._subsystem_id

    def get_OptimData(self) -> OptimDataBasis:
        """Return the snapshot of the subsystem's optimization data.

        Returns:
            The optimization data of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._optimdata

    def get_ConvInnerLoop(self) -> bool:
        """Return the inner loop convergence flag of this snapshot.

        Returns:
            True if the subsystem was inner loop converged, False otherwise.
        """
        # No copy needed - bool is a primitive/immutable type.
        return self._convinnerloop

    def get_ConvOuterLoop(self) -> bool:
        """Return the outer loop convergence flag of this snapshot.

        Returns:
            True if the subsystem was outer loop converged, False otherwise.
        """
        # No copy needed - bool is a primitive/immutable type.
        return self._convouterloop
