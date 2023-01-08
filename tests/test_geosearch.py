# -*- coding: utf-8 -*-
import unittest

from collections import defaultdict
from decimal import Decimal
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


class TestSearchLoc(unittest.TestCase):
    """Test the functionality of mediawikiapi.geosearch."""

    def test_geosearch(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            api.geosearch(Decimal("40.67693"), Decimal("117.23193")),
            mock_data["great_wall_of_china.geo_seach"],
        )

    def test_geosearch_with_radius(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            api.geosearch(Decimal("40.67693"), Decimal("117.23193"), radius=10000),
            mock_data["great_wall_of_china.geo_seach_with_radius"],
        )

    def test_geosearch_with_existing_title(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            api.geosearch(
                Decimal("40.67693"), Decimal("117.23193"), title="Great Wall of China"
            ),
            mock_data["great_wall_of_china.geo_seach_with_existing_article_name"],
        )

    def test_geosearch_with_non_existing_title(self) -> None:
        self.assertEqual(
            api.geosearch(Decimal("40.67693"), Decimal("117.23193"), title="Test"),
            mock_data["great_wall_of_china.geo_seach_with_non_existing_article_name"],
        )
