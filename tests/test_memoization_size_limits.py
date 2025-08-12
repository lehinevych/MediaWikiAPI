import unittest

import pytest

from mediawikiapi.sync.util import memorized


class TestMemoizationSizeLimits(unittest.TestCase):
    def setUp(self):
        # Reset any cached state between tests
        self.call_count = 0

    def test_cache_size_limit(self):
        """Test that cache respects the size limit"""
        call_count = 0  # Local to this test only

        # Creating a fresh memoized function for this test
        class TestClass:
            def __init__(self):
                self.counter = 0

            @memorized(max_size=3)  # Set cache size to 3 entries
            def cached_function(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        test_instance = TestClass()

        # Fill the cache with 3 entries
        result1 = test_instance.cached_function("A")  # Oldest entry
        result2 = test_instance.cached_function("B")
        result3 = test_instance.cached_function("C")  # Newest entry

        self.assertEqual(result1, "A-1")
        self.assertEqual(result2, "B-2")
        self.assertEqual(result3, "C-3")
        self.assertEqual(test_instance.counter, 3)

        # Add a 4th entry, should evict the oldest (A)
        result4 = test_instance.cached_function("D")
        self.assertEqual(result4, "D-4")
        self.assertEqual(test_instance.counter, 4)

        # Now "A" should be evicted from the cache and recomputed
        result1_recomputed = test_instance.cached_function("A")
        self.assertEqual(result1_recomputed, "A-5")  # Note the new value
        self.assertEqual(test_instance.counter, 5)  # One more call

        # At this point, the LRU order should be: B (oldest), C, D, A (newest)
        # Let's add one more item to evict B
        result5 = test_instance.cached_function("E")
        self.assertEqual(result5, "E-6")
        self.assertEqual(test_instance.counter, 6)

        # Now B should be evicted, while C, D, A, E should be in the cache
        result_b = test_instance.cached_function("B")
        self.assertEqual(result_b, "B-7")  # B recomputed
        self.assertEqual(test_instance.counter, 7)

        # C was evicted when we added B, since our max_size is 3
        # So now our cache only has: D, A, E (newest)
        result_c = test_instance.cached_function("C")
        self.assertEqual(result_c, "C-8")  # C is recomputed
        self.assertEqual(test_instance.counter, 8)

        # Now our cache has: A, E, C (newest)
        # D will be recomputed
        result_d = test_instance.cached_function("D")
        self.assertEqual(result_d, "D-9")  # D is recomputed
        self.assertEqual(test_instance.counter, 9)  # One more computation

        # Let's add a new value F, which should evict E (the oldest)
        result_f = test_instance.cached_function("F")
        self.assertEqual(result_f, "F-10")
        self.assertEqual(test_instance.counter, 10)

        # Now E should be evicted, and access should recompute
        result_e = test_instance.cached_function("E")
        self.assertEqual(result_e, "E-11")  # E recomputed
        self.assertEqual(test_instance.counter, 11)

    def test_lru_behavior(self):
        """Test that the cache uses LRU (Least Recently Used) eviction strategy"""

        # Creating a fresh memoized function for this test
        class TestClass:
            def __init__(self):
                self.counter = 0

            @memorized(max_size=3)  # Set cache size to 3 entries
            def cached_function(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        test_instance = TestClass()

        # Fill the cache with 3 entries
        test_instance.cached_function("A")  # A is oldest
        test_instance.cached_function("B")
        test_instance.cached_function("C")  # C is newest
        self.assertEqual(test_instance.counter, 3)

        # Access B, making it most recent and A still the least recently used
        # Order is now: A (oldest), C, B (newest)
        test_instance.cached_function("B")
        self.assertEqual(test_instance.counter, 3)  # No new calls

        # Add a 4th entry, should evict A (the least recently used)
        # Order becomes: C (oldest), B, D (newest)
        test_instance.cached_function("D")
        self.assertEqual(test_instance.counter, 4)

        # A should be recomputed since it was evicted
        test_instance.cached_function("A")
        self.assertEqual(test_instance.counter, 5)  # A is recomputed

        # Order is now: B (oldest), D, A (newest)
        # Add E, which should evict B since it's now the oldest in LRU order
        test_instance.cached_function("E")
        self.assertEqual(test_instance.counter, 6)

        # B should be recomputed
        result_b = test_instance.cached_function("B")
        self.assertEqual(result_b, "B-7")  # B recomputed
        self.assertEqual(test_instance.counter, 7)

        # Now order is D (oldest), A, E, B (newest)
        # D should be evicted next
        result_f = test_instance.cached_function("F")
        self.assertEqual(result_f, "F-8")
        self.assertEqual(test_instance.counter, 8)

        # D should be recomputed
        result_d = test_instance.cached_function("D")
        self.assertEqual(result_d, "D-9")  # Recomputed
        self.assertEqual(test_instance.counter, 9)

    def test_default_unlimited_size(self):
        """Test that the default behavior has no size limit"""

        # Creating a fresh memoized function for this test
        class TestClass:
            def __init__(self):
                self.counter = 0

            @memorized  # No max_size specified
            def cached_function(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        test_instance = TestClass()

        # Add many entries to the cache
        for i in range(100):
            test_instance.cached_function(f"key{i}")

        self.assertEqual(test_instance.counter, 100)

        # Call again with the same arguments - all should be cached
        for i in range(100):
            test_instance.cached_function(f"key{i}")

        self.assertEqual(test_instance.counter, 100)  # No new calls

    def test_combined_ttl_and_size_limit(self):
        """Test that both TTL and size limit work together"""
        import time

        # Creating a fresh memoized function for this test
        class TestClass:
            def __init__(self):
                self.counter = 0

            @memorized(ttl=0.1, max_size=2)
            def cached_function(self, arg):
                self.counter += 1
                return f"{arg}-{self.counter}"

        test_instance = TestClass()

        # Fill the cache with 2 entries
        test_instance.cached_function("A")
        test_instance.cached_function("B")
        self.assertEqual(test_instance.counter, 2)

        # Wait for cache to expire
        time.sleep(0.2)

        # Even though we're within the size limit, entries should be expired
        test_instance.cached_function("A")
        test_instance.cached_function("B")
        self.assertEqual(test_instance.counter, 4)  # Both recomputed
