import time
import unittest

import pytest

from mediawikiapi.util import memorized


class TestMemoizationExpiry(unittest.TestCase):
    def test_cache_expiration(self):
        """Test that cached values expire after TTL"""
        call_count = 0

        @memorized(ttl=0.5)  # Set TTL to 0.5 seconds
        def cached_function(arg):
            nonlocal call_count
            call_count += 1
            return f"{arg}-{call_count}"

        # First call
        result1 = cached_function("test")
        self.assertEqual(result1, "test-1")
        self.assertEqual(call_count, 1)

        # Call again immediately - should return cached value
        result2 = cached_function("test")
        self.assertEqual(result2, "test-1")
        self.assertEqual(call_count, 1)  # Function not called again

        # Wait for cache to expire
        time.sleep(0.6)

        # Call again after expiration - should compute new value
        result3 = cached_function("test")
        self.assertEqual(result3, "test-2")
        self.assertEqual(call_count, 2)  # Function called again

    def test_default_no_expiration(self):
        """Test that default behavior has no expiration"""
        call_count = 0

        @memorized  # No TTL specified
        def cached_function(arg):
            nonlocal call_count
            call_count += 1
            return f"{arg}-{call_count}"

        # First call
        result1 = cached_function("test")
        self.assertEqual(result1, "test-1")
        self.assertEqual(call_count, 1)

        # Wait some time
        time.sleep(0.1)

        # Call again - should still use cached value
        result2 = cached_function("test")
        self.assertEqual(result2, "test-1")
        self.assertEqual(call_count, 1)  # Function not called again

    def test_class_method_expiration(self):
        """Test expiration works with class methods"""

        class TestClass:
            def __init__(self):
                self.call_count = 0

            @memorized(ttl=0.5)
            def cached_method(self, arg):
                self.call_count += 1
                return f"{arg}-{self.call_count}"

        instance = TestClass()

        # First call
        result1 = instance.cached_method("test")
        self.assertEqual(result1, "test-1")
        self.assertEqual(instance.call_count, 1)

        # Call again immediately - should return cached value
        result2 = instance.cached_method("test")
        self.assertEqual(result2, "test-1")
        self.assertEqual(instance.call_count, 1)

        # Wait for cache to expire
        time.sleep(0.6)

        # Call again after expiration - should compute new value
        result3 = instance.cached_method("test")
        self.assertEqual(result3, "test-2")
        self.assertEqual(instance.call_count, 2)
