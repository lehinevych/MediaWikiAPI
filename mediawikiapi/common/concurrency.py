"""
Concurrency control utilities.

This module provides utilities for managing concurrency in both
synchronous and asynchronous implementations of the MediaWiki API.
"""

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union, Set, Callable


class BackpressureController:
    """
    Controller for managing backpressure in high-volume request scenarios.

    This class tracks request patterns and can apply adaptive backpressure
    to prevent overwhelming the MediaWiki API servers.
    """

    def __init__(
        self,
        window_size: int = 60,  # 60 second window
        threshold_percent: float = 0.8,  # 80% of max capacity triggers backpressure
        cooldown_factor: float = 0.9,  # Backpressure decreases by 10% each window
        max_delay: float = 5.0,  # Maximum delay in seconds
    ):
        """
        Initialize the backpressure controller.

        Args:
            window_size: Size of the sliding window in seconds
            threshold_percent: Percentage of capacity at which to start applying backpressure
            cooldown_factor: Factor by which backpressure decreases each window
            max_delay: Maximum delay in seconds
        """
        self.window_size = window_size
        self.threshold_percent = threshold_percent
        self.cooldown_factor = cooldown_factor
        self.max_delay = max_delay

        self.request_timestamps: List[float] = []
        self.error_timestamps: List[float] = []
        self.current_backpressure: float = 0.0
        self.last_update_time: float = time.time()

    def record_request(self) -> None:
        """Record a new request."""
        current_time = time.time()
        self.request_timestamps.append(current_time)
        self._cleanup_old_entries(current_time)
        self._update_backpressure(current_time)

    def record_error(self, status_code: Optional[int] = None) -> None:
        """
        Record an error response.

        Args:
            status_code: HTTP status code if available
        """
        current_time = time.time()
        self.error_timestamps.append(current_time)
        self._cleanup_old_entries(current_time)

        # Errors cause immediate backpressure increase
        if status_code in {429, 503, 504}:  # Rate limiting or server overload
            self.current_backpressure = min(
                self.current_backpressure + 0.5,  # Large increase for rate limit errors
                self.max_delay,
            )
        else:
            self.current_backpressure = min(
                self.current_backpressure + 0.1,  # Small increase for other errors
                self.max_delay,
            )

    def get_delay(self, priority: int = 0) -> float:
        """
        Get the current backpressure delay.

        Args:
            priority: Request priority (higher values = higher priority)

        Returns:
            Delay in seconds
        """
        # High priority requests get less delay
        if priority > 0:
            return max(0.0, self.current_backpressure / (priority + 1))
        return self.current_backpressure

    def _cleanup_old_entries(self, current_time: float) -> None:
        """
        Remove entries older than the window size.

        Args:
            current_time: Current timestamp
        """
        cutoff_time = current_time - self.window_size

        # Clean up old request timestamps
        self.request_timestamps = [
            ts for ts in self.request_timestamps if ts >= cutoff_time
        ]

        # Clean up old error timestamps
        self.error_timestamps = [
            ts for ts in self.error_timestamps if ts >= cutoff_time
        ]

    def _update_backpressure(self, current_time: float) -> None:
        """
        Update backpressure based on request patterns.

        Args:
            current_time: Current timestamp
        """
        # Only update periodically
        if current_time - self.last_update_time < 1.0:  # Update at most once per second
            return

        self.last_update_time = current_time

        # Calculate request rate per second
        window_requests = len(self.request_timestamps)
        window_errors = len(self.error_timestamps)

        # Cool down backpressure over time
        self.current_backpressure *= self.cooldown_factor

        # Apply more backpressure if we have many errors
        error_ratio = window_errors / max(1, window_requests)
        if error_ratio > 0.05:  # More than 5% errors
            self.current_backpressure = min(
                self.current_backpressure + (error_ratio * 2), self.max_delay
            )


class AsyncRequestLimiter:
    """
    Limiter for controlling concurrent async requests.

    This class provides semaphores and monitoring for limiting
    concurrent requests both globally and per host.
    """

    def __init__(
        self,
        global_limit: int = 10,
        per_host_limit: int = 4,
    ):
        """
        Initialize the request limiter.

        Args:
            global_limit: Maximum number of concurrent requests globally
            per_host_limit: Maximum number of concurrent requests per host
        """
        self.global_limit = global_limit
        self.per_host_limit = per_host_limit
        self.global_semaphore = asyncio.Semaphore(global_limit)
        self.host_semaphores: Dict[str, asyncio.Semaphore] = {}
        self.active_requests: int = 0
        self.active_requests_per_host: Dict[str, int] = {}

    def get_host_semaphore(self, host: str) -> asyncio.Semaphore:
        """
        Get or create a semaphore for a specific host.

        Args:
            host: Hostname

        Returns:
            Semaphore for the host
        """
        if host not in self.host_semaphores:
            self.host_semaphores[host] = asyncio.Semaphore(self.per_host_limit)
            self.active_requests_per_host[host] = 0
        return self.host_semaphores[host]

    def set_global_limit(self, limit: int) -> None:
        """
        Set a new global request limit.

        Args:
            limit: New global limit
        """
        if limit < 1:
            raise ValueError("Global limit must be at least 1")
        self.global_limit = limit
        # Create a new semaphore with the new limit
        self.global_semaphore = asyncio.Semaphore(limit)

    def set_per_host_limit(self, limit: int) -> None:
        """
        Set a new per-host request limit.

        Args:
            limit: New per-host limit
        """
        if limit < 1:
            raise ValueError("Per-host limit must be at least 1")
        self.per_host_limit = limit
        # Create new semaphores for each host with the new limit
        for host in self.host_semaphores:
            self.host_semaphores[host] = asyncio.Semaphore(limit)
