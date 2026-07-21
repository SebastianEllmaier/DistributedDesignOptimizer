---
title: ChatHandler
---

← Back to [handlers](index.md)

# ChatHandler

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\ChatHandler.py](ChatHandler_source.md)

Handler for LLM-based chat interactions with optimization results.

## Classes

### ChatHandler

> **Inherits from:** `QObject`

> Manages LLM interaction for analyzing optimization results.

#### Methods

??? abstract "__init__(self, config: dict[str, str], parent: QObject | None) → None"
    Initialize the chat handler.


    **Args:**
    > config: Dictionary containing LLM client credentials.  
    > parent: Optional parent QObject.  

??? abstract "is_available(self) → bool"
    Whether the LLM backend is usable.


    **Returns:**
    > bool: True if the LLM call function is available.  

??? abstract "set_context(self, analysis_type: str, context_data: dict) → None"
    Update the current analysis context and reset conversation history.


    **Args:**
    > analysis_type: The type of analysis being viewed.  
    > context_data: Dictionary of context information for the LLM.  

??? abstract "ask(self, question: str) → None"
    Send a question to the LLM in a background thread.


    **Args:**
    > question: The user's question to send to the LLM.  

??? abstract "clear_history(self) → None"
    Clear the conversation history.

??? abstract "cancel(self) → None"
    Stop any running LLM worker.

