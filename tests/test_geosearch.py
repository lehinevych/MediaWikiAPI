# -*- coding: utf-8 -*-
import pytest
import unittest
from decimal import Decimal
from mediawikiapi import MediaWikiAPI
from tests.request_mock_data import mock_data


@pytest.mark.vcr()
class TestSearchLoci(unittest.TestCase):
    """Test the functionality of mediawikiapi.geosearch."""

    api = MediaWikiAPI()

    def test_geosearch(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            self.api.geosearch(Decimal("40.67693"), Decimal("117.23193")),
            mock_data["great_wall_of_china.geo_seach"],
        )

    def test_geosearch_with_radius(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            self.api.geosearch(Decimal("40.67693"), Decimal("117.23193"), radius=10000),
            mock_data["great_wall_of_china.geo_seach_with_radius"],
        )

    def test_geosearch_with_existing_title(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertEqual(
            self.api.geosearch(
                Decimal("40.67693"), Decimal("117.23193"), title="Great Wall of China"
            ),
            mock_data["great_wall_of_china.geo_seach_with_existing_article_name"],
        )

    def test_geosearch_with_non_existing_title(self) -> None:
        self.assertEqual(
            self.api.geosearch(Decimal("40.67693"), Decimal("117.23193"), title="Test"),
            mock_data["great_wall_of_china.geo_seach_with_non_existing_article_name"],
        )
