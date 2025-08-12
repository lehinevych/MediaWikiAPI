import random
import time
import socket
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

from ..base.base_requestsession import BaseRequestSession
from ..common.api_version import MediaWikiVersion
from ..common.continuation_util import (
    should_continue, get_continue_params, merge_continue_results
)
from ..config import Config
from ..exceptions import NetworkError, HTTPTimeoutError
from ..language import Language


class RequestSession(BaseRequestSession):
    """
    Synchronous request session for the MediaWiki API.
    
    This class extends BaseRequestSession with synchronous HTTP requests
    using the requests library.
    
    The RequestSession class can be used as a context manager to ensure
    proper resource cleanup:
    
    Example:
        ```python
        with RequestSession() as session:
            data = session.request(params, config)
        # Session is automatically closed after the with block
        ```
    """

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        """Initialize the request session with a new requests Session.
        
        Args:
            session: Optional existing requests.Session to use. If not provided,
                     a new session will be created.
        """
        super().__init__()
        self.__session: requests.Session = session or requests.Session()
        self.__rate_limit_last_call: Optional[datetime] = None
        self.__reuse_count: int = 0
        self.__max_reuse_count: int = 1000  # Limit to prevent memory leaks

    def __del__(self) -> None:
        """Clean up the session when the object is deleted."""
        if self.session is not None:
            self.session.close()
            
    def __enter__(self) -> 'RequestSession':
        """Enter the context manager.
        
        Returns:
            The RequestSession instance
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager and clean up resources.
        
        Args:
            exc_type: The exception type, if an exception was raised
            exc_val: The exception value, if an exception was raised
            exc_tb: The exception traceback, if an exception was raised
        """
        self.close()
        
    def close(self) -> None:
        """Close the session and clean up resources."""
        if self.session is not None:
            self.session.close()

    @property
    def session(self) -> requests.Session:
        """Get the underlying requests Session object."""
        return self.__session

    def new_session(self) -> None:
        """Create a new requests Session."""
        if self.session is not None:
            self.session.close()
        self.__session = requests.Session()
        self.__reuse_count = 0
        
    def increment_reuse_counter(self) -> int:
        """Increment the session reuse counter and check if we need a new session.
        
        Returns:
            Current reuse count after increment
        """
        self.__reuse_count += 1
        return self.__reuse_count
        
    def should_refresh_session(self) -> bool:
        """Check if the session should be refreshed based on usage.
        
        Returns:
            True if the session should be refreshed, False otherwise
        """
        return self.__reuse_count >= self.__max_reuse_count
        
    def set_max_reuse_count(self, count: int) -> None:
        """Set the maximum number of times a session can be reused.
        
        Args:
            count: Maximum reuse count
        """
        if count < 1:
            raise ValueError("Maximum reuse count must be at least 1")
        self.__max_reuse_count = count

    def detect_api_version(self, api_url: str, config: Config) -> Optional[MediaWikiVersion]:
        """
        Detect the MediaWiki API version for a specific API URL.
        
        Args:
            api_url: The API URL to check
            config: Configuration object
            
        Returns:
            MediaWikiVersion if detected, None otherwise
        """
        # Create a siteinfo query to get the generator string
        params = {
            "action": "query",
            "meta": "siteinfo",
            "format": "json"
        }
        
        # Prepare request headers
        headers = prepare_request_headers(config)
        
        try:
            r = self.session.get(
                api_url,
                params=params,
                headers=headers,
                timeout=config.timeout,
            )
            r.raise_for_status()
            data = r.json()
            
            # Extract generator string
            if "query" in data and "general" in data["query"] and "generator" in data["query"]["general"]:
                generator = data["query"]["general"]["generator"]
                # Parse the generator string to get the version
                return MediaWikiVersion.from_generator_string(generator)
        except Exception as e:
            # If there's an error, return None
            return None
            
        return None
        
    def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the MediaWiki API.
        
        Args:
            params: API request parameters
            config: Configuration object
            language: Optional language override
            
        Returns:
            API response as a dictionary
        """
        # Prepare parameters using helper method from the base class
        params = self._prepare_params(params)
        
        # Build the user agent
        headers = prepare_request_headers(config)
        
        # Handle rate limiting
        if (
            self.__rate_limit_last_call
            and config.rate_limit
            and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
        ):
            # It hasn't been long enough since the last API call
            # so wait until we're in the clear to make the request
            wait_time = (
                self.__rate_limit_last_call + config.rate_limit
            ) - datetime.now()
            time.sleep(int(wait_time.total_seconds()))
            self.__rate_limit_last_call = datetime.now()
        
        # Get the API URL using the configured language or the override
        api_url = config.get_api_url(language)
        
        # Check if we need to refresh the session
        if self.increment_reuse_counter() > self.__max_reuse_count:
            self.new_session()
        
        # Check if we need to detect the API version
        if api_url not in config.detected_api_versions:
            version = self.detect_api_version(api_url, config)
            if version:
                config.set_api_version(api_url, version)
            
        # Implement retry logic for the request
        attempt = 0
        max_attempts = config.max_retries + 1  # +1 for the initial attempt
        last_exception = None
        
        while attempt < max_attempts:
            try:
                # If this is a retry, apply backoff
                if attempt > 0:
                    backoff_time = config.get_retry_backoff(attempt - 1)
                    # Add small random jitter to prevent thundering herd
                    jitter = random.uniform(0, 0.1 * backoff_time)
                    time.sleep(backoff_time + jitter)
                
                # Make the request with improved error handling
                r = self.session.get(
                    api_url,
                    params=params,
                    headers=headers,
                    timeout=config.timeout,
                )
                
                # Get status code for retry decision
                status_code = r.status_code
                
                # Raise HTTP errors explicitly
                r.raise_for_status()
                
                # Parse JSON response
                try:
                    data: Dict[str, Any] = r.json()
                    # Success! Break out of retry loop
                    break
                    
                except ValueError as e:
                    # Handle invalid JSON response
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "url": api_url,
                            "status_code": r.status_code,
                            "content_sample": r.text[:500] if r.text else None,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Invalid JSON response from API after {attempt + 1} attempts: {str(e)}",
                            original_exception=e
                        )
                    last_exception = e
                    
            except Timeout as e:
                # Always retry timeouts if we haven't exceeded max_retries
                if not config.should_retry(attempt, None):
                    error_context = {
                        "timeout": config.timeout, 
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise HTTPTimeoutError(
                        str(params.get("titles", params.get("search", query_identifier))), 
                        timeout=config.timeout
                    )
                last_exception = e
                
            except HTTPError as e:
                # Get status code for retry decision
                status_code = e.response.status_code if hasattr(e, "response") else None
                
                if not config.should_retry(attempt, status_code):
                    error_context = {
                        "url": api_url,
                        "status_code": status_code,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"HTTP error {status_code} after {attempt + 1} attempts",
                        original_exception=e
                    )
                last_exception = e
                
            except ConnectionError as e:
                # Always retry connection errors if we haven't exceeded max_retries
                if not config.should_retry(attempt, None):
                    error_context = {
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"Connection error while accessing the MediaWiki API after {attempt + 1} attempts: {str(e)}", 
                        original_exception=e
                    )
                last_exception = e
                
            except RequestException as e:
                # Get status code for retry decision if available
                status_code = getattr(e.response, "status_code", None) if hasattr(e, "response") else None
                
                if not config.should_retry(attempt, status_code):
                    error_context = {
                        "url": api_url,
                        "status_code": status_code,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"Error during API request after {attempt + 1} attempts: {str(e)}", 
                        original_exception=e
                    )
                last_exception = e
                
            # Increment attempt counter for next iteration
            attempt += 1
        
        # If we've exhausted all retries and still have an exception, raise it
        if attempt >= max_attempts and last_exception is not None:
            error_context = {
                "url": api_url,
                "attempts": attempt
            }
            raise NetworkError(
                f"Maximum retry attempts ({max_attempts}) exceeded",
                original_exception=last_exception
            )
        
        # If there's no continue token, return the data as is
        if not should_continue(data):
            return data
        
        # Handle continuation
        result = data  # Start with the initial result
        
        # Continue requesting while there's a continue token
        while should_continue(result):
            # Get parameters for continuation request
            continue_params = get_continue_params(result, params)
            
            # Respect rate limits
            if (
                self.__rate_limit_last_call
                and config.rate_limit
                and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
            ):
                wait_time = (
                    self.__rate_limit_last_call + config.rate_limit
                ) - datetime.now()
                if wait_time.total_seconds() > 0:
                    time.sleep(int(wait_time.total_seconds()))
            
            # Make the continuation request with retry logic
            attempt = 0
            max_attempts = config.max_retries + 1  # +1 for the initial attempt
            last_exception = None
            
            while attempt < max_attempts:
                try:
                    # If this is a retry, apply backoff
                    if attempt > 0:
                        backoff_time = config.get_retry_backoff(attempt - 1)
                        # Add small random jitter to prevent thundering herd
                        jitter = random.uniform(0, 0.1 * backoff_time)
                        time.sleep(backoff_time + jitter)
                    
                    # Make the request
                    r = self.session.get(
                        api_url,
                        params=continue_params,
                        headers=headers,
                        timeout=config.timeout,
                    )
                    self.__rate_limit_last_call = datetime.now()
                    
                    # Get status code for retry decision
                    status_code = r.status_code
                    
                    # Raise HTTP errors explicitly
                    r.raise_for_status()
                    
                    # Parse JSON response
                    try:
                        continued_data = r.json()
                        # Success! Break out of retry loop
                        break
                        
                    except ValueError as e:
                        # Handle invalid JSON response
                        if not config.should_retry(attempt, None):
                            error_context = {
                                "url": api_url,
                                "status_code": r.status_code,
                                "content_sample": r.text[:500] if r.text else None,
                                "continuation": True,
                                "attempts": attempt + 1
                            }
                            raise NetworkError(
                                f"Invalid JSON response from API during continuation after {attempt + 1} attempts: {str(e)}",
                                original_exception=e
                            )
                        last_exception = e
                        
                except Timeout as e:
                    # Always retry timeouts if we haven't exceeded max_retries
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "timeout": config.timeout, 
                            "url": api_url, 
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise HTTPTimeoutError(
                            str(params.get("titles", params.get("search", query_identifier))), 
                            timeout=config.timeout
                        )
                    last_exception = e
                    
                except HTTPError as e:
                    # Get status code for retry decision
                    status_code = e.response.status_code if hasattr(e, "response") else None
                    
                    if not config.should_retry(attempt, status_code):
                        error_context = {
                            "url": api_url,
                            "status_code": status_code,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"HTTP error {status_code} during continuation after {attempt + 1} attempts",
                            original_exception=e
                        )
                    last_exception = e
                    
                except ConnectionError as e:
                    # Always retry connection errors if we haven't exceeded max_retries
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "url": api_url, 
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Connection error during continuation after {attempt + 1} attempts: {str(e)}", 
                            original_exception=e
                        )
                    last_exception = e
                    
                except RequestException as e:
                    # Get status code for retry decision if available
                    status_code = getattr(e.response, "status_code", None) if hasattr(e, "response") else None
                    
                    if not config.should_retry(attempt, status_code):
                        error_context = {
                            "url": api_url,
                            "status_code": status_code,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Error during continuation request after {attempt + 1} attempts: {str(e)}", 
                            original_exception=e
                        )
                    last_exception = e
                    
                # Increment attempt counter for next iteration
                attempt += 1
            
            # If we've exhausted all retries and still have an exception, raise it
            if attempt >= max_attempts and last_exception is not None:
                error_context = {
                    "url": api_url,
                    "continuation": True,
                    "attempts": attempt
                }
                raise NetworkError(
                    f"Maximum retry attempts ({max_attempts}) exceeded during continuation",
                    original_exception=last_exception
                )
            
            # Merge the data from the continued request with the initial result
            merge_continue_results(result, continued_data)
            
            # If there are no more continue tokens, we're done
            if not should_continue(result):
                break
        
        return result