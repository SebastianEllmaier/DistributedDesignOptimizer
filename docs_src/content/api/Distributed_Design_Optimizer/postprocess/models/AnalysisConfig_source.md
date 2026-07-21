---
title: AnalysisConfig (Source)
---

← Back to [AnalysisConfig documentation](AnalysisConfig.md)

# AnalysisConfig - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\models\AnalysisConfig.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Configuration model for topology analysis settings."""
from dataclasses import dataclass


@dataclass
class AnalysisConfig:
    """Configuration for a topology analysis run."""

    analysis_type: str = "master_graph"
    # Options: "master_graph" | "clustering" | "weighted_degree" |
    #          "weighted_in_degree" | "weighted_out_degree" |
    #          "pagerank" | "primal_residual" | "dual_residual" | "compromise"

    mode: str = "static"
    # Options: "static" | "dynamic"

    entry_id: str = ""
    # Which data source entry to analyze

```
