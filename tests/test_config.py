# -*- coding: utf-8 -*-
import unittest
from datetime import timedelta
from mediawikiapi.config import Config
from mediawikiapi import Language


class TestConfig(unittest.TestCase):
    def test_default_language_config(self) -> None:
        self.assertEqual(Config().language, Language.DEFAULT_LANGUAGE)

    def test_default_user_agent_config(self) -> None:
        self.assertEqual(Config().user_agent, Config.DEFAULT_USER_AGENT)

    def test_default_get_api_url(self) -> None:
        self.assertEqual(
            Config().get_api_url(), Config.API_URL.format(Language.DEFAULT_LANGUAGE)
        )

    def test_default_get_api_url_with_custom_language(self) -> None:
        fr_lang = "fr"
        uk_lang = "uk"
        config = Config()
        self.assertEqual(
            config.get_api_url(language=fr_lang), config.API_URL.format(fr_lang)
        )
        self.assertEqual(
            config.get_api_url(language=Language(uk_lang)),
            config.API_URL.format(uk_lang),
        )

    def test_default_rate_limit_is_None(self) -> None:
        self.assertEqual(Config().rate_limit, None)

    def test_default_donate_url(self) -> None:
        self.assertEqual(Config().donate_url(), Config.DONATE_URL)

    def test_custom_api_url_with_language_support(self) -> None:
        api_url = "https://{}.wiktionary.org/w/api.php"
        self.assertEqual(
            Config(mediawiki_url=api_url).get_api_url(),
            api_url.format(Language.DEFAULT_LANGUAGE),
        )

    def test_custom_api_url(self) -> None:
        api_url = "https://wiki.archlinux.org"
        self.assertEqual(Config(mediawiki_url=api_url).get_api_url(), api_url)

    def test_custom_rate_limit_as_int(self) -> None:
        rate_limit: int = 10
        self.assertEqual(
            Config(rate_limit=rate_limit).rate_limit, timedelta(milliseconds=10)
        )

    def test_custom_rate_limit_as_timedelta(self) -> None:
        rate_limit: timedelta = timedelta(milliseconds=10)
        self.assertEqual(Config(rate_limit=rate_limit).rate_limit, rate_limit)

    def test_set_rate_limit(self) -> None:
        rate_limit_int = 10
        rate_limit: timedelta = timedelta(milliseconds=rate_limit_int)
        config = Config()
        config.rate_limit = None
        self.assertEqual(config.rate_limit, None)
        config.rate_limit = rate_limit_int  # type:ignore
        self.assertEqual(config.rate_limit, rate_limit)
        config.rate_limit = rate_limit
        self.assertEqual(config.rate_limit, rate_limit)

    def test_custom_language(self) -> None:
        custom_lang = "fr"
        self.assertEqual(Config(language=custom_lang).language, custom_lang)

    def test_set_custom_language(self) -> None:
        fr_lang = "fr"
        uk_lang = "uk"
        config = Config()
        config.language = fr_lang
        self.assertEqual(config.language, fr_lang)
        config.language = Language(uk_lang)  # type:ignore
        self.assertEqual(config.language, uk_lang)

    def test_default_headers(self) -> None:
        """Test that default headers include User-Agent"""
        config = Config()
        headers = config.get_headers()
        self.assertIn("User-Agent", headers)
        self.assertEqual(headers["User-Agent"], Config.DEFAULT_USER_AGENT)

    def test_access_token_in_headers(self) -> None:
        """Test that access_token is included in Authorization header"""
        access_token = "test_token_12345"
        config = Config(access_token=access_token)
        headers = config.get_headers()
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], f"Bearer {access_token}")

    def test_custom_headers(self) -> None:
        """Test that custom headers are included"""
        custom_headers = {"X-Custom-Header": "custom_value", "X-Another": "another"}
        config = Config(custom_headers=custom_headers)
        headers = config.get_headers()
        self.assertIn("X-Custom-Header", headers)
        self.assertEqual(headers["X-Custom-Header"], "custom_value")
        self.assertIn("X-Another", headers)
        self.assertEqual(headers["X-Another"], "another")

    def test_custom_headers_override_defaults(self) -> None:
        """Test that custom headers can override default User-Agent"""
        custom_user_agent = "MyCustomBot/1.0"
        custom_headers = {"User-Agent": custom_user_agent}
        config = Config(custom_headers=custom_headers)
        headers = config.get_headers()
        self.assertEqual(headers["User-Agent"], custom_user_agent)

    def test_access_token_and_custom_headers(self) -> None:
        """Test that access_token and custom headers work together"""
        access_token = "test_token_12345"
        custom_headers = {"X-Custom": "value"}
        config = Config(access_token=access_token, custom_headers=custom_headers)
        headers = config.get_headers()
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], f"Bearer {access_token}")
        self.assertIn("X-Custom", headers)
        self.assertEqual(headers["X-Custom"], "value")
        self.assertIn("User-Agent", headers)
