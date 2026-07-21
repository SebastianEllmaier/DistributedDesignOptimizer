---
title: CopyToMiddleLevel()
---

# CopyToMiddleLevel()

<div class="algorithm" markdown="0">
<div class="algorithm-caption"><strong>Procedure</strong> SubSystemBasis.CopyToMiddleLevel()</div>
<div class="algo-body">
<div class="algo-line algo-indent-0"><span><span class="algo-keyword">for every</span> MiddleLevelDataStorage <span class="algo-keyword">in</span> self._middlelevels <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> CouplingParameters <span class="algo-keyword">in</span> self._couplingparameters <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-2"><span>Match CouplingParameters.ID against MiddleLevelDataStorage.ID pair</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">if</span> match found <span class="algo-keyword">then</span></span></div>
<div class="algo-line algo-indent-3"><span>Acquire multiprocessing lock on MiddleLevelDataStorage</span></div>
<div class="algo-line algo-indent-3"><span>Determine storage slot (parent=0, child=1) from ID pair</span></div>
<div class="algo-line algo-indent-3"><span>Copy from CouplingParameters into MiddleLevelCoupling <span class="algo-comment">▷ polymorphic</span></span></div>
<div class="algo-line algo-indent-4"><span>Write MappedResponseVariables → MiddleLevelCoupling</span></div>
<div class="algo-line algo-indent-4"><span>Write CouplingVariable → MiddleLevelCoupling</span></div>
<div class="algo-line algo-indent-4"><span>Write SharedDesignVariables → MiddleLevelCoupling</span></div>
<div class="algo-line algo-indent-4"><span>Write TargetSharedDesignVariables → MiddleLevelCoupling</span></div>
<div class="algo-line algo-indent-3"><span>Release multiprocessing lock</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end if</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line algo-indent-0"><span><span class="algo-keyword">end for</span></span></div>
</div>
</div>
