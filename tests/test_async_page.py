# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest
import pytest_asyncio
from bs4 import BeautifulSoup

import mediawikiapi
from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.async_api.async_wikipediapage import AsyncWikipediaPage


@pytest_asyncio.fixture(scope="module")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI(config=Config(timeout=10))
    yield api_instance
    await api_instance.close()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_missing(api):
    """Test that page raises a PageError for a nonexistant page."""
    with pytest.raises(mediawikiapi.PageError):
        await api.page("purpleberrynotexist", auto_suggest=False)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_redirect_true(api):
    """Test that a page successfully redirects a query."""
    # no error should be raised if redirect is True
    mp = await api.page("Template:cn", auto_suggest=False)

    assert mp.title == "Template:Citation needed"
    assert mp.url == "https://en.wikipedia.org/wiki/Template:Citation_needed"


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_redirect_false(api):
    """Test that page raises an error on a redirect when redirect == False."""
    with pytest.raises(mediawikiapi.RedirectError):
        await api.page("Template:cn", auto_suggest=False, redirect=False)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_properties(api):
    """Test basic page properties."""
    page = await api.page("Python (programming language)")
    assert page.title == "Python (programming language)"
    assert page.pageid > 0
    assert "https://en.wikipedia.org/wiki/Python" in page.url


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_content(api):
    """Test page content retrieval."""
    page = await api.page("Python (programming language)")
    content = await page.content
    # Just check that it returns a non-empty string
    assert isinstance(content, str)
    assert len(content) > 1000


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_summary(api):
    """Test page summary retrieval."""
    page = await api.page("Python (programming language)")
    summary = await page.summary
    # Just check that it returns a non-empty string
    assert isinstance(summary, str)
    assert len(summary) > 100
    assert "programming language" in summary.lower()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_sections(api):
    """Test page sections retrieval."""
    page = await api.page("Python (programming language)")
    sections = await page.sections
    # Check that common sections are present
    common_sections = ["History", "Features", "Syntax"]
    for section in common_sections:
        assert any(section in s for s in sections)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_links(api):
    """Test page links retrieval."""
    page = await api.page("Python (programming language)")
    links = await page.links
    # Just check that it returns a non-empty list
    assert isinstance(links, list)
    assert len(links) > 50


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_references(api):
    """Test page references retrieval."""
    page = await api.page("Python (programming language)")
    references = await page.references
    # Just check that it returns a non-empty list
    assert isinstance(references, list)
    assert len(references) > 10
    # Check that all references are URLs
    for ref in references[:5]:  # Check first 5 only for performance
        assert ref.startswith("http")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_categories(api):
    """Test page categories retrieval."""
    page = await api.page("Python (programming language)")
    categories = await page.categories
    # Check that common categories are present
    assert isinstance(categories, list)
    programming_categories = ["programming language"]
    # Check if any category contains these strings (case-insensitive)
    for term in programming_categories:
        matching = [c for c in categories if term.lower() in c.lower()]
        assert len(matching) > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_section_content(api):
    """Test section content retrieval."""
    page = await api.page("Python (programming language)")
    # Find a section that should exist
    sections = await page.sections
    test_section = next((s for s in sections if "History" in s), None)

    if test_section:
        section_content = await page.section(test_section)
        assert isinstance(section_content, str)
        assert len(section_content) > 100
    else:
        pytest.fail("Could not find 'History' section in Python page")
