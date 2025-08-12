Error Handling and Retry Mechanisms
================================

MediaWikiAPI provides a comprehensive error handling system to manage various types of errors that can occur during API interactions, including transient network issues, server errors, and rate limiting.

Exception Types
--------------

MediaWikiAPI defines a hierarchy of exception types to represent different error scenarios:

.. code-block:: python

    MediaWikiAPIException  # Base exception class
    ├── PageError          # When a requested page doesn't exist
    ├── RedirectError      # When a page is a redirect but redirects aren't allowed
    ├── LanguageError      # When an unavailable language is requested
    ├── HTTPTimeoutError   # When an API request times out
    ├── RateLimitError     # When the MediaWiki API rate limit is exceeded
    ├── AccessDeniedError  # When access to the API is denied
    ├── InvalidParameterError  # When an invalid parameter is provided
    ├── ServerError        # When a server error occurs
    └── NetworkError       # For other network-related errors

These exceptions provide context-rich error messages that include specific details about what went wrong, making debugging easier.

Context Information
-----------------

All exceptions include contextual information that can help diagnose the issue:

.. code-block:: python

    try:
        wikipedia = MediaWikiAPI()
        page = wikipedia.page("Nonexistent page title")
    except PageError as e:
        print(f"Error message: {e}")
        print(f"Error context: {e.context}")  # Contains detailed context information

The context can include:

* Original query parameters
* HTTP status codes
* Error codes from the MediaWiki API
* Information about retry attempts
* URLs that were accessed
* And more

Retry Mechanisms
--------------

MediaWikiAPI includes configurable retry mechanisms for transient errors:

Configuration
~~~~~~~~~~~~

You can configure retry behavior when creating a MediaWikiAPI instance:

.. code-block:: python

    # Default retry configuration
    wikipedia = MediaWikiAPI(
        max_retries=3,                        # Maximum number of retry attempts
        retry_backoff_factor=0.5,             # Exponential backoff factor in seconds
        retry_backoff_max=60,                 # Maximum backoff time in seconds
        retry_status_codes={429, 500, 502, 503, 504}  # HTTP status codes to retry
    )

    # Disable retries entirely
    wikipedia = MediaWikiAPI(retry_strategy=Config.RetryStrategy.NONE)

    # Use aggressive retry strategy for important requests
    wikipedia = MediaWikiAPI(retry_strategy=Config.RetryStrategy.AGGRESSIVE)

Retry Strategies
~~~~~~~~~~~~~~

MediaWikiAPI provides three retry strategies:

* ``Config.RetryStrategy.DEFAULT``: Standard retry configuration for most use cases
* ``Config.RetryStrategy.NONE``: Disable retries completely
* ``Config.RetryStrategy.AGGRESSIVE``: More aggressive retry strategy with more retries, shorter initial delays, and more status codes

When using the ``AGGRESSIVE`` strategy, the system will retry on additional HTTP status codes (408, 429, 500-504, 520-524) and use more retry attempts.

Exponential Backoff
~~~~~~~~~~~~~~~~~

The retry mechanism uses exponential backoff with jitter to prevent the "thundering herd" problem. The backoff time is calculated as:

.. code-block:: python

    backoff_time = min(
        retry_backoff_max,
        retry_backoff_factor * (2 ** attempt_number)
    )

This provides progressively longer waits between retry attempts.

Asynchronous Retries
~~~~~~~~~~~~~~~~~~

Both synchronous and asynchronous API implementations include the same retry mechanisms. For the async API:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI

    async def main():
        wikipedia = AsyncMediaWikiAPI(max_retries=3)
        try:
            # This will automatically retry transient errors
            page = await wikipedia.page("Python (programming language)")
            print(page.summary)
        except Exception as e:
            print(f"Error after retries: {e}")

    asyncio.run(main())

Best Practices
------------

1. **Use appropriate retry settings for your use case**: 
   - For user-facing applications, use shorter timeouts and fewer retries
   - For batch jobs or background processes, consider more aggressive retries

2. **Handle exceptions gracefully**:
   - Catch specific exceptions when possible
   - Log the exception context for debugging

3. **Consider rate limiting**:
   - Always enable rate limiting with ``rate_limit=True`` to respect MediaWiki API guidelines
   - For batch processing, use longer rate limiting intervals

4. **Enable error logging**:
   - Log both the error message and context information for proper debugging

5. **Use aggressive retry strategy sparingly**:
   - Only use aggressive retry for critical operations
   - Avoid overloading the MediaWiki API with too many retries

Example Error Handling
--------------------

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import (
        PageError, 
        NetworkError, 
        HTTPTimeoutError,
        RateLimitError
    )

    wikipedia = MediaWikiAPI(max_retries=3)

    try:
        page = wikipedia.page("Python (programming language)")
        print(page.summary)
    except PageError as e:
        print(f"Page not found: {e}")
    except HTTPTimeoutError as e:
        print(f"Request timed out: {e}")
        print(f"Consider increasing timeout: {e.context.get('timeout')}")
    except RateLimitError as e:
        wait_time = e.context.get('retry_after', 60)
        print(f"Rate limit exceeded. Try again after {wait_time} seconds")
    except NetworkError as e:
        print(f"Network error: {e}")
        print(f"Context: {e.context}")
        if e.context.get('attempts', 0) > 1:
            print(f"Failed after {e.context['attempts']} attempts")
    except Exception as e:
        print(f"Unexpected error: {e}")