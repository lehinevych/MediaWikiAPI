import unittest
import pytest
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from decimal import Decimal


@pytest.mark.vcr()
class TestContinuation(unittest.TestCase):
    """Test the continuation functionality of MediaWikiAPI"""

    def setUp(self) -> None:
        self.api = MediaWikiAPI(config=Config(timeout=10))
        # New York coordinates
        self.ny_lat = Decimal("40.7128")
        self.ny_lon = Decimal("-74.0060")

    def test_custom_query_with_continue(self) -> None:
        """Test that custom_query method follows continuation tokens"""
        # This query should return results that require continuation
        query_params = {
            "action": "query",
            "generator": "geosearch",
            "ggsradius": 10000,
            "ggscoord": f"{self.ny_lat}|{self.ny_lon}",
            "ggslimit": 50,
            "prop": "pageviews",
        }

        # Test with follow_continue=True
        result_with_continue = self.api.custom_query(query_params, follow_continue=True)

        # Test with follow_continue=False
        result_without_continue = self.api.custom_query(
            query_params, follow_continue=False
        )

        # With follow_continue=True, we should get more pages or at least the same number
        # compared to not following continuation tokens
        pages_with_continue = len(
            result_with_continue.get("query", {}).get("pages", {})
        )
        pages_without_continue = len(
            result_without_continue.get("query", {}).get("pages", {})
        )

        # The test might not always require continuation if the number of results is small,
        # so we check that we get at least as many results with continuation as without
        self.assertGreaterEqual(
            pages_with_continue,
            pages_without_continue,
            "Following continuation tokens should return at least as many results",
        )

        # If there was a continuation token in the non-continued result, then the continued
        # result should definitely have more pages
        if "continue" in result_without_continue:
            self.assertGreater(
                pages_with_continue,
                pages_without_continue,
                "When continuation token is present, following it should return more results",
            )

        # The continue token should not be present in the final result when follow_continue=True
        self.assertNotIn(
            "continue",
            result_with_continue,
            "Final result should not contain a continue token when follow_continue=True",
        )

    def test_geosearch_prop_pageviews(self) -> None:
        """Test the specific use case from GitHub issue #77"""
        # Create a query directly using custom_query for the issue case
        query_params = {
            "action": "query",
            "generator": "geosearch",
            "ggsradius": 10000,
            "ggscoord": f"{self.ny_lat}|{self.ny_lon}",
            "ggssort": "relevance",
            "prop": "pageviews",
            "ggslimit": 50,
        }

        result = self.api.custom_query(query_params)

        # Verify that we got pages
        self.assertIn("query", result, "Result should contain a query object")
        self.assertIn("pages", result["query"], "Query should contain pages")

        # Check that pages have pageviews data
        pages = result["query"]["pages"]
        for page_id, page_data in pages.items():
            # Not all pages will have pageviews, but some should
            if "pageviews" in page_data:
                # If we found at least one page with pageviews, the test passes
                return

        # If we got here, no pages had pageviews, which would be unusual
        self.fail("No pages with pageviews data were found")


if __name__ == "__main__":
    unittest.main()
