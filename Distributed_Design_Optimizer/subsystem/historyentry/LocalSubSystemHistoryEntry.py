# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local subsystem history entry module.

This module provides the history log entry for a local subsystem, extending the
subsystem history entry with scaler and inconsistency snapshots.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.historyentry import SubSystemHistoryEntry
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import LocalSubSystemOptimData
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface


class LocalSubSystemHistoryEntry(SubSystemHistoryEntry):
    """History log entry for a local subsystem.

    Extends SubSystemHistoryEntry with the scalers, inconsistencies and maximum
    inconsistency information that only exist for local subsystems.
    """

    def __init__(self,
                 subsystem_id: str,
                 outerloop_itr: int,
                 innerloop_itr: int,
                 innerloop_itr_runtime: float | None,
                 innerloop_itr_numberofdesignvariableevaluations: int | None,
                 optimdata: LocalSubSystemOptimData,
                 convinnerloop: bool,
                 convouterloop: bool,
                 scalers: List[ScalerBasis],
                 inconsistencies: List[InConsistencySizeInterface],
                 maxinconsistencyvalue: float | None,
                 maxinconsistencysubsystemID: str | None
                 ) -> None:
        """Create a new LocalSubSystemHistoryEntry.

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
            scalers: Snapshot of the subsystem's scalers.
            inconsistencies: Snapshot of the subsystem's inconsistencies.
            maxinconsistencyvalue: Maximum inconsistency value of this snapshot.
            maxinconsistencysubsystemID: Identifier of the coupled subsystem with
                the maximum inconsistency.
        """
        super().__init__(subsystem_id=subsystem_id,
                         outerloop_itr=outerloop_itr,
                         innerloop_itr=innerloop_itr,
                         innerloop_itr_runtime=innerloop_itr_runtime,
                         innerloop_itr_numberofdesignvariableevaluations=innerloop_itr_numberofdesignvariableevaluations,
                         optimdata=optimdata,
                         convinnerloop=convinnerloop,
                         convouterloop=convouterloop)

        self._scalers: List[ScalerBasis] = scalers
        self._inconsistencies: List[InConsistencySizeInterface] = inconsistencies
        self._maxinconsistencyvalue: float | None = maxinconsistencyvalue
        self._maxinconsistencysubsystemID: str | None = maxinconsistencysubsystemID

    def get_OptimData(self) -> LocalSubSystemOptimData:
        """Return the snapshot of the subsystem's optimization data.

        Returns:
            The local subsystem optimization data of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._optimdata

    def get_Scalers(self) -> List[ScalerBasis]:
        """Return the snapshot of the subsystem's scalers.

        Returns:
            The list of scalers of this snapshot.
        """
        # No copy - the stored list is the snapshot itself, returned by reference intentionally.
        return self._scalers

    def get_Inconsistencies(self) -> List[InConsistencySizeInterface]:
        """Return the snapshot of the subsystem's inconsistencies.

        Returns:
            The list of inconsistencies of this snapshot.
        """
        # No copy - the stored list is the snapshot itself, returned by reference intentionally.
        return self._inconsistencies

    def get_maxInconsistencyValue(self) -> float | None:
        """Return the maximum inconsistency value of this snapshot.

        Returns:
            The maximum inconsistency value, or None if not set.
        """
        # No copy needed - float is a primitive/immutable type.
        return self._maxinconsistencyvalue

    def get_MaxInconsistencyCoupledSubsystemID(self) -> str | None:
        """Return the coupled subsystem identifier with the maximum inconsistency.

        Returns:
            The coupled subsystem identifier, or None if not set.
        """
        # No copy needed - str is a primitive/immutable type.
        return self._maxinconsistencysubsystemID
