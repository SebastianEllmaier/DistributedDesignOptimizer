---
title: llm_api (Source)
---

← Back to [llm_api documentation](llm_api.md)

# llm_api - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\llm_api.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""LLM API module.

This module provides an interface to large language models for
assistance in optimization analysis.
"""

from typing import Any, Dict, List

import logging
import requests
from Distributed_Design_Optimizer.postprocess.handlers.llm_utils import (
    LlmApiModel,
    get_access_token,
    get_generate_chat_response,
)

logger = logging.getLogger(__name__)
 
def call_llm_api(
    messages: List[Dict[str, str]],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Call the LLM API with the given messages and configuration.

    Args:
        messages: List of message dictionaries for the chat.
        config: Configuration dictionary with API credentials.

    Returns:
        The API response as a dictionary.
    """
 
    with requests.Session() as requests_session:
 
        requests_session.proxies = {"http": "", "https": ""}
        requests_session.hooks = {
            "response": lambda r, *args, **kwargs: r.raise_for_status()
        }
 
        access_token = get_access_token(requests_session, config)
 
        requests_session.headers.update(
            {
                "Accept": "application/json",
                "x-apikey": config["CLIENT_ID"],
                "Authorization": f"Bearer {access_token}",
            }
        )
 
        payload = {
            "model": LlmApiModel.GPT_4o,
            "temperature": 0.7,
            "max_completion_tokens": 1024,
            "messages": messages
        }
 
        response = get_generate_chat_response(requests_session, payload)
 
        logger.info(f"Chat API response received.")
 
        return response
```
