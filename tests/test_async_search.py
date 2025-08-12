# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio

from mediawikiapi import AsyncMediaWikiAPI
from tests.request_mock_data import mock_data


@pytest_asyncio.fixture(scope="module")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI()
    yield api_instance
    await api_instance.close()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_search(api):
    """Test parsing an async mediawikiapi request result."""
    results = await api.search("Barack Obama")
    # Check that essential results are present regardless of order
    assert "Barack Obama" in results
    assert "Family of Barack Obama" in results
    assert "Presidency of Barack Obama" in results


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_limit(api):
    """Test limiting a request results."""
    results = await api.search("Porsche", results=3)
    assert len(results) == 3
    # The exact results might differ, so just check the length


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_suggestion(api):
    """Test getting a suggestion as well as search results."""
    search, suggestion = await api.search("hallelulejah", suggestion=True)
    assert search == []
    assert suggestion == "hallelujah"


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_suggestion_none(api):
    """Test getting a suggestion when there is no suggestion."""
    search, suggestion = await api.search("qmxjsudek", suggestion=True)
    assert search == []
    assert suggestion is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_language_cache(api):
    """Test that search results are properly cached per language."""
    # First search in English
    query = "Python"
    en_results = await api.search(query)

    # Cache should return same results on second call
    second_results = await api.search(query)
    assert second_results == en_results

    # Switch to French
    api.config.language = "fr"
    fr_results = await api.search(query)

    # Results should be different in French
    assert en_results != fr_results

    # French results should be cached
    second_fr_results = await api.search(query)
    assert second_fr_results == fr_results

    # Switch back to English
    api.config.language = "en"

    # Should get cached English results
    final_en_results = await api.search(query)
    assert final_en_results == en_results