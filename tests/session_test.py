# -*- coding: utf-8 -*-
import unittest

from mediawikiapi import MediaWikiAPI

api = MediaWikiAPI()


class TestSession(unittest.TestCase):

    def test_new_session(self):
        """ Test the new_session function """
        api.session.new_session()
        s1 = api.session.session
        self.assertIsNotNone(s1)

        api.session.new_session()
        s2 = api.session.session
        self.assertIsNotNone(s2)

        self.assertNotEqual(s1, s2)

    def test_get_session(self):
        """ Test the get_session function """
        api.session.new_session()
        s1 = api.session.session
        self.assertIsNotNone(s1)

        s2 = api.session.session
        self.assertIsNotNone(s2)
        self.assertEqual(s1, s2)
