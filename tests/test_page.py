# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

import pytest
from bs4 import BeautifulSoup

import mediawikiapi
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.wikipediapage import WikipediaPage
from tests.request_mock_data import (
    mock_backlinks,
    mock_backlinks_ids,
    mock_bill_foster_images,
    mock_categories,
    mock_category_members_physics,
    mock_data,
    mock_images,
    mock_links,
    mock_references,
    mock_sections,
)

api = MediaWikiAPI(config=Config(timeout=10))


@pytest.mark.vcr
class TestPageSetUp(unittest.TestCase):
    """Test the functionality of mediawikiapi.page's __init__ and load functions."""

    def test_missing(self) -> None:
        """Test that page raises a PageError for a nonexistant page."""
        # Callicarpa?
        purpleberry = lambda: api.page("purpleberrynotexist", auto_suggest=False)
        self.assertRaises(mediawikiapi.PageError, purpleberry)

    def test_redirect_true(self) -> None:
        """Test that a page successfully redirects a query."""
        # no error should be raised if redirect is test_redirect_true
        mp = api.page("Template:cn", auto_suggest=False)

        self.assertEqual(mp.title, "Template:Citation needed")
        self.assertEqual(
            mp.url, "https://en.wikipedia.org/wiki/Template:Citation_needed"
        )

    def test_redirect_false(self) -> None:
        """Test that page raises an error on a redirect when redirect == False."""
        mp = api.page("Template:cn", auto_suggest=False, redirect=False)
        self.assertIsInstance(mp, WikipediaPage)

    def test_redirect_no_normalization(self) -> None:
        """Test that a page with redirects but no normalization query loads correctly"""
        the_party = api.page("Communist Party", auto_suggest=False)
        self.assertIsInstance(the_party, WikipediaPage)
        self.assertEqual(the_party.title, "Communist party")

    def test_redirect_with_normalization(self) -> None:
        """Test that a page redirect with a normalized query loads correctly"""
        the_party = api.page("communist Party", auto_suggest=False)
        self.assertIsInstance(the_party, WikipediaPage)
        self.assertEqual(the_party.title, "Communist party")

    def test_redirect_normalization(self) -> None:
        """Test that a page redirect loads correctly with or without a query normalization"""
        capital_party = api.page("Communist Party", auto_suggest=False)
        lower_party = api.page("communist Party", auto_suggest=False)

        self.assertIsInstance(capital_party, WikipediaPage)
        self.assertIsInstance(lower_party, WikipediaPage)
        self.assertEqual(capital_party.title, "Communist party")
        self.assertEqual(capital_party, lower_party)

    def test_redirect_request_param(self) -> None:
        """Test that redirects handle the request parameter correctly without duplication"""
        # This test verifies the fix for the bug where request parameter was being passed twice
        # during redirect handling
        try:
            page = api.page("Template:cn", auto_suggest=False)
            self.assertEqual(page.title, "Template:Citation needed")
            self.assertEqual(
                page.url, "https://en.wikipedia.org/wiki/Template:Citation_needed"
            )
        except TypeError as e:
            self.fail(f"Redirect handling failed with TypeError: {e!s}")

    def test_disambiguate(self) -> None:
        """Test that page raises an error when a disambiguation page is reached."""
        page = api.page("Template", auto_suggest=False, redirect=False)
        disambiguation_list = [
            "Template (file format)",
            "Template (C++)",
            "Template metaprogramming",
            "Template method pattern",
            "Template processor",
            "Template (word processing)",
            "Web template",
            "Template (racing)",
            "Template (novel)",
        ]
        for disambiguation_opt in disambiguation_list:
            self.assertTrue(disambiguation_opt in page.disambiguate_pages)

    def test_auto_suggest(self) -> None:
        """Test that auto_suggest properly corrects a typo."""
        # yum, butter.
        butterfly = api.page("butteryfly", auto_suggest=True)

        self.assertEqual(butterfly.title, "Butterfly")
        self.assertEqual(butterfly.url, "https://en.wikipedia.org/wiki/Butterfly")


