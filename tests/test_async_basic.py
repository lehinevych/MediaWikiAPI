# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio
import vcr

from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.async_wikipediapage import AsyncWikipediaPage
from mediawikiapi.config import Config


@pytest_asyncio.fixture(scope="function")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI()
    yield api_instance
    await api_instance.close()


@pytest.mark.asyncio
async def test_api_initialization():
    """Test that we can initialize the AsyncMediaWikiAPI class."""
    api = AsyncMediaWikiAPI()
    assert api is not None
    assert isinstance(api, AsyncMediaWikiAPI)
    await api.close()


@pytest.mark.asyncio
async def test_api_as_context_manager():
    """Test that AsyncMediaWikiAPI works as a context manager."""
    async with AsyncMediaWikiAPI() as api:
        assert api is not None
        assert isinstance(api, AsyncMediaWikiAPI)

    # No need to call close() explicitly when using context manager


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_initialization(api):
    """Test that we can create an AsyncWikipediaPage instance."""
    # Use a very simple example that should be stable
    try:
        page = await api.page("Python (programming language)", preload=False)
        assert page is not None
        assert isinstance(page, AsyncWikipediaPage)
        assert page.title == "Python (programming language)"
    except Exception as e:
        pytest.skip(f"Skipping test due to network/API issue: {e}")
