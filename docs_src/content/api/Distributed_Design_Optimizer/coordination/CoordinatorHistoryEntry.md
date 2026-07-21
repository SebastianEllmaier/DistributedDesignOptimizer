---
title: CoordinatorHistoryEntry
---

← Back to [coordination](index.md)

# CoordinatorHistoryEntry

**Source:** [Distributed_Design_Optimizer\coordination\CoordinatorHistoryEntry.py](CoordinatorHistoryEntry_source.md)

Coordinator history entry module.

This module provides the history log entry for the coordinator. An entry is a
snapshot of selected coordinator-level state captured at one inner loop iteration.

## Classes

### CoordinatorHistoryEntry

> **Inherits from:** [HistoryEntry](../subsystem/historyentry/HistoryEntry.md#historyentry)

> History log entry for the coordinator.

> Extends HistoryEntry with the system-wide metrics and analysis summaries that
> the coordinator records for each inner loop iteration.

#### Methods

??? abstract "__init__(self, outerloop_itr: int, innerloop_itr: int, innerloop_itr_runtime: float | None, innerloop_itr_numberofdesignvariableevaluations: int | None, maxinconsistencyvalue: float, maxinconsistencyID: str, maxratioofactiveconstraints: float, maxratioofactiveconstraintsID: str, performancemetrics: [PerformanceMetrics](../postprocess/PerformanceMetrics.md#performancemetrics), centralitymeasures: Dict, compromisemeasures: Dict, inconsistencyoscillationindex: Dict, clusteranalysis: Dict, couplingstrength: Dict[Tuple[str, str], float], mastergraph: nx.MultiDiGraph) → None"
    Create a new CoordinatorHistoryEntry.


    **Args:**
    > outerloop_itr: Outer loop iteration number of this snapshot.  
    > innerloop_itr: Inner loop iteration number of this snapshot.  
    > innerloop_itr_runtime: Runtime of the inner loop iteration.  
    > innerloop_itr_numberofdesignvariableevaluations: Number of design  
    > variable evaluations of the inner loop iteration.  
    > maxinconsistencyvalue: Maximum inconsistency value across all subsystems.  
    > maxinconsistencyID: Identifier of the subsystem with the maximum inconsistency.  
    > maxratioofactiveconstraints: Maximum ratio of active constraints across all subsystems.  
    > maxratioofactiveconstraintsID: Identifier of the subsystem with the maximum ratio of active constraints.  
    > performancemetrics: Snapshot of the coordinator performance metrics.  
    > centralitymeasures: Snapshot of the centrality measures summary.  
    > compromisemeasures: Snapshot of the compromise measures summary.  
    > inconsistencyoscillationindex: Snapshot of the inconsistency oscillation index summary.  
    > clusteranalysis: Snapshot of the cluster analysis summary.  
    > couplingstrength: Snapshot of the coupling strength summary.  
    > mastergraph: Snapshot of the master graph.  

??? abstract "get_MaxInconsistencyValue(self) → float"
    Return the maximum inconsistency value across all subsystems.


    **Returns:**
    > The maximum inconsistency value.  

??? abstract "get_MaxInconsistencyValueSubsystemID(self) → str"
    Return the identifier of the subsystem with the maximum inconsistency.


    **Returns:**
    > The subsystem identifier.  

??? abstract "get_MaxRatioOfActiveConstraints(self) → float"
    Return the maximum ratio of active constraints across all subsystems.


    **Returns:**
    > The maximum ratio of active constraints.  

??? abstract "get_MaxRatioOfActiveConstraintsSubsystemID(self) → str"
    Return the identifier of the subsystem with the maximum ratio of active constraints.


    **Returns:**
    > The subsystem identifier.  

??? abstract "get_PerformanceMetrics(self) → [PerformanceMetrics](../postprocess/PerformanceMetrics.md#performancemetrics)"
    Return the snapshot of the coordinator performance metrics.


    **Returns:**
    > The performance metrics of this snapshot.  

??? abstract "get_CentralityMeasures(self) → Dict"
    Return the snapshot of the centrality measures summary.


    **Returns:**
    > The centrality measures summary of this snapshot.  

??? abstract "get_CompromiseMeasures(self) → Dict"
    Return the snapshot of the compromise measures summary.


    **Returns:**
    > The compromise measures summary of this snapshot.  

??? abstract "get_InConsistencyOscillationIndex(self) → Dict"
    Return the snapshot of the inconsistency oscillation index summary.


    **Returns:**
    > The inconsistency oscillation index summary of this snapshot.  

??? abstract "get_ClusterAnalysis(self) → Dict"
    Return the snapshot of the cluster analysis summary.


    **Returns:**
    > The cluster analysis summary of this snapshot.  

??? abstract "get_CouplingStrength(self) → Dict[Tuple[str, str], float]"
    Return the snapshot of the coupling strength summary.


    **Returns:**
    > The coupling strength summary of this snapshot.  

??? abstract "get_MasterGraph(self) → nx.MultiDiGraph"
    Return the snapshot of the master graph.


    **Returns:**
    > The master graph of this snapshot.  

