"""
Basic tests for error handling and exception types in MediaWikiAPI.
"""

import pytest
from unittest.mock import patch, MagicMock

from mediawikiapi.exceptions import (
    HTTPTimeoutError, 
    MediaWikiAPIException, 
    PageError, 
    RedirectError,
    LanguageError,
    RateLimitError,
    AccessDeniedError,
    InvalidParameterError,
    ServerError,
    NetworkError
)
from mediawikiapi.common.error_handling import handle_api_error, handle_page_error, handle_redirect, handle_language_error


class TestBasicErrorHandling:
    """Tests for basic error handling functions"""
    
    def test_handle_api_error_timeout(self):
        """Test handling of timeout errors"""
        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "HTTP request timed out."}}, "test")
            
        with pytest.raises(HTTPTimeoutError):
            handle_api_error({"error": {"info": "Pool queue is full"}}, "test")
    
    def test_handle_api_error_rate_limit(self):
        """Test handling of rate limit errors"""
        with pytest.raises(RateLimitError):
            handle_api_error({
                "error": {
                    "code": "ratelimited",
                    "info": "Rate limit exceeded"
                }
            }, "test")
    
    def test_handle_api_error_access_denied(self):
        """Test handling of access denied errors"""
        with pytest.raises(AccessDeniedError):
            handle_api_error({
                "error": {
                    "code": "permissiondenied",
                    "info": "Permission denied"
                }
            }, "test")
    
    def test_handle_api_error_invalid_parameter(self):
        """Test handling of invalid parameter errors"""
        with pytest.raises(InvalidParameterError):
            handle_api_error({
                "error": {
                    "code": "invalidparameter",
                    "info": "Invalid parameter 'title'"
                }
            }, "test")
    
    def test_handle_api_error_server_error(self):
        """Test handling of server errors"""
        with pytest.raises(ServerError):
            handle_api_error({
                "error": {
                    "code": "internal_api_error",
                    "info": "Server error"
                }
            }, "test")
    
    def test_handle_api_error_generic(self):
        """Test handling of generic errors"""
        with pytest.raises(MediaWikiAPIException):
            handle_api_error({
                "error": {
                    "code": "unknown_error",
                    "info": "Unknown error"
                }
            }, "test")
    
    def test_handle_page_error(self):
        """Test handling of page not found errors"""
        with pytest.raises(PageError):
            handle_page_error({"query": {"pages": {"-1": {"missing": ""}}}}, "Nonexistent Page")
        
        with pytest.raises(PageError):
            handle_page_error({"query": {"pages": {"-1": {"missing": ""}}}}, pageid=12345)
    
    def test_handle_redirect(self):
        """Test handling of redirect errors"""
        with pytest.raises(RedirectError):
            handle_redirect({"query": {"redirects": [{"from": "Test", "to": "Test Page"}]}}, "Test", allow_redirect=False)
        
        # Ensure it doesn't raise when redirects are allowed
        result = handle_redirect({"query": {"redirects": [{"from": "Test", "to": "Test Page"}]}}, "Test", allow_redirect=True)
        assert "query" in result
        
        # No redirect, should return the response unchanged
        response = {"query": {"pages": {}}}
        result = handle_redirect(response, "Test", allow_redirect=False)
        assert result == response
    
    def test_handle_language_error(self):
        """Test handling of language errors"""
        with pytest.raises(LanguageError):
            handle_language_error("invalid", ["en", "fr", "de", "es"])


if __name__ == "__main__":
    pytest.main()