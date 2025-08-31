"""
Tests for parameter validation functions.
"""

import decimal
import unittest

import pytest

from mediawikiapi.common.validation import (
    validate_title_or_pageid,
    validate_geosearch_params,
    validate_search_params,
    validate_limit,
    validate_category_params,
    validate_sentences_and_chars,
)


class TestValidation(unittest.TestCase):
    """Test the parameter validation functions."""

    def test_validate_title_or_pageid(self):
        """Test title/pageid validation."""
        # Valid scenarios
        validate_title_or_pageid(title="Test")
        validate_title_or_pageid(pageid=12345)

        # Invalid scenarios
        with pytest.raises(
            ValueError, match="Either a title or a pageid must be specified"
        ):
            validate_title_or_pageid()

        with pytest.raises(
            ValueError, match="Please specify only a title or only a pageid, not both"
        ):
            validate_title_or_pageid(title="Test", pageid=12345)

    def test_validate_geosearch_params(self):
        """Test geosearch parameter validation."""
        # Valid scenarios
        validate_geosearch_params(
            latitude=40.748817, longitude=-73.985428, radius=1000, results=10
        )
        validate_geosearch_params(
            latitude="40.748817", longitude="-73.985428", radius=10, results=1
        )

        # Invalid scenarios
        with pytest.raises(
            ValueError, match="Latitude and longitude must be valid numbers"
        ):
            validate_geosearch_params(
                latitude="invalid", longitude=-73.985428, radius=1000, results=10
            )

        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            validate_geosearch_params(
                latitude=100, longitude=-73.985428, radius=1000, results=10
            )

        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            validate_geosearch_params(
                latitude=40.748817, longitude=200, radius=1000, results=10
            )

        with pytest.raises(
            ValueError, match="Radius must be between 10 and 10000 meters"
        ):
            validate_geosearch_params(
                latitude=40.748817, longitude=-73.985428, radius=5, results=10
            )

        with pytest.raises(
            ValueError, match="Radius must be between 10 and 10000 meters"
        ):
            validate_geosearch_params(
                latitude=40.748817, longitude=-73.985428, radius=15000, results=10
            )

        with pytest.raises(ValueError, match="Number of results must be positive"):
            validate_geosearch_params(
                latitude=40.748817, longitude=-73.985428, radius=1000, results=0
            )

    def test_validate_search_params(self):
        """Test search parameter validation."""
        # Valid scenarios
        validate_search_params(query="test", results=10)

        # Invalid scenarios
        with pytest.raises(ValueError, match="Query cannot be empty"):
            validate_search_params(query="", results=10)

        with pytest.raises(ValueError, match="Number of results must be positive"):
            validate_search_params(query="test", results=0)

    def test_validate_limit(self):
        """Test limit validation."""
        # Valid scenarios
        validate_limit(limit=10)
        validate_limit(limit="max")
        validate_limit(limit="max_value")

        # Invalid scenarios
        with pytest.raises(
            ValueError, match="String limit must be 'max' or 'max_value'"
        ):
            validate_limit(limit="unlimited")

        with pytest.raises(ValueError, match="Limit must be positive"):
            validate_limit(limit=0)

        with pytest.raises(ValueError, match="Limit cannot exceed 500"):
            validate_limit(limit=1000)

        with pytest.raises(
            ValueError, match="Limit must be an integer or 'max'/'max_value'"
        ):
            validate_limit(limit=10.5)

    def test_validate_category_params(self):
        """Test category parameter validation."""
        # Valid scenarios
        validate_category_params(title="Science")
        validate_category_params(pageid=12345)
        validate_category_params(title="Science", cmtype="page")
        validate_category_params(title="Science", cmtype="subcat")
        validate_category_params(title="Science", cmtype="file")

        # Invalid scenarios
        with pytest.raises(
            ValueError,
            match="Please specify only a category title or only a pageid, not both",
        ):
            validate_category_params(title="Science", pageid=12345)

        with pytest.raises(
            ValueError, match="Either a category title or a pageid must be specified"
        ):
            validate_category_params()

        with pytest.raises(
            ValueError,
            match="Category member type must be one of: 'page', 'subcat', or 'file'",
        ):
            validate_category_params(title="Science", cmtype="invalid")

    def test_validate_sentences_and_chars(self):
        """Test sentences/chars parameter validation."""
        # Valid scenarios
        validate_sentences_and_chars(sentences=5, chars=None)
        validate_sentences_and_chars(sentences=None, chars=500)
        validate_sentences_and_chars(sentences=None, chars=None)
        validate_sentences_and_chars(sentences=0, chars=0)

        # Invalid scenarios
        with pytest.raises(
            ValueError, match="Number of sentences must be non-negative"
        ):
            validate_sentences_and_chars(sentences=-1, chars=None)

        with pytest.raises(
            ValueError, match="Number of characters must be non-negative"
        ):
            validate_sentences_and_chars(sentences=None, chars=-1)

        with pytest.raises(
            ValueError, match="Specify only one of sentences or chars, not both"
        ):
            validate_sentences_and_chars(sentences=5, chars=500)


if __name__ == "__main__":
    unittest.main()
