# -*- coding: utf-8 -*-
import pytest
import unittest
from mediawikiapi import MediaWikiAPI
from tests.request_mock_data import mock_data


@pytest.mark.vcr()
class TestSearch(unittest.TestCase):
    """Test the functionality of mediawikiapi.search."""

    api = MediaWikiAPI()

    def test_search(self) -> None:
        """Test parsing a mediawikiapi request result."""
        self.assertEqual(self.api.search("Barack Obama"), mock_data["barack.search"])

    def test_limit(self) -> None:
        """Test limiting a request results."""
        self.assertEqual(
            self.api.search("Porsche", results=3), mock_data["porsche.search"]
        )

    def test_suggestion(self) -> None:
        """Test getting a suggestion as well as search results."""
        search, suggestion = self.api.search("hallelulejah", suggestion=True)
        self.assertEqual(search, [])
        self.assertEqual(suggestion, "hallelujah")

    def test_suggestion_none(self) -> None:
        """Test getting a suggestion when there is no suggestion."""
        search, suggestion = self.api.search("qmxjsudek", suggestion=True)
        self.assertEqual(search, [])
        self.assertEqual(suggestion, None)

    def test_language_cache(self) -> None:
        """Test that search results are properly cached per language."""
        # First search in English
        query = "Python"
        en_results = self.api.search(query)

        # Cache should return same results on second call
        self.assertEqual(self.api.search(query), en_results)

        # Switch to French
        self.api.config.language = "fr"
        fr_results = self.api.search(query)

        # Results should be different in French
        self.assertNotEqual(en_results, fr_results)

        # French results should be cached
        self.assertEqual(self.api.search(query), fr_results)

        # Switch back to English
        self.api.config.language = "en"

        # Should get cached English results
        self.assertEqual(self.api.search(query), en_results)
