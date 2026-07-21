---
title: _auto_update_delegate
---

← Back to [widgets](index.md)

# _auto_update_delegate

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\_auto_update_delegate.py](_auto_update_delegate_source.md)

Delegate handling auto-update lifecycle for MainWindow.

## Classes

### AutoUpdateDelegate

> **Inherits from:** `QObject`

> Manages auto-update worker lifecycle.

#### Methods

??? abstract "__init__(self, data_handler: [DataHandler](../handlers/DataHandler.md#datahandler), auto_update_action: QAction, status_bar: QStatusBar, parent: QObject | None) → None"
    Initialize the auto-update delegate.


    **Args:**
    > data_handler: Handler providing access to loaded data entries.  
    > auto_update_action: The toggle action controlling auto-update.  
    > status_bar: Status bar for displaying update messages.  
    > parent: Optional parent QObject.  

??? abstract "worker(self) → [AutoUpdateWorker](../workers/AutoUpdateWorker.md#autoupdateworker) | None"
    Return the active auto-update worker, or None if not running.


    **Returns:**
    > The active worker instance, or None if auto-update is stopped.  

??? abstract "on_toggled(self, enabled: bool) → None"
    Handle auto-update action toggled.


    **Args:**
    > enabled: Whether auto-update is being enabled or disabled.  

??? abstract "manual_update(self) → None"
    Check for file changes and reload if any.

??? abstract "stop(self) → None"
    Stop worker if running (for cleanup on close).

