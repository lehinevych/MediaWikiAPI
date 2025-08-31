"""Tests for concurrency controls in the MediaWikiAPI."""

import asyncio
import pytest
from unittest.mock import patch, Mock, AsyncMock

from mediawikiapi.async_api.async_mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.async_api.async_requestsession import AsyncRequestSession
from mediawikiapi.common.concurrency import BackpressureController, AsyncRequestLimiter
from mediawikiapi.config import Config


class TestBackpressureController:
    """Tests for the BackpressureController class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        controller = BackpressureController()
        assert controller.window_size == 60
        assert controller.threshold_percent == 0.8
        assert controller.cooldown_factor == 0.9
        assert controller.max_delay == 5.0
        assert controller.current_backpressure == 0.0

    def test_record_request(self):
        """Test recording a request."""
        controller = BackpressureController()
        controller.record_request()
        assert len(controller.request_timestamps) == 1

    def test_record_error(self):
        """Test recording an error."""
        controller = BackpressureController()
        controller.record_error(429)  # Rate limit error
        assert len(controller.error_timestamps) == 1
        assert controller.current_backpressure > 0

    def test_get_delay_with_priority(self):
        """Test getting delay with different priorities."""
        controller = BackpressureController()
        controller.current_backpressure = 1.0

        # Higher priority should get less delay
        delay_low = controller.get_delay(0)
        delay_high = controller.get_delay(10)

        assert delay_low > delay_high

    def test_cleanup_old_entries(self):
        """Test cleaning up old entries."""
        controller = BackpressureController(window_size=0.1)  # Small window for testing
        controller.record_request()
        controller.record_error()

        # Wait for entries to age out
        import time

        time.sleep(0.2)

        controller._cleanup_old_entries(time.time())
        assert len(controller.request_timestamps) == 0
        assert len(controller.error_timestamps) == 0


class TestAsyncRequestLimiter:
    """Tests for the AsyncRequestLimiter class."""

    def test_init(self):
        """Test initialization."""
        limiter = AsyncRequestLimiter(global_limit=5, per_host_limit=3)
        assert limiter.global_limit == 5
        assert limiter.per_host_limit == 3

    def test_get_host_semaphore(self):
        """Test getting a host semaphore."""
        limiter = AsyncRequestLimiter()
        semaphore = limiter.get_host_semaphore("example.org")
        assert semaphore is not None
        assert "example.org" in limiter.host_semaphores

    def test_set_global_limit(self):
        """Test setting a new global limit."""
        limiter = AsyncRequestLimiter()
        limiter.set_global_limit(20)
        assert limiter.global_limit == 20

    def test_set_per_host_limit(self):
        """Test setting a new per-host limit."""
        limiter = AsyncRequestLimiter()
        limiter.set_per_host_limit(8)
        assert limiter.per_host_limit == 8


class TestAsyncRequestSession:
    """Tests for concurrency controls in AsyncRequestSession."""

    @pytest.mark.asyncio
    async def test_init_with_pool_settings(self):
        """Test initialization with connection pool settings."""
        session = AsyncRequestSession(pool_size=50, pool_connections_per_host=5)
        assert session._AsyncRequestSession__pool_size == 50
        assert session._AsyncRequestSession__pool_connections_per_host == 5

    @pytest.mark.asyncio
    async def test_set_max_concurrent_requests(self):
        """Test setting maximum concurrent requests."""
        session = AsyncRequestSession()
        session.set_max_concurrent_requests(15)
        assert session._AsyncRequestSession__max_concurrent_requests == 15

    @pytest.mark.asyncio
    async def test_backpressure_control(self):
        """Test that backpressure is applied."""
        # Create a session with a mock backpressure controller
        session = AsyncRequestSession()
        mock_controller = Mock()
        mock_controller.record_request = Mock()
        mock_controller.get_delay = Mock(return_value=0.1)
        session._AsyncRequestSession__backpressure_controller = mock_controller

        # Mock the session to avoid actual HTTP requests
        mock_session = AsyncMock()
        mock_session.get = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value={"query": {}})
        mock_session.get.return_value.__aenter__.return_value = mock_response
        session._AsyncRequestSession__session = mock_session

        # Make a request
        config = Config()
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await session.request({"action": "query"}, config)

            # Verify backpressure was applied
            mock_controller.record_request.assert_called_once()
            mock_controller.get_delay.assert_called_once()
            mock_sleep.assert_called_once_with(0.1)


class TestAsyncMediaWikiAPI:
    """Tests for concurrency controls in AsyncMediaWikiAPI."""

    def test_init_with_config(self):
        """Test initialization with concurrency settings in config."""
        config = Config(
            connection_pool_size=75, connections_per_host=8, max_concurrent_requests=12
        )
        api = AsyncMediaWikiAPI(config)
        assert api.session._AsyncRequestSession__pool_size == 75
        assert api.session._AsyncRequestSession__pool_connections_per_host == 8
        assert api.session._AsyncRequestSession__max_concurrent_requests == 12

    def test_set_connection_pool_size(self):
        """Test setting connection pool size."""
        api = AsyncMediaWikiAPI()
        api.set_connection_pool_size(60)
        assert api.config.connection_pool_size == 60
        assert api.session._AsyncRequestSession__pool_size == 60

    def test_set_connections_per_host(self):
        """Test setting connections per host."""
        api = AsyncMediaWikiAPI()
        api.set_connections_per_host(7)
        assert api.config.connections_per_host == 7
        assert api.session._AsyncRequestSession__pool_connections_per_host == 7

    def test_set_concurrent_request_limit(self):
        """Test setting concurrent request limit."""
        api = AsyncMediaWikiAPI()
        api.set_concurrent_request_limit(15)
        assert api.config.max_concurrent_requests == 15
        assert api.session._AsyncRequestSession__max_concurrent_requests == 15
