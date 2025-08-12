import asyncio
import unittest
import time
from typing import Any, Dict, Optional

import pytest

from mediawikiapi import AsyncMediaWikiAPI, Config
from mediawikiapi.async_util import async_memorized


class TestAsyncCacheParameters(unittest.TestCase):
    """Tests for TTL and max_size parameters in async cache functionality."""

    def test_ttl_parameter(self):
        """Test that TTL parameter works with async cached functions."""

        counter = 0

        @async_memorized(ttl=0.1)  # Very short TTL for testing
        async def cached_func(arg):
            nonlocal counter
            counter += 1
            return f"{arg}-{counter}"

        async def run_tests():
            nonlocal counter

            # First call should cache
            result1 = await cached_func("test")
            assert result1 == "test-1"
            assert counter == 1

            # Second call should use cache
            result2 = await cached_func("test")
            assert result2 == "test-1"
            assert counter == 1

            # Wait for TTL to expire
            await asyncio.sleep(0.2)

            # Call should recompute after TTL expiration
            result3 = await cached_func("test")
            assert result3 == "test-2"  # Counter incremented
            assert counter == 2

            return "OK"

        # Run the async test
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_tests())
        self.assertEqual(result, "OK")

    def test_max_size_parameter(self):
        """Test that max_size parameter works with async cached functions."""

        counter = 0

        @async_memorized(max_size=2)  # Only cache 2 entries
        async def cached_func(arg):
            nonlocal counter
            counter += 1
            return f"{arg}-{counter}"

        async def run_tests():
            nonlocal counter

            # Fill cache with 2 entries
            result_a = await cached_func("A")
            result_b = await cached_func("B")
            assert counter == 2

            # Access both again - should be cached
            await cached_func("A")
            await cached_func("B")
            assert counter == 2  # No change

            # Add a third entry - should evict oldest (A)
            result_c = await cached_func("C")
            assert counter == 3

            # A should be recomputed, B and C should be cached
            result_a2 = await cached_func("A")
            assert result_a2 != result_a  # Recomputed
            assert counter == 4

            # B was evicted after adding A again (now the oldest), so B gets recomputed
            await cached_func("B") 
            assert counter == 5  # B is recomputed
            
            # Current cache should have A and B only, C was evicted
            await cached_func("C") 
            assert counter == 6  # C is recomputed

            return "OK"

        # Run the async test
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_tests())
        self.assertEqual(result, "OK")

    def test_config_ttl_parameter(self):
        """Test that Config's cache_ttl is used when no explicit TTL is provided."""

        counter = 0

        class MockAPI:
            def __init__(self):
                self.config = Config(cache_ttl=0.1)  # Very short TTL from config
                self.counter = 0

            @async_memorized  # No explicit TTL, should use config
            async def cached_method(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        async def run_tests():
            api = MockAPI()

            # First call should cache
            result1 = await api.cached_method("test")
            assert result1 == "test-1"
            assert api.counter == 1

            # Second call should use cache
            result2 = await api.cached_method("test")
            assert result2 == "test-1"
            assert api.counter == 1

            # Wait for TTL to expire
            await asyncio.sleep(0.2)

            # Call should recompute after TTL expiration
            result3 = await api.cached_method("test")
            assert result3 == "test-2"  # Counter incremented
            assert api.counter == 2

            return "OK"

        # Run the async test
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_tests())
        self.assertEqual(result, "OK")

    def test_config_max_size_parameter(self):
        """Test that Config's cache_max_size is used when no explicit max_size is provided."""

        class MockAPI:
            def __init__(self):
                self.config = Config(cache_max_size=2)  # Only cache 2 entries
                self.counter = 0

            @async_memorized  # No explicit max_size, should use config
            async def cached_method(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        async def run_tests():
            api = MockAPI()

            # Fill cache with 2 entries
            result_a = await api.cached_method("A")
            result_b = await api.cached_method("B")
            assert api.counter == 2

            # Access both again - should be cached
            await api.cached_method("A")
            await api.cached_method("B")
            assert api.counter == 2  # No change

            # Add a third entry - should evict oldest (A)
            result_c = await api.cached_method("C")
            assert api.counter == 3

            # A should be recomputed, B and C should be cached
            result_a2 = await api.cached_method("A")
            assert result_a2 != result_a  # Recomputed
            assert api.counter == 4

            return "OK"

        # Run the async test
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_tests())
        self.assertEqual(result, "OK")

    def test_override_parameters(self):
        """Test that decorator parameters override config parameters."""

        class MockAPI:
            def __init__(self):
                self.config = Config(cache_ttl=10.0, cache_max_size=10)  # Config values
                self.counter = 0

            @async_memorized(ttl=0.1, max_size=2)  # Override with decorator values
            async def cached_method(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        async def run_tests():
            api = MockAPI()

            # Test TTL override (0.1 from decorator vs 10.0 from config)
            result1 = await api.cached_method("test")
            await api.cached_method("test")  # Should use cache
            assert api.counter == 1

            # Wait for decorator TTL to expire
            await asyncio.sleep(0.2)

            # Call should recompute after TTL expiration
            result2 = await api.cached_method("test")
            assert api.counter == 2  # Recomputed due to decorator TTL

            # Test max_size override (2 from decorator vs 10 from config)
            await api.cached_method("A")  # This and "test" fill the cache
            assert api.counter == 3

            # Add third entry - should evict oldest ("test")
            await api.cached_method("B")
            assert api.counter == 4

            # "test" should be recomputed
            await api.cached_method("test")
            assert api.counter == 5

            return "OK"

        # Run the async test
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run_tests())
        self.assertEqual(result, "OK")
