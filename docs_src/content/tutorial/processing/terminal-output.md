---
title: Terminal Output
---

# Terminal Output

To monitor the execution of the abbr:DDO framework, various information is provided to the user through the terminal.
Messages originating from the abbr:DDO framework itself are printed in <span style="color:#035970; background-color:#333333; padding:0 4px; border-radius:3px">BLUE</span>, while those from third party packages (such as the selected optimizers solving each subsystem optimization problem) are printed in <span style="color:#FFFFFF; background-color:#333333; padding:0 4px; border-radius:3px">WHITE</span> to the terminal.


## 1. Startup

Upon starting the optimization as detailed in [Tutorial > Problem Definition and Algorithm Execution](../problem-definition-and-algorithm-execution/index.md#8-executing-the-coordination-method), a summary about the algorithm configuration is printed.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%%</span>
<span style="color:#035970">%%%                   Running DistributedDesignOptimizer</span>
<span style="color:#035970">%%%</span>
<span style="color:#035970">%%% Use-case name:           SSBJ</span>
<span style="color:#035970">%%% Coordination Method:     ALC</span>
<span style="color:#035970">%%% ALC: ConvergenceIndicator_Innerloop:</span>
<span style="color:#035970">%%%     ConvergenceIndicator_Innerloop_DeWit:     tolerancetotalobjective:     0.0005</span>
<span style="color:#035970">%%% ALC: ConvergenceIndicator_Outerloop:</span>
<span style="color:#035970">%%%     ConvergenceIndicator_Outerloop_DeWit:     toleranceconsistency:    1e-05</span>
<span style="color:#035970">%%% ALC: UpdateCouplingParameterMethod_Outerloop:</span>
<span style="color:#035970">%%%     UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights:     beta:                1.3</span>
<span style="color:#035970">%%%                                                                         gamma:               0.5</span>
<span style="color:#035970">%%%                                                                         initialweight:       0.01</span>
<span style="color:#035970">%%%                                                                         initialmultiplier:   0.0</span>
<span style="color:#035970">%%% ALC: IterationScheme:     SequentialForward</span>
<span style="color:#035970">%%%</span>
<span style="color:#035970">%%% Subsystems:</span>
<span style="color:#035970">%%%    SubSystem 0 (Level 0, 5 design variables)</span>
<span style="color:#035970">%%%    SubSystem 1 (Level 1, 2 design variables)</span>
<span style="color:#035970">%%%    SubSystem 2 (Level 1, 12 design variables)</span>
<span style="color:#035970">%%%    SubSystem 3 (Level 1, 26 design variables)</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>

## 2. Initialization

Next, the coordinator initializes all subsystems and their coupling parameters as defined in the [Unified Algorithmic Structure](../../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md).
This reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Initialization ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Initialization</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>

## 3. Beginning of (Innerloop) Iteration

The [Unified Algorithmic Structure](../../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md) alternates between inner and outer loops. The following terminal prints indicate the beginning of new iteration loops respectively.
Depending on the chosen [`innerloop_iterationscheme`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/index.md), the subsystem (and controller) tasks are executed in series or parallel in the innerloop. 

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Outerloop Iteration Nr. 0 ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Innerloop Iteration Nr. 0 (Outerloop Nr. 0) ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% SequentialForward: Starting InnerLoop Jobs Execution using Multiprocessing ...</span>
<span style="color:#035970">%%%                    Subsystems are executed one-at-a-time in forward index order</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>

## 4. Third-Party Optimization

The innerloop executes the selected third-party subsystem optimization algorithms which print their respective messages to the terminal.
As the subsystem optimization algorithms may run in parallel, their prints can overlap in the terminal. 

In case of the [SSBJ](../../examples/SSBJ/index.md) Example using [`Solver_PyNomadBBO`](../../api/Distributed_Design_Optimizer/subsystem/optimization/solver/Solver_PyNomadBBO.md) for all subsystems, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
BBE OBJ
1   0.560057
4   0.53506 
5   0.3382  
13   0.285214
37   0.28309 
47   0.222151
127   0.220054
131   0.179062
135   0.17699 
139   0.133883
150   0.085175
153   0.040006
163   0.002741
172   0.002726
...
...
...
964   0.002725
966   0.002725
A termination criterion is reached: No termination (all). Mesh minimum precision reached (Algo)

Best feasible solutions:    #87934 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097820905628    h =   0                      (L2)
                            #87947 ( 0.0620352 0 0.38802 5e-14 0.0461847 )      Evaluation OK    f =   0.00272500097819124805    h =   0                      (L2)
                            #87953 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097821125331    h =   0                      (L2)
                            #87958 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.0027250009781907272     h =   0                      (L2)
                            #87959 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097814034432    h =   0                      (L2)
                            #87964 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097813472555    h =   0                      (L2)
                            #87970 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097816308915    h =   0                      (L2)
                            #87976 ( 0.0620352 0 0.38802 0 0.0461847 )  Evaluation OK    f =   0.00272500097819318703    h =   0                      (L2)
... A total of 33 feasible solutions were found.

Best infeasible solutions:  #50632 ( 0.0621737 0 0.388101 2e-06 0.0461873 )     Evaluation OK    f =   0.00272703866752036297    h =   0.00000000000014292312 (L2)
                            #65884 ( 0.0620354 1.2436e-09 0.388019 1e-07 0.0461847 )    Evaluation OK    f =   0.00272504761560003446    h =   0.0000000000001        (L2)
                            #65893 ( 0.0620362 4.9744e-09 0.388018 4e-07 0.0461848 )    Evaluation OK    f =   0.00272518752339867944    h =   0.0000000000001662639  (L2)
                            #66991 ( 0.0620339 0 0.388017 0 0.0461848 ) Evaluation OK    f =   0.0027250072003177743     h =   0.0000000000001        (L2)
                            #67902 ( 0.0620252 1.74504e-09 0.388013 3.14868e-09 0.0461847 )     Evaluation OK    f =   0.00272500396694225384    h =   0.0000000000001        (L2)
                            #67903 ( 0.0620359 0 0.388019 5e-08 0.0461847 )     Evaluation OK    f =   0.00272502363135756522    h =   0.0000000000001        (L2)
                            #67899 ( 0.0620362 2e-08 0.388018 0 0.0461847 )     Evaluation OK    f =   0.00272502120124165593    h =   0.0000000000001        (L2)
                            #67912 ( 0.0619952 6.98016e-09 0.387994 1.25947e-08 0.0461847 )     Evaluation OK    f =   0.00272501292893865101    h =   0.0000000000001        (L2)
... A total of 126 infeasible solutions were found.

Blackbox evaluations:         1019
Total model evaluations:      72085
Cache hits:                   207
Total number of evaluations:  1226
...
...
...
BBE OBJ
1   0.000018
30   0.0     
48   0.0     
51   0.0     
54   0.0     
56   0.0     
58   0.0     
60   0.0     
62   0.0     
64   0.0     
66   0.0     
68   0.0     
70   0.0     
79   0.0     
103   0.0
...
...
...
1904   0.0     
2468   0.0     
A termination criterion is reached: No termination (all). Mesh minimum precision reached (Algo)

Best feasible solutions:    #2780 ( 0.04911 0.036962 )  Evaluation OK    f =   0.00000015800053834515    h =   0                      (L2)
                            #2788 ( 0.04926 0.036992 )  Evaluation OK    f =   0.00000015800053637113    h =   0                      (L2)
                            #2793 ( 0.0492 0.036992 )   Evaluation OK    f =   0.0000001580004582558     h =   0                      (L2)
                            #2794 ( 0.04922 0.037012 )  Evaluation OK    f =   0.00000015800053601107    h =   0                      (L2)
                            #2796 ( 0.04917 0.036982 )  Evaluation OK    f =   0.00000015800045922938    h =   0                      (L2)
                            #2801 ( 0.04915 0.036962 )  Evaluation OK    f =   0.00000015800054288442    h =   0                      (L2)
                            #2802 ( 0.0492 0.0369995 )  Evaluation OK    f =   0.00000015800047591424    h =   0                      (L2)
                            #2803 ( 0.04917 0.0369745 ) Evaluation OK    f =   0.00000015800047946704    h =   0                      (L2)
... A total of 4771 feasible solutions were found.

Best infeasible solutions:  #5503 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013240272254    h =   0.00000000179873402619 (L2)
                            #6090 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013243097827    h =   0.00000000179871089552 (L2)
                            #6089 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013237446681    h =   0.00000000179875715701 (L2)
                            #6411 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013240360161    h =   0.00000000179873171312 (L2)
                            #6412 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013240184346    h =   0.00000000179873633926 (L2)
                            #6788 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013240273717    h =   0.00000000179873381524 (L2)
                            #6789 ( 0.107247 0.252636 ) Evaluation OK    f =   0.0000072801324027079     h =   0.00000000179873423714 (L2)
                            #7182 ( 0.107247 0.252636 ) Evaluation OK    f =   0.00000728013240271677    h =   0.00000000179873401509 (L2)
... A total of 10 infeasible solutions were found.

Blackbox evaluations:         4950
Total model evaluations:      1947
Cache hits:                   192
Total number of evaluations:  5142
...
...
...
BBE OBJ
1   0.000188
2   0.000168
3   0.000106
5   0.000102
7   0.000072
20   0.000067
24   0.00003 
44   0.000026
82   0.000022
121   0.000001 
...
...
...
4333   0.0     
4334   0.0     
A termination criterion is reached: No termination (all). Mesh minimum precision reached (Algo)

Best feasible solutions:    #88407 ( 1 0.859623 0.646734 0.444232 0.666837 0.0909509 0.499923 0.499995 0.505547 0.0733582 0.0356785 0.53737 )   Evaluation OK    f =   0.00000032521780261866     h =   0                      (L2)
                            #88409 ( 0.999865 0.859622 0.646772 0.444235 0.666831 0.0909489 0.499922 0.499993 0.505546 0.0733608 0.0356773 0.537366 )   Evaluation OK    f =   0.00000032521780621309     h =   0                      (L2)
                            #88411 ( 1 0.859646 0.646741 0.444235 0.666837 0.0909504 0.499925 0.499993 0.505549 0.073359 0.0356752 0.53737 )    Evaluation OK    f =   0.00000032521780571125     h =   0                      (L2)
                            #88415 ( 1 0.859649 0.646741 0.444235 0.666834 0.0909475 0.499925 0.499999 0.505546 0.0733609 0.0356828 0.537371 )  Evaluation OK    f =   0.0000003252178092015      h =   0                      (L2)
                            #88416 ( 0.999893 0.859634 0.646758 0.444236 0.666839 0.0909483 0.499917 0.499999 0.505547 0.0733588 0.0356817 0.537369 )   Evaluation OK    f =   0.00000032521779922415     h =   0                      (L2)
                            #88417 ( 0.99984 0.85963 0.646775 0.444236 0.666842 0.090947 0.499912 0.500002 0.505547 0.0733577 0.0356832 0.537369 )      Evaluation OK    f =   0.00000032521780604919     h =   0                      (L2)
                            #88419 ( 0.999906 0.859643 0.646749 0.444235 0.666836 0.0909503 0.49992 0.499997 0.505546 0.0733607 0.0356839 0.53737 )     Evaluation OK    f =   0.00000032521780906915     h =   0                      (L2)
                            #88420 ( 0.999946 0.859655 0.646763 0.444239 0.666831 0.0909481 0.499922 0.499991 0.505551 0.0733601 0.0356743 0.537367 )   Evaluation OK    f =   0.00000032521780813622     h =   0                      (L2)
... A total of 8744 feasible solutions were found.

Best infeasible solutions:  #88490 ( 0.878779 0.601427 0.910983 0.218992 0.3552 0.632066 0.820715 0.851906 0.0253722 0.0999961 0.0635959 0.534607 )     Evaluation OK    f =   0.00009118964762737443     h =   0.0000000000001        (L2)
                            #88557 ( 0.878778 0.601431 0.910982 0.218992 0.3552 0.632066 0.820713 0.851905 0.0253722 0.0999958 0.0635955 0.534607 )     Evaluation OK    f =   0.00009118946734721622     h =   0.00000000000019167636 (L2)
                            #88556 ( 0.878781 0.601424 0.910984 0.218991 0.3552 0.632066 0.820717 0.851906 0.0253721 0.0999963 0.0635964 0.534607 )     Evaluation OK    f =   0.00009118982790860059     h =   0.0000000000001        (L2)
                            #88948 ( 0.878778 0.601428 0.910985 0.218992 0.355199 0.632066 0.820714 0.851906 0.0253719 0.0999962 0.0635962 0.534607 )   Evaluation OK    f =   0.00009118971740894385     h =   0.0000000000001        (L2)
                            #88949 ( 0.878781 0.601427 0.910981 0.218992 0.355201 0.632066 0.820716 0.851906 0.0253724 0.0999959 0.0635957 0.534607 )   Evaluation OK    f =   0.00009118957784618523     h =   0.0000000000001        (L2)
                            #89483 ( 0.87878 0.60143 0.910982 0.218992 0.3552 0.632066 0.820713 0.851905 0.0253722 0.0999958 0.0635955 0.534607 )       Evaluation OK    f =   0.00009118945138036892     h =   0.00000000000014832284 (L2)
                            #89487 ( 0.878784 0.601425 0.910975 0.218992 0.355205 0.632065 0.820717 0.851906 0.0253731 0.0999955 0.0635949 0.534607 )   Evaluation OK    f =   0.00009118936850489862     h =   0.00000000000015797819 (L2)
                            #89618 ( 0.87878 0.601427 0.910981 0.218992 0.355201 0.632066 0.820716 0.851906 0.0253724 0.0999959 0.0635957 0.534607 )    Evaluation OK    f =   0.00009118957841469426     h =   0.0000000000001        (L2)
... A total of 96 infeasible solutions were found.

Blackbox evaluations:         11776
Total model evaluations:      78350
Cache hits:                   342
Total number of evaluations:  12118
...
...
...
BBE OBJ
1   0.000073
2   0.000088
5   0.000093
34   0.000025
86   0.000118
214   0.000037
498   0.000077
754   0.000063
875   0.000029
2001   0.000002
3006   0.000003
3009   0.000003
3027   0.000002
3059   0.000002
3061   0.000002
...
...
...
14628   0.000002
14747   0.000002
A termination criterion is reached: No termination (all). Mesh minimum precision reached (Algo)

Best feasible solutions:    #28416 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666576 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280873200673    h =   0                      (L2)
                            #28469 ( 0.706107 0.48003 0.273848 0.120064 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666576 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280872452861    h =   0                      (L2)
                            #28563 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533834 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666577 0.0880672 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280866914585    h =   0                      (L2)
                            #28653 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618771 0.106915 0.168147 0.666808 0.533834 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666576 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280875223496    h =   0                      (L2)
                            #28680 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666578 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280875156577    h =   0                      (L2)
                            #28664 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666576 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280872682511    h =   0                      (L2)
                            #28733 ( 0.706107 0.48003 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127258 0.38259 0.533125 0.304049 0.449785 0.666577 0.0880671 0.498283 0.500005 0.505117 0.185223 ) Evaluation OK    f =   0.00000176280870946084    h =   0                      (L2)
                            #28701 ( 0.706107 0.480031 0.273848 0.120065 0.348266 0.133928 0.0618776 0.106915 0.168147 0.666808 0.533833 0.454007 0.156347 0.644923 0.342484 0.127259 0.38259 0.533125 0.304049 0.449785 0.666577 0.0880671 0.498283 0.500005 0.505117 0.185223 )        Evaluation OK    f =   0.00000176280874748868    h =   0                      (L2)
... A total of 1943 feasible solutions were found.

Best infeasible solutions:  #6047 ( 0.666667 0.39988 0.39988 0.39988 0.39988 0.39988 0.39988 0.662921 0.662921 0.662921 0.549504 0.549504 0.549504 0.549504 0.549504 0.549504 0.549504 0.549504 0.549504 0.444444 0.666667 0.0909091 0.6 0.5 0.505561 0.210526 ) Evaluation OK    f =   0.0000032086457057264     h =   0.0000000000001        (L2)
                            #6723 ( 0.88 0.46288 0.38288 0.38388 0.38388 0.30988 0.38888 0.721921 0.713921 0.752921 0.532504 0.526504 0.549504 0.649504 0.540504 0.234504 0.363504 0.536504 0.539504 0.441444 0.666667 0.0929091 0.506 0.502 0.505561 0.185526 ) Evaluation OK    f =   0.00000198596767037619    h =   0.0000000000001        (L2)
                            #6844 ( 0.878 0.47388 0.38988 0.38488 0.38588 0.30988 0.23988 0.722921 0.712921 0.748921 0.532504 0.533504 0.241504 0.600504 0.533504 0.234504 0.362504 0.544504 0.541504 0.440444 0.666667 0.0909091 0.5 0.502 0.506561 0.185526 )  Evaluation OK    f =   0.00000192326903446852    h =   0.0000000000001        (L2)
                            #6913 ( 0.878 0.47388 0.38988 0.38488 0.38588 0.30988 0.23988 0.722921 0.712921 0.748921 0.532504 0.533504 0.441504 0.600504 0.533504 0.234504 0.362504 0.444504 0.541504 0.440444 0.666667 0.0909091 0.5 0.502 0.506561 0.185526 )  Evaluation OK    f =   0.00000193292195146748    h =   0.0000000000001        (L2)
                            #6973 ( 0.878 0.47388 0.38988 0.38488 0.38588 0.20988 0.23988 0.722921 0.712921 0.748921 0.532504 0.533504 0.341504 0.600504 0.533504 0.234504 0.362504 0.544504 0.641504 0.440444 0.666667 0.0909091 0.5 0.502 0.506561 0.185526 )  Evaluation OK    f =   0.00000191347520108818    h =   0.0000000000001        (L2)
                            #6941 ( 0.878 0.47388 0.48988 0.38488 0.38588 0.20988 0.23988 0.722921 0.712921 0.748921 0.532504 0.533504 0.441504 0.600504 0.533504 0.234504 0.362504 0.544504 0.541504 0.440444 0.666667 0.0909091 0.5 0.502 0.506561 0.185526 )  Evaluation OK    f =   0.00000194430205822875    h =   0.0000000000001        (L2)
                            #7270 ( 0.776 0.47388 0.38988 0.38488 0.38588 0.15688 0.14088 0.722921 0.712921 0.748921 0.531504 0.533504 0.341504 0.598504 0.533504 0.235504 0.363504 0.545504 0.544504 0.440444 0.666667 0.0919091 0.5 0.502 0.507561 0.185526 )  Evaluation OK    f =   0.00000187601218278788    h =   0.0000000000001        (L2)
                            #7490 ( 0.79 0.47388 0.39788 0.28288 0.37388 0.12088 0.16688 0.714921 0.720921 0.752921 0.532504 0.564504 0.442504 0.588504 0.543504 0.257504 0.377504 0.547504 0.559504 0.441444 0.666667 0.0909091 0.503 0.502 0.507561 0.185526 ) Evaluation OK    f =   0.00000187576937511812    h =   0.0000000000001        (L2)
... A total of 3077 infeasible solutions were found.

Blackbox evaluations:         16845
Cache hits:                   588
Total number of evaluations:  17433
</pre></div>
</div>

## 5. Update of Coupling Parameters in Innerloop

Once the subsystem optimization algorithms have finished, each subsystem may be tasked to update relevant coupling parameters based on information from neighbors (see [Unified Algorithmic Structure](../../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md)).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Update of CouplingParameters in InnerLoop ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Update of CouplingParameters in InnerLoop</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>


## 6. Innerloop Convergence Criterion

The innerloop iteration concludes with the evaluation of the [`ConvergenceIndicator_Innerloop_Interface`](../../api/Distributed_Design_Optimizer/coordination/convergence/ConvergenceIndicator_Innerloop_Interface.md). 

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Innerloop_DeWit: Starting Innerloop Convergence Evaluation ...</span>
<span style="color:#035970">%%%                                                   Evaluating local convergence in each subsystem, then aggregating</span>
<span style="color:#035970">%%%                                                   via logical AND</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Innerloop_DeWit: Finished Innerloop Convergence Evaluation:</span>
<span style="color:#035970">%%%                                                   SubSystem 0 ConvInnerLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 1 ConvInnerLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 2 ConvInnerLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 3 ConvInnerLoop is False</span>
<span style="color:#035970">%%%                                                   Overall ConvInnerLoop (Logical AND over all subsystems) is False</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>


## 7. Data Logging

The relevant information of the [`LocalSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md), [`ControllerSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md), and [`Coordinator`](../../api/Distributed_Design_Optimizer/coordination/Coordinator.md) are appended to their `subsystemhistory` and `coordinatorhistory` attributes at the end of the `Coordinator.innerloop_iteration()`. Furthermore, the newly appended history is pickled and stored as a `.dill` file. Further details in [Data Logging](../../framework-architecture/data-logging.md)

Successful data logging is reported as follows for the [SSBJ](../../examples/SSBJ/index.md) Example:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Appending important information to each subsystem history and saving into historyfiles/*.dill ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished appending and saving each subsystem history</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Appending important information to coordinator history and saving into historyfiles/*.dill ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished appending and saving coordinator history</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>

## 8. End of Innerloop Iteration

A summary of `Coordinator.innerloop_iteration()` is provided next. It includes various information from the [`Coordinator`](../../api/Distributed_Design_Optimizer/coordination/Coordinator.md), each [`LocalSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) and [`ControllerSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md) (if existing).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Innerloop Iteration Nr. 0 (Outerloop Nr. 0) after 1188 sec. and 34590 design variables</span>
<span style="color:#035970">%%%     evaluations</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%%    SubSystem 0:</span>
<span style="color:#035970">%%%        Outerloop Iteration:             0</span>
<span style="color:#035970">%%%        Innerloop Iteration:             0</span>
<span style="color:#035970">%%%        Solver_PyNomadBBO solver took 5 sec. and tried 1019 design variables evaluations</span>
<span style="color:#035970">%%%        Solver Message:                  No termination (all). Mesh minimum precision reached (Algo)</span>
<span style="color:#035970">%%%        No equality TotalConstraints exist for Subsystem 0.</span>
<span style="color:#035970">%%%        Inequality TotalConstraints of Subsystem 0 are VALIDATED!</span>
<span style="color:#035970">%%%        Design variables:                [0] 0.06203518403239</span>
<span style="color:#035970">%%%                                         [1] 0.0</span>
<span style="color:#035970">%%%                                         [2] 0.3880196236825</span>
<span style="color:#035970">%%%                                         [3] 5e-14</span>
<span style="color:#035970">%%%                                         [4] 0.04618473895582329</span>
<span style="color:#035970">%%%        Responses Unscaled:              [0] 2000.0000190438984</span>
<span style="color:#035970">%%%                                         [1] 10100.000000004751</span>
<span style="color:#035970">%%%        Local Objective Value:           0.002721088435395695</span>
<span style="color:#035970">%%%        Local Obj. Value Unscaled:       10100.000000004751</span>
<span style="color:#035970">%%%        Total Objective Value:           0.002725000978191248</span>
<span style="color:#035970">%%%        Dist. from Ref. Local Obj.:      24199.99999999525</span>
<span style="color:#035970">%%%        Inconsistencies:</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 1:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  None</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] -0.016168198994417626</span>
<span style="color:#035970">%%%                                                                       [1] 0.03177980193043836</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 2:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] -0.052548116903828365</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.0001525011517085062</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 3:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  None</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.1323047541040131</span>
<span style="color:#035970">%%%                                                                       [1] -0.008090311739650607</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%%    SubSystem 1:</span>
<span style="color:#035970">%%%        Outerloop Iteration:             0</span>
<span style="color:#035970">%%%        Innerloop Iteration:             0</span>
<span style="color:#035970">%%%        Solver_PyNomadBBO solver took 7 sec. and tried 4950 design variables evaluations</span>
<span style="color:#035970">%%%        Solver Message:                  No termination (all). Mesh minimum precision reached (Algo)</span>
<span style="color:#035970">%%%        No equality TotalConstraints exist for Subsystem 1.</span>
<span style="color:#035970">%%%        Inequality TotalConstraints of Subsystem 1 are VALIDATED!</span>
<span style="color:#035970">%%%        Design variables:                [0] 0.04913395838943</span>
<span style="color:#035970">%%%                                         [1] 0.03697866852931</span>
<span style="color:#035970">%%%        Responses Unscaled:              [0] 0.9375</span>
<span style="color:#035970">%%%                                         [1] 2331.758055316274</span>
<span style="color:#035970">%%%                                         [2] 3176.2401155565603</span>
<span style="color:#035970">%%%                                         [3] 1.0421876536177144</span>
<span style="color:#035970">%%%                                         [4] 0.7717964562109273</span>
<span style="color:#035970">%%%                                         [5] 6643.461217477258</span>
<span style="color:#035970">%%%        Local Objective Value:           None</span>
<span style="color:#035970">%%%        Local Obj. Value Unscaled:       None</span>
<span style="color:#035970">%%%        Total Objective Value:           1.5800048339853288e-07</span>
<span style="color:#035970">%%%        Inconsistencies:</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 0:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] -0.016168198994417626</span>
<span style="color:#035970">%%%                                                                       [1] 0.03177980193043836</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  None</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 2:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.0005021090153920701</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.005985984157024012</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%%    SubSystem 2:</span>
<span style="color:#035970">%%%        Outerloop Iteration:             0</span>
<span style="color:#035970">%%%        Innerloop Iteration:             0</span>
<span style="color:#035970">%%%        Solver_PyNomadBBO solver took 55 sec. and tried 11776 design variables evaluations</span>
<span style="color:#035970">%%%        Solver Message:                  No termination (all). Mesh minimum precision reached (Algo)</span>
<span style="color:#035970">%%%        No equality TotalConstraints exist for Subsystem 2.</span>
<span style="color:#035970">%%%        Inequality TotalConstraints of Subsystem 2 are VALIDATED!</span>
<span style="color:#035970">%%%        Design variables:                [0]  0.99984275759357</span>
<span style="color:#035970">%%%                                         [1]  0.85962002929362</span>
<span style="color:#035970">%%%                                         [2]  0.64677665739374</span>
<span style="color:#035970">%%%                                         [3]  0.44424013145373</span>
<span style="color:#035970">%%%                                         [4]  0.6668419697851</span>
<span style="color:#035970">%%%                                         [5]  0.0909525258967</span>
<span style="color:#035970">%%%                                         [6]  0.49990657223819</span>
<span style="color:#035970">%%%                                         [7]  0.49999730136284</span>
<span style="color:#035970">%%%                                         [8]  0.50554328356312</span>
<span style="color:#035970">%%%                                         [9]  0.07336444343446</span>
<span style="color:#035970">%%%                                         [10] 0.03567816447889</span>
<span style="color:#035970">%%%                                         [11] 0.53737331888608</span>
<span style="color:#035970">%%%        Responses Unscaled:              [0] 0.9999264473233428</span>
<span style="color:#035970">%%%                                         [1] 0.1882824121708645</span>
<span style="color:#035970">%%%                                         [2] -0.06234662506404158</span>
<span style="color:#035970">%%%                                         [3] 22974.2886414427</span>
<span style="color:#035970">%%%                                         [4] 4052.4242083554846</span>
<span style="color:#035970">%%%                                         [5] 3.987098247015753</span>
<span style="color:#035970">%%%        Local Objective Value:           None</span>
<span style="color:#035970">%%%        Local Obj. Value Unscaled:       None</span>
<span style="color:#035970">%%%        Total Objective Value:           3.252177559404391e-07</span>
<span style="color:#035970">%%%        Inconsistencies:</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 0:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.0001525011517085062</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] -0.052548116903828365</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 1:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.005985984157024012</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.0005021090153920701</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 3:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.003979774841685824</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.0005399409084551055</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  [0] -0.00554450380966004</span>
<span style="color:#035970">%%%                                                                       [1] 0.00026546348510003703</span>
<span style="color:#035970">%%%                                                                       [2] 0.002885344679300003</span>
<span style="color:#035970">%%%                                                                       [3] 0.0016238454403499913</span>
<span style="color:#035970">%%%                                                                       [4] -7.66601277996104e-06</span>
<span style="color:#035970">%%%                                                                       [5] 0.00042579908144990686</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%%    SubSystem 3:</span>
<span style="color:#035970">%%%        Outerloop Iteration:             0</span>
<span style="color:#035970">%%%        Innerloop Iteration:             0</span>
<span style="color:#035970">%%%        Solver_PyNomadBBO solver took 550 sec. and tried 16845 design variables evaluations</span>
<span style="color:#035970">%%%        Solver Message:                  No termination (all). Mesh minimum precision reached (Algo)</span>
<span style="color:#035970">%%%        No equality TotalConstraints exist for Subsystem 3.</span>
<span style="color:#035970">%%%        Inequality TotalConstraints of Subsystem 3 are VALIDATED!</span>
<span style="color:#035970">%%%        Design variables:                [0]  0.70610671710153</span>
<span style="color:#035970">%%%                                         [1]  0.48003041186106</span>
<span style="color:#035970">%%%                                         [2]  0.27384803228897</span>
<span style="color:#035970">%%%                                         [3]  0.12006457411997</span>
<span style="color:#035970">%%%                                         [4]  0.3482655421965</span>
<span style="color:#035970">%%%                                         [5]  0.13392806496154</span>
<span style="color:#035970">%%%                                         [6]  0.06187757543771</span>
<span style="color:#035970">%%%                                         [7]  0.10691509964691</span>
<span style="color:#035970">%%%                                         [8]  0.16814705916461</span>
<span style="color:#035970">%%%                                         [9]  0.66680783298528</span>
<span style="color:#035970">%%%                                         [10] 0.53383354196663</span>
<span style="color:#035970">%%%                                         [11] 0.4540070273086</span>
<span style="color:#035970">%%%                                         [12] 0.15634670088283</span>
<span style="color:#035970">%%%                                         [13] 0.64492323190039</span>
<span style="color:#035970">%%%                                         [14] 0.34248351943039</span>
<span style="color:#035970">%%%                                         [15] 0.12725859103883</span>
<span style="color:#035970">%%%                                         [16] 0.3825902883083</span>
<span style="color:#035970">%%%                                         [17] 0.53312514427728</span>
<span style="color:#035970">%%%                                         [18] 0.30404923060348</span>
<span style="color:#035970">%%%                                         [19] 0.44978463526339</span>
<span style="color:#035970">%%%                                         [20] 0.6665765063</span>
<span style="color:#035970">%%%                                         [21] 0.0880671812174</span>
<span style="color:#035970">%%%                                         [22] 0.49828272679784</span>
<span style="color:#035970">%%%                                         [23] 0.50000496737562</span>
<span style="color:#035970">%%%                                         [24] 0.50511748448167</span>
<span style="color:#035970">%%%                                         [25] 0.18522326348929</span>
<span style="color:#035970">%%%        Responses Unscaled:              [0]  926189.9148817632</span>
<span style="color:#035970">%%%                                         [1]  286012.0628694255</span>
<span style="color:#035970">%%%                                         [2]  25945.615637890758</span>
<span style="color:#035970">%%%                                         [3]  980573.1309415305</span>
<span style="color:#035970">%%%                                         [4]  302805.8710947217</span>
<span style="color:#035970">%%%                                         [5]  27469.067792106038</span>
<span style="color:#035970">%%%                                         [6]  926189.9148817632</span>
<span style="color:#035970">%%%                                         [7]  286012.0628694255</span>
<span style="color:#035970">%%%                                         [8]  25945.615637890758</span>
<span style="color:#035970">%%%                                         [9]  -52707.97419404772</span>
<span style="color:#035970">%%%                                         [10] -16276.485185905429</span>
<span style="color:#035970">%%%                                         [11] -1476.5231379842935</span>
<span style="color:#035970">%%%                                         [12] -107091.190253815</span>
<span style="color:#035970">%%%                                         [13] -33070.293411201594</span>
<span style="color:#035970">%%%                                         [14] -2999.975292199574</span>
<span style="color:#035970">%%%                                         [15] -52707.97419404772</span>
<span style="color:#035970">%%%                                         [16] -16276.485185905429</span>
<span style="color:#035970">%%%                                         [17] -1476.5231379842935</span>
<span style="color:#035970">%%%                                         [18] 162473859.1874211</span>
<span style="color:#035970">%%%                                         [19] 275776444.91800433</span>
<span style="color:#035970">%%%                                         [20] 3653293026.8134294</span>
<span style="color:#035970">%%%                                         [21] 223401556.382704</span>
<span style="color:#035970">%%%                                         [22] 379192611.76225597</span>
<span style="color:#035970">%%%                                         [23] 5023277911.868464</span>
<span style="color:#035970">%%%                                         [24] 5975414.294263941</span>
<span style="color:#035970">%%%                                         [25] 1845516.1072245</span>
<span style="color:#035970">%%%                                         [26] 213112.01167144877</span>
<span style="color:#035970">%%%                                         [27] 8216194.654612918</span>
<span style="color:#035970">%%%                                         [28] 2537584.647433687</span>
<span style="color:#035970">%%%                                         [29] 293029.01604824205</span>
<span style="color:#035970">%%%                                         [30] 162473859.1874211</span>
<span style="color:#035970">%%%                                         [31] 275776444.91800433</span>
<span style="color:#035970">%%%                                         [32] 3653293026.8134294</span>
<span style="color:#035970">%%%                                         [33] 223401556.382704</span>
<span style="color:#035970">%%%                                         [34] 379192611.76225597</span>
<span style="color:#035970">%%%                                         [35] 5023277911.868464</span>
<span style="color:#035970">%%%                                         [36] 2794785.7142176013</span>
<span style="color:#035970">%%%                                         [37] 465947.4471547252</span>
<span style="color:#035970">%%%                                         [38] 80221.39971676923</span>
<span style="color:#035970">%%%                                         [39] 3842830.3570492016</span>
<span style="color:#035970">%%%                                         [40] 640677.7398377471</span>
<span style="color:#035970">%%%                                         [41] 110304.42461055767</span>
<span style="color:#035970">%%%                                         [42] 227642.2409800539</span>
<span style="color:#035970">%%%                                         [43] 128817.79172956357</span>
<span style="color:#035970">%%%                                         [44] 32922.35096143384</span>
<span style="color:#035970">%%%                                         [45] 1006623.4291252864</span>
<span style="color:#035970">%%%                                         [46] 362746.4272809146</span>
<span style="color:#035970">%%%                                         [47] 62648.372279833675</span>
<span style="color:#035970">%%%                                         [48] -9300.211241505622</span>
<span style="color:#035970">%%%                                         [49] -11358.434327493982</span>
<span style="color:#035970">%%%                                         [50] -38444.29093138642</span>
<span style="color:#035970">%%%                                         [51] 980705.4333039487</span>
<span style="color:#035970">%%%                                         [52] 303444.29086827324</span>
<span style="color:#035970">%%%                                         [53] 72030.82812947911</span>
<span style="color:#035970">%%%                                         [54] -303224.66828200815</span>
<span style="color:#035970">%%%                                         [55] -171588.24301611158</span>
<span style="color:#035970">%%%                                         [56] -43853.32399806821</span>
<span style="color:#035970">%%%                                         [57] 1064736.2850926465</span>
<span style="color:#035970">%%%                                         [58] 412468.7570360847</span>
<span style="color:#035970">%%%                                         [59] 80265.29167621456</span>
<span style="color:#035970">%%%                                         [60] 527838.7338078193</span>
<span style="color:#035970">%%%                                         [61] 297644.92166686716</span>
<span style="color:#035970">%%%                                         [62] 75970.53506205967</span>
<span style="color:#035970">%%%                                         [63] -17869.041403318624</span>
<span style="color:#035970">%%%                                         [64] -19770.37112379638</span>
<span style="color:#035970">%%%                                         [65] -38428.86821140306</span>
<span style="color:#035970">%%%                                         [66] 111473.90256019276</span>
<span style="color:#035970">%%%                                         [67] 47605.11558037528</span>
<span style="color:#035970">%%%                                         [68] 66628.32421562141</span>
<span style="color:#035970">%%%                                         [69] 397795.29934239195</span>
<span style="color:#035970">%%%                                         [70] 223711.8556720914</span>
<span style="color:#035970">%%%                                         [71] 57042.297456014814</span>
<span style="color:#035970">%%%                                         [72] 0.5246029937368208</span>
<span style="color:#035970">%%%                                         [73] 0.5493536234611129</span>
<span style="color:#035970">%%%                                         [74] 0.4405502462647719</span>
<span style="color:#035970">%%%                                         [75] 0.20889241370901487</span>
<span style="color:#035970">%%%                                         [76] 0.07815353501308357</span>
<span style="color:#035970">%%%                                         [77] 0.00833339258824683</span>
<span style="color:#035970">%%%                                         [78] 0.05140728191965839</span>
<span style="color:#035970">%%%                                         [79] 0.04151005042992416</span>
<span style="color:#035970">%%%                                         [80] 0.058617173061230446</span>
<span style="color:#035970">%%%                                         [81] 0.10872119720317053</span>
<span style="color:#035970">%%%                                         [82] 0.04490061361767454</span>
<span style="color:#035970">%%%                                         [83] 0.008336737042205061</span>
<span style="color:#035970">%%%                                         [84] 0.4300238334185493</span>
<span style="color:#035970">%%%                                         [85] 0.1891056920561264</span>
<span style="color:#035970">%%%                                         [86] 0.058284839900034406</span>
<span style="color:#035970">%%%                                         [87] 0.08762869890479158</span>
<span style="color:#035970">%%%                                         [88] 0.13304240221375244</span>
<span style="color:#035970">%%%                                         [89] 0.5028824761307494</span>
<span style="color:#035970">%%%                                         [90] 0.3120345760890309</span>
<span style="color:#035970">%%%                                         [91] 0.0925545211898293</span>
<span style="color:#035970">%%%                                         [92] 0.030085190925563138</span>
<span style="color:#035970">%%%                                         [93] -0.08573485256662572</span>
<span style="color:#035970">%%%                                         [94] -0.29595272898447</span>
<span style="color:#035970">%%%                                         [95] -0.40884711943611574</span>
<span style="color:#035970">%%%                                         [96] 17568.951639885992</span>
<span style="color:#035970">%%%                                         [97] 4194.204950730799</span>
<span style="color:#035970">%%%                                         [98] 20.609669075407933</span>
<span style="color:#035970">%%%        Local Objective Value:           None</span>
<span style="color:#035970">%%%        Local Obj. Value Unscaled:       None</span>
<span style="color:#035970">%%%        Total Objective Value:           1.7628086691458522e-06</span>
<span style="color:#035970">%%%        Inconsistencies:</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 0:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.1323047541040131</span>
<span style="color:#035970">%%%                                                                       [1] -0.008090311739650607</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  None</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%           Inconsistencies with SubSystem 2:</span>
<span style="color:#035970">%%%               MappedResponse - CopyCouplingVariable:                  [0] 0.0005399409084551055</span>
<span style="color:#035970">%%%               CopyMappedResponse - CouplingVariable:                  [0] 0.003979774841685824</span>
<span style="color:#035970">%%%               SharedDesignVariable - CopyTargetSharedDesignVariable:  None</span>
<span style="color:#035970">%%%               CopySharedDesignVariable - TargetSharedDesignVariable:  [0] -0.00554450380966004</span>
<span style="color:#035970">%%%                                                                       [1] 0.00026546348510003703</span>
<span style="color:#035970">%%%                                                                       [2] 0.002885344679300003</span>
<span style="color:#035970">%%%                                                                       [3] 0.0016238454403499913</span>
<span style="color:#035970">%%%                                                                       [4] -7.66601277996104e-06</span>
<span style="color:#035970">%%%                                                                       [5] 0.00042579908144990686</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%% Performance Metrics:</span>
<span style="color:#035970">%%%    Global Objective Function Value:           0.002721088435395695</span>
<span style="color:#035970">%%%    Distance from Ref. Global Obj. (Unscaled): 24199.99999999525</span>
<span style="color:#035970">%%%    L2 Norm from Ref. Design Vars (Unscaled):  None</span>
<span style="color:#035970">%%% </span>
<span style="color:#035970">%%% Coordinator:</span>
<span style="color:#035970">%%%    Max Inconsistency Value:             0.1323047541040131 (SubSystem 3)</span>
<span style="color:#035970">%%%    Max Ratio Active Constraints:        0.6666666666666666 (SubSystem 0)</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Innerloop_DeWit: Innerloop Convergence Indicator is False</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>

## 9. Update of Coupling Parameters in Outerloop

Once the algorithm exits the innerloop (i.e. [`ConvergenceIndicator_Innerloop_Interface`](../../api/Distributed_Design_Optimizer/coordination/convergence/ConvergenceIndicator_Innerloop_Interface.md) evaluates to `True`), each subsystem may be tasked to update relevant coupling parameters based on information from neighbors (see [Unified Algorithmic Structure](../../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md)).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Prepare Update of CouplingParameters ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Prepare Update of CouplingParameters</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Starting Update of CouplingParameters in Outerloop ...</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Update of CouplingParameters in Outerloop</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>


## 10. Outerloop Convergence Criterion

The outerloop iteration concludes with the evaluation of the [`ConvergenceIndicator_Outerloop_Interface`](../../api/Distributed_Design_Optimizer/coordination/convergence/ConvergenceIndicator_Outerloop_Interface.md). 

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Outerloop_DeWit: Starting Outerloop Convergence Evaluation ...</span>
<span style="color:#035970">%%%                                                   Evaluating inconsistencies and outer-loop convergence in each</span>
<span style="color:#035970">%%%                                                   subsystem, then aggregating via logical AND</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>

<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Outerloop_DeWit: Finished Outerloop Convergence Evaluation:</span>
<span style="color:#035970">%%%                                                   SubSystem 0 ConvOuterLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 1 ConvOuterLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 2 ConvOuterLoop is False</span>
<span style="color:#035970">%%%                                                   SubSystem 3 ConvOuterLoop is False</span>
<span style="color:#035970">%%%                                                   Overall ConvOuterLoop (Logical AND over all subsystems) is False</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>


## 11. End of Outerloop Iteration

A summary of `Coordinator.outerloop_iteration()` is provided next. It includes various information from the [`Coordinator`](../../api/Distributed_Design_Optimizer/coordination/Coordinator.md).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
<span style="color:#035970">%%% Coordinator: Finished Outerloop Iteration Nr. 0 after 2 innerloop iterations</span>
<span style="color:#035970">%%%     Cumulative Runtime:                  1968 sec.</span>
<span style="color:#035970">%%%     Cumulative DV Evaluations:           61223</span>
<span style="color:#035970">%%%     Max Inconsistency Value:             0.13133821638460727 (SubSystem 3)</span>
<span style="color:#035970">%%% Centralized_ConvergenceIndicator_Outerloop_DeWit: Outerloop Convergence Indicator is False</span>
<span style="color:#035970">%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%</span>
</pre></div>
</div>


## 12. Termination Summary

The abbr:DDO execution terminates once the [`ConvergenceIndicator_Outerloop_Interface`](../../api/Distributed_Design_Optimizer/coordination/convergence/ConvergenceIndicator_Outerloop_Interface.md) evaluates to `True`.
A summary about the algorithm configuration is printed, followed by various information from the [`Coordinator`](../../api/Distributed_Design_Optimizer/coordination/Coordinator.md), each [`LocalSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) and [`ControllerSubSystemBasis`](../../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md) (if existing).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows TODO:

<div class="collapsible-code">
<div class="highlight"><pre style="background:#1E1E1E; color:#FFFFFF; padding:1em; overflow-x:auto; border-radius:0.3em;">
<span style="color:#035970">  </span>
<span style="color:#035970">  </span>
<span style="color:#035970">  </span>
<span style="color:#035970">  </span>
<span style="color:#035970">  </span>
</pre></div>
</div>

