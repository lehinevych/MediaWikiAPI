import unittest
import pytest
from mediawikiapi.util import memorized
from mediawikiapi import MediaWikiAPI
from typing import Any, Optional


class MockConfig:
    def __init__(self, language: str = "en"):
        self.language = language


class MockInstanceWithConfig:
    """Test class that mimics MediaWikiAPI's config structure"""

    def __init__(self, language: str = "en"):
        self.config = MockConfig(language)

    @memorized
    def cached_method(self, arg: str) -> str:
        return f"{self.config.language}:{arg}"

    @memorized
    def method_with_kwargs(self, arg: str, *, suffix: str = "") -> str:
        return f"{self.config.language}:{arg}{suffix}"

    @memorized
    def method_with_unhashable_arg(self, arg: list[str]) -> str:
        return f"{self.config.language}:{str(arg)}"


class MockInstanceWithoutConfig:
    """Test class without config attribute"""

    @memorized
    def cached_method(self, arg: str) -> str:
        return arg


class MockInstanceWithIncompleteConfig:
    """Test class with config but no language attribute"""

    def __init__(self) -> None:
        self.config = object()

    @memorized
    def cached_method(self, arg: str) -> str:
        return arg


@memorized
def standalone_cached_function(arg: str) -> str:
    return arg


@pytest.mark.vcr()
class TestMemoization(unittest.TestCase):
    def test_basic_caching(self) -> None:
        """Test basic caching functionality with language"""
        instance = MockInstanceWithConfig()

        # First call should cache
        result1 = instance.cached_method("test")
        self.assertEqual(result1, "en:test")

        # Second call should return cached value
        result2 = instance.cached_method("test")
        self.assertEqual(result2, "en:test")
        self.assertEqual(result1, result2)

    def test_language_specific_caching(self) -> None:
        """Test that cache is language-specific"""
        instance = MockInstanceWithConfig()

        # Cache result for English
        en_result = instance.cached_method("test")
        self.assertEqual(en_result, "en:test")

        # Change language and verify new result is cached separately
        instance.config.language = "fr"
        fr_result = instance.cached_method("test")
        self.assertEqual(fr_result, "fr:test")
        self.assertNotEqual(en_result, fr_result)

        # Verify original English result is still cached
        instance.config.language = "en"
        self.assertEqual(instance.cached_method("test"), en_result)

    def test_kwargs_caching(self) -> None:
        """Test caching with keyword arguments"""
        instance = MockInstanceWithConfig()

        # Test with different keyword arguments
        result1 = instance.method_with_kwargs("test", suffix="_1")
        result2 = instance.method_with_kwargs("test", suffix="_2")

        self.assertNotEqual(result1, result2)

        # Verify cache works for same arguments
        self.assertEqual(instance.method_with_kwargs("test", suffix="_1"), result1)

    def test_unhashable_arguments(self) -> None:
        """Test behavior with unhashable arguments (should not cache)"""
        instance = MockInstanceWithConfig()

        # Call with unhashable argument (list)
        result1 = instance.method_with_unhashable_arg(["item"])
        result2 = instance.method_with_unhashable_arg(["item"])

        # Results should be equal but not cached
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "en:['item']")

    def test_instance_without_config(self) -> None:
        """Test caching on instance without config attribute"""
        instance = MockInstanceWithoutConfig()

        result1 = instance.cached_method("test")
        result2 = instance.cached_method("test")

        # Should still cache without language
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "test")

    def test_instance_with_incomplete_config(self) -> None:
        """Test caching on instance with config but no language attribute"""
        instance = MockInstanceWithIncompleteConfig()

        result1 = instance.cached_method("test")
        result2 = instance.cached_method("test")

        # Should still cache without language
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "test")

    def test_standalone_function(self) -> None:
        """Test caching on standalone function without instance"""
        result1 = standalone_cached_function("test")
        result2 = standalone_cached_function("test")

        # Should cache normally
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "test")

    def test_none_argument(self) -> None:
        """Test caching with None as argument"""
        instance = MockInstanceWithConfig()

        # Test with None as an argument
        result1 = instance.cached_method(None)
        result2 = instance.cached_method(None)

        # Should handle None argument gracefully and cache it
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "en:None")

    def test_real_mediawikiapi_instance(self) -> None:
        """Test caching with actual MediaWikiAPI instance"""
        api = MediaWikiAPI()

        # First search in English
        query = "Python"
        en_results = api.search(query)

        # Cache should return same results
        self.assertEqual(api.search(query), en_results)

        # Switch to French
        api.config.language = "fr"
        fr_results = api.search(query)

        # Results should be different and cached separately
        self.assertNotEqual(en_results, fr_results)
        self.assertEqual(api.search(query), fr_results)

        # Switch back to English
        api.config.language = "en"
        self.assertEqual(api.search(query), en_results)
