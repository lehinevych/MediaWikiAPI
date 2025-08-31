.. _retry_mechanisms_tutorial:

Retry Mechanisms
==============

Introduction
-----------

Network requests can fail for various reasons: temporary server issues, network glitches, rate limiting, or high load. MediaWikiAPI includes built-in retry mechanisms that automatically attempt to recover from transient errors, making your applications more robust with minimal effort.

This tutorial explains how the retry system works and how to configure it for your needs.

Understanding the Retry System
----------------------------

MediaWikiAPI's retry system automatically retries failed requests based on:

1. The type of error (some errors are retryable, others are not)
2. The HTTP status code (certain status codes indicate temporary issues)
3. The number of attempts already made
4. Your configured retry settings

By default, the system uses exponential backoff with jitter, which means each retry waits progressively longer with a small random factor added to prevent multiple clients from retrying simultaneously.

Default Retry Behavior
--------------------

By default, MediaWikiAPI is configured with these retry settings:

* Maximum retries: 3 attempts
* Backoff factor: 0.5 seconds (base delay)
* Maximum backoff: 60 seconds
* Retryable status codes: 429, 500, 502, 503, 504

This means the system will retry up to 3 times with these delays:

1. First retry: ~0.5 seconds (plus jitter)
2. Second retry: ~1 second (plus jitter)
3. Third retry: ~2 seconds (plus jitter)

Configuring Retry Settings
------------------------

You can customize the retry behavior through the `Config` class:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Custom retry configuration
    config = Config(
        max_retries=5,                  # Maximum number of retry attempts
        retry_backoff_factor=1.0,       # Base delay in seconds
        retry_backoff_max=120,          # Maximum delay in seconds
        retry_status_codes={429, 503},  # HTTP status codes to retry
    )

    # Create API with custom retry settings
    mediawiki = MediaWikiAPI(config=config)

    # Now use the API as normal
    # Failed requests will be retried according to your configuration
    page = mediawiki.page("Python (programming language)")

Retry Strategies
--------------

MediaWikiAPI provides predefined retry strategies for common scenarios:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # No retries at all
    no_retry_config = Config(retry_strategy=Config.RetryStrategy.NONE)
    
    # Default retry strategy
    default_retry_config = Config(retry_strategy=Config.RetryStrategy.DEFAULT)
    
    # Aggressive retry strategy (more retries, shorter initial delay, more status codes)
    aggressive_retry_config = Config(retry_strategy=Config.RetryStrategy.AGGRESSIVE)
    
    # Create API instances with different strategies
    no_retry_api = MediaWikiAPI(config=no_retry_config)
    default_retry_api = MediaWikiAPI(config=default_retry_config)
    aggressive_retry_api = MediaWikiAPI(config=aggressive_retry_config)

The predefined strategies set these values:

1. **NONE**: No retries (`max_retries=0`)
2. **DEFAULT**: Standard settings (`max_retries=3, retry_backoff_factor=0.5, retry_backoff_max=60`)
3. **AGGRESSIVE**: More aggressive retries (`max_retries=5, retry_backoff_factor=0.3, retry_backoff_max=120`)

When to Use Each Strategy
-----------------------

Choose your retry strategy based on the context:

* **NONE**: When immediate failure is preferred, or you're handling retries manually
* **DEFAULT**: For most applications and general API usage
* **AGGRESSIVE**: For critical operations where success is more important than speed

Understanding Backoff and Jitter
------------------------------

The retry system uses exponential backoff with jitter:

1. **Exponential backoff**: Each retry waits longer than the previous one
   * Wait time = `retry_backoff_factor * (2 ^ attempt)`
   * Example: With factor=0.5, waits are ~0.5s, ~1s, ~2s, ~4s...

2. **Jitter**: A small random variation (±10%) is added to prevent "thundering herd" problems
   * When multiple clients retry at once, jitter spreads them out

Here's how backoff is calculated:

.. code-block:: python

    def calculate_backoff(config, attempt):
        """Calculate retry backoff time in seconds."""
        # Exponential backoff: factor * 2^attempt
        backoff = config.retry_backoff_factor * (2 ** attempt)
        
        # Cap at maximum backoff
        backoff = min(backoff, config.retry_backoff_max)
        
        # Add jitter (±10%)
        jitter_factor = random.uniform(0.9, 1.1)
        backoff = backoff * jitter_factor
        
        return backoff

Retryable Errors and Status Codes
-------------------------------

Not all errors are retryable. By default, MediaWikiAPI retries:

1. **Network errors**: Connection errors, DNS failures, etc.
2. **HTTP timeouts**: When the server doesn't respond in time
3. **Rate limiting**: Status code 429 (Too Many Requests)
4. **Server errors**: Status codes 500, 502, 503, 504

You can customize which HTTP status codes trigger retries:

.. code-block:: python

    # Custom status codes to retry
    config = Config(
        retry_status_codes={
            408,  # Request Timeout
            429,  # Too Many Requests
            500,  # Internal Server Error
            502,  # Bad Gateway
            503,  # Service Unavailable
            504,  # Gateway Timeout
            520,  # Cloudflare Unknown Error
            521,  # Cloudflare Web Server Down
            522,  # Cloudflare Connection Timeout
        }
    )

Monitoring Retries
----------------

MediaWikiAPI doesn't provide built-in retry monitoring, but you can implement simple logging:

