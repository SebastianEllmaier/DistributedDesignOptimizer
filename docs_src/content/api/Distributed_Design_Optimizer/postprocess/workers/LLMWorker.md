---
title: LLMWorker
---

← Back to [workers](index.md)

# LLMWorker

**Source:** [Distributed_Design_Optimizer\postprocess\workers\LLMWorker.py](LLMWorker_source.md)

Background worker for asynchronous LLM API calls.

## Classes

### LLMWorker

> **Inherits from:** [CallableWorker](CallableWorker.md#callableworker)

> Background worker for LLM API calls.

#### Methods

??? abstract "__init__(self, call_fn: Callable[Ellipsis, Any], messages: list[dict], config: dict, parent: QObject | None) → None"
    Initialize the LLM worker.


    **Args:**
    > call_fn: Callable that performs the LLM API request.  
    > messages: Chat message history to send.  
    > config: LLM configuration parameters.  
    > parent: Optional parent QObject.  

