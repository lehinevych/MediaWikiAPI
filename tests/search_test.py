# -*- coding: utf-8 -*-
import unittest

from collections import defaultdict
from typing import Dict, Any
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from tests.request_mock_data import mock_data, mock_wiki_calls


# mock out _wiki_request
class _wiki_request(object):
    calls: Dict[str, int] = defaultdict(int)

    @classmethod
    def __call__(cls, params: Dict[str, Any], config: Config) -> Dict[str, Any]:
        cls.calls[params.__str__()] += 1
        return mock_wiki_calls[tuple(sorted(params.items()))]


api = MediaWikiAPI()
api.session.request = _wiki_request()  # type:ignore


class TestSearch(unittest.TestCase):
    """Test the functionality of mediawikiapi.search."""

    def test_search(self) -> None:
        """Test parsing a mediawikiapi request result."""
        self.assertEqual(api.search("Barack Obama"), mock_data["barack.search"])

    def test_limit(self) -> None:
        """Test limiting a request results."""
        self.assertEqual(api.search("Porsche", results=3), mock_data["porsche.search"])

    def test_suggestion(self) -> None:
        """Test getting a suggestion as well as search results."""
        search, suggestion = api.search("hallelulejah", suggestion=True)
        self.assertEqual(search, [])
        self.assertEqual(suggestion, "hallelujah")

    def test_suggestion_none(self) -> None:
        """Test getting a suggestion when there is no suggestion."""
        search, suggestion = api.search("qmxjsudek", suggestion=True)
        self.assertEqual(search, [])
        self.assertEqual(suggestion, None)
