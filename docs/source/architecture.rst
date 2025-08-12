Architecture
============

MediaWikiAPI employs a clean architecture that separates concerns and reduces code duplication between synchronous and asynchronous implementations.

Module Structure
--------------

The library is organized into the following modules:

- ``mediawikiapi.base``: Contains abstract base classes that define common interfaces
- ``mediawikiapi.sync``: Contains synchronous implementations using the ``requests`` library
- ``mediawikiapi.async_api``: Contains asynchronous implementations using ``aiohttp`` and ``async/await`` syntax
- ``mediawikiapi.common``: Contains shared utilities for validation and error handling

Base Classes
-----------

The core of the architecture revolves around three key abstract base classes, located in the ``mediawikiapi.base`` module:

.. code-block:: python

   BaseMediaWikiAPI
   ├── MediaWikiAPI
   └── AsyncMediaWikiAPI

   BaseWikipediaPage
   ├── WikipediaPage
   └── AsyncWikipediaPage

   BaseRequestSession
   ├── RequestSession
   └── AsyncRequestSession

These base classes provide common interfaces and implementations, which are then specialized by the synchronous and asynchronous concrete classes.

BaseMediaWikiAPI
~~~~~~~~~~~~~~~

``BaseMediaWikiAPI`` defines the core API interface with generic type parameters for:

- The page class type (``WikipediaPage`` or ``AsyncWikipediaPage``)
- The return type from request methods (direct ``Dict`` or ``Coroutine``)

It implements common functionality like:

- Helper methods for parameter preparation
- Response processing and error handling
- Cache invalidation

BaseWikipediaPage
~~~~~~~~~~~~~~~~

``BaseWikipediaPage`` defines the interface for Wikipedia page objects with:

- Common properties like title, content, images, etc.
- Methods for extracting sections
- Helper methods for building query parameters

BaseRequestSession
~~~~~~~~~~~~~~~~

``BaseRequestSession`` defines the interface for making HTTP requests to the MediaWiki API with:

- Methods for building API URLs
- Parameter preparation
- User-agent handling

Common Utilities Module
--------------------

The ``mediawikiapi.common`` module contains shared functionality used by both synchronous and asynchronous implementations:

mediawikiapi.common.validation
^^^^^^^^^^^^^^^^^^^^^^^^

Contains parameter validation functions used by both synchronous and asynchronous implementations:

- ``validate_title_or_pageid``
- ``validate_geosearch_params``
- ``validate_search_params``
- ``validate_limit``
- and more

mediawikiapi.common.error_handling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contains error handling and response processing functions:

- ``handle_api_error``
- ``handle_page_error``
- ``handle_redirect``
- ``process_search_results``
- ``process_geosearch_results``
- and more

Exception Handling
----------------

The library uses a hierarchy of exception classes:

.. code-block:: python

   MediaWikiAPIException
   ├── PageError
   ├── LanguageError
   ├── RedirectError
   └── HTTPTimeoutError

Synchronous vs. Asynchronous Modules
--------------------------------

The library provides both synchronous and asynchronous interfaces with the same functionality:

- ``mediawikiapi.sync`` module: Contains ``MediaWikiAPI``, ``WikipediaPage``, and ``RequestSession`` classes that use the ``requests`` library
- ``mediawikiapi.async_api`` module: Contains ``AsyncMediaWikiAPI``, ``AsyncWikipediaPage``, and ``AsyncRequestSession`` classes that use ``aiohttp`` with ``async/await`` syntax

Example Usage
-----------

Synchronous:

.. code-block:: python

   from mediawikiapi import MediaWikiAPI

   api = MediaWikiAPI()
   results = api.search("Python programming")
   summary = api.summary("Python (programming language)")
   
   page = api.page("Python (programming language)")
   content = page.content
   references = page.references

Asynchronous:

.. code-block:: python

   import asyncio
   from mediawikiapi import AsyncMediaWikiAPI

   async def main():
       api = AsyncMediaWikiAPI()
       results = await api.search("Python programming")
       summary = await api.summary("Python (programming language)")
       
       page = await api.page("Python (programming language)")
       content = await page.content
       references = await page.references
       
       await api.close()  # Close the session when done

   asyncio.run(main())