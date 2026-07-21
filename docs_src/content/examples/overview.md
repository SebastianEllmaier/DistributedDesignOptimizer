# Examples Overview

The framework ships with a set of ready-to-run example use cases located under
[`userfiles/`](../api/userfiles/index.md). Each one demonstrates the distributed optimization workflow on a
different multidisciplinary design problem. The table below summarizes and
compares the available examples along a few criteria.

<div class="table-scroll" markdown>
<table class="doc-table examples-overview" markdown>
<thead>
<tr>
<th rowspan="2">Example</th>
<th rowspan="2">Number of Subsystems</th>
<th rowspan="2">Analytical vs. Engineering Problem</th>
<th colspan="3">Number of Design Variables per Subsystem</th>
<th rowspan="2">Number of Scalar Couplings</th>
</tr>
<tr>
<th>Local</th>
<th>Shared</th>
<th>Additional (coupling)</th>
</tr>
</thead>
<tbody markdown>
<tr markdown>
<td markdown="span">[GeometricProgramming](GeometricProgramming/index.md)</td>
<td>3</td>
<td>Analytical</td>
<td>3&nbsp;/&nbsp;3&nbsp;/&nbsp;3</td>
<td>0&nbsp;/&nbsp;1&nbsp;/&nbsp;1</td>
<td>2&nbsp;/&nbsp;0&nbsp;/&nbsp;0</td>
<td>3</td>
</tr>
<tr markdown>
<td markdown="span">[Sellar](Sellar/index.md)</td>
<td>2</td>
<td>Analytical</td>
<td>1&nbsp;/&nbsp;0</td>
<td>2&nbsp;/&nbsp;2</td>
<td>1&nbsp;/&nbsp;1</td>
<td>4</td>
</tr>
<tr markdown>
<td markdown="span">[SpeedReducer](SpeedReducer/index.md)</td>
<td>3</td>
<td>Engineering</td>
<td>0&nbsp;/&nbsp;2&nbsp;/&nbsp;2</td>
<td>3&nbsp;/&nbsp;3&nbsp;/&nbsp;3</td>
<td>0&nbsp;/&nbsp;0&nbsp;/&nbsp;0</td>
<td>9</td>
</tr>
<tr markdown>
<td markdown="span">[SSBJ](SSBJ/index.md)</td>
<td>4</td>
<td>Engineering</td>
<td>0&nbsp;/&nbsp;1&nbsp;/&nbsp;3&nbsp;/&nbsp;19</td>
<td>0&nbsp;/&nbsp;0&nbsp;/&nbsp;6&nbsp;/&nbsp;6</td>
<td>5&nbsp;/&nbsp;1&nbsp;/&nbsp;3&nbsp;/&nbsp;1</td>
<td>16</td>
</tr>
<tr markdown>
<td markdown="span">[TwoBarTruss](TwoBarTruss/index.md)</td>
<td>3</td>
<td>Engineering</td>
<td>2&nbsp;/&nbsp;2&nbsp;/&nbsp;2</td>
<td>0&nbsp;/&nbsp;0&nbsp;/&nbsp;0</td>
<td>2&nbsp;/&nbsp;1&nbsp;/&nbsp;2</td>
<td>5</td>
</tr>
</tbody>
</table>
</div>

## Reading the table

- **Number of design variables per subsystem** is split into three
    categories, each listed in subsystem order (`SS0 / SS1 / ...`):
    - **Local** — design variables that belong exclusively to a single
        subsystem ($x$).
    - **Shared** — design variables that are shared between neighboring
        subsystems ($z$).
    - **Additional (coupling)** — variables that the decomposition adds as
        extra design variables to represent the couplings ($h$) between
        subsystems.

    The size of a subsystem's full design vector is the sum of its local,
    shared and additional design variables.

- **Number of scalar couplings** counts the total number of scalar coupling
    relationships (coupling variables plus shared design variables, i.e. the
    scalar consistency constraints) exchanged between neighboring subsystems.
