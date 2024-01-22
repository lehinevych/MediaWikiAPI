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
