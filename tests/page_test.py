# -*- coding: utf-8 -*-
import unittest
import mediawikiapi
from bs4 import BeautifulSoup
from decimal import Decimal
from typing import Dict, Any
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from mediawikiapi.wikipediapage import WikipediaPage
from tests.request_mock_data import (
    mock_data,
    mock_images,
    mock_links,
    mock_references,
    mock_categories,
    mock_backlinks,
    mock_backlinks_ids,
    mock_bill_foster_images,
    mock_sections,
    mock_category_members_physics,
)

api = MediaWikiAPI()


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
        butterfly = api.page("butteryfly")

        self.assertEqual(butterfly.title, "Butterfly")
        self.assertEqual(butterfly.url, "https://en.wikipedia.org/wiki/Butterfly")


class TestPage(unittest.TestCase):
    """Test the functionality of the rest of mediawikiapi.page."""

    maxDiff = None

    def setUp(self) -> None:
        # shortest wikipedia articles with images and sections
        self.celtuce = api.page("Celtuce")
        self.cyclone = api.page("2007 Atlantic hurricane season")
        self.great_wall_of_china = api.page("Great Wall of China")
        self.avatar = api.page(title="Avatar_(2009_film)")

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
        self.assertEqual(self.celtuce.revision_id, mock_data["celtuce.revid"])
        self.assertEqual(self.cyclone.revision_id, mock_data["cyclone.revid"])

    def test_backlinks(self) -> None:
        """Test the backlinks."""
        self.assertCountEqual(self.celtuce.backlinks, mock_backlinks["celtuce"])
        self.assertCountEqual(self.cyclone.backlinks, mock_backlinks["cyclone"])

    def test_backlinks_ids(self) -> None:
        """Test the backlinks ids."""
        self.assertCountEqual(self.celtuce.backlinks_ids, mock_backlinks_ids["celtuce"])
        self.assertCountEqual(self.cyclone.backlinks_ids, mock_backlinks_ids["cyclone"])

    def test_parent_id(self) -> None:
        """Test the parent id."""
        self.assertEqual(self.celtuce.parent_id, mock_data["celtuce.parentid"])
        self.assertEqual(self.cyclone.parent_id, mock_data["cyclone.parentid"])

    def test_images(self) -> None:
        """Test the list of image URLs."""
        self.assertCountEqual(self.celtuce.images, mock_images["celtuce"])
        self.assertCountEqual(self.cyclone.images, mock_images["cyclone"])

    def test_hanging_page_image_query(self) -> None:
        bill_foster_page = api.page("Bill Foster (politician)", preload=True)
        self.assertCountEqual(bill_foster_page.images, mock_bill_foster_images)

    def test_references(self) -> None:
        """Test the list of reference URLs."""
        self.assertCountEqual(self.celtuce.references, mock_references)

    def test_links(self) -> None:
        """Test the list of titles of links to Wikipedia pages."""
        self.assertCountEqual(self.celtuce.links, mock_links["celtuce"])
        self.assertCountEqual(self.cyclone.links, mock_links["cyclone"])

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
        # Strip is used to nuke \n from the end
        self.assertIn(mock_data["celtuce.summary"], self.celtuce.summary)

    def test_categories(self) -> None:
        """Test the list of categories of Wikipedia pages."""
        self.assertCountEqual(self.celtuce.categories, mock_categories["celtuce"])
        self.assertCountEqual(self.cyclone.categories, mock_categories["cyclone"])

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
        self.assertEqual(self.celtuce.pageprops, mock_data["celtuce.pageprops"])
        self.assertEqual(self.cyclone.pageprops, mock_data["cyclone.pageprops"])

    def test_infobox(self) -> None:
        """Test infobox of a page"""
        self.assertEqual(self.avatar.infobox, mock_data["infobox_avatar"])

    def test_category_members(self) -> None:
        """Test category members"""
        self.assertEqual(
            api.category_members(title="Physics"),
            mock_category_members_physics,
        )
        self.assertEqual(
            api.category_members(pageid=692318),
            mock_category_members_physics,
        )
        with self.assertRaises(ValueError):
            api.category_members(title="Wikipedia", pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(title="")