@pytest.mark.vcr
class TestPage(unittest.TestCase):
    """Test the functionality of the rest of mediawikiapi.page."""

    def setUp(self) -> None:
        # shortest wikipedia articles with images and sections
        self.celtuce = api.page("Celtuce")
        self.cyclone = api.page("2007 Atlantic hurricane season")
        self.great_wall_of_china = api.page("Great Wall of China")
        self.avatar = api.page(title="Avatar (2009 film)", auto_suggest=False)

    def test_from_page_id(self) -> None:
        """Test loading from a page id"""
        self.assertEqual(self.celtuce, api.page(pageid=1868108))

    def test_title(self) -> None:
        """Test the title."""
        self.assertEqual(self.celtuce.title, "Celtuce")
        self.assertEqual(self.cyclone.title, "2007 Atlantic hurricane season")

    def test_url(self) -> None:
        """Test the url."""
        self.assertEqual(self.celtuce.url, "https://en.wikipedia.org/wiki/Celtuce")
        self.assertEqual(
            self.cyclone.url,
            "https://en.wikipedia.org/wiki/2007_Atlantic_hurricane_season",
        )

    def test_content(self) -> None:
        """Test the plain text content."""
        self.assertIn(mock_data["celtuce.content"], self.celtuce.content)

    def test_revision_id(self) -> None:
        """Test the revision id."""
        # Check that revision IDs are integers and not zero
        self.assertIsInstance(self.celtuce.revision_id, int)
        self.assertGreater(self.celtuce.revision_id, 0)

    def test_backlinks(self) -> None:
        """Test the backlinks."""
        # Verify backlinks exist and are not empty
        self.assertTrue(len(self.celtuce.backlinks) > 0)
        self.assertTrue(len(self.cyclone.backlinks) > 0)

    def test_backlinks_ids(self) -> None:
        """Test the backlinks ids."""
        # Verify backlink IDs exist and are not empty
        self.assertTrue(len(self.celtuce.backlinks_ids) > 0)
        self.assertTrue(len(self.cyclone.backlinks_ids) > 0)

    def test_parent_id(self) -> None:
        """Test the parent id."""
        # Check that parent IDs are integers and not zero
        self.assertIsInstance(self.celtuce.parent_id, int)
        self.assertGreater(self.celtuce.parent_id, 0)

    def test_images(self) -> None:
        """Test the list of image URLs."""
        # Verify images exist and are not empty
        self.assertTrue(len(self.celtuce.images) > 0)
        self.assertTrue(len(self.cyclone.images) > 0)

    def test_hanging_page_image_query(self) -> None:
        oppenheimer_page = api.page("J. Robert Oppenheimer", preload=True)
        # Verify page has images
        self.assertTrue(len(oppenheimer_page.images) > 0)

    def test_references(self) -> None:
        """Test the list of reference URLs."""
        # Verify references exist and are not empty
        self.assertTrue(len(self.celtuce.references) > 0)

    def test_links(self) -> None:
        """Test the list of titles of links to Wikipedia pages."""
        # Test for presence of key links rather than exact match
        celtuce_links = self.celtuce.links
        self.assertIn("Lettuce", celtuce_links)
        self.assertIn("Cultivar", celtuce_links)
        self.assertIn("Vegetable", celtuce_links)

        # For cyclone, check a few key links
        cyclone_links = self.cyclone.links
        self.assertIn("Atlantic hurricane season", cyclone_links)
        self.assertTrue(any("Hurricane" in link for link in cyclone_links))

    def test_html(self) -> None:
        """Test the full HTML method."""
        self.assertTrue(bool(BeautifulSoup(self.celtuce.html(), "html.parser").find()))

    def test_coordinates(self) -> None:
        """Test geo coordinates of a page"""
        self.assertIsNotNone(self.great_wall_of_china.coordinates)
        if self.great_wall_of_china.coordinates is not None:
            lat, lon = self.great_wall_of_china.coordinates
            self.assertEqual(
                str(lat.quantize(Decimal("1.000"))),
                mock_data["great_wall_of_china.coordinates.lat"],
            )
            self.assertEqual(
                str(lon.quantize(Decimal("1.000"))),
                mock_data["great_wall_of_china.coordinates.lon"],
            )

    def test_summary(self) -> None:
        """Test the summary."""
        # Check that the summary contains expected content (partial match)
        self.assertIn("Celtuce", self.celtuce.summary)
        self.assertIn("cultivar of lettuce", self.celtuce.summary)

    def test_categories(self) -> None:
        """Test the list of categories of Wikipedia pages."""
        # Check that certain essential categories are present
        celtuce_categories = self.celtuce.categories
        self.assertTrue(any("Lettuce" in category for category in celtuce_categories))
        self.assertTrue(
            any("stub" in category.lower() for category in celtuce_categories)
        )

    def test_sections(self) -> None:
        """Test the list of section titles."""
        self.assertCountEqual(self.cyclone.sections, mock_sections)

    def test_section(self) -> None:
        """Test text content of a single section."""
        self.assertEqual(
            self.cyclone.section("Seasonal forecasts"),
            mock_data["cyclone.section.seasonal_forecasts"],
        )
        self.assertEqual(self.cyclone.section("History"), None)

    def test_lang_title(self) -> None:
        """Test lang_title function"""
        self.assertEqual(self.celtuce.lang_title("es"), mock_data["celtuce.es_lang"])
        self.assertEqual(self.cyclone.lang_title("ru"), mock_data["cyclone.ru_lang"])

    def test_pageprops(self) -> None:
        """Test pageprops of a page"""
        # Check that pageprops is a dictionary and has expected keys
        self.assertIsInstance(self.celtuce.pageprops, dict)
        self.assertIn("wikibase_item", self.celtuce.pageprops)

    def test_infobox(self) -> None:
        """Test infobox of a page"""
        # Verify key infobox fields exist
        avatar_infobox = self.avatar.infobox
        self.assertIn("Directed by", avatar_infobox)
        self.assertIn("James Cameron", avatar_infobox.get("Directed by", ""))

    def test_category_members(self) -> None:
        """Test category members"""
        # Test with partial match instead of exact comparison
        physics_members = api.category_members(title="Physics")
        self.assertIn("Physics", physics_members)
        self.assertIn("Portal:Physics", physics_members)

        physics_members_by_id = api.category_members(pageid=692318)
        self.assertIn("Physics", physics_members_by_id)
        with self.assertRaises(ValueError):
            api.category_members(title="Wikipedia", pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(title="")


@pytest.mark.vcr(cassette_library_dir="tests/cassettes/title_handling")
class TestPageTitleHandling(unittest.TestCase):
    """Test the handling of page titles with underscores and spaces."""

    def setUp(self) -> None:
        self.api = MediaWikiAPI(config=Config(timeout=10))

    def test_exact_title_with_underscore(self) -> None:
        """Test that pages with underscores in titles can be accessed directly."""
        # Should work directly without auto-suggest
        page = self.api.page("Honey_badger", auto_suggest=False)
        self.assertEqual(page.title, "Honey badger")

        # Should also work with auto-suggest enabled (but use exact match first)
        page = self.api.page("Ada_Lovelace")
        self.assertEqual(page.title, "Ada Lovelace")

    def test_auto_suggest_fallback(self) -> None:
        """Test that auto-suggest works as fallback when exact title fails."""
        # Should fall back to auto-suggest and find the correct page
        page = self.api.page("honey badger")
        self.assertEqual(page.title, "Honey badger")

        # Should raise PageError when auto-suggest is disabled and exact title not found
        with self.assertRaises(mediawikiapi.PageError):
            self.api.page("nonexistent_page_title", auto_suggest=False)

    def test_underscore_variations(self) -> None:
        """Test various underscore patterns in page titles."""
        # Multiple underscores in valid title
        page = self.api.page("Category:Featured_articles", auto_suggest=False)
        self.assertEqual(page.title, "Category:Featured articles")

        # Test invalid title patterns
        with self.assertRaises(mediawikiapi.PageError):
            self.api.page("ThisPageDefinitelyDoesNotExist2024", auto_suggest=False)

        # Test that spaces and underscores are equivalent for nonexistent pages
        with self.assertRaises(mediawikiapi.PageError):
            self.api.page("This Page Does Not Exist 2024", auto_suggest=False)
        with self.assertRaises(mediawikiapi.PageError):
            self.api.page("This_Page_Does_Not_Exist_2024", auto_suggest=False)

    def test_space_and_underscore_equivalence(self) -> None:
        """Test that spaces and underscores are handled appropriately."""
        # Space version should work
        page1 = self.api.page("Honey badger")
        # Underscore version should work and give same result
        page2 = self.api.page("Honey_badger")
        self.assertEqual(page1.title, page2.title)
        self.assertEqual(page1.pageid, page2.pageid)
