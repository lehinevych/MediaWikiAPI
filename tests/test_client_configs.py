# -*- coding: utf-8 -*-
import unittest

from collections import defaultdict
from decimal import Decimal
from typing import Dict, Any
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config

api = MediaWikiAPI(config=Config(mediawiki_url="https://{}.wiktionary.org/w/api.php"))

<<<<<<< HEAD

class TestSearchLoc(unittest.TestCase):
    def test_search_in_wiktionary(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertIn("python", api.search("python"))
=======
class TestSearchLoc(unittest.TestCase):

    def test_search_in_wiktionary(self) -> None:
        """Test parsing a mediawikiapi location request result."""
        self.assertIn("python", api.search("python"))
    
>>>>>>> 6cceb4e (add the config tests, increase coverage to 82% and rename test files)
