---
title: Data Logging
---

# Data Logging

Various data is generated while the abbr:DDO framework executes a coordination method for some distributed design optimization problem from [`userfiles`](../api/userfiles/index.md). Some of this data is necessary for the coordination algorithm itself (e.g. change of objective function value or coupling constraint violation from previous to current iterations for convergence criteria), while other data is used for processing the algorithm behavior as detailed in [Tutorial > Processing](../tutorial/processing/index.md). Furthermore, the data may be only available within an individual [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) processing unit or aggregated in the [`Coordinator`](../api/Distributed_Design_Optimizer/coordination/Coordinator.md). 

Each instance of [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md), [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md) holds a `subsystemhistory` attribute, while the [`Coordinator`](../api/Distributed_Design_Optimizer/coordination/Coordinator.md) holds a `coordinatorhistory` attribute. These are implemented as a `deque` (queue) to which a *snapshot* of relevant information of the instance itself is appended periodically at the end of every `Coordinator.innerloop_iteration()`.

Each snapshot is stored as a dedicated, typed *history entry* object. The entry classes form a small hierarchy that mirrors the producers of the history:

- [`HistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/HistoryEntry.md) &mdash; the neutral base class holding the iteration bookkeeping fields (`outerloop_itr`, `innerloop_itr`, `innerloop_itr_runtime`, `innerloop_itr_numberofdesignvariableevaluations`) common to every producer.
- [`SubSystemHistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/SubSystemHistoryEntry.md) &mdash; extends [`HistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/HistoryEntry.md) with the state common to every subsystem snapshot (`subsystem_id`, `optimdata`, convergence flags).
    - [`LocalSubSystemHistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/LocalSubSystemHistoryEntry.md) &mdash; additionally captures the `scalers`, `inconsistencies` and maximum inconsistency information that only exist for local subsystems.
    - [`ControllerSubSystemHistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/ControllerSubSystemHistoryEntry.md) &mdash; the controller variant, which holds no scalers or inconsistencies.
- [`CoordinatorHistoryEntry`](../api/Distributed_Design_Optimizer/coordination/CoordinatorHistoryEntry.md) &mdash; extends [`HistoryEntry`](../api/Distributed_Design_Optimizer/subsystem/historyentry/HistoryEntry.md) with the system-wide metrics and analysis summaries recorded by the coordinator.

The `appendtohistory()` methods construct the appropriate entry, deep-copying the mutable snapshot data:


<div class="collapsible-code" markdown>

```python
class LocalSubSystemBasis(SubSystemBasis):

    def appendtohistory(self) -> None:
        """Append the current subsystem state to the history, including inconsistency data."""
        self._subsystemhistory.append(LocalSubSystemHistoryEntry(subsystem_id=self.get_SUBSYSTEMID(),
                                                                 outerloop_itr=self.get_OuterLoop_Itr(),
                                                                 innerloop_itr=self.get_InnerLoop_Itr(),
                                                                 innerloop_itr_runtime=self.get_InnerLoop_Itr_Runtime(),
                                                                 innerloop_itr_numberofdesignvariableevaluations=self.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(),
                                                                 optimdata=copy.deepcopy(self.get_OptimData()),
                                                                 convinnerloop=self.get_ConvInnerLoop(),
                                                                 convouterloop=self.get_ConvOuterLoop(),
                                                                 scalers=copy.deepcopy(self.get_Scalers()),
                                                                 inconsistencies=copy.deepcopy(self.get_Inconsistencies()),
                                                                 maxinconsistencyvalue=self.get_maxInconsistencyValue(),
                                                                 maxinconsistencysubsystemID=self.get_MaxInconsistencyCoupledSubsystemID()
                                                                 ))
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class ControllerSubSystemBasis(SubSystemBasis):

    def appendtohistory(self) -> None:
        """Append the current controller state to the history."""
        self._subsystemhistory.append(ControllerSubSystemHistoryEntry(subsystem_id=self.get_SUBSYSTEMID(),
                                                                      outerloop_itr=self.get_OuterLoop_Itr(),
                                                                      innerloop_itr=self.get_InnerLoop_Itr(),
                                                                      innerloop_itr_runtime=self.get_InnerLoop_Itr_Runtime(),
                                                                      innerloop_itr_numberofdesignvariableevaluations=self.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(),
                                                                      optimdata=copy.deepcopy(self.get_OptimData()),
                                                                      convinnerloop=self.get_ConvInnerLoop(),
                                                                      convouterloop=self.get_ConvOuterLoop(),
                                                                      ))
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Coordinator:

    def appendtohistory(self) -> None:
        """Append current iteration state to the coordinator history."""
        self._coordinatorhistory.append(CoordinatorHistoryEntry(outerloop_itr=self._outerloop_itr,
                                                                innerloop_itr=self._innerloop_itr,
                                                                innerloop_itr_runtime=self._innerloop_itr_runtime,
                                                                innerloop_itr_numberofdesignvariableevaluations=self._innerloop_itr_numberofdesignvariableevaluations,
                                                                maxinconsistencyvalue=self.get_MaxInconsistencyValue(),
                                                                maxinconsistencyID=self.get_MaxInconsistencyValueSubsystemID(),
                                                                maxratioofactiveconstraints=self.get_MaxRatioOfActiveConstraints(),
                                                                maxratioofactiveconstraintsID=self.get_MaxRatioOfActiveConstraintsSubsystemID(),
                                                                performancemetrics=copy.deepcopy(self._performancemetric),
                                                                centralitymeasures=copy.deepcopy(self._centralitycomputer.get_centrality_summary()),
                                                                compromisemeasures=copy.deepcopy(self._compromisecomputer.get_compromise_summary()),
                                                                inconsistencyoscillationindex=copy.deepcopy(self._inconsistencyoscillationcomputer.get_InConsistencyOscillationIndex_summary()),
                                                                clusteranalysis=copy.deepcopy(self._clustercomputer.get_cluster_summary()),
                                                                couplingstrength=copy.deepcopy(self._couplingstrengthcomputer.get_couplingstrength()),
                                                                mastergraph=copy.deepcopy(self._mastergraph),
                                                                ))
```

</div>

The instance can read relevant data back from its history entries. 

Furthermore, the newly appended queue is pickled and stored as a `.dill` file into the use-case's `historyfiles/` folder (located at `userfiles/<usecasename>/historyfiles/` and created automatically if it does not yet exist) periodically at the end of every `Coordinator.innerloop_iteration()`. The folder location is derived automatically from the location of the use-case's `InputFile`, so the `.dill` files are stored alongside the use-case that produced them, independent of the directory from which the use-case's `main.py` is launched. These `.dill` files may then be accessed for processing the algorithm behavior as detailed in [Tutorial > Processing](../tutorial/processing/index.md).
