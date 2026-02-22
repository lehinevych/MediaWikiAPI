"""
Tests for Personal Access Token authentication and custom headers.

These tests verify that authentication headers are properly included in API requests.
"""

import unittest
from typing import Any
from unittest.mock import Mock, patch
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.language import Language


class TestAuthentication(unittest.TestCase):
    """Test authentication header handling in API requests"""

    def setUp(self) -> None:
        """Set mock Language cache before each test and clear memoization"""
        self._original_languages = Language.predefined_languages
        Language.predefined_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "ru": "Russian",
            "uk": "Ukrainian",
        }
        # Clear memoization cache to ensure tests are isolated
        if hasattr(MediaWikiAPI, "_memoized_functions"):
            for func in MediaWikiAPI._memoized_functions.values():
                if hasattr(func, "cache"):
                    func.cache.clear()

    def tearDown(self) -> None:
        """Restore original Language cache after each test"""
        Language.predefined_languages = self._original_languages

    @patch("mediawikiapi.requestsession.requests.Session")
    def test_access_token_sent_in_request(self, mock_session_class: Any) -> None:
        """Verify that access token is included in Authorization header"""
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session

        # Mock the response
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {"search": [{"title": "Test Page", "pageid": 123}]}
        }
        mock_session.get.return_value = mock_response

        # Create config and API
        access_token = "test_token_12345"
        config = Config(access_token=access_token)
        api = MediaWikiAPI(config=config)

        # Make a request with unique query
        api.search("access token test")

        # Verify headers were passed
        mock_session.get.assert_called()
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]

        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], f"Bearer {access_token}")

    @patch("mediawikiapi.requestsession.requests.Session")
    def test_custom_headers_sent_in_request(self, mock_session_class: Any) -> None:
        """Verify that custom headers are included in requests"""
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {"search": [{"title": "Test Page", "pageid": 123}]}
        }
        mock_session.get.return_value = mock_response

        # Create config with custom headers
        custom_headers = {
            "X-Custom-Header": "custom_value",
            "X-Application-Name": "TestApp",
        }
        config = Config(custom_headers=custom_headers)
        api = MediaWikiAPI(config=config)

        # Make a request with unique query
        api.search("custom headers test")

        # Verify custom headers were passed
        mock_session.get.assert_called()
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]

        self.assertIn("X-Custom-Header", headers)
        self.assertEqual(headers["X-Custom-Header"], "custom_value")
        self.assertIn("X-Application-Name", headers)
        self.assertEqual(headers["X-Application-Name"], "TestApp")

    @patch("mediawikiapi.requestsession.requests.Session")
    def test_combined_auth_and_custom_headers(self, mock_session_class: Any) -> None:
        """Verify that access token and custom headers work together"""
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {"search": [{"title": "Test Page", "pageid": 123}]}
        }
        mock_session.get.return_value = mock_response

        # Create combined config
        access_token = "test_token_12345"
        custom_headers = {"X-App-Version": "1.0.0"}
        config = Config(access_token=access_token, custom_headers=custom_headers)
        api = MediaWikiAPI(config=config)

        # Make a request with unique query
        api.search("combined auth test")

        # Verify both sets of headers
        mock_session.get.assert_called()
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]

        # Check Authorization header
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], f"Bearer {access_token}")

        # Check custom header
        self.assertIn("X-App-Version", headers)
        self.assertEqual(headers["X-App-Version"], "1.0.0")

        # Check default User-Agent is still present
        self.assertIn("User-Agent", headers)

    @patch("mediawikiapi.requestsession.requests.Session")
    def test_custom_user_agent_override(self, mock_session_class: Any) -> None:
        """Verify that custom User-Agent can override default"""
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {"search": [{"title": "Test Page", "pageid": 123}]}
        }
        mock_session.get.return_value = mock_response

        # Create config with custom User-Agent
        custom_user_agent = "MyCustomBot/1.0"
        custom_headers = {"User-Agent": custom_user_agent}
        config = Config(custom_headers=custom_headers)
        api = MediaWikiAPI(config=config)

        # Make a request with unique query to avoid cache
        api.search("user agent override test")

        # Verify custom User-Agent was used
        mock_session.get.assert_called()
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]

        self.assertEqual(headers["User-Agent"], custom_user_agent)
        self.assertNotEqual(headers["User-Agent"], Config.DEFAULT_USER_AGENT)

    @patch("mediawikiapi.requestsession.requests.Session")
    def test_no_auth_token_by_default(self, mock_session_class: Any) -> None:
        """Verify that Authorization header is not present without access_token"""
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        mock_response = Mock()
        mock_response.json.return_value = {
            "query": {"search": [{"title": "Test Page", "pageid": 123}]}
        }
        mock_session.get.return_value = mock_response

        # Create config without token
        config = Config()
        api = MediaWikiAPI(config=config)

        # Make a request with unique query
        api.search("no auth test")

        # Verify no Authorization header
        mock_session.get.assert_called()
        call_args = mock_session.get.call_args
        headers = call_args[1]["headers"]

        self.assertNotIn("Authorization", headers)
        self.assertIn("User-Agent", headers)  # But User-Agent should be present


if __name__ == "__main__":
    unittest.main()
