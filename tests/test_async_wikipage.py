# -*- coding: utf-8 -*-
import pytest
import pytest_asyncio
from decimal import Decimal

from mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.exceptions import PageError, RedirectError


@pytest_asyncio.fixture(scope="function")
async def api():
    """Create an instance of AsyncMediaWikiAPI for testing."""
    api_instance = AsyncMediaWikiAPI(config=Config(timeout=10))
    yield api_instance
    await api_instance.close()


@pytest_asyncio.fixture(scope="function")
async def python_page(api):
    """Create a page fixture for Python programming language."""
    page = await api.page("Python (programming language)")
    yield page


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_basic_properties(python_page):
    """Test the basic properties of a page."""
    assert python_page.title == "Python (programming language)"
    assert isinstance(python_page.pageid, int)
    assert python_page.pageid > 0
    assert "en.wikipedia.org" in python_page.url


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_content(python_page):
    """Test retrieving the content of a page."""
    content = await python_page.content
    assert isinstance(content, str)
    assert len(content) > 1000
    assert "Guido van Rossum" in content  # Python's creator should be mentioned


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_summary(python_page):
    """Test retrieving the summary of a page."""
    summary = await python_page.summary
    assert isinstance(summary, str)
    assert len(summary) > 100
    assert "programming language" in summary.lower()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_images(python_page):
    """Test retrieving images from a page."""
    images = await python_page.images
    assert isinstance(images, list)
    assert len(images) > 0
    # Check that images are URLs
    for image in images[:5]:  # Check the first few for performance
        assert isinstance(image, str)
        assert image.startswith("http")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_references(python_page):
    """Test retrieving references from a page."""
    references = await python_page.references
    assert isinstance(references, list)
    assert len(references) > 0
    # Check that references are URLs
    for ref in references[:5]:  # Check the first few for performance
        assert isinstance(ref, str)
        assert ref.startswith("http")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_links(python_page):
    """Test retrieving links from a page."""
    links = await python_page.links
    assert isinstance(links, list)
    assert len(links) > 0
    # Common related terms that should be linked
    common_links = ["Programming language", "Open-source software", "Computer programming"]
    found_links = [link for link in common_links if link in links]
    assert len(found_links) > 0  # At least one common link should be found


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_categories(python_page):
    """Test retrieving categories from a page."""
    categories = await python_page.categories
    assert isinstance(categories, list)
    assert len(categories) > 0
    # Common categories that Python should be in
    common_categories = ["programming language", "cross-platform", "object-oriented"]
    assert any(any(cat.lower() in c.lower() for cat in common_categories) for c in categories)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_sections(python_page):
    """Test retrieving sections from a page."""
    sections = await python_page.sections
    assert isinstance(sections, list)
    assert len(sections) > 0
    # Common sections in the Python article
    common_sections = ["History", "Features", "Syntax", "Libraries"]
    found_sections = [section for section in common_sections if any(section in s for s in sections)]
    assert len(found_sections) > 0  # At least one common section should be found


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_section_content(python_page):
    """Test retrieving specific section content."""
    sections = await python_page.sections
    history_section = next((s for s in sections if "History" in s), None)
    
    if history_section:
        content = await python_page.section(history_section)
        assert isinstance(content, str)
        assert len(content) > 100
        # Guido van Rossum should be mentioned in the history section
        assert "Guido van Rossum" in content
    else:
        pytest.fail("Could not find History section in the Python page")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_coordinates(api):
    """Test retrieving coordinates from a page with known location."""
    # Use Eiffel Tower which definitely has coordinates
    page = await api.page("Eiffel Tower")
    coordinates = await page.coordinates
    
    assert coordinates is not None
    assert isinstance(coordinates, tuple)
    assert len(coordinates) == 2
    assert isinstance(coordinates[0], Decimal)  # Latitude
    assert isinstance(coordinates[1], Decimal)  # Longitude
    # Check coordinates are roughly correct for Paris
    assert 48 < float(coordinates[0]) < 49  # Paris latitude ~48.8°
    assert 2 < float(coordinates[1]) < 3    # Paris longitude ~2.3°


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_page_error(api):
    """Test that PageError is raised for non-existent pages."""
    with pytest.raises(PageError):
        await api.page("ThisPageDefinitelyDoesNotExistOnWikipedia123456789")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_redirect(api):
    """Test page redirects."""
    # "Python language" should redirect to "Python (programming language)"
    page = await api.page("Python language")
    assert page.title == "Python (programming language)"
    
    # With redirect=False, should raise RedirectError
    with pytest.raises(RedirectError):
        await api.page("Python language", redirect=False)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_lang_title(python_page):
    """Test getting the page title in different languages."""
    # Get Spanish title for Python
    es_title = await python_page.lang_title("es")
    assert es_title is not None
    assert isinstance(es_title, str)
    # Spanish title should be "Python" or may include terms like "lenguaje" 
    assert "Python" in es_title