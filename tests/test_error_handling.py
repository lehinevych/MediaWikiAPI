"""
Tests for error handling functions.
"""
import unittest

import pytest

from mediawikiapi.exceptions import (
    HTTPTimeoutError,
    MediaWikiAPIException,
    PageError,
    RedirectError,
    LanguageError,
)
from mediawikiapi.common.error_handling import (
    handle_api_error,
    handle_page_error,
    handle_redirect,
    handle_language_error,
    process_search_results,
    process_geosearch_results,
    process_random_results,
    process_category_members_results,
)


class TestErrorHandling(unittest.TestCase):
    """Test the error handling functions."""

    def test_handle_api_error(self):
        """Test API error handling."""
        # No error
        handle_api_error({"query": {"pages": {}}}, "test")
        
        # HTTP timeout error
        with pytest.raises(HTTPTimeoutError):
            handle_api_error(
                {"error": {"info": "HTTP request timed out."}},
                "test",
            )
            
        with pytest.raises(HTTPTimeoutError):
            handle_api_error(
                {"error": {"info": "Pool queue is full"}},
                "test",
            )
            
        # General API error
        with pytest.raises(MediaWikiAPIException):
            handle_api_error(
                {"error": {"info": "Unknown error"}},
                "test",
            )

    def test_handle_page_error(self):
        """Test page error handling."""
        # No error
        handle_page_error({"query": {"pages": {"123": {"title": "Test"}}}}, "Test", 123)
        
        # Missing page by title
        with pytest.raises(PageError) as exc_info:
            handle_page_error(
                {"query": {"pages": {"-1": {"missing": ""}}}}, 
                "Nonexistent", 
                None
            )
        assert "does not match any pages" in str(exc_info.value)
        
        # Missing page by ID
        with pytest.raises(PageError) as exc_info:
            handle_page_error(
                {"query": {"pages": {"-1": {"missing": ""}}}}, 
                None, 
                99999
            )
        assert "does not match any pages" in str(exc_info.value)

    def test_handle_redirect(self):
        """Test redirect handling."""
        # No redirect
        response = handle_redirect({"query": {}}, "Test", True)
        assert response == {"query": {}}
        
        # Redirect allowed
        response = handle_redirect(
            {"query": {"redirects": [{"from": "Test", "to": "Real Test"}]}},
            "Test",
            True,
        )
        assert "redirects" in response["query"]
        
        # Redirect not allowed
        with pytest.raises(RedirectError):
            handle_redirect(
                {"query": {"redirects": [{"from": "Test", "to": "Real Test"}]}},
                "Test",
                False,
            )

    def test_handle_language_error(self):
        """Test language error handling."""
        # Valid language
        handle_language_error("en", ["en", "fr", "de"])
        
        # Invalid language
        with pytest.raises(LanguageError):
            handle_language_error("xx", ["en", "fr", "de"])

    def test_process_search_results(self):
        """Test search result processing."""
        # Basic search results
        results = process_search_results(
            {"query": {"search": [{"title": "Test1"}, {"title": "Test2"}]}},
            False,
        )
        assert results == ["Test1", "Test2"]
        
        # Search with suggestion (has suggestion)
        results, suggestion = process_search_results(
            {
                "query": {
                    "search": [{"title": "Test1"}, {"title": "Test2"}],
                    "searchinfo": {"suggestion": "better test"},
                }
            },
            True,
        )
        assert results == ["Test1", "Test2"]
        assert suggestion == "better test"
        
        # Search with suggestion (no suggestion)
        results, suggestion = process_search_results(
            {"query": {"search": [{"title": "Test1"}, {"title": "Test2"}]}},
            True,
        )
        assert results == ["Test1", "Test2"]
        assert suggestion is None

    def test_process_geosearch_results(self):
        """Test geosearch result processing."""
        # Results in 'pages' format
        results = process_geosearch_results(
            {
                "query": {
                    "pages": {
                        "123": {"title": "Location1"},
                        "456": {"title": "Location2"},
                        "-1": {"missing": ""},
                    }
                }
            }
        )
        assert sorted(results) == ["Location1", "Location2"]
        
        # Results in 'geosearch' format
        results = process_geosearch_results(
            {
                "query": {
                    "geosearch": [
                        {"title": "Location1"},
                        {"title": "Location2"},
                    ]
                }
            }
        )
        assert sorted(results) == ["Location1", "Location2"]

    def test_process_random_results(self):
        """Test random result processing."""
        # Single result
        result = process_random_results(
            {"query": {"random": [{"title": "Random1"}]}},
            1,
        )
        assert result == "Random1"
        
        # Multiple results
        results = process_random_results(
            {"query": {"random": [{"title": "Random1"}, {"title": "Random2"}]}},
            2,
        )
        assert results == ["Random1", "Random2"]

    def test_process_category_members_results(self):
        """Test category members result processing."""
        # Valid results
        results = process_category_members_results(
            {
                "query": {
                    "categorymembers": [
                        {"title": "Member1"},
                        {"title": "Member2"},
                    ]
                }
            }
        )
        assert results == ["Member1", "Member2"]
        
        # Error in response
        with pytest.raises(ValueError):
            process_category_members_results(
                {"error": {"info": "Category not found"}}
            )


if __name__ == "__main__":
    unittest.main()