---
title: llm_utils
---

← Back to [handlers](index.md)

# llm_utils

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\llm_utils.py](llm_utils_source.md)

LLM utilities module.

This module provides utility functions for large language model
interactions.

## Classes

### LlmApiModel

> **Inherits from:** `str`, `Enum`

> Enumeration of supported LLM API models.

## Functions

??? abstract "get_access_token(requests_session: requests.Session, config: Dict[str, Any]) → str"
    Get access token from auth server using OAuth2 client credentials flow.


    **Args:**
    > requests_session: The requests session to use.  
    > config: Configuration dictionary with client credentials.  


    **Returns:**
    > Access token if authentication succeeded.  

??? abstract "get_generate_chat_response(requests_session: requests.Session, payload: dict) → dict"
    Generate a chat response from the LLM API.


    **Args:**
    > requests_session: The requests session to use.  
    > payload: The request payload dictionary.  


    **Returns:**
    > The API response as a dictionary.  

