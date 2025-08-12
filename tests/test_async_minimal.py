# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio
import os

from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.async_api.async_wikipediapage import AsyncWikipediaPage

# Force VCR to use existing cassettes
os.environ["VCR_RECORD_MODE"] = "once"


@pytest_asyncio.fixture(scope="function")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI()
    yield api_instance
    await api_instance.close()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_initialization(api):
    """Test that we can create an AsyncWikipediaPage instance."""
    # Use a very simple example that should be stable
    page = await api.page("Python (programming language)", preload=False)
    assert page is not None
    assert isinstance(page, AsyncWikipediaPage)
    assert page.title == "Python (programming language)"
    assert int(page.pageid) > 0
    assert "en.wikipedia.org" in page.url
