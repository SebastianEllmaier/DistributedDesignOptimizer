# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.

# Invalidate bytecode caches once when the package structure changes so
# beartype's import hook doesn't trip over stale .pyc files that reference
# old module paths.  A hash of the current sub-package names is compared
# with a stored sentinel; caches are purged only when they differ.
import hashlib as _hl, pathlib as _pl, shutil as _sh

_pkg_dir = _pl.Path(__file__).parent
_sub_dirs = sorted(d.name for d in _pkg_dir.iterdir()
                   if d.is_dir() and not d.name.startswith(("_", ".")))
_current_hash = _hl.md5(",".join(_sub_dirs).encode()).hexdigest()
_sentinel = _pkg_dir / "__pycache__" / ".structure_hash"

if not _sentinel.exists() or _sentinel.read_text().strip() != _current_hash:
    for _cache in _pkg_dir.rglob("__pycache__"):
        if _cache.is_dir():
            _sh.rmtree(_cache, ignore_errors=True)
    _sentinel.parent.mkdir(exist_ok=True)
    _sentinel.write_text(_current_hash)

del _hl, _pl, _sh, _pkg_dir, _sub_dirs, _current_hash, _sentinel

from beartype.claw import beartype_this_package
beartype_this_package()

import multiprocessing as _mp
if _mp.current_process().name == 'MainProcess':
    from Distributed_Design_Optimizer.generate_inits import main as _generate_inits
    _generate_inits()
    del _generate_inits
del _mp

# <AUTOGEN_INIT>
from Distributed_Design_Optimizer import coordination
from Distributed_Design_Optimizer import middlelevel
from Distributed_Design_Optimizer import postprocess
from Distributed_Design_Optimizer import subsystem
# </AUTOGEN_INIT>
