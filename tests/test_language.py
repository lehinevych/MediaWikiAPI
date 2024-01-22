# -*- coding: utf-8 -*-
import pytest
import unittest
from mediawikiapi import LanguageError
from mediawikiapi import Language


@pytest.mark.vcr()
class TestLanguage(unittest.TestCase):
    """Test the Language class"""

    def setUp(self) -> None:
        self.lang_class = Language()

    def test_default_language(self) -> None:
        """Test that default language set to en"""
        self.assertEqual(self.lang_class.language, "en")

    def test_set_language(self) -> None:
        """Test the set language"""
        self.lang_class.language = "fr"
        self.assertEqual(self.lang_class.language, "fr")

    def test_set_fake_language(self) -> None:
        """Test exception when try to set wrong language"""
        with self.assertRaises(LanguageError):
            self.lang_class.language = "fakelang"
