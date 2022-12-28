import requests
from typing import Dict, Optional
from .exceptions import LanguageError

__all__ = ["Language"]


class Language(object):
    """
    Language used in mediawiki, if language is not defined English will be used
    """

    DEFAULT_LANGUAGE = "en"
    predefined_languages = None

    def __init__(self, language: Optional[str] = None):
        if self.__class__.predefined_languages is None:
            self.__class__.predefined_languages = self.__get_available_languages()
        if language is None:
            self.language = self.DEFAULT_LANGUAGE
        else:
            self.language = language

    @property
    def language(self) -> str:
        """
        Return language
        """
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        """
        Change the language of the API being requested.
        Set `language` to one of the two letter prefixes found on the
        `list of all Wikipedias <http://meta.wikimedia.org/wiki/List_of_Wikipedias>`_.
        Raise error if language not in a list of predefined languages
        Args:
        * language - (string) a string specifying the language
        """
        language = language.lower()
        if (
            self.__class__.predefined_languages
            and language in self.__class__.predefined_languages.keys()
        ):
            self._language = language
        else:
            raise LanguageError(language)

    def __get_available_languages(self) -> Dict[str, str]:
        """
        Internal static function for getting all available language on mediawiki
        """
        params = {
            "meta": "siteinfo",
            "siprop": "languages",
            "format": "json",
            "action": "query",
        }
        headers = {
            "User-Agent": "mediawikiapi (https://github.com/lehinevych/MediaWikiAPI/)"
        }
        response = requests.get(
            "https://en.wikipedia.org/w/api.php", params=params, headers=headers
        )
        response_dict = response.json()
        languages = response_dict["query"]["languages"]
        return {lang["code"]: lang["*"] for lang in languages}
