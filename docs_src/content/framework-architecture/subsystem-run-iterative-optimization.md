---
title: run_IterativeOptimization
---

# run_IterativeOptimization

<div class="algorithm" markdown="0">
<div class="algorithm-caption"><strong>Procedure</strong> SubSystemBasis.run_IterativeOptimization()</div>
<div class="algo-body">
<div class="algo-line algo-indent-0"><span>optimdata ← OptimizationBasis.callOptimizer(subsystem) <span class="algo-comment">▷ returns optimization results</span></span></div>
<div class="algo-line algo-indent-1"><span>SolverInterface.execute(subsystem) <span class="algo-comment">▷ dispatched to concrete solver</span></span></div>
<div class="algo-line algo-indent-1"><span>Retrieve design variable bounds and scaling</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">repeat</span> <span class="algo-comment">▷ solver iterations (objective callback)</span></span></div>
<div class="algo-line algo-indent-2"><span>Set current design variables</span></div>
<div class="algo-line algo-indent-2"><span>evaluateTotalObjective()</span></div>
<div class="algo-line algo-indent-3"><span>runAnalysis()</span></div>
<div class="algo-line algo-indent-4"><span>AnalysisInterface.evaluateLocalResponses() <span class="algo-comment">▷ user-defined</span></span></div>
<div class="algo-line algo-indent-3"><span>mapToCouplingParameters()</span></div>
<div class="algo-line algo-indent-4"><span>AnalysisInterface.mapLocalResponsesDesignVariables_to_CouplingParameters() <span class="algo-comment">▷ user-defined</span></span></div>
<div class="algo-line algo-indent-3"><span>evaluateLocalObjective()</span></div>
<div class="algo-line algo-indent-4"><span>LocalObjectiveInterface.evaluateLocalObjective() <span class="algo-comment">▷ user-defined</span></span></div>
<div class="algo-line algo-indent-3"><span>evaluateCoordinationObjective() <span class="algo-comment">▷ coordination-specific penalty/augmented terms</span></span></div>
<div class="algo-line algo-indent-3"><span>Combine: f = LocalObjective + CoordinationObjective</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span>evaluateTotalConstraint()</span></div>
<div class="algo-line algo-indent-3"><span>runAnalysis() <span class="algo-comment">▷ same as above</span></span></div>
<div class="algo-line algo-indent-3"><span>mapToCouplingParameters() <span class="algo-comment">▷ same as above</span></span></div>
<div class="algo-line algo-indent-3"><span>evaluateLocalConstraints()</span></div>
<div class="algo-line algo-indent-4"><span>LocalConstraintsInterface.evaluateEqualityLocalConstraints() <span class="algo-comment">▷ user-defined</span></span></div>
<div class="algo-line algo-indent-4"><span>LocalConstraintsInterface.evaluateInEqualityLocalConstraints() <span class="algo-comment">▷ user-defined</span></span></div>
<div class="algo-line algo-indent-3"><span>evaluateCoordinationEqualityConstraint() <span class="algo-comment">▷ coordination-specific</span></span></div>
<div class="algo-line algo-indent-3"><span>Combine: ceq = LocalEqConstraints + CoordinationEqConstraints</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> solver converged</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-0"><span>updateSubsystemfromOptimdata(optimdata)</span></div>
<div class="algo-line algo-indent-1"><span>Set optimal design variables, objectives, constraints</span></div>
<div class="algo-line algo-indent-1"><span>mapToCouplingParameters() <span class="algo-comment">▷ final coupling update</span></span></div>
<div class="algo-line algo-indent-1"><span>runAnalysis() <span class="algo-comment">▷ re-evaluate at optimum</span></span></div>
</div>
</div>
<div class="algo-line algo-indent-3"><span>evaluateCoordinationEqualityConstraint() <span class="algo-comment">▷ coordination-specific</span></span></div>
<div class="algo-line algo-indent-3"><span>Combine: ceq = LocalEqConstraints + CoordinationEqConstraints</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> solver converged</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-0"><span>updateSubsystemfromOptimdata(optimdata)</span></div>
<div class="algo-line algo-indent-1"><span>Set optimal design variables, objectives, constraints</span></div>
<div class="algo-line algo-indent-1"><span>mapToCouplingParameters() <span class="algo-comment">▷ final coupling update</span></span></div>
<div class="algo-line algo-indent-1"><span>runAnalysis() <span class="algo-comment">▷ re-evaluate at optimum</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">end procedure</span></span></div>
</div>
</div>
