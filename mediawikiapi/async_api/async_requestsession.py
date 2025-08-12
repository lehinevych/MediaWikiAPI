import asyncio
import random
import socket
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union, Coroutine, List
from urllib.parse import urlparse

import aiohttp
from aiohttp.client_exceptions import (
    ClientError, 
    ClientResponseError, 
    ClientConnectorError, 
    ServerTimeoutError,
    ContentTypeError
)

from ..base.base_requestsession import BaseRequestSession
from ..common.api_version import MediaWikiVersion
from ..common.continuation_util import (
    should_continue, get_continue_params, merge_continue_results
)
from ..common.http_util import (
    calculate_backoff_with_jitter, prepare_api_url, prepare_error_context,
    prepare_request_headers, should_rate_limit, should_retry_status_code
)
from ..common.concurrency import AsyncRequestLimiter, BackpressureController
from ..config import Config
from ..exceptions import NetworkError, HTTPTimeoutError
from ..language import Language


class AsyncRequestSession(BaseRequestSession):
    """Asynchronous request wrapper class for aiohttp with advanced connection pooling"""

    def __init__(self, pool_size: int = 100, pool_connections_per_host: int = 10) -> None:
        """Initialize the async session with connection pooling
        
        Args:
            pool_size: Total number of connections in the pool
            pool_connections_per_host: Maximum number of connections per host
        """
        super().__init__()
        self.__session: Optional[aiohttp.ClientSession] = None
        self.__rate_limit_last_call: Optional[datetime] = None
        self.__reuse_count: int = 0
        self.__max_reuse_count: int = 1000  # Limit to prevent memory leaks
        self.__pool_size = pool_size
        self.__pool_connections_per_host = pool_connections_per_host
        
        # Advanced concurrency controls
        self.__max_concurrent_requests: int = 10  # Default max concurrent requests
        self.__request_limiter = AsyncRequestLimiter(
            global_limit=self.__max_concurrent_requests,
            per_host_limit=self.__pool_connections_per_host
        )
        self.__backpressure_controller = BackpressureController()
        self.__active_requests: int = 0

    @property
    async def session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp client session with optimized connection pooling"""
        if self.__session is None or self.__session.closed:
            # Create a TCP connector with connection pooling settings
            connector = aiohttp.TCPConnector(
                limit=self.__pool_size,  # Total number of concurrent connections
                limit_per_host=self.__pool_connections_per_host,  # Connections per host
                enable_cleanup_closed=True,  # Clean up closed connections
                force_close=False,  # Keep connections alive
                ttl_dns_cache=300  # Cache DNS results for 5 minutes
            )
            self.__session = aiohttp.ClientSession(connector=connector)
        return self.__session

    async def close(self) -> None:
        """Close the session if it exists"""
        if self.__session and not self.__session.closed:
            await self.__session.close()
            self.__session = None

    async def new_session(self) -> None:
        """Create a new session with connection pooling, closing the old one if it exists"""
        await self.close()
        # Create a TCP connector with connection pooling settings
        connector = aiohttp.TCPConnector(
            limit=self.__pool_size,  # Total number of concurrent connections
            limit_per_host=self.__pool_connections_per_host,  # Connections per host
            enable_cleanup_closed=True,  # Clean up closed connections
            force_close=False,  # Keep connections alive
            ttl_dns_cache=300  # Cache DNS results for 5 minutes
        )
        self.__session = aiohttp.ClientSession(connector=connector)
        self.__reuse_count = 0
        
        # Initialize the semaphore for concurrent request limiting
        self.__request_semaphore = asyncio.Semaphore(self.__max_concurrent_requests)
        
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
        
    def set_pool_size(self, size: int) -> None:
        """Set the size of the connection pool.
        
        Args:
            size: Maximum number of connections in the pool
        """
        if size < 1:
            raise ValueError("Pool size must be at least 1")
        self.__pool_size = size
        # We need to recreate the session for this to take effect
        if self.__session and not self.__session.closed:
            asyncio.create_task(self.new_session())
            
    def set_max_connections_per_host(self, limit: int) -> None:
        """Set the maximum number of connections per host.
        
        Args:
            limit: Maximum number of connections per host
        """
        if limit < 1:
            raise ValueError("Connections per host must be at least 1")
        self.__pool_connections_per_host = limit
        # Update both the connection pool and request limiter
        self.__request_limiter.set_per_host_limit(limit)
        # We need to recreate the session for this to take effect
        if self.__session and not self.__session.closed:
            asyncio.create_task(self.new_session())
            
    def set_max_concurrent_requests(self, limit: int) -> None:
        """Set the maximum number of concurrent requests.
        
        Args:
            limit: Maximum number of concurrent requests
        """
        if limit < 1:
            raise ValueError("Max concurrent requests must be at least 1")
        self.__max_concurrent_requests = limit
        self.__request_limiter.set_global_limit(limit)

    async def detect_api_version(self, api_url: str, config: Config) -> Optional[MediaWikiVersion]:
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
            session = await self.session
            async with session.get(
                api_url,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=config.timeout),
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                # Extract generator string
                if "query" in data and "general" in data["query"] and "generator" in data["query"]["general"]:
                    generator = data["query"]["general"]["generator"]
                    # Parse the generator string to get the version
                    return MediaWikiVersion.from_generator_string(generator)
        except Exception as e:
            # If there's an error, return None
            return None
            
        return None
        
    async def request(
        self,
        params: Dict[str, Any],
        config: Config,
        language: Optional[Union[str, Language]] = None,
        priority: int = 0,  # Higher values indicate higher priority
    ) -> Dict[str, Any]:
        """Make a request to the MediaWiki API with backpressure control.
        
        Args:
            params: API request parameters
            config: Configuration object
            language: Optional language override
            priority: Request priority (higher values = higher priority, default 0)
            
        Returns:
            API response as a dictionary
        """
        # Prepare the API URL
        api_url = prepare_api_url(config, language)
        # Extract host for per-host limiting
        parsed_url = urlparse(api_url)
        host = parsed_url.netloc
        
        # Record this request for backpressure calculations
        self.__backpressure_controller.record_request()
        
        # Apply backpressure based on request patterns
        backpressure_delay = self.__backpressure_controller.get_delay(priority)
        if backpressure_delay > 0:
            await asyncio.sleep(backpressure_delay)
        
        # Get semaphores for global and per-host concurrency control
        host_semaphore = self.__request_limiter.get_host_semaphore(host)
        
        # Limit both global concurrency and per-host concurrency
        async with self.__request_limiter.global_semaphore, host_semaphore:
            # Increment the active request counter
            self.__active_requests += 1
            
            # Use a try-finally block to ensure we always decrement the counter
            try:
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

        headers = prepare_request_headers(config)

        # Respect rate limits
        should_limit, wait_seconds = should_rate_limit(self.__rate_limit_last_call, config)
        if should_limit and wait_seconds:
            await asyncio.sleep(wait_seconds)
            self.__rate_limit_last_call = datetime.now()

        api_url = prepare_api_url(config, language)
        query_identifier = str(params.get("titles", params.get("search", "unknown")))
        
        # Check if we need to refresh the session
        if self.increment_reuse_counter() > self.__max_reuse_count:
            await self.new_session()
        
        # Check if we need to detect the API version
        if api_url not in config.detected_api_versions:
            version = await self.detect_api_version(api_url, config)
            if version:
                config.set_api_version(api_url, version)
            
        # Implement retry logic
        attempt = 0
        max_attempts = config.max_retries + 1  # +1 for the initial attempt
        last_exception = None
        
        while attempt < max_attempts:
            try:
                # If this is a retry, apply backoff
                if attempt > 0:
                    # Calculate backoff with jitter
                    backoff_with_jitter = calculate_backoff_with_jitter(config, attempt - 1)
                    await asyncio.sleep(backoff_with_jitter)
                    
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
                # Record timeout error for backpressure control
                self.__backpressure_controller.record_error(None)
                
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
                
                # Record error for backpressure control
                self.__backpressure_controller.record_error(status_code)
                
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
        if not should_continue(data):
            # Decrement active requests counter before returning
            self.__active_requests -= 1
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
            merge_continue_results(result, continued_data)
            
            # If there are no more continue tokens, we're done
            if not should_continue(result):
                break

        # Decrement active requests counter before returning
        self.__active_requests -= 1
        return result
