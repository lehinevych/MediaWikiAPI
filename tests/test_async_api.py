# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio
import vcr

from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.config import Config


@pytest_asyncio.fixture(scope="function")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI()
    yield api_instance
    await api_instance.close()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_search(api):
    """Test the search method with a known query."""
    results = await api.search("Python programming")
    assert len(results) > 0
    assert "Python (programming language)" in results


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_geosearch(api):
    """Test the geosearch method with known coordinates."""
    # Coordinates near the Empire State Building
    results = await api.geosearch(latitude=40.748817, longitude=-73.985428, radius=1000)
    assert len(results) > 0
    # The Empire State Building should be in the results
    assert any("Empire State Building" in title for title in results)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_summary(api):
    """Test the summary method with a known page."""
    summary = await api.summary("Python (programming language)")
    assert len(summary) > 100
    assert "programming language" in summary.lower()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_random(api):
    """Test the random method."""
    # Get a single random page
    random_page = await api.random()
    assert isinstance(random_page, str)
    assert len(random_page) > 0

    # Get multiple random pages
    random_pages = await api.random(pages=3)
    assert isinstance(random_pages, list)
    assert len(random_pages) == 3


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_language_setting(api):
    """Test changing language settings."""
    # Get results in English
    api.config.language = "en"
    en_results = await api.search("Computer")

    # Get results in Spanish
    api.config.language = "es"
    es_results = await api.search("Computer")

    # Results should differ between languages
    assert en_results != es_results

    # Reset to English for other tests
    api.config.language = "en"


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_languages(api):
    """Test retrieving available languages."""
    languages = await api.languages()
    assert len(languages) > 50  # Wikipedia supports many languages
    assert "en" in languages
    assert "es" in languages
    assert "fr" in languages


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_category_members(api):
    """Test retrieving category members."""
    members = await api.category_members(title="Programming languages", cmlimit=10)
    assert len(members) > 0
    # This test might be a bit fragile since category contents can change
    common_langs = ["Python", "JavaScript", "C++", "Java"]
    found_langs = [lang for lang in common_langs if any(lang in m for m in members)]
    assert len(found_langs) > 0  # At least one common language should be found


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_custom_query(api):
    """Test custom query to the API."""
    query_params = {
        "action": "query",
        "generator": "random",
        "grnnamespace": 0,
        "grnlimit": 5,
        "prop": "info",
    }
    result = await api.custom_query(query_params)
    assert "query" in result
    assert "pages" in result["query"]
    assert len(result["query"]["pages"]) == 5
