# -*- coding: utf-8 -*-
import unittest
import mediawikiapi
from bs4 import BeautifulSoup
from decimal import Decimal
from mediawikiapi import MediaWikiAPI
from tests.request_mock_data import mock_data

api = MediaWikiAPI()


# mock out _wiki_request
def _wiki_request(params, config):
    return mock_data["_wiki_request calls"][tuple(sorted(params.items()))]


# api.session.request = _wiki_request


class TestPageSetUp(unittest.TestCase):
    """Test the functionality of mediawikiapi.page's __init__ and load functions."""

    def test_missing(self):
        """Test that page raises a PageError for a nonexistant page."""
        # Callicarpa?
        purpleberry = lambda: api.page("purpleberrynotexist", auto_suggest=False)
        self.assertRaises(mediawikiapi.PageError, purpleberry)

    def test_redirect_true(self):
        """Test that a page successfully redirects a query."""
        # no error should be raised if redirect is test_redirect_true
        mp = api.page("Template:cn", auto_suggest=False)

        self.assertEqual(mp.title, "Template:Citation needed")
        self.assertEqual(mp.url, "https://en.wikipedia.org/wiki/Template:Citation_needed")

    def test_redirect_false(self):
        """Test that page raises an error on a redirect when redirect == False."""
        mp = api.page("Template:cn", auto_suggest=False, redirect=False)
        self.assertIsInstance(mp, mediawikiapi.WikipediaPage)

    def test_redirect_no_normalization(self):
        """Test that a page with redirects but no normalization query loads correctly"""
        the_party = api.page("Communist Party", auto_suggest=False)
        self.assertIsInstance(the_party, mediawikiapi.WikipediaPage)
        self.assertEqual(the_party.title, "Communist party")

    def test_redirect_with_normalization(self):
        """Test that a page redirect with a normalized query loads correctly"""
        the_party = api.page("communist Party", auto_suggest=False)
        self.assertIsInstance(the_party, mediawikiapi.WikipediaPage)
        self.assertEqual(the_party.title, "Communist party")

    def test_redirect_normalization(self):
        """Test that a page redirect loads correctly with or without a query normalization"""
        capital_party = api.page("Communist Party", auto_suggest=False)
        lower_party = api.page("communist Party", auto_suggest=False)

        self.assertIsInstance(capital_party, mediawikiapi.WikipediaPage)
        self.assertIsInstance(lower_party, mediawikiapi.WikipediaPage)
        self.assertEqual(capital_party.title, "Communist party")
        self.assertEqual(capital_party, lower_party)

    def test_disambiguate(self):
        """Test that page raises an error when a disambiguation page is reached."""
        page = api.page("Template", auto_suggest=False, redirect=False)
        disambiguation_list = [u'Template (file format)', u'Template (C++)', u'Template metaprogramming',
                               u'Template method pattern', u'Template processor', u'Template (word processing)',
                               u'Web template', u'Template (racing)', u'Template (novel)']
        for disambiguation_opt in disambiguation_list:
            self.assertTrue(disambiguation_opt in page.disambiguate_pages)

    def test_auto_suggest(self):
        """Test that auto_suggest properly corrects a typo."""
        # yum, butter.
        butterfly = api.page("butteryfly")

        self.assertEqual(butterfly.title, "Butterfly")
        self.assertEqual(butterfly.url, "https://en.wikipedia.org/wiki/Butterfly")


