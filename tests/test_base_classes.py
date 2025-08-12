"""
Tests for abstract base classes.
"""
import unittest
from unittest.mock import MagicMock, patch

from mediawikiapi.base.base_mediawikiapi import BaseMediaWikiAPI
from mediawikiapi.base.base_requestsession import BaseRequestSession
from mediawikiapi.base.base_wikipediapage import BaseWikipediaPage
from mediawikiapi.config import Config


class TestBaseMediaWikiAPI(unittest.TestCase):
    """Test the BaseMediaWikiAPI class helper methods."""

    def setUp(self):
        """Set up a concrete implementation of BaseMediaWikiAPI."""
        # Create a mock implementation of BaseMediaWikiAPI
        class ConcreteMediaWikiAPI(BaseMediaWikiAPI):
            def get_cache_statistics(self):
                return {}
                
            def invalidate_all_caches(self):
                return {}
                
            def search(self, *args, **kwargs):
                pass
                
            def geosearch(self, *args, **kwargs):
                pass
                
            def suggest(self, *args, **kwargs):
                pass
                
            def random(self, *args, **kwargs):
                pass
                
            def summary(self, *args, **kwargs):
                pass
                
            def page(self, *args, **kwargs):
                pass
                
            def languages(self):
                pass
                
            def category_members(self, *args, **kwargs):
                pass
                
            def custom_query(self, *args, **kwargs):
                pass
        
        self.api = ConcreteMediaWikiAPI()

    def test_init(self):
        """Test initialization with default and custom configs."""
        # Default config
        api = self.api
        self.assertIsInstance(api.config, Config)
        
        # Custom config
        config = Config()
        config.language = "fr"
        api = self.api.__class__(config)
        self.assertEqual(api.config.language, "fr")

    def test_prepare_search_params(self):
        """Test search parameter preparation."""
        params = self.api._prepare_search_params("test query", 20, True)
        self.assertEqual(params["list"], "search")
        self.assertEqual(params["srlimit"], 20)
        self.assertEqual(params["srsearch"], "test query")
        self.assertEqual(params["srinfo"], "suggestion")
        
        params = self.api._prepare_search_params("test query", 10, False)
        self.assertNotIn("srinfo", params)

    def test_prepare_geosearch_params(self):
        """Test geosearch parameter preparation."""
        params = self.api._prepare_geosearch_params(40.748, -73.985, "Empire State", 15, 500)
        self.assertEqual(params["list"], "geosearch")
        self.assertEqual(params["gsradius"], 500)
        self.assertEqual(params["gscoord"], "40.748|-73.985")
        self.assertEqual(params["gslimit"], 15)
        self.assertEqual(params["titles"], "Empire State")
        
        params = self.api._prepare_geosearch_params(40.748, -73.985, None, 10, 1000)
        self.assertNotIn("titles", params)

    def test_prepare_suggest_params(self):
        """Test suggest parameter preparation."""
        params = self.api._prepare_suggest_params("test query")
        self.assertEqual(params["list"], "search")
        self.assertEqual(params["srinfo"], "suggestion")
        self.assertEqual(params["srsearch"], "test query")

    def test_prepare_random_params(self):
        """Test random parameter preparation."""
        params = self.api._prepare_random_params(5)
        self.assertEqual(params["list"], "random")
        self.assertEqual(params["rnnamespace"], 0)
        self.assertEqual(params["rnlimit"], 5)

    def test_prepare_summary_params(self):
        """Test summary parameter preparation."""
        # With sentences
        params = self.api._prepare_summary_params("Test Page", 3, None)
        self.assertEqual(params["prop"], "extracts")
        self.assertEqual(params["titles"], "Test Page")
        self.assertEqual(params["exsentences"], 3)
        self.assertNotIn("exchars", params)
        self.assertNotIn("exintro", params)
        
        # With chars
        params = self.api._prepare_summary_params("Test Page", None, 200)
        self.assertEqual(params["exchars"], 200)
        self.assertNotIn("exsentences", params)
        self.assertNotIn("exintro", params)
        
        # With neither (uses intro)
        params = self.api._prepare_summary_params("Test Page", None, None)
        self.assertIn("exintro", params)
        self.assertNotIn("exsentences", params)
        self.assertNotIn("exchars", params)

    def test_prepare_category_members_params(self):
        """Test category members parameter preparation."""
        # With title
        params = self.api._prepare_category_members_params("Science", None, 25, "page")
        self.assertEqual(params["list"], "categorymembers")
        self.assertEqual(params["cmtitle"], "Category:Science")
        self.assertEqual(params["cmlimit"], "25")
        self.assertEqual(params["cmtype"], "page")
        
        # With pageid
        params = self.api._prepare_category_members_params(None, 12345, 50, "subcat")
        self.assertEqual(params["cmpageid"], "12345")
        self.assertEqual(params["cmlimit"], "50")
        self.assertEqual(params["cmtype"], "subcat")
        
        # Neither title nor pageid
        with self.assertRaises(ValueError):
            self.api._prepare_category_members_params(None, None, 10, "page")
            
        # Both title and pageid
        with self.assertRaises(ValueError):
            self.api._prepare_category_members_params("Science", 12345, 10, "page")

    def test_handle_error_response(self):
        """Test error response handling."""
        # No error
        self.api._handle_error_response({"query": {}}, "test")
        
        # HTTP timeout
        with self.assertRaises(Exception):
            self.api._handle_error_response(
                {"error": {"info": "HTTP request timed out."}},
                "test",
            )


