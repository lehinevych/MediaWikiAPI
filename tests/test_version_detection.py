"""
Tests for MediaWiki API version detection in RequestSession.
"""

import pytest
from unittest.mock import MagicMock, patch

from mediawikiapi.common.api_version import MediaWikiVersion
from mediawikiapi.config import Config
from mediawikiapi.sync.mediawikiapi import MediaWikiAPI
from mediawikiapi.sync.requestsession import RequestSession
from mediawikiapi.async_api.async_mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.async_api.async_requestsession import AsyncRequestSession


class TestSyncVersionDetection:
    """Tests for synchronous version detection"""

    @patch("requests.Session.get")
    def test_detect_api_version(self, mock_get):
        """Test API version detection in sync RequestSession"""
        # Create mock response with version info
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "query": {"general": {"generator": "MediaWiki 1.35.0-wmf.35"}}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Create session and config
        session = RequestSession()
        config = Config()
        api_url = "https://en.wikipedia.org/w/api.php"

        # Detect version
        version = session.detect_api_version(api_url, config)

        # Check if the correct request was made
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["action"] == "query"
        assert kwargs["params"]["meta"] == "siteinfo"

        # Check if version was correctly parsed
        assert version is not None
        assert version.major == 1
        assert version.minor == 35
        assert version.patch == 0

    @patch("requests.Session.get")
    def test_version_detection_during_request(self, mock_get):
        """Test if version detection happens during first request"""
        # Mock two responses: first for version detection, second for the actual request
        response1 = MagicMock()
        response1.json.return_value = {
            "query": {"general": {"generator": "MediaWiki 1.35.0-wmf.35"}}
        }
        response1.status_code = 200

        response2 = MagicMock()
        response2.json.return_value = {"query": {"pages": {}}}
        response2.status_code = 200

        mock_get.side_effect = [response1, response2]

        # Create API
        api = MediaWikiAPI()

        # Make a request that should trigger version detection
        api.search("test")

        # Check if version was detected and stored
        api_url = api.config.get_api_url()
        version = api.config.get_api_version(api_url)

        assert version is not None
        assert version.major == 1
        assert version.minor == 35
        assert version.patch == 0

        # Check if mock was called twice: once for detection, once for the search
        assert mock_get.call_count == 2


@pytest.mark.asyncio
class TestAsyncVersionDetection:
    """Tests for asynchronous version detection"""

    @pytest.mark.asyncio
    async def test_detect_api_version(self):
        """Test API version detection in async RequestSession"""
        # Create mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(
            return_value={
                "query": {"general": {"generator": "MediaWiki 1.35.0-wmf.35"}}
            }
        )
        mock_response.status = 200
        mock_response.raise_for_status = MagicMock()

        # Setup async context manager mock
        mock_cm = MagicMock()
        mock_cm.__aenter__ = MagicMock(return_value=mock_response)
        mock_cm.__aexit__ = MagicMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_cm)

        # Make the session's get and json methods awaitable
        mock_response.__aenter__ = mock_cm.__aenter__
        mock_response.__aexit__ = mock_cm.__aexit__
        mock_response.json.__await__ = lambda: (
            yield from [mock_response.json.return_value].__iter__()
        )
        mock_cm.__aenter__.__await__ = lambda: (yield from [mock_response].__iter__())
        mock_cm.__aexit__.__await__ = lambda *args: (yield from [None].__iter__())

        # Create session and patch the session getter
        session = AsyncRequestSession()
        session._AsyncRequestSession__session = mock_session

        # Get version
        config = Config()
        api_url = "https://en.wikipedia.org/w/api.php"
        version = await session.detect_api_version(api_url, config)

        # Check that session.get was called correctly
        mock_session.get.assert_called_once()
        args, kwargs = mock_session.get.call_args
        assert kwargs["params"]["action"] == "query"
        assert kwargs["params"]["meta"] == "siteinfo"

        # Check if version was correctly parsed
        assert version is not None
        assert version.major == 1
        assert version.minor == 35
        assert version.patch == 0


if __name__ == "__main__":
    pytest.main()