class TestPage(unittest.TestCase):
    """Test the functionality of the rest of mediawikiapi.page."""
    maxDiff = None

    def setUp(self):
        # shortest wikipedia articles with images and sections
        self.celtuce = api.page("Celtuce")
        self.cyclone = api.page("2007 Atlantic hurricane season")
        self.great_wall_of_china = api.page("Great Wall of China")
        self.avatar = api.page(title="Avatar_(2009_film)")

    def test_from_page_id(self):
        """Test loading from a page id"""
        self.assertEqual(self.celtuce, api.page(pageid=1868108))

    def test_title(self):
        """Test the title."""
        self.assertEqual(self.celtuce.title, "Celtuce")
        self.assertEqual(self.cyclone.title, "2007 Atlantic hurricane season")

    def test_url(self):
        """Test the url."""
        self.assertEqual(self.celtuce.url, "https://en.wikipedia.org/wiki/Celtuce")
        self.assertEqual(self.cyclone.url, "https://en.wikipedia.org/wiki/2007_Atlantic_hurricane_season")

    def test_content(self):
        """Test the plain text content."""
        self.assertIn(mock_data['data']["celtuce.content"], self.celtuce.content)

    def test_revision_id(self):
        """Test the revision id."""
        self.assertEqual(self.celtuce.revision_id, mock_data['data']["celtuce.revid"])
        self.assertEqual(self.cyclone.revision_id, mock_data['data']["cyclone.revid"])

    def test_backlinks(self):
        """Test the backlinks."""
        self.assertCountEqual(self.celtuce.backlinks, mock_data['data']["celtuce.backlinks"])
        self.assertCountEqual(self.cyclone.backlinks, mock_data['data']["cyclone.backlinks"])

    def test_backlinks_ids(self):
        """Test the backlinks ids."""
        self.assertCountEqual(self.celtuce.backlinks_ids, mock_data['data']["celtuce.backlinks_ids"])
        self.assertCountEqual(self.cyclone.backlinks_ids, mock_data['data']["cyclone.backlinks_ids"])

    def test_parent_id(self):
        """Test the parent id."""
        self.assertEqual(self.celtuce.parent_id, mock_data['data']["celtuce.parentid"])
        self.assertEqual(self.cyclone.parent_id, mock_data['data']["cyclone.parentid"])

    def test_images(self):
        """Test the list of image URLs."""
        self.assertCountEqual(self.celtuce.images, mock_data['data']["celtuce.images"])
        self.assertCountEqual(self.cyclone.images, mock_data['data']["cyclone.images"])

    def test_hanging_page_image_query(self):
        bill_foster_page = api.page('Bill Foster (politician)', preload=True)
        self.assertCountEqual(bill_foster_page.images, mock_data['data']["bill_foster_page.images"])

    def test_references(self):
        """Test the list of reference URLs."""
        self.assertCountEqual(self.celtuce.references, mock_data['data']["celtuce.references"])

    def test_links(self):
        """Test the list of titles of links to Wikipedia pages."""
        self.assertCountEqual(self.celtuce.links, mock_data['data']["celtuce.links"])
        self.assertCountEqual(self.cyclone.links, mock_data['data']["cyclone.links"])


    def test_html(self):
        """Test the full HTML method."""
        self.assertTrue(bool(BeautifulSoup(self.celtuce.html(), "html.parser").find()))

    def test_coordinates(self):
        """Test geo coordinates of a page"""
        lat, lon = self.great_wall_of_china.coordinates
        self.assertEqual(str(lat.quantize(Decimal('1.000'))), mock_data['data']['great_wall_of_china.coordinates.lat'])
        self.assertEqual(str(lon.quantize(Decimal('1.000'))), mock_data['data']['great_wall_of_china.coordinates.lon'])

    def test_summary(self):
        """Test the summary."""
        # Strip is used to nuke \n from the end
        self.assertIn(mock_data['data']["celtuce.summary"], self.celtuce.summary)
        self.assertIn(mock_data['data']["cyclone.summary"], self.cyclone.summary)

    def test_categories(self):
        """Test the list of categories of Wikipedia pages."""
        self.assertCountEqual(self.celtuce.categories, mock_data['data']["celtuce.categories"])
        self.assertCountEqual(self.cyclone.categories, mock_data['data']["cyclone.categories"])

    def test_sections(self):
        """Test the list of section titles."""
        self.assertCountEqual(self.cyclone.sections, mock_data['data']["cyclone.sections"])

    def test_section(self):
        """Test text content of a single section."""
        self.assertEqual(self.cyclone.section("Seasonal forecasts"), mock_data['data']["cyclone.section.seasonal_forecasts"])
        self.assertEqual(self.cyclone.section("History"), None)

    def test_lang_title(self):
        """ Test lang_title function"""
        self.assertEqual(self.celtuce.lang_title('es'), mock_data['data']["celtuce.es_lang"])
        self.assertEqual(self.cyclone.lang_title('ru'), mock_data['data']["cyclone.ru_lang"])

    def test_pageprops(self):
        """Test pageprops of a page"""
        self.assertEqual(self.celtuce.pageprops, mock_data['data']["celtuce.pageprops"])
        self.assertEqual(self.cyclone.pageprops, mock_data['data']["cyclone.pageprops"])

    def test_infobox(self):
        """Test infobox of a page"""
        self.assertEqual(self.avatar.infobox, mock_data['data']["infobox_avatar"])

    def test_category_members(self):
        """Test category members"""
        self.assertEqual(api.category_members(title='Physics'), mock_data['data']["category_members_physics"])
        self.assertEqual(api.category_members(pageid=692318), mock_data['data']["category_members_physics"])
        with self.assertRaises(ValueError):
            api.category_members(title='Wikipedia', pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(pageid=6923181)
        with self.assertRaises(ValueError):
            api.category_members(title='')
