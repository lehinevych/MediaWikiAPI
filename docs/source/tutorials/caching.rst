.. _caching_tutorial:

Caching and Memoization Tutorial
==============================

MediaWikiAPI includes a powerful caching system that can significantly improve performance by reducing redundant API calls. This tutorial explains how the caching system works and how to configure it to optimize your application.

Understanding MediaWikiAPI's Caching
----------------------------------

MediaWikiAPI uses memoization to cache API call results in memory. When you make an API call that you've made before with the same parameters, the library will return the cached result instead of making a new request to the MediaWiki server.

Benefits of caching include:

* **Reduced latency**: Cached responses return almost instantly
* **Lower bandwidth usage**: Fewer HTTP requests to the MediaWiki servers
* **Reduced server load**: Beneficial for both your application and the wiki servers
* **Improved reliability**: Can work even during temporary network issues (using stale data)

How Memoization Works
-------------------

The library uses function decorators (``@memorized`` for synchronous methods and ``@async_memorized`` for async methods) to cache the results based on:

1. The method name
2. The method arguments
3. The instance's configuration (e.g., language settings)

This ensures that cached results are only used when the exact same request is made.

Default Caching Behavior
----------------------

By default, MediaWikiAPI enables caching with these settings:

* No expiration (cached items remain valid indefinitely)
* No limit on cache size (will continue to grow as new requests are made)
* In-memory storage (cache is lost when the program terminates)

Basic Caching Configuration
-------------------------

You can configure caching behavior through the ``Config`` class:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Create a configuration with custom cache settings
    config = Config(
        # Cache expires after 1 hour (3600 seconds)
        cache_ttl=3600,
        
        # Limit cache to 1000 items
        cache_max_size=1000
    )

    # Create API instance with this configuration
    mediawiki = MediaWikiAPI(config=config)

    # Use the API as normal
    # Results will be cached according to the configuration
    page = mediawiki.page("Python (programming language)")
    summary = mediawiki.summary("Python (programming language)")

Cache Expiration
--------------

Setting a cache TTL (time-to-live) ensures that your application doesn't use stale data:

.. code-block:: python

    # Cache that expires after 10 minutes
    config = Config(cache_ttl=600)  # 600 seconds = 10 minutes
    
    # Cache that expires after 1 day
    config = Config(cache_ttl=86400)  # 86400 seconds = 24 hours
    
    # No expiration (default)
    config = Config(cache_ttl=None)

When an item's TTL expires, the next request will fetch fresh data from the MediaWiki server.

Cache Size Limits
---------------

To prevent memory leaks in long-running applications, you can limit the cache size:

.. code-block:: python

    # Limit cache to 100 items
    config = Config(cache_max_size=100)
    
    # Limit cache to 10,000 items
    config = Config(cache_max_size=10000)
    
    # No size limit (default)
    config = Config(cache_max_size=None)

When the cache reaches its size limit, the least recently used items are removed to make space for new items.

Disabling Caching
---------------

For certain scenarios, you might want to disable caching entirely:

.. code-block:: python

    # Disable caching by setting TTL to 0
    config = Config(cache_ttl=0)
    mediawiki = MediaWikiAPI(config=config)

    # Every call will now make a fresh request
    page = mediawiki.page("Python (programming language)")

Manual Cache Invalidation
-----------------------

MediaWikiAPI allows you to manually invalidate cache entries when needed:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()

    # Make an initial request (this will be cached)
    results = mediawiki.search("Python")
    print(f"Found {len(results)} results")

    # Invalidate the cache for a specific method call
    mediawiki.invalidate_cache("search", "Python")

    # This will now make a fresh request
    results = mediawiki.search("Python")
    print(f"Found {len(results)} results after cache invalidation")

    # Invalidate all cached calls to a method
    invalidated_count = mediawiki.invalidate_all_method_cache("search")
    print(f"Invalidated {invalidated_count} cached search results")

    # Invalidate all caches across all methods
    cache_stats = mediawiki.invalidate_all_caches()
    print(f"Invalidated caches: {cache_stats}")

Monitoring Cache Usage
--------------------

To understand how the cache is being used, you can get cache statistics:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()

    # Make some requests
    mediawiki.search("Python")
    mediawiki.search("JavaScript")
    mediawiki.page("Python (programming language)")
    mediawiki.summary("JavaScript")

    # Get cache statistics
    cache_stats = mediawiki.get_cache_statistics()
    print("Cache statistics:")
    for method_name, entry_count in cache_stats.items():
        print(f"  {method_name}: {entry_count} entries")

Caching with Async API
--------------------

The asynchronous API has the same caching capabilities as the synchronous API:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.config import Config

    async def main():
        # Configure caching for async API
        config = Config(
            cache_ttl=3600,       # 1 hour TTL
            cache_max_size=500    # Limit to 500 entries
        )
        
        async with AsyncMediaWikiAPI(config=config) as api:
            # First request will hit the network
            results1 = await api.search("Python")
            print(f"First request found {len(results1)} results")
            
            # Second identical request will use cache
            results2 = await api.search("Python")
            print(f"Second request found {len(results2)} results (from cache)")
            
            # Get cache statistics
            cache_stats = api.get_cache_statistics()
            print(f"Cache statistics: {cache_stats}")
            
            # Invalidate specific cache entry
            api.invalidate_cache("search", "Python")
            
            # This will hit the network again
            results3 = await api.search("Python")
            print(f"Third request found {len(results3)} results (after invalidation)")

    asyncio.run(main())

