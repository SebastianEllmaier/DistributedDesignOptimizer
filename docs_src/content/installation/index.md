---
title: Installation
---

# Installation

This section walks through setting up the abbr:DDO framework locally, from cloning the repository to running your first use-case.

## Prerequisites

Before starting, make sure the following are installed and available on your `PATH`:

- **Python 3.13 or newer** — the framework is developed and tested against Python 3.13.
- **git** — for cloning the repository.

## 1. Cloning the repository

Clone the repository from its [GitHub location](repo:url):

```powershell
git clone repo:url.git
cd DistributedDesignOptimizer
```

## 2. Creating and activating a virtual environment

A dedicated virtual environment keeps the framework's pinned dependencies isolated from other Python projects:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Installing dependencies

With the virtual environment activated, install all pinned dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

## Next steps

- [Tutorial > Problem Definition and Algorithm Execution](../tutorial/problem-definition-and-algorithm-execution/index.md) walks through defining and solving a distributed design optimization problem with the framework.
- [Tutorial > Processing](../tutorial/processing/index.md) covers inspecting and post-processing the results logged in `historyfiles/`.