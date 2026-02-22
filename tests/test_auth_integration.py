"""
Integration tests for authentication using responses library to intercept HTTP calls.

These tests verify that headers are correctly sent in real HTTP requests.
"""

import unittest
from unittest.mock import patch
import responses
from responses import matchers
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.language import Language


class TestAuthenticationIntegration(unittest.TestCase):
    """Integration tests that intercept actual HTTP requests"""

    def setUp(self) -> None:
        """Set mock Language cache before each test to prevent real API calls"""
        self._original_languages = Language.predefined_languages
        Language.predefined_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "ru": "Russian",
            "uk": "Ukrainian",
        }

    def tearDown(self) -> None:
        """Restore original Language cache after each test"""
        Language.predefined_languages = self._original_languages

    @responses.activate
    def test_auth_header_sent_in_real_request(self) -> None:
        """Verify Authorization header is sent in actual HTTP request"""
        access_token = "test_token_12345"
        config = Config(access_token=access_token)
        api = MediaWikiAPI(config=config)

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={"query": {"search": [{"title": "AuthTokenTest", "pageid": 123}]}},
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "AuthTokenTest",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        api.search("AuthTokenTest")

        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert "Authorization" in request.headers
        assert request.headers["Authorization"] == f"Bearer {access_token}"

    @responses.activate
    def test_custom_headers_sent_in_real_request(self) -> None:
        """Verify custom headers are sent in actual HTTP request"""
        custom_headers = {"X-Custom-App": "TestApp", "X-Version": "1.0.0"}
        config = Config(custom_headers=custom_headers)
        api = MediaWikiAPI(config=config)

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={"query": {"search": [{"title": "CustomHeadersTest", "pageid": 124}]}},
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "CustomHeadersTest",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        api.search("CustomHeadersTest")

        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert "X-Custom-App" in request.headers
        assert request.headers["X-Custom-App"] == "TestApp"
        assert "X-Version" in request.headers
        assert request.headers["X-Version"] == "1.0.0"

    @responses.activate
    def test_user_agent_override(self) -> None:
        """Verify custom User-Agent overrides default"""
        custom_user_agent = "MyBot/1.0 (test@example.com)"
        custom_headers = {"User-Agent": custom_user_agent}
        config = Config(custom_headers=custom_headers)
        api = MediaWikiAPI(config=config)

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={"query": {"search": [{"title": "UserAgentTest", "pageid": 125}]}},
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "UserAgentTest",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        api.search("UserAgentTest")

        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert request.headers["User-Agent"] == custom_user_agent

    @responses.activate
    def test_no_auth_without_token(self) -> None:
        """Verify no Authorization header when access_token not provided"""
        config = Config()
        api = MediaWikiAPI(config=config)

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={"query": {"search": [{"title": "NoAuthTest", "pageid": 126}]}},
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "NoAuthTest",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        api.search("NoAuthTest")

        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert "Authorization" not in request.headers
        assert "User-Agent" in request.headers

    @responses.activate
    def test_headers_in_continuation_requests(self) -> None:
        """Verify headers are included in continuation requests too"""
        access_token = "test_token_12345"
        config = Config(access_token=access_token)
        api = MediaWikiAPI(config=config)

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={
                "continue": {"continue": "-||", "sroffset": 10},
                "query": {"search": [{"title": "ContinuationTest 1", "pageid": 127}]},
            },
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "ContinuationTest",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php",
            json={
                "query": {"search": [{"title": "ContinuationTest 2", "pageid": 128}]}
            },
            match=[
                matchers.query_param_matcher(
                    {
                        "list": "search",
                        "srlimit": "10",
                        "limit": "10",
                        "srsearch": "ContinuationTest",
                        "sroffset": "10",
                        "continue": "-||",
                        "format": "json",
                        "action": "query",
                    }
                )
            ],
            status=200,
        )

        api.search("ContinuationTest", follow_continue=True)

        assert len(responses.calls) == 2
        for call in responses.calls:
            request = call.request
            assert "Authorization" in request.headers
            assert request.headers["Authorization"] == f"Bearer {access_token}"


if __name__ == "__main__":
    unittest.main()