Optimizing Cache Configuration
----------------------------

Finding the right cache configuration depends on your specific use case:

1. **Long-lived data**: For data that rarely changes (historical information, etc.):
   - Longer TTLs (hours or days)
   - Larger cache size
   
   ```python
   config = Config(cache_ttl=86400, cache_max_size=10000)  # 1 day TTL, 10K items
   ```

2. **Frequently changing data**: For data that updates often:
   - Shorter TTLs (minutes)
   - Smaller cache size
   
   ```python
   config = Config(cache_ttl=300, cache_max_size=100)  # 5 minute TTL, 100 items
   ```

3. **Memory-constrained environments**: For limited memory scenarios:
   - Smaller cache size
   - Consider disabling caching for large responses
   
   ```python
   config = Config(cache_max_size=50)  # Only 50 items maximum
   ```

4. **High-throughput applications**:
   - Larger cache size
   - Moderate TTL
   
   ```python
   config = Config(cache_ttl=1800, cache_max_size=5000)  # 30 minute TTL, 5K items
   ```

Performance Comparison Example
----------------------------

Here's a simple benchmark demonstrating the performance benefits of caching:

.. code-block:: python

    import time
    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Function to measure execution time
    def time_execution(func):
        start = time.time()
        result = func()
        end = time.time()
        return result, end - start

    # Create API with caching enabled
    cached_api = MediaWikiAPI(config=Config(cache_ttl=None))

    # Create API with caching disabled
    uncached_api = MediaWikiAPI(config=Config(cache_ttl=0))

    # Test with caching disabled (first run)
    _, uncached_time_first = time_execution(
        lambda: uncached_api.page("Python (programming language)")
    )
    print(f"Uncached (first request): {uncached_time_first:.4f} seconds")

    # Test with caching disabled (second run)
    _, uncached_time_second = time_execution(
        lambda: uncached_api.page("Python (programming language)")
    )
    print(f"Uncached (second request): {uncached_time_second:.4f} seconds")

    # Test with caching enabled (first run - will populate cache)
    _, cached_time_first = time_execution(
        lambda: cached_api.page("Python (programming language)")
    )
    print(f"Cached (first request): {cached_time_first:.4f} seconds")

    # Test with caching enabled (second run - should use cache)
    _, cached_time_second = time_execution(
        lambda: cached_api.page("Python (programming language)")
    )
    print(f"Cached (second request): {cached_time_second:.4f} seconds")

    # Calculate speedup
    speedup = uncached_time_second / cached_time_second
    print(f"Caching speedup: {speedup:.2f}x faster")

    # Test with multiple requests
    search_terms = ["Python", "JavaScript", "TypeScript", "Ruby", "Go"]
    
    # Uncached multiple requests
    _, uncached_multi_time = time_execution(
        lambda: [uncached_api.search(term) for term in search_terms]
    )
    print(f"Uncached (multiple requests): {uncached_multi_time:.4f} seconds")
    
    # Cached multiple requests (first time)
    _, cached_multi_time_first = time_execution(
        lambda: [cached_api.search(term) for term in search_terms]
    )
    print(f"Cached (multiple requests, first time): {cached_multi_time_first:.4f} seconds")
    
    # Cached multiple requests (second time, should use cache)
    _, cached_multi_time_second = time_execution(
        lambda: [cached_api.search(term) for term in search_terms]
    )
    print(f"Cached (multiple requests, second time): {cached_multi_time_second:.4f} seconds")
    
    # Calculate multi-request speedup
    multi_speedup = uncached_multi_time / cached_multi_time_second
    print(f"Multi-request caching speedup: {multi_speedup:.2f}x faster")

Best Practices
------------

1. **Balance TTL with data freshness**: Set TTL based on how frequently the data changes.

2. **Set appropriate cache size limits**: Consider your application's memory constraints.

3. **Invalidate selectively**: When you need fresh data, invalidate only the necessary cache entries.

4. **Monitor cache statistics**: Watch how the cache grows and adjust settings if needed.

5. **Consider different configs for different API instances**: You might want different caching behavior for different parts of your application.

   ```python
   # For relatively static content
   stable_config = Config(cache_ttl=3600)  # 1 hour
   stable_api = MediaWikiAPI(config=stable_config)
   
   # For frequently changing content
   dynamic_config = Config(cache_ttl=300)  # 5 minutes
   dynamic_api = MediaWikiAPI(config=dynamic_config)
   ```

6. **Use in-memory caching for short-lived processes**: The default in-memory cache works well for scripts or short-lived applications.

Next Steps
---------

Now that you understand MediaWikiAPI's caching system, you might want to explore:

- :ref:`error_handling_tutorial` to learn how caching interacts with error handling and retries
- :ref:`performance_best_practices` for overall performance optimization tips
- :ref:`api` for detailed API documentation of cache-related methods