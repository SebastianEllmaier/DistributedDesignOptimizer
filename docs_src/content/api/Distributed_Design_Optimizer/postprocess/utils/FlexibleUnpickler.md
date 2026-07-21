---
title: FlexibleUnpickler
---

← Back to [utils](index.md)

# FlexibleUnpickler

**Source:** [Distributed_Design_Optimizer\postprocess\utils\FlexibleUnpickler.py](FlexibleUnpickler_source.md)

Flexible unpickler that handles lazy-import module/class shadowing.

## Classes

### FlexibleUnpickler

> **Inherits from:** `dill.Unpickler`

> Custom unpickler that handles lazy-import module/class shadowing.

> When DDO subsystem classes are serialized, the unpickler may encounter
> module-level names that have been replaced by lazy-import proxies.
> This class repairs those before resolving.

#### Methods

??? abstract "find_class(self, module: str, name: str) → typing.Any"
    Find a class/callable, repairing lazy-import shadowing first.


    **Args:**
    > module: Fully-qualified module path of the pickled object.  
    > name: Class or callable name to resolve within the module.  


    **Returns:**
    > The resolved class or callable object.  

