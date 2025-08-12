"""
Sync module containing synchronous implementations of MediaWikiAPI.

This module provides synchronous implementations of the MediaWikiAPI
classes using the requests library.
"""

from .mediawikiapi import MediaWikiAPI
from .wikipediapage import WikipediaPage
from .requestsession import RequestSession
from .util import memorized
from .cache_util import (
    get_cache_statistics, 
    invalidate_all_caches
)

__all__ = [
    "MediaWikiAPI",
    "WikipediaPage",
    "RequestSession",
    "memorized",
    "get_cache_statistics",
    "invalidate_all_caches"
]