.. _error_handling_tutorial:

Error Handling and Retries
=========================

Introduction
-----------

When working with MediaWikiAPI, you'll need to handle various errors that can occur during API interactions. This tutorial will help you understand the exception hierarchy, implement proper error handling, and configure retry mechanisms to build more robust applications.

Exception Hierarchy
-----------------

MediaWikiAPI provides a comprehensive hierarchy of exceptions to help you handle different types of errors gracefully. Here's an overview of the main exception types:

.. code-block:: text

    MediaWikiAPIException (base exception)
    ├── HTTPTimeoutError (timeout during HTTP request)
    ├── PageError (page doesn't exist)
    ├── RedirectError (page is a redirect)
    ├── DisambiguationError (page is a disambiguation page)
    ├── OddError (unexpected response from API)
    ├── NetworkError (general network issues)
    │   ├── RateLimitError (hit API rate limits)
    │   └── AccessDeniedError (access forbidden)
    └── CacheError (issues with caching)

All exceptions derive from ``MediaWikiAPIException``, which allows you to catch all MediaWikiAPI errors with a single exception handler if needed.

Exception Types in Detail
-----------------------

Let's look at each exception type and how to handle it:

MediaWikiAPIException
~~~~~~~~~~~~~~~~~~~

This is the base exception for all MediaWikiAPI errors:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import MediaWikiAPIException

    mediawiki = MediaWikiAPI()

    try:
        # Any MediaWikiAPI operation
        page = mediawiki.page("Example")
    except MediaWikiAPIException as e:
        print(f"An error occurred: {e}")

HTTPTimeoutError
~~~~~~~~~~~~~~

Raised when an HTTP request times out:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import HTTPTimeoutError
    from mediawikiapi.config import Config

    # Configure with a very short timeout to demonstrate
    config = Config(timeout=0.1)  # 100ms timeout
    mediawiki = MediaWikiAPI(config=config)

    try:
        page = mediawiki.page("Python (programming language)")
    except HTTPTimeoutError as e:
        print(f"Request timed out: {e}")
        print(f"Timeout setting: {e.timeout} seconds")

PageError
~~~~~~~~

Raised when trying to access a non-existent page:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import PageError

    mediawiki = MediaWikiAPI()

    try:
        page = mediawiki.page("This Page Definitely Does Not Exist XYZ123")
    except PageError as e:
        print(f"Page not found: {e}")
        print(f"Requested title: {e.title}")

RedirectError
~~~~~~~~~~~

Raised when a page is a redirect, if automatic redirection is disabled:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import RedirectError

    mediawiki = MediaWikiAPI()

    try:
        # By default, redirects are followed automatically
        # Let's disable redirect following to see the RedirectError
        page = mediawiki.page("Python Programming Language", redirect=False)
    except RedirectError as e:
        print(f"Redirect detected: {e}")
        # We can access the target page
        print(f"Redirects to: {e.redirects_to}")
        
        # Handle the redirect manually if desired
        target_page = mediawiki.page(e.redirects_to)
        print(f"Target page title: {target_page.title}")

DisambiguationError
~~~~~~~~~~~~~~~~~

Raised when a page is a disambiguation page (has multiple interpretations):

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import DisambiguationError

    mediawiki = MediaWikiAPI()

    try:
        # "Python" is a disambiguation page
        page = mediawiki.page("Python")
    except DisambiguationError as e:
        print(f"Disambiguation page found: {e}")
        print("Options available:")
        for option in e.options:
            print(f"  - {option}")
        
        # Automatically select the first option
        if e.options:
            selected_page = mediawiki.page(e.options[0])
            print(f"Selected: {selected_page.title}")

NetworkError
~~~~~~~~~~

Base exception for network-related errors:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import NetworkError
    from mediawikiapi.config import Config

    # Point to an invalid URL to trigger a network error
    config = Config(mediawiki_url="https://invalid.example.com/api.php")
    mediawiki = MediaWikiAPI(config=config)

    try:
        results = mediawiki.search("test")
    except NetworkError as e:
        print(f"Network error: {e}")
        if e.original_exception:
            print(f"Original exception: {type(e.original_exception).__name__}")

RateLimitError
~~~~~~~~~~~~

Raised when you've hit MediaWiki's rate limits:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import RateLimitError
    
    mediawiki = MediaWikiAPI()
    
    try:
        # This is just an example; you'd need to actually trigger a rate limit
        # by making many requests in quick succession
        # Simulated error handling:
        raise RateLimitError("Rate limit exceeded")
    except RateLimitError as e:
        print(f"Rate limit error: {e}")
        print("Waiting before retrying...")
        import time
        time.sleep(5)  # Wait 5 seconds before retrying
        print("Retrying now...")

AccessDeniedError
~~~~~~~~~~~~~~~

Raised when access to a resource is forbidden:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import AccessDeniedError
    
    mediawiki = MediaWikiAPI()
    
    try:
        # This is just an example; you'd need to actually trigger an access denied error
        # Simulated error handling:
        raise AccessDeniedError("Access denied to protected page")
    except AccessDeniedError as e:
        print(f"Access denied: {e}")
        print("This operation requires authentication.")

Combining Exception Handlers
--------------------------

For more detailed error handling, you can catch specific exceptions in order from most specific to most general:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import (
        PageError,
        DisambiguationError,
        RedirectError,
        HTTPTimeoutError,
        NetworkError,
        MediaWikiAPIException,
    )

    mediawiki = MediaWikiAPI()

    def get_page_safely(title):
        try:
            return mediawiki.page(title)
        except PageError:
            print(f"The page '{title}' does not exist.")
        except DisambiguationError as e:
            print(f"'{title}' is ambiguous. Options: {e.options[:3]}...")
            # Choose the first option
            if e.options:
                print(f"Selecting first option: {e.options[0]}")
                return mediawiki.page(e.options[0])
        except RedirectError as e:
            print(f"'{title}' redirects to '{e.redirects_to}'")
            return mediawiki.page(e.redirects_to)
        except HTTPTimeoutError:
            print(f"Request for '{title}' timed out. Try again later.")
        except NetworkError as e:
            print(f"Network error while accessing '{title}': {e}")
        except MediaWikiAPIException as e:
            print(f"General API error for '{title}': {e}")
        return None

    # Try with different cases
    pages_to_try = [
        "Python (programming language)",  # Regular page
        "This Does Not Exist XYZ123",     # Non-existent page
        "Python",                         # Disambiguation page
        "Python Programming Language",    # Redirect
    ]

    for title in pages_to_try:
        print(f"\nTrying: {title}")
        page = get_page_safely(title)
        if page:
            print(f"Retrieved page: {page.title} ({len(page.content)} chars)")
        else:
            print("Failed to retrieve page")

Exception Handling with Async API
-------------------------------

Error handling with the asynchronous API follows the same patterns but requires ``async/await``:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.exceptions import (
        PageError,
        DisambiguationError,
        MediaWikiAPIException
    )

    async def main():
        async_api = AsyncMediaWikiAPI()
        
        try:
            # Try to retrieve some pages
            tasks = [
                get_page_safely(async_api, "Python (programming language)"),
                get_page_safely(async_api, "This Does Not Exist XYZ123"),
                get_page_safely(async_api, "Python"),
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Task {i} failed with: {result}")
                elif result:
                    print(f"Task {i} succeeded: {result.get('title')}")
                else:
                    print(f"Task {i} returned None")
            
        finally:
            await async_api.close()
    
    async def get_page_safely(api, title):
        try:
            page = await api.page(title)
            content = await page.content
            return {"title": await page.title, "content_length": len(content)}
        except PageError:
            print(f"The page '{title}' does not exist.")
        except DisambiguationError as e:
            print(f"'{title}' is ambiguous. Options: {e.options[:3]}...")
        except MediaWikiAPIException as e:
            print(f"API error for '{title}': {e}")
        return None

    asyncio.run(main())

Additional Error Properties
-------------------------

MediaWikiAPI's exceptions include additional properties that can provide more context about the error:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import NetworkError, PageError

    mediawiki = MediaWikiAPI()

    try:
        # This is just an example to show properties
        raise NetworkError(
            "Connection error",
            original_exception=ValueError("Example"),
            context={"url": "https://example.org", "status_code": 500}
        )
    except NetworkError as e:
        print(f"Error message: {str(e)}")
        print(f"Original exception: {type(e.original_exception).__name__}")
        print(f"Context: {e.context}")

    try:
        # Another example with PageError
        page = mediawiki.page("This Page Does Not Exist XYZ123")
    except PageError as e:
        print(f"Error message: {str(e)}")
        print(f"Page title: {e.title}")
        print(f"Page ID: {e.pageid}")

Creating Your Own Error Handling System
-------------------------------------

For large applications, consider creating a dedicated error handling system:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import (
        MediaWikiAPIException, PageError, DisambiguationError, 
        NetworkError, HTTPTimeoutError
    )

    class WikiErrorHandler:
        def __init__(self, log_function=print):
            self.log_function = log_function
            self.mediawiki = MediaWikiAPI()
            
        def log_error(self, message):
            """Log an error message"""
            self.log_function(f"ERROR: {message}")
            
        def get_page(self, title, max_retries=3):
            """Get a page with error handling and retries"""
            retries = 0
            while retries <= max_retries:
                try:
                    return self.mediawiki.page(title)
                    
                except PageError:
                    self.log_error(f"Page '{title}' does not exist.")
                    return None
                    
                except DisambiguationError as e:
                    self.log_error(f"'{title}' is ambiguous. Options: {e.options[:3]}...")
                    # Choose the first option
                    if e.options:
                        new_title = e.options[0]
                        self.log_error(f"Selecting first option: {new_title}")
                        return self.mediawiki.page(new_title)
                    return None
                    
                except HTTPTimeoutError:
                    retries += 1
                    if retries <= max_retries:
                        wait_time = 2 ** retries  # Exponential backoff: 2, 4, 8 seconds
                        self.log_error(f"Timeout error. Retry {retries}/{max_retries} in {wait_time}s")
                        import time
                        time.sleep(wait_time)
                    else:
                        self.log_error(f"Max retries reached for '{title}'")
                        return None
                    
                except NetworkError as e:
                    self.log_error(f"Network error: {e}")
                    return None
                    
                except MediaWikiAPIException as e:
                    self.log_error(f"API error: {e}")
                    return None
                    
        def search_safely(self, query, results=10):
            """Perform a search with error handling"""
            try:
                return self.mediawiki.search(query, results=results)
            except MediaWikiAPIException as e:
                self.log_error(f"Search error for '{query}': {e}")
                return []

    # Usage
    handler = WikiErrorHandler()
    page = handler.get_page("Python (programming language)")
    if page:
        print(f"Got page: {page.title}")
    
    search_results = handler.search_safely("artificial intelligence")
    print(f"Search results: {search_results[:3]}...")

Next Steps
---------

Now that you understand the exception types in MediaWikiAPI, you can:

1. Learn about retry mechanisms in :ref:`retry_mechanisms_tutorial`
2. See how to use error context in :ref:`error_context_tutorial`
3. Explore best practices for error recovery in :ref:`error_recovery_tutorial`
4. See the complete API reference for exceptions in :ref:`api`