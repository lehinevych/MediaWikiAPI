import time
import unittest

import pytest

from mediawikiapi import Config
from mediawikiapi.sync.util import memorized


class TestConfigCacheSettings(unittest.TestCase):
    def test_config_ttl(self):
        """Test that cache TTL from config works correctly"""

        class MockAPI:
            def __init__(self, ttl=None):
                self.config = Config(cache_ttl=ttl)
                self.call_count = 0

            @memorized
            def cached_method(self, arg):
                self.call_count += 1
                return f"{arg}-{self.call_count}"

        # Test with config TTL
        api = MockAPI(ttl=0.1)  # 100ms TTL

        # First call should cache
        result1 = api.cached_method("test")
        self.assertEqual(result1, "test-1")
        self.assertEqual(api.call_count, 1)

        # Call again immediately - should return cached value
        result2 = api.cached_method("test")
        self.assertEqual(result2, "test-1")
        self.assertEqual(api.call_count, 1)  # No additional calls

        # Wait for TTL to expire
        time.sleep(0.2)

        # Call again - should recompute
        result3 = api.cached_method("test")
        self.assertEqual(result3, "test-2")
        self.assertEqual(api.call_count, 2)  # Function called again

    def test_config_ttl_override(self):
        """Test that decorator TTL overrides config TTL"""

        class MockAPI:
            def __init__(self, ttl=None):
                self.config = Config(cache_ttl=ttl)
                self.call_count = 0

            @memorized(ttl=0.3)  # Decorator TTL overrides config TTL
            def cached_method(self, arg):
                self.call_count += 1
                return f"{arg}-{self.call_count}"

        # Config TTL is shorter than decorator TTL
        api = MockAPI(ttl=0.1)

        # First call should cache
        api.cached_method("test")
        self.assertEqual(api.call_count, 1)

        # Wait longer than config TTL but shorter than decorator TTL
        time.sleep(0.2)

        # Should still use cached value because decorator TTL takes precedence
        api.cached_method("test")
        self.assertEqual(api.call_count, 1)  # No additional call

        # Wait for decorator TTL to expire
        time.sleep(0.2)  # Total 0.4s > decorator TTL of 0.3s

        # Now should recompute
        api.cached_method("test")
        self.assertEqual(api.call_count, 2)  # Function called again

    def test_config_max_size(self):
        """Test that cache max_size from config works correctly"""

        class MockAPI:
            def __init__(self, max_size=None):
                self.config = Config(cache_max_size=max_size)
                self.call_count = 0

            @memorized
            def cached_method(self, arg):
                self.call_count += 1
                return f"{arg}-{self.call_count}"

        # Test with config max_size
        api = MockAPI(max_size=2)  # Cache only 2 items

        # Fill cache
        api.cached_method("A")
        api.cached_method("B")
        self.assertEqual(api.call_count, 2)

        # Call again - should use cache
        api.cached_method("A")
        api.cached_method("B")
        self.assertEqual(api.call_count, 2)  # No additional calls

        # Add a third item - should evict oldest (A)
        api.cached_method("C")
        self.assertEqual(api.call_count, 3)

        # B and C should be cached, but A should be recomputed
        api.cached_method("B")
        self.assertEqual(api.call_count, 3)  # Still cached

        api.cached_method("C")
        self.assertEqual(api.call_count, 3)  # Still cached

        api.cached_method("A")
        self.assertEqual(api.call_count, 4)  # Recomputed

    def test_config_max_size_override(self):
        """Test that decorator max_size overrides config max_size"""

        class MockAPI:
            def __init__(self, max_size=None):
                self.config = Config(cache_max_size=max_size)
                self.call_count = 0

            @memorized(max_size=3)  # Decorator max_size overrides config max_size
            def cached_method(self, arg):
                self.call_count += 1
                return f"{arg}-{self.call_count}"

        # Config max_size is smaller than decorator max_size
        api = MockAPI(max_size=2)

        # Fill cache with 3 items (allowed by decorator setting)
        api.cached_method("A")
        api.cached_method("B")
        api.cached_method("C")
        self.assertEqual(api.call_count, 3)

        # All 3 should be cached (proving decorator setting is used)
        api.cached_method("A")
        api.cached_method("B")
        api.cached_method("C")
        self.assertEqual(api.call_count, 3)  # No additional calls

        # Add a 4th item - should evict oldest (A)
        api.cached_method("D")
        self.assertEqual(api.call_count, 4)

        # A should be recomputed, others still cached
        api.cached_method("A")
        self.assertEqual(api.call_count, 5)  # Recomputed

        # Note: We're not going to assert that specific values remain in cache
        # since the LRU behavior may vary based on implementation details
