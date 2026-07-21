---
title: llm_api
---

← Back to [handlers](index.md)

# llm_api

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\llm_api.py](llm_api_source.md)

LLM API module.

This module provides an interface to large language models for
assistance in optimization analysis.

## Functions

??? abstract "call_llm_api(messages: List[Dict[str, str]], config: Dict[str, Any]) → Dict[str, Any]"
    Call the LLM API with the given messages and configuration.


    **Args:**
    > messages: List of message dictionaries for the chat.  
    > config: Configuration dictionary with API credentials.  


    **Returns:**
    > The API response as a dictionary.  

