"""
Base module containing abstract base classes for MediaWikiAPI.

This module provides the foundation classes that both synchronous
and asynchronous implementations extend.
"""

from .base_mediawikiapi import BaseMediaWikiAPI
from .base_wikipediapage import BaseWikipediaPage
from .base_requestsession import BaseRequestSession

__all__ = ["BaseMediaWikiAPI", "BaseWikipediaPage", "BaseRequestSession"]