class TestBaseRequestSession(unittest.TestCase):
    """Test the BaseRequestSession class helper methods."""

    def setUp(self):
        """Set up a concrete implementation of BaseRequestSession."""
        class ConcreteRequestSession(BaseRequestSession):
            def request(self, params, config):
                pass
        
        self.session = ConcreteRequestSession()

    def test_build_api_url(self):
        """Test API URL building."""
        config = Config()
        config.language = "en"
        url = self.session._build_api_url(config)
        self.assertEqual(url, "https://en.wikipedia.org/w/api.php")
        
        config.language = "fr"
        url = self.session._build_api_url(config)
        self.assertEqual(url, "https://fr.wikipedia.org/w/api.php")

    def test_prepare_params(self):
        """Test parameter preparation."""
        # Basic params
        params = self.session._prepare_params({"titles": "Test"})
        self.assertEqual(params["format"], "json")
        self.assertEqual(params["action"], "query")
        self.assertEqual(params["titles"], "Test")
        
        # With custom action
        params = self.session._prepare_params({"action": "opensearch", "search": "Test"})
        self.assertEqual(params["action"], "opensearch")
        self.assertNotEqual(params["action"], "query")  # Action is preserved

    def test_build_user_agent(self):
        """Test user agent building."""
        config = Config()
        config.user_agent = "Test User Agent"
        user_agent = self.session._build_user_agent(config)
        self.assertEqual(user_agent, "Test User Agent")


class TestBaseWikipediaPage(unittest.TestCase):
    """Test the BaseWikipediaPage class helper methods."""

    def setUp(self):
        """Set up a concrete implementation of BaseWikipediaPage."""
        class ConcreteWikipediaPage(BaseWikipediaPage):
            def __init__(self, request, title=None, pageid=None, original_title=""):
                # Custom implementation to handle property conflict
                self.request = request
                if title is not None:
                    self.title = title
                    self.original_title = original_title or title
                elif pageid is not None:
                    self._pageid = pageid  # Store in _pageid instead of pageid
                else:
                    raise ValueError("Either a title or a pageid must be specified")
            
            def __repr__(self):
                if hasattr(self, 'title'):
                    return f"<ConcreteWikipediaPage {self.title}>"
                else:
                    return f"<ConcreteWikipediaPage {self.pageid}>"
                
            @property
            def pageid(self):
                return getattr(self, '_pageid', 12345)
                
            @property
            def url(self):
                if hasattr(self, 'title'):
                    return f"https://en.wikipedia.org/wiki/{self.title}"
                else:
                    return f"https://en.wikipedia.org/wiki/?curid={self.pageid}"
                
            def html(self):
                pass
                
            def section(self, section_title):
                pass
                
            def lang_title(self, lang_code):
                pass
        
        self.request_mock = MagicMock()
        self.page_with_title = ConcreteWikipediaPage(
            self.request_mock, title="Test Page"
        )
        self.page_with_pageid = ConcreteWikipediaPage(
            self.request_mock, pageid=12345
        )

    def test_init(self):
        """Test initialization with title and pageid."""
        # With title
        page = self.page_with_title
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.original_title, "Test Page")
        self.assertEqual(page.request, self.request_mock)
        
        # With pageid
        page = self.page_with_pageid
        self.assertEqual(page.pageid, 12345)
        self.assertEqual(page.request, self.request_mock)
        
        # With neither (should raise ValueError)
        with self.assertRaises(ValueError):
            BaseWikipediaPage.__init__(
                self.page_with_title, self.request_mock, None, None
            )

    def test_title_query_param(self):
        """Test title query parameter building."""
        # With title
        params = self.page_with_title._title_query_param
        self.assertEqual(params, {"titles": "Test Page"})
        
        # With pageid
        params = self.page_with_pageid._title_query_param
        self.assertEqual(params, {"pageids": 12345})

    def test_eq(self):
        """Test equality comparison."""
        # Same attributes
        page1 = self.page_with_title.__class__(self.request_mock, title="Test Page")
        page2 = self.page_with_title.__class__(self.request_mock, title="Test Page")
        self.assertEqual(page1, page2)
        
        # Different title
        page3 = self.page_with_title.__class__(self.request_mock, title="Other Page")
        self.assertNotEqual(page1, page3)
        
        # Different types
        self.assertNotEqual(page1, "Not a WikipediaPage")

    def test_build_extracts_params(self):
        """Test extracts parameter building."""
        # With sentences
        params = self.page_with_title._build_extracts_params(5, None)
        self.assertEqual(params["prop"], "extracts")
        self.assertEqual(params["explaintext"], "")
        self.assertEqual(params["titles"], "Test Page")
        self.assertEqual(params["exsentences"], 5)
        
        # With chars
        params = self.page_with_title._build_extracts_params(None, 200)
        self.assertEqual(params["exchars"], 200)
        
        # With neither
        params = self.page_with_title._build_extracts_params(None, None)
        self.assertIn("exintro", params)

    def test_extract_section_text(self):
        """Test section text extraction."""
        content = """
        == Introduction ==
        This is an introduction.
        
        == Section 1 ==
        This is section 1.
        
        === Subsection 1.1 ===
        This is subsection 1.1.
        
        == Section 2 ==
        This is section 2.
        """
        
        # Extract existing section
        section = self.page_with_title._extract_section_text(content, "Section 1")
        self.assertIn("This is section 1", section)
        
        # Extract non-existent section
        section = self.page_with_title._extract_section_text(content, "Nonexistent")
        self.assertIsNone(section)


if __name__ == "__main__":
    unittest.main()