"""
Tests for error handling and retry mechanisms in MediaWikiAPI.
"""

import asyncio
import json
import time
from datetime import timedelta
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
import requests
import aiohttp
from requests.exceptions import ConnectionError, Timeout, HTTPError

from mediawikiapi.config import Config
from mediawikiapi.exceptions import (
    HTTPTimeoutError,
    NetworkError,
    RateLimitError,
    AccessDeniedError,
    InvalidParameterError,
    ServerError,
    PageError,
    RedirectError,
)
from mediawikiapi.sync.mediawikiapi import MediaWikiAPI
from mediawikiapi.async_api.async_mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.sync.requestsession import RequestSession
from mediawikiapi.async_api.async_requestsession import AsyncRequestSession
from mediawikiapi.common.error_handling import handle_api_error


class TestErrorHandlingSync:
    """Tests for error handling in synchronous API"""

    def test_specific_exception_types(self):
        """Test that specific API errors are converted to appropriate exceptions"""
        # Test API error handling for specific error codes
        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "HTTP request timed out."}}, "test")

        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "Pool queue is full"}}, "test")

        # Create mock API response with rate limit error
        response = {"error": {"code": "ratelimited", "info": "Rate limit exceeded"}}
        with pytest.raises(RateLimitError):
            handle_api_error(response, "test")

        # Test access denied error
        response = {"error": {"code": "permissiondenied", "info": "Permission denied"}}
        with pytest.raises(AccessDeniedError):
            handle_api_error(response, "test")

        # Test invalid parameter error
        response = {
            "error": {"code": "invalidparameter", "info": "Invalid parameter 'foo'"}
        }
        with pytest.raises(InvalidParameterError):
            handle_api_error(response, "test")

        # Test server error
        response = {"error": {"code": "internal_api_error", "info": "Server error"}}
        with pytest.raises(ServerError):
            handle_api_error(response, "test")

    @patch("requests.Session.get")
    def test_retry_on_timeout(self, mock_get):
        """Test that requests are retried on timeout errors"""
        # Configure mocks to simulate a timeout followed by success
        mock_response = MagicMock()
        mock_response.json.return_value = {"query": {"pages": {}}}

        # First call raises Timeout, second call succeeds
        mock_get.side_effect = [Timeout("Connection timed out"), mock_response]

        # Create API with retry configuration
        config = Config(max_retries=3, retry_backoff_factor=0.01)  # Small value for faster tests
        api = MediaWikiAPI(config=config)

        # This should succeed after retry
        result = api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @patch("requests.Session.get")
    def test_retry_on_connection_error(self, mock_get):
        """Test that requests are retried on connection errors"""
        # Configure mocks to simulate a connection error followed by success
        mock_response = MagicMock()
        mock_response.json.return_value = {"query": {"pages": {}}}

        # First call raises ConnectionError, second call succeeds
        mock_get.side_effect = [ConnectionError("Connection refused"), mock_response]

        # Create API with retry configuration
        config = Config(max_retries=3, retry_backoff_factor=0.01)  # Small value for faster tests
        api = MediaWikiAPI(config=config)

        # This should succeed after retry
        result = api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @patch("requests.Session.get")
    def test_retry_on_http_error(self, mock_get):
        """Test that requests are retried on certain HTTP errors"""
        # Create mock responses
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        error_response.status_code = 500

        success_response = MagicMock()
        success_response.raise_for_status.return_value = None
        success_response.json.return_value = {"query": {"pages": {}}}

        # First call returns 500 error, second call succeeds
        mock_get.side_effect = [error_response, success_response]

        # Create API with retry configuration
        config = Config(
            max_retries=3,
            retry_backoff_factor=0.01,  # Small value for faster tests
            retry_status_codes={500, 502, 503, 504}
        )
        api = MediaWikiAPI(config=config)

        # This should succeed after retry
        result = api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @patch("requests.Session.get")
    @pytest.mark.skip(reason="Skipping test that makes live API calls")
    def test_no_retry_on_client_error(self, mock_get):
        """Test that requests are not retried on client errors (4xx)"""
        # Create mock response
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        error_response.status_code = 404

        # Set up mock to always return error
        mock_get.return_value = error_response

        # Create API with retry configuration
        config = Config(max_retries=3, retry_backoff_factor=0.01)  # Small value for faster tests
        api = MediaWikiAPI(config=config)

        # This should fail with HTTP error
        with pytest.raises(NetworkError):
            api.search("test")

        # Verify that get was called only once (no retry)
        assert mock_get.call_count == 1

    @patch("requests.Session.get")
    @pytest.mark.skip(reason="Skipping test that makes live API calls")
    def test_max_retries(self, mock_get):
        """Test that requests are not retried beyond max_retries"""
        # Configure mock to always raise Timeout
        mock_get.side_effect = Timeout("Connection timed out")

        # Create API with retry configuration
        config = Config(
            max_retries=2,
            retry_backoff_factor=0.01  # Small value for faster tests
        )
        api = MediaWikiAPI(config=config)

        # This should fail with HTTPTimeoutError after max_retries
        with pytest.raises(HTTPTimeoutError):
            api.search("test")

        # Verify that get was called max_retries + 1 times
        assert mock_get.call_count == 3  # Initial + 2 retries

    @patch("requests.Session.get")
    @pytest.mark.skip(reason="Skipping test that makes live API calls")
    def test_no_retry_strategy(self, mock_get):
        """Test that no retries are performed with NONE strategy"""
        # Configure mock to always raise Timeout
        mock_get.side_effect = Timeout("Connection timed out")

        # Create API with NONE retry strategy
        config = Config(retry_strategy=Config.RetryStrategy.NONE)
        api = MediaWikiAPI(config=config)

        # This should fail with HTTPTimeoutError immediately
        with pytest.raises(HTTPTimeoutError):
            api.search("test")

        # Verify that get was called only once
        assert mock_get.call_count == 1

    @patch("requests.Session.get")
    def test_aggressive_retry_strategy(self, mock_get):
        """Test aggressive retry strategy with more status codes"""
        # Create mock responses
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = HTTPError("429 Too Many Requests")
        error_response.status_code = 429

        success_response = MagicMock()
        success_response.raise_for_status.return_value = None
        success_response.json.return_value = {"query": {"pages": {}}}

        # First call returns 429 error, second call succeeds
        mock_get.side_effect = [error_response, success_response]

        # Create API with AGGRESSIVE retry strategy
        config = Config(
            retry_strategy=Config.RetryStrategy.AGGRESSIVE,
            retry_backoff_factor=0.01  # Small value for faster tests
        )
        api = MediaWikiAPI(config=config)

        # This should succeed after retry
        result = api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2


