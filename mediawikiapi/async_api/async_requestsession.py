import asyncio
import random
import socket
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union, Coroutine

import aiohttp
from aiohttp.client_exceptions import (
    ClientError, 
    ClientResponseError, 
    ClientConnectorError, 
    ServerTimeoutError,
    ContentTypeError
)

from ..base.base_requestsession import BaseRequestSession
from ..config import Config
from ..exceptions import NetworkError, HTTPTimeoutError
from ..language import Language


class AsyncRequestSession(BaseRequestSession):
    """Asynchronous request wrapper class for aiohttp"""

    def __init__(self) -> None:
        """Initialize the async session"""
        super().__init__()
        self.__session: Optional[aiohttp.ClientSession] = None
        self.__rate_limit_last_call: Optional[datetime] = None
        self.__reuse_count: int = 0
        self.__max_reuse_count: int = 1000  # Limit to prevent memory leaks

    @property
    async def session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp client session"""
        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self.__session

    async def close(self) -> None:
        """Close the session if it exists"""
        if self.__session and not self.__session.closed:
            await self.__session.close()
            self.__session = None

    async def new_session(self) -> None:
        """Create a new session, closing the old one if it exists"""
        await self.close()
        self.__session = aiohttp.ClientSession()
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

    async def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
    ) -> Dict[str, Any]:
        """
        Make an asynchronous request to the Wikipedia API using the given search parameters,
        language and configuration

        Arguments:

        * params (dictionary)
        * config - the configuration to be used for request

        Keyword arguments:

        * language - the wiki language
        """
        # Use base class method to prepare parameters
        params = self._prepare_params(params)

        headers = {"User-Agent": self._build_user_agent(config)}

        if (
            self.__rate_limit_last_call
            and config.rate_limit
            and (self.__rate_limit_last_call + config.rate_limit) > datetime.now()
        ):
            # it hasn't been long enough since the last API call
            # so wait until we're in the clear to make the request
            wait_time = (
                self.__rate_limit_last_call + config.rate_limit
            ) - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            self.__rate_limit_last_call = datetime.now()

        api_url = config.get_api_url(language)
        query_identifier = str(params.get("titles", params.get("search", "unknown")))
        
        # Check if we need to refresh the session
        if self.increment_reuse_counter() > self.__max_reuse_count:
            await self.new_session()
            
        # Implement retry logic
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
                    await asyncio.sleep(backoff_time + jitter)
                    
                session = await self.session
                async with session.get(
                    api_url,
                    params=params,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=config.timeout),
                ) as response:
                    # Get status code for retry decision
                    status_code = response.status
                    
                    # Check for HTTP errors
                    response.raise_for_status()
                    
                    try:
                        data: Dict[str, Any] = await response.json()
                        # Success! Break out of retry loop
                        break
                        
                    except ContentTypeError as e:
                        # Handle invalid JSON response
                        if not config.should_retry(attempt, None):
                            error_context = {
                                "url": api_url,
                                "status_code": response.status,
                                "content_type": response.content_type,
                                "attempts": attempt + 1
                            }
                            text_sample = await response.text()
                            error_context["content_sample"] = text_sample[:500] if text_sample else None
                            
                            raise NetworkError(
                                f"Invalid JSON response from API after {attempt + 1} attempts: {str(e)}",
                                original_exception=e
                            )
                        last_exception = e
                        
            except ServerTimeoutError as e:
                # Always retry timeouts if we haven't exceeded max_retries
                if not config.should_retry(attempt, None):
                    error_context = {
                        "timeout": config.timeout, 
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise HTTPTimeoutError(query_identifier, timeout=config.timeout)
                last_exception = e
                
            except asyncio.TimeoutError as e:
                # Always retry asyncio timeouts if we haven't exceeded max_retries
                if not config.should_retry(attempt, None):
                    error_context = {
                        "timeout": config.timeout, 
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise HTTPTimeoutError(query_identifier, timeout=config.timeout)
                last_exception = e
                
            except ClientConnectorError as e:
                # Always retry connection errors if we haven't exceeded max_retries
                if not config.should_retry(attempt, None):
                    error_context = {
                        "url": api_url, 
                        "host": e.host, 
                        "port": e.port,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"Connection error while accessing the MediaWiki API after {attempt + 1} attempts: {str(e)}",
                        original_exception=e
                    )
                last_exception = e
                
            except ClientResponseError as e:
                # Get status code for retry decision
                status_code = e.status
                
                if not config.should_retry(attempt, status_code):
                    error_context = {
                        "url": api_url,
                        "status_code": e.status,
                        "message": e.message,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"HTTP error {e.status} after {attempt + 1} attempts: {e.message}",
                        original_exception=e
                    )
                last_exception = e
                
            except ClientError as e:
                # Handle other aiohttp client errors
                if not config.should_retry(attempt, None):
                    error_context = {
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"Error during API request after {attempt + 1} attempts: {str(e)}",
                        original_exception=e
                    )
                last_exception = e
                
            except Exception as e:
                # Handle any other unexpected errors
                if not config.should_retry(attempt, None):
                    error_context = {
                        "url": api_url,
                        "attempts": attempt + 1
                    }
                    raise NetworkError(
                        f"Unexpected error during API request after {attempt + 1} attempts: {str(e)}",
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
        if "continue" not in data:
            return data

        # Handle continuation
        result = data  # Start with the initial result

        # Continue requesting while there's a continue token
        while "continue" in result:
            # Copy the original parameters and update with continue tokens
            continue_params = params.copy()
            continue_params.update(result["continue"])

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
                    await asyncio.sleep(wait_time.total_seconds())

            # Make the continuation request with retry logic
            api_url = config.get_api_url(language)
            
            # Implement retry logic for continuation requests
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
                        await asyncio.sleep(backoff_time + jitter)
                        
                    session = await self.session
                    async with session.get(
                        api_url,
                        params=continue_params,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=config.timeout),
                    ) as response:
                        self.__rate_limit_last_call = datetime.now()
                        
                        # Get status code for retry decision
                        status_code = response.status
                        
                        # Check for HTTP errors
                        response.raise_for_status()
                        
                        try:
                            continued_data = await response.json()
                            # Success! Break out of retry loop
                            break
                            
                        except ContentTypeError as e:
                            # Handle invalid JSON response
                            if not config.should_retry(attempt, None):
                                error_context = {
                                    "url": api_url,
                                    "status_code": response.status,
                                    "content_type": response.content_type,
                                    "continuation": True,
                                    "attempts": attempt + 1
                                }
                                text_sample = await response.text()
                                error_context["content_sample"] = text_sample[:500] if text_sample else None
                                
                                raise NetworkError(
                                    f"Invalid JSON response from API during continuation after {attempt + 1} attempts: {str(e)}",
                                    original_exception=e
                                )
                            last_exception = e
                            
                except ServerTimeoutError as e:
                    # Always retry timeouts if we haven't exceeded max_retries
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "timeout": config.timeout, 
                            "url": api_url,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise HTTPTimeoutError(query_identifier, timeout=config.timeout)
                    last_exception = e
                    
                except asyncio.TimeoutError as e:
                    # Always retry asyncio timeouts if we haven't exceeded max_retries
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "timeout": config.timeout, 
                            "url": api_url,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise HTTPTimeoutError(query_identifier, timeout=config.timeout)
                    last_exception = e
                    
                except ClientConnectorError as e:
                    # Always retry connection errors if we haven't exceeded max_retries
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "url": api_url, 
                            "host": e.host, 
                            "port": e.port,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Connection error during continuation after {attempt + 1} attempts: {str(e)}",
                            original_exception=e
                        )
                    last_exception = e
                    
                except ClientResponseError as e:
                    # Get status code for retry decision
                    status_code = e.status
                    
                    if not config.should_retry(attempt, status_code):
                        error_context = {
                            "url": api_url,
                            "status_code": e.status,
                            "message": e.message,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"HTTP error {e.status} during continuation after {attempt + 1} attempts: {e.message}",
                            original_exception=e
                        )
                    last_exception = e
                    
                except ClientError as e:
                    # Handle other aiohttp client errors
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "url": api_url,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Error during continuation request after {attempt + 1} attempts: {str(e)}",
                            original_exception=e
                        )
                    last_exception = e
                    
                except Exception as e:
                    # Handle any other unexpected errors
                    if not config.should_retry(attempt, None):
                        error_context = {
                            "url": api_url,
                            "continuation": True,
                            "attempts": attempt + 1
                        }
                        raise NetworkError(
                            f"Unexpected error during continuation request after {attempt + 1} attempts: {str(e)}",
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
            if "query" in continued_data:
                # Handle pages
                if "pages" in continued_data.get("query", {}) and "pages" in result.get(
                    "query", {}
                ):
                    for pageid, page_data in continued_data["query"]["pages"].items():
                        if pageid in result["query"]["pages"]:
                            # Page exists in the result, merge properties
                            for prop, value in page_data.items():
                                if prop in result["query"]["pages"][pageid]:
                                    # If the property is a list, extend it
                                    if isinstance(value, list) and isinstance(
                                        result["query"]["pages"][pageid][prop], list
                                    ):
                                        result["query"]["pages"][pageid][prop].extend(
                                            value
                                        )
                                    else:
                                        # Otherwise, replace it
                                        result["query"]["pages"][pageid][prop] = value
                                else:
                                    # Property doesn't exist in the result, add it
                                    result["query"]["pages"][pageid][prop] = value
                        else:
                            # Page doesn't exist in the result, add it
                            result["query"]["pages"][pageid] = page_data

                # Handle lists in the query (like search results, backlinks, etc.)
                for prop, value in continued_data["query"].items():
                    if prop != "pages":
                        if prop not in result["query"]:
                            result["query"][prop] = value
                        elif isinstance(value, list) and isinstance(
                            result["query"][prop], list
                        ):
                            # If the property is a list, extend it
                            result["query"][prop].extend(value)

            # Update the continue token
            if "continue" in continued_data:
                result["continue"] = continued_data["continue"]
            else:
                # No more continue tokens, we're done
                if "continue" in result:
                    del result["continue"]
                break

        return result
