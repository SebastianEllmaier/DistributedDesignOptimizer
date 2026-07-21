---
title: CopyFromMiddleLevel()
---

# CopyFromMiddleLevel()

<div class="algorithm" markdown="0">
<div class="algorithm-caption"><strong>Procedure</strong> SubSystemBasis.CopyFromMiddleLevel()</div>
<div class="algo-body">
<div class="algo-line algo-indent-0"><span><span class="algo-keyword">for every</span> MiddleLevelDataStorage <span class="algo-keyword">in</span> self._middlelevels <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-1"><span>Get MiddleLevelDataStorage ID pair [id_parent, id_child]</span></div>
<div class="algo-line algo-indent-1"><span>Determine neighbor ID from the pair (the one ≠ self._subsystemid)</span></div>
<div class="algo-line algo-indent-1"><span>Acquire multiprocessing lock and read neighbor coupling data from storage</span></div>
<div class="algo-line algo-indent-1"><span>Find matching CouplingParameters by neighbor ID</span></div>
<div class="algo-line algo-indent-1"><span>Copy from MiddleLevelCoupling into local CouplingParameters <span class="algo-comment">▷ polymorphic</span></span></div>
<div class="algo-line algo-indent-2"><span>Read MappedResponseVariables → store as CopyMappedResponseVariables</span></div>
<div class="algo-line algo-indent-2"><span>Read CouplingVariable → store as CopyCouplingVariable</span></div>
<div class="algo-line algo-indent-2"><span>Read SharedDesignVariables → store as CopySharedDesignVariables</span></div>
<div class="algo-line algo-indent-2"><span>Read TargetSharedDesignVariables → store as CopyTargetSharedDesignVariables</span></div>
<div class="algo-line algo-indent-0"><span><span class="algo-keyword">end for</span></span></div>
</div>
</div>