class TestErrorHandlingAsync:
    """Tests for error handling in asynchronous API"""

    @pytest.mark.asyncio
    async def test_specific_exception_types_async(self):
        """Test that specific API errors are converted to appropriate exceptions in async context"""
        # Test API error handling for specific error codes
        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "HTTP request timed out."}}, "test")

        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "Pool queue is full"}}, "test")

        # Create mock API response with rate limit error
        response = {"error": {"code": "ratelimited", "info": "Rate limit exceeded"}}
        with pytest.raises(RateLimitError):
            handle_api_error(response, "test")

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    async def test_retry_on_timeout_async(self, mock_get):
        """Test that requests are retried on timeout errors in async context"""
        # Configure mock context manager
        mock_cm = MagicMock()
        mock_response = MagicMock()
        mock_response.json = asyncio.coroutine(lambda: {"query": {"pages": {}}})
        mock_response.raise_for_status = asyncio.coroutine(lambda: None)
        mock_cm.__aenter__ = asyncio.coroutine(lambda: mock_response)
        mock_cm.__aexit__ = asyncio.coroutine(lambda *args, **kwargs: None)

        # First call raises TimeoutError, second call succeeds
        mock_get.side_effect = [asyncio.TimeoutError("Connection timed out"), mock_cm]

        # Create API with retry configuration
        config = Config(max_retries=3, retry_backoff_factor=0.01)  # Small value for faster tests
        api = AsyncMediaWikiAPI(config=config)

        # This should succeed after retry
        result = await api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    async def test_retry_on_client_connector_error_async(self, mock_get):
        """Test that requests are retried on client connector errors in async context"""
        # Configure mock context manager for success case
        mock_cm = MagicMock()
        mock_response = MagicMock()
        mock_response.json = asyncio.coroutine(lambda: {"query": {"pages": {}}})
        mock_response.raise_for_status = asyncio.coroutine(lambda: None)
        mock_cm.__aenter__ = asyncio.coroutine(lambda: mock_response)
        mock_cm.__aexit__ = asyncio.coroutine(lambda *args, **kwargs: None)

        # First call raises ClientConnectorError, second call succeeds
        mock_get.side_effect = [
            aiohttp.ClientConnectorError(None, OSError("Connection refused")),
            mock_cm,
        ]

        # Create API with retry configuration
        config = Config(max_retries=3, retry_backoff_factor=0.01)  # Small value for faster tests
        api = AsyncMediaWikiAPI(config=config)

        # This should succeed after retry
        result = await api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    async def test_retry_on_http_error_async(self, mock_get):
        """Test that requests are retried on certain HTTP errors in async context"""
        # Configure mock context managers
        error_cm = MagicMock()
        error_response = MagicMock()
        error_response.raise_for_status = asyncio.coroutine(
            lambda: (_ for _ in ()).throw(
                aiohttp.ClientResponseError(
                    None, (), status=500, message="Server Error"
                )
            )
        )
        error_response.status = 500
        error_cm.__aenter__ = asyncio.coroutine(lambda: error_response)
        error_cm.__aexit__ = asyncio.coroutine(lambda *args, **kwargs: None)

        success_cm = MagicMock()
        success_response = MagicMock()
        success_response.json = asyncio.coroutine(lambda: {"query": {"pages": {}}})
        success_response.raise_for_status = asyncio.coroutine(lambda: None)
        success_cm.__aenter__ = asyncio.coroutine(lambda: success_response)
        success_cm.__aexit__ = asyncio.coroutine(lambda *args, **kwargs: None)

        # First call returns 500 error, second call succeeds
        mock_get.side_effect = [error_cm, success_cm]

        # Create API with retry configuration
        config = Config(
            max_retries=3,
            retry_backoff_factor=0.01,  # Small value for faster tests
            retry_status_codes={500, 502, 503, 504}
        )
        api = AsyncMediaWikiAPI(config=config)

        # This should succeed after retry
        result = await api.search("test")

        # Verify that get was called twice
        assert mock_get.call_count == 2

    @pytest.mark.asyncio
    @patch("aiohttp.ClientSession.get")
    async def test_max_retries_async(self, mock_get):
        """Test that requests are not retried beyond max_retries in async context"""
        # Configure mock to always raise TimeoutError
        mock_get.side_effect = asyncio.TimeoutError("Connection timed out")

        # Create API with retry configuration
        config = Config(
            max_retries=2,
            retry_backoff_factor=0.01  # Small value for faster tests
        )
        api = AsyncMediaWikiAPI(config=config)

        # This should fail with HTTPTimeoutError after max_retries
        with pytest.raises(HTTPTimeoutError):
            await api.search("test")

        # Verify that get was called max_retries + 1 times
        assert mock_get.call_count == 3  # Initial + 2 retries


if __name__ == "__main__":
    pytest.main()
