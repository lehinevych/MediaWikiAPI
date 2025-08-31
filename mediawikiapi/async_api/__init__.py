"""
Async API module containing asynchronous implementations of MediaWikiAPI.

This module provides asynchronous implementations of the MediaWikiAPI
classes using aiohttp and async/await syntax.
"""

from .async_util import async_memorized
from .async_wikipediapage import AsyncWikipediaPage
from .async_requestsession import AsyncRequestSession
from .async_mediawikiapi import AsyncMediaWikiAPI

# We import these after AsyncMediaWikiAPI to avoid circular imports
from .async_cache_util import get_cache_statistics, invalidate_all_caches

__all__ = [
    "AsyncMediaWikiAPI",
    "AsyncWikipediaPage",
    "AsyncRequestSession",
    "async_memorized",
    "get_cache_statistics",
    "invalidate_all_caches",
]
