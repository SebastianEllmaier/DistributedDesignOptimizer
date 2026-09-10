# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""LLM utilities module.

This module provides utility functions for large language model
interactions.
"""

import os
import time
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict
import requests
import logging

logger = logging.getLogger(__name__)
 
# Base URL of the LLM API. Configure via the LLM_API_BASE_PATH environment
# variable to point at your provider's endpoint (e.g. https://api.openai.com/v1).
API_BASE_PATH_V2 = os.environ.get("LLM_API_BASE_PATH", "")
 
class LlmApiModel(str, Enum):
    """Enumeration of supported LLM API models."""
    # add more models as needed
    TITAN = "amazon/titan-embed-text-v2"
    OPENAI = "openai/text-embedding-3-small"
    SONNET = "anthropic/claude-3-7-sonnet"
    GPT_4o = "openai/gpt-4o"
    COHERE = "cohere/rerank-3-5"
 
 
# Get access token
def get_access_token(
    requests_session: requests.Session, config: Dict[str, Any]
) -> str:
    """Get access token from auth server using OAuth2 client credentials flow.

    Args:
        requests_session: The requests session to use.
        config: Configuration dictionary with client credentials.

    Returns:
        Access token if authentication succeeded.
    """
 
    # Make request to get access token. Configure the OAuth2 token endpoint via
    # the LLM_AUTH_ENDPOINT environment variable for your identity provider.
    auth_endpoint = os.environ.get("LLM_AUTH_ENDPOINT", "")
    logger.info(f"Requesting access token from: {auth_endpoint}")
   
    auth_response = requests_session.post(
        auth_endpoint,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": config["CLIENT_ID"],
            "client_secret": config["CLIENT_SECRET"],
            "scope": "machine2machine",
        },
    )
 
    logger.info(f"Auth response status code: {auth_response.status_code}")
   
    # Check response status code
    if auth_response.status_code != HTTPStatus.OK:
        logger.error(f"Auth response headers: {dict(auth_response.headers)}")
        logger.error(f"Auth response content: {auth_response.text}")
        # raise if request failed
        raise Exception(
            f"OAuth2 authentication failed. HTTP status code: {auth_response.status_code}."
        )
    else:
        # Get access token from response
        auth_json = auth_response.json()
        access_token = auth_json.get("access_token")
       
        if not access_token:
            logger.error(f"No access token in response: {auth_json}")
            raise Exception("No access token received from authentication server")
           
        logger.info(msg="Successfully received access token.")
 
        logger.info(f"Token length: {len(access_token)}")
        return access_token
 
 
# Helpers
def get_generate_chat_response(requests_session: requests.Session, payload: dict) -> dict:
    """Generate a chat response from the LLM API.

    Args:
        requests_session: The requests session to use.
        payload: The request payload dictionary.

    Returns:
        The API response as a dictionary.
    """
 
    # Debug logging
    url = f"{API_BASE_PATH_V2}/chat/completions"
    logger.info(f"Chat API URL: {url}")
    logger.info(f"Chat API payload: {payload}")
    logger.info(f"Chat API headers: {dict(requests_session.headers)}")
   
    response = requests_session.post(
        f"{API_BASE_PATH_V2}/chat/completions",  # nosec CWE-295, CWE-295
        json=payload,  # nosec CWE-295, CWE-295
        verify=False,  # nosec CWE-295, CWE-295
    )
    if response.status_code == 200:
        x = response.json()
        return response.json()
    else:
        response.raise_for_status()