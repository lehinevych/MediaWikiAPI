"""
HTTP request processing utilities.

This module provides functions for processing HTTP requests and responses
in a consistent way across synchronous and asynchronous implementations.
"""

from datetime import datetime
import random
from typing import Any, Dict, Optional, Tuple, Union

from ..config import Config
from ..language import Language
from .type_definitions import WikiQuery, WikiResponse


def prepare_request_headers(config: Config) -> Dict[str, str]:
    """
    Prepare headers for an HTTP request.
    
    Args:
        config: Configuration object
        
    Returns:
        Dictionary of HTTP headers
    """
    return {"User-Agent": config.user_agent}


def prepare_api_url(config: Config, language: Optional[Union[str, Language]] = None) -> str:
    """
    Prepare the API URL for a request.
    
    Args:
        config: Configuration object
        language: Optional language override
        
    Returns:
        API URL for the request
    """
    return config.get_api_url(language)


def should_rate_limit(
    last_call: Optional[datetime], 
    config: Config
) -> Tuple[bool, Optional[float]]:
    """
    Check if a request should be rate limited.
    
    Args:
        last_call: Timestamp of the last API call
        config: Configuration object
        
    Returns:
        Tuple of (should_limit, wait_seconds)
    """
    if (
        last_call 
        and config.rate_limit 
        and (last_call + config.rate_limit) > datetime.now()
    ):
        wait_time = (last_call + config.rate_limit) - datetime.now()
        return True, wait_time.total_seconds()
    return False, None


def calculate_backoff_with_jitter(config: Config, attempt: int) -> float:
    """
    Calculate backoff time with jitter for retries.
    
    Args:
        config: Configuration object
        attempt: Attempt number (0-based)
        
    Returns:
        Backoff time in seconds
    """
    backoff_time = config.get_retry_backoff(attempt)
    jitter = random.uniform(0, 0.1 * backoff_time)
    return backoff_time + jitter


def should_retry_status_code(config: Config, attempt: int, status_code: Optional[int]) -> bool:
    """
    Check if a request should be retried based on HTTP status code.
    
    Args:
        config: Configuration object
        attempt: Current attempt number (0-based)
        status_code: HTTP status code
        
    Returns:
        True if the request should be retried, False otherwise
    """
    return config.should_retry(attempt, status_code)


def prepare_error_context(
    api_url: str,
    status_code: Optional[int] = None,
    message: Optional[str] = None,
    attempts: Optional[int] = None,
    continuation: bool = False,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Prepare error context for network errors.
    
    Args:
        api_url: API URL that was accessed
        status_code: Optional HTTP status code
        message: Optional error message
        attempts: Optional number of attempts made
        continuation: Whether this was a continuation request
        **kwargs: Additional context values
        
    Returns:
        Dictionary of error context
    """
    context = {"url": api_url}
    
    if status_code is not None:
        context["status_code"] = status_code
    if message is not None:
        context["message"] = message
    if attempts is not None:
        context["attempts"] = attempts
    if continuation:
        context["continuation"] = True
        
    # Add any additional context
    context.update(kwargs)
    
    return context