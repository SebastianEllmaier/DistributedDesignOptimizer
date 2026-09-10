---
title: CoordinatorHistoryEntry (Source)
---

← Back to [CoordinatorHistoryEntry documentation](CoordinatorHistoryEntry.md)

# CoordinatorHistoryEntry - Source Code

**File:** `Distributed_Design_Optimizer\coordination\CoordinatorHistoryEntry.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Coordinator history entry module.

This module provides the history log entry for the coordinator. An entry is a
snapshot of selected coordinator-level state captured at one inner loop iteration.
"""

from typing import Dict, Tuple
import networkx as nx
from Distributed_Design_Optimizer.subsystem.historyentry import HistoryEntry
from Distributed_Design_Optimizer.postprocess import PerformanceMetrics


class CoordinatorHistoryEntry(HistoryEntry):
    """History log entry for the coordinator.

    Extends HistoryEntry with the system-wide metrics and analysis summaries that
    the coordinator records for each inner loop iteration.
    """

    def __init__(self,
                 outerloop_itr: int,
                 innerloop_itr: int,
                 innerloop_itr_runtime: float | None,
                 innerloop_itr_numberofdesignvariableevaluations: int | None,
                 maxinconsistencyvalue: float,
                 maxinconsistencyID: str,
                 maxratioofactiveconstraints: float,
                 maxratioofactiveconstraintsID: str,
                 performancemetrics: PerformanceMetrics,
                 centralitymeasures: Dict,
                 compromisemeasures: Dict,
                 inconsistencyoscillationindex: Dict,
                 clusteranalysis: Dict,
                 couplingstrength: Dict[Tuple[str, str], float],
                 mastergraph: nx.MultiDiGraph
                 ) -> None:
        """Create a new CoordinatorHistoryEntry.

        Args:
            outerloop_itr: Outer loop iteration number of this snapshot.
            innerloop_itr: Inner loop iteration number of this snapshot.
            innerloop_itr_runtime: Runtime of the inner loop iteration.
            innerloop_itr_numberofdesignvariableevaluations: Number of design
                variable evaluations of the inner loop iteration.
            maxinconsistencyvalue: Maximum inconsistency value across all subsystems.
            maxinconsistencyID: Identifier of the subsystem with the maximum inconsistency.
            maxratioofactiveconstraints: Maximum ratio of active constraints across all subsystems.
            maxratioofactiveconstraintsID: Identifier of the subsystem with the maximum ratio of active constraints.
            performancemetrics: Snapshot of the coordinator performance metrics.
            centralitymeasures: Snapshot of the centrality measures summary.
            compromisemeasures: Snapshot of the compromise measures summary.
            inconsistencyoscillationindex: Snapshot of the inconsistency oscillation index summary.
            clusteranalysis: Snapshot of the cluster analysis summary.
            couplingstrength: Snapshot of the coupling strength summary.
            mastergraph: Snapshot of the master graph.
        """
        super().__init__(outerloop_itr=outerloop_itr,
                         innerloop_itr=innerloop_itr,
                         innerloop_itr_runtime=innerloop_itr_runtime,
                         innerloop_itr_numberofdesignvariableevaluations=innerloop_itr_numberofdesignvariableevaluations)

        self._maxinconsistencyvalue: float = maxinconsistencyvalue
        self._maxinconsistencyID: str = maxinconsistencyID
        self._maxratioofactiveconstraints: float = maxratioofactiveconstraints
        self._maxratioofactiveconstraintsID: str = maxratioofactiveconstraintsID
        self._performancemetrics: PerformanceMetrics = performancemetrics
        self._centralitymeasures: Dict = centralitymeasures
        self._compromisemeasures: Dict = compromisemeasures
        self._inconsistencyoscillationindex: Dict = inconsistencyoscillationindex
        self._clusteranalysis: Dict = clusteranalysis
        self._couplingstrength: Dict[Tuple[str, str], float] = couplingstrength
        self._mastergraph: nx.MultiDiGraph = mastergraph

    def get_MaxInconsistencyValue(self) -> float:
        """Return the maximum inconsistency value across all subsystems.

        Returns:
            The maximum inconsistency value.
        """
        # No copy needed - float is a primitive/immutable type.
        return self._maxinconsistencyvalue

    def get_MaxInconsistencyValueSubsystemID(self) -> str:
        """Return the identifier of the subsystem with the maximum inconsistency.

        Returns:
            The subsystem identifier.
        """
        # No copy needed - str is a primitive/immutable type.
        return self._maxinconsistencyID

    def get_MaxRatioOfActiveConstraints(self) -> float:
        """Return the maximum ratio of active constraints across all subsystems.

        Returns:
            The maximum ratio of active constraints.
        """
        # No copy needed - float is a primitive/immutable type.
        return self._maxratioofactiveconstraints

    def get_MaxRatioOfActiveConstraintsSubsystemID(self) -> str:
        """Return the identifier of the subsystem with the maximum ratio of active constraints.

        Returns:
            The subsystem identifier.
        """
        # No copy needed - str is a primitive/immutable type.
        return self._maxratioofactiveconstraintsID

    def get_PerformanceMetrics(self) -> PerformanceMetrics:
        """Return the snapshot of the coordinator performance metrics.

        Returns:
            The performance metrics of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._performancemetrics

    def get_CentralityMeasures(self) -> Dict:
        """Return the snapshot of the centrality measures summary.

        Returns:
            The centrality measures summary of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._centralitymeasures

    def get_CompromiseMeasures(self) -> Dict:
        """Return the snapshot of the compromise measures summary.

        Returns:
            The compromise measures summary of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._compromisemeasures

    def get_InConsistencyOscillationIndex(self) -> Dict:
        """Return the snapshot of the inconsistency oscillation index summary.

        Returns:
            The inconsistency oscillation index summary of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._inconsistencyoscillationindex

    def get_ClusterAnalysis(self) -> Dict:
        """Return the snapshot of the cluster analysis summary.

        Returns:
            The cluster analysis summary of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._clusteranalysis

    def get_CouplingStrength(self) -> Dict[Tuple[str, str], float]:
        """Return the snapshot of the coupling strength summary.

        Returns:
            The coupling strength summary of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._couplingstrength

    def get_MasterGraph(self) -> nx.MultiDiGraph:
        """Return the snapshot of the master graph.

        Returns:
            The master graph of this snapshot.
        """
        # No copy - the stored object is the snapshot itself, returned by reference intentionally.
        return self._mastergraph

```
