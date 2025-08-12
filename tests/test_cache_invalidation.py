import unittest
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from mediawikiapi import MediaWikiAPI
from mediawikiapi.util import memorized


class TestCacheInvalidation(unittest.TestCase):
    def test_decorator_invalidation(self):
        """Test the direct cache invalidation methods on decorated functions"""

        counter = 0

        @memorized
        def test_func(arg):
            nonlocal counter
            counter += 1
            return f"{arg}-{counter}"

        # First call should increment counter
        result1 = test_func("test")
        self.assertEqual(result1, "test-1")
        self.assertEqual(counter, 1)

        # Second call should use cache
        result2 = test_func("test")
        self.assertEqual(result2, "test-1")
        self.assertEqual(counter, 1)  # No increment

        # Invalidate the cache for this specific call
        self.assertTrue(test_func.invalidate_cache("test"))

        # Call again - should recompute
        result3 = test_func("test")
        self.assertEqual(result3, "test-2")
        self.assertEqual(counter, 2)  # Incremented

        # Call with different args - should compute new value
        test_func("other")
        self.assertEqual(counter, 3)

        # Invalidate all cache
        count = test_func.invalidate_all_cache()
        self.assertEqual(count, 2)  # Two entries were in cache

        # Both calls should recompute now
        test_func("test")
        test_func("other")
        self.assertEqual(counter, 5)  # Two more increments

    def test_instance_method_invalidation(self):
        """Test cache invalidation on instance methods using mocks"""
        api = MediaWikiAPI()

        # Create a mock search method with cache invalidation
        search_results = ["Python", "Python language", "Python snake"]

        # Mock the search method
        with patch.object(api, "search") as mock_search:
            # Set up the mock to return our predefined results and expose invalidation methods
            mock_search.return_value = search_results
            mock_search.invalidate_cache = Mock(return_value=True)
            mock_search.invalidate_all_cache = Mock(return_value=2)

            # Call the search method
            api.search("Python")
            api.search("Python")  # Should use cache (if real)

            # Test invalidate_cache method
            self.assertTrue(api.invalidate_cache("search", "Python"))
            mock_search.invalidate_cache.assert_called_once_with(api, "Python")

            # Test invalidate_all_method_cache method
            count = api.invalidate_all_method_cache("search")
            self.assertEqual(count, 2)
            mock_search.invalidate_all_cache.assert_called_once()

    def test_global_cache_operations(self):
        """Test global cache operations with mocked functions"""
        api = MediaWikiAPI()

        # Mock the cache util functions
        with (
            patch("mediawikiapi.cache_util.get_cache_statistics") as mock_stats,
            patch("mediawikiapi.cache_util.invalidate_all_caches") as mock_invalidate,
        ):
            # Set up mocks to return our predefined results
            mock_stats.return_value = {"search": 2, "page": 1}
            mock_invalidate.return_value = {"search": 2, "page": 1}

            # Get statistics
            stats = api.get_cache_statistics()
            self.assertIsInstance(stats, Dict)
            self.assertEqual(len(stats), 2)
            self.assertEqual(stats.get("search"), 2)
            self.assertEqual(stats.get("page"), 1)

            # Invalidate all caches
            invalidated = api.invalidate_all_caches()
            self.assertIsInstance(invalidated, Dict)

            # Check that mocks were called with the API instance
            mock_stats.assert_called_once_with(api)
            mock_invalidate.assert_called_once_with(api)