.. code-block:: python

    import logging
    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config
    from mediawikiapi.exceptions import NetworkError, HTTPTimeoutError

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("mediawikiapi_retry")

    # Create a retry count tracker
    retry_counts = {}

    # Custom retry handler function
    def log_retry(attempt, error, next_wait):
        operation = "unknown"
        if hasattr(error, "context") and error.context and "url" in error.context:
            operation = error.context["url"]
        
        retry_counts[operation] = retry_counts.get(operation, 0) + 1
        
        logger.warning(
            f"Retry {attempt} for {operation}: {type(error).__name__} - "
            f"Waiting {next_wait:.2f}s before next attempt"
        )

    # Create API with custom config that does retries
    config = Config(max_retries=3)
    mediawiki = MediaWikiAPI(config=config)

    # Monkey patch the internal _calculate_retry_wait method to log retries
    original_should_retry = config.should_retry
    def should_retry_with_logging(attempt, status_code=None):
        should = original_should_retry(attempt, status_code)
        if should:
            logger.info(f"Will retry attempt {attempt} with status {status_code}")
        return should
    config.should_retry = should_retry_with_logging

    # Use the API (example with potential errors)
    try:
        # Use the API...
        page = mediawiki.page("Python (programming language)")
    except Exception as e:
        logger.error(f"Final error after retries: {e}")

    # Print retry statistics
    logger.info(f"Retry counts: {retry_counts}")

Async Retry Behavior
-----------------

The asynchronous API (`AsyncMediaWikiAPI`) uses the same retry configuration but implements the waiting with `asyncio.sleep()` instead of blocking:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.config import Config

    async def main():
        # Configure retry settings
        config = Config(
            max_retries=3,
            retry_backoff_factor=1.0,
        )
        
        # Create async API with retry settings
        async_api = AsyncMediaWikiAPI(config=config)
        
        try:
            # Use the API
            page = await async_api.page("Python (programming language)")
            print(f"Retrieved page: {page.title}")
        finally:
            # Always close the session
            await async_api.close()

    # Run the async code
    asyncio.run(main())

Implementing Custom Retry Logic
-----------------------------

For advanced scenarios, you might want to implement custom retry logic on top of MediaWikiAPI's built-in mechanisms:

.. code-block:: python

    import time
    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import MediaWikiAPIException, HTTPTimeoutError

    class RetryHandler:
        def __init__(self, max_attempts=5, base_delay=1.0):
            self.mediawiki = MediaWikiAPI()
            self.max_attempts = max_attempts
            self.base_delay = base_delay
            
        def calculate_wait_time(self, attempt):
            """Calculate wait time with exponential backoff."""
            return self.base_delay * (2 ** attempt)
            
        def with_retry(self, operation, *args, **kwargs):
            """Execute an operation with retries."""
            attempt = 0
            last_exception = None
            
            while attempt < self.max_attempts:
                try:
                    # Try the operation
                    return operation(*args, **kwargs)
                    
                except HTTPTimeoutError as e:
                    # Always retry timeouts
                    last_exception = e
                    attempt += 1
                    
                    if attempt < self.max_attempts:
                        wait_time = self.calculate_wait_time(attempt - 1)
                        print(f"Timeout error, retrying in {wait_time:.1f}s ({attempt}/{self.max_attempts})")
                        time.sleep(wait_time)
                    
                except MediaWikiAPIException as e:
                    # For other API errors, don't retry
                    raise e
                    
            # If we get here, we've exhausted all retries
            raise last_exception or RuntimeError("All retry attempts failed")
            
        def get_page(self, title):
            """Get a page with retries."""
            return self.with_retry(self.mediawiki.page, title)
            
        def search(self, query, results=10):
            """Search with retries."""
            return self.with_retry(self.mediawiki.search, query, results=results)

    # Usage
    retry_handler = RetryHandler(max_attempts=3)
    try:
        page = retry_handler.get_page("Python (programming language)")
        print(f"Retrieved page: {page.title}")
    except Exception as e:
        print(f"All retries failed: {e}")

Combining Retries with Caching
----------------------------

When combining retries with caching, consider:

1. **Cache before retrying**: Use cached data to avoid unnecessary retries
2. **Don't cache errors**: Avoid caching failed responses
3. **Consider stale-while-revalidate**: Use stale data while refreshing in the background

Here's an example combining caching and retries:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config
    from mediawikiapi.exceptions import MediaWikiAPIException

    # Configure with both caching and retries
    config = Config(
        # Caching settings
        cache_ttl=3600,           # 1 hour cache
        cache_max_size=1000,      # Limit to 1000 items
        
        # Retry settings
        max_retries=3,
        retry_backoff_factor=1.0,
    )

    mediawiki = MediaWikiAPI(config=config)

    def get_content_safely(title):
        try:
            # First try the regular API call (will use cache if available)
            page = mediawiki.page(title)
            return page.content
        except MediaWikiAPIException as e:
            print(f"Error retrieving {title}: {e}")
            
            # If we have a cached version, use it despite the error
            # (not built into MediaWikiAPI, this is just an example approach)
            if mediawiki.invalidate_cache("page", title):
                print(f"Invalidated cache for {title}, will refresh next time")
            
            # Return None on error
            return None

    # Use the function
    content = get_content_safely("Python (programming language)")
    if content:
        print(f"Content length: {len(content)} characters")
    else:
        print("Could not retrieve content")

Best Practices for Retry Configuration
-----------------------------------

1. **Balance retry count and delay**: More retries provide reliability but add latency
2. **Consider the operation context**: Critical operations may need more retries
3. **Be respectful to the server**: Don't set aggressive retries for non-critical operations
4. **Add jitter**: Always use jitter to prevent synchronized retries
5. **Implement circuit breakers**: Consider stopping retries if persistent failures occur
6. **Log retry attempts**: Monitor retry patterns to identify systematic issues

Next Steps
---------

Now that you understand MediaWikiAPI's retry mechanisms, you can:

1. Learn about error context and handling in :ref:`error_context_tutorial`
2. Explore best practices for error recovery in :ref:`error_recovery_tutorial`
3. Check the complete API reference in :ref:`api`