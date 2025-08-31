.. _async_api_tutorial:

Asynchronous API Tutorial
=========================

This tutorial covers the asynchronous API capabilities of MediaWikiAPI, which can significantly improve performance for applications that make multiple concurrent requests.

Introduction to Async API
------------------------

The ``AsyncMediaWikiAPI`` class provides asynchronous versions of all the methods available in the synchronous ``MediaWikiAPI`` class. Using this API requires a basic understanding of Python's asynchronous programming model with ``async/await``.

When to Use Async API
--------------------

Consider using the async API when:

* Your application needs to make multiple concurrent API requests
* You're building an application with an asynchronous framework (like FastAPI, aiohttp, or asyncio)
* You need to optimize for high throughput rather than simplicity
* You're working with other async libraries or services

Basic Setup
----------

To use the async API, you'll need to:

1. Import the ``AsyncMediaWikiAPI`` class
2. Create an instance of the class
3. Use ``async/await`` syntax with its methods
4. Properly close the session when you're done

Here's a simple example:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI

    async def main():
        # Create an instance
        api = AsyncMediaWikiAPI()
        
        try:
            # Use async methods
            results = await api.search("Python programming")
            print(results)
            
            # Get a page
            page = await api.page("Python (programming language)")
            content = await page.content  # Page properties are also awaitable
            print(f"First 100 chars: {content[:100]}...")
            
        finally:
            # Always close the session when done
            await api.close()

    # Run the async function
    asyncio.run(main())

Key Differences from Sync API
----------------------------

When using the async API, keep in mind these key differences:

1. **Method Calls**: All methods must be awaited with ``await``
2. **Page Properties**: Page properties (content, images, links, etc.) are also awaitable
3. **Session Management**: You need to explicitly close the session with ``await api.close()``
4. **Context Manager**: You can use the async context manager pattern with ``async with``
5. **Concurrency Control**: The async API provides additional concurrency control options

Using Async Context Manager
-------------------------

A cleaner way to manage the async session is with an async context manager:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI

    async def main():
        # Use the API as an async context manager
        async with AsyncMediaWikiAPI() as api:
            # The session will be automatically closed after the block
            results = await api.search("Python programming")
            print(results)
            
            page = await api.page("Python (programming language)")
            summary = await api.summary("Python (programming language)")
            print(summary[:100])

    asyncio.run(main())

Making Concurrent Requests
------------------------

One of the main advantages of the async API is the ability to make multiple concurrent requests:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI

    async def main():
        async with AsyncMediaWikiAPI() as api:
            # Create multiple search tasks
            search_terms = ["Python", "JavaScript", "TypeScript", "Rust", "Go"]
            search_tasks = [api.search(term) for term in search_terms]
            
            # Execute all searches concurrently
            search_results = await asyncio.gather(*search_tasks)
            
            # Process results
            for term, results in zip(search_terms, search_results):
                print(f"{term}: {results[:2]}...")  # Show first 2 results
            
            # Concurrent page retrieval
            page_titles = ["Python (programming language)", "JavaScript", "TypeScript"]
            page_tasks = [api.page(title) for title in page_titles]
            pages = await asyncio.gather(*page_tasks)
            
            # Get content for each page concurrently
            content_tasks = [page.content for page in pages]
            contents = await asyncio.gather(*content_tasks)
            
            # Print page titles and content lengths
            for page, content in zip(pages, contents):
                title = await page.title  # Even title is awaitable
                print(f"{title}: {len(content)} characters")

    asyncio.run(main())

Advanced Usage: Limiting Concurrency
----------------------------------

While concurrency improves performance, unlimited concurrency can lead to issues. The async API provides several ways to control concurrency:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.config import Config

    async def main():
        # Configure with concurrency limits
        config = Config(
            max_concurrent_requests=10,  # Limit to 10 concurrent requests
            connection_pool_size=20,     # Total connections in pool
            connections_per_host=5       # Max connections to any host
        )
        
        async with AsyncMediaWikiAPI(config=config) as api:
            # Generate many tasks
            search_terms = [f"Topic {i}" for i in range(30)]
            
            # Custom concurrency control with semaphore
            semaphore = asyncio.Semaphore(5)  # Additional limit of 5 concurrent operations
            
            async def search_with_limit(term):
                async with semaphore:
                    return await api.search(term)
            
            # Create limited tasks
            tasks = [search_with_limit(term) for term in search_terms]
            
            # Execute with managed concurrency
            results = await asyncio.gather(*tasks)
            print(f"Completed {len(results)} searches")

    asyncio.run(main())

Handling Errors in Async Context
------------------------------

Error handling in async code requires some special attention:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.exceptions import PageError, DisambiguationError

    async def main():
        async with AsyncMediaWikiAPI() as api:
            try:
                # Try to get a non-existent page
                page = await api.page("This page definitely does not exist")
                
            except PageError as e:
                print(f"Page not found: {e}")
                
            try:
                # Try a disambiguation page
                page = await api.page("Python")
                
            except DisambiguationError as e:
                print(f"Disambiguation page found with options: {e.options}")
                
                # Automatically select the first option
                if e.options:
                    page = await api.page(e.options[0])
                    title = await page.title
                    print(f"Selected: {title}")
            
            # Handle multiple requests with error handling
            titles = ["Python", "NonExistentPage123", "JavaScript"]
            
            # Function to safely get a page
            async def safe_get_page(title):
                try:
                    page = await api.page(title)
                    content_length = len(await page.content)
                    return {"title": title, "status": "success", "length": content_length}
                except Exception as e:
                    return {"title": title, "status": "error", "error": str(e)}
            
            # Run all requests with error handling
            results = await asyncio.gather(*(safe_get_page(title) for title in titles))
            
            for result in results:
                if result["status"] == "success":
                    print(f"✅ {result['title']}: {result['length']} chars")
                else:
                    print(f"❌ {result['title']}: {result['error']}")

    asyncio.run(main())

Performance Comparison
--------------------

Here's a simple benchmark comparing sync vs. async performance:

.. code-block:: python

    import time
    import asyncio
    from mediawikiapi import MediaWikiAPI, AsyncMediaWikiAPI

    def sync_searches(terms):
        api = MediaWikiAPI()
        start_time = time.time()
        
        results = []
        for term in terms:
            results.append(api.search(term))
            
        duration = time.time() - start_time
        return results, duration

    async def async_searches(terms):
        api = AsyncMediaWikiAPI()
        start_time = time.time()
        
        try:
            tasks = [api.search(term) for term in terms]
            results = await asyncio.gather(*tasks)
            
            duration = time.time() - start_time
            return results, duration
        finally:
            await api.close()

    # Run the benchmark
    search_terms = ["Python", "JavaScript", "TypeScript", "Rust", "Go", 
                   "Machine Learning", "Artificial Intelligence", "Data Science", 
                   "Web Development", "Cloud Computing"]

    # Sync version
    sync_results, sync_duration = sync_searches(search_terms)
    print(f"Sync version took {sync_duration:.2f} seconds")

    # Async version  
    async def run_async_benchmark():
        async_results, async_duration = await async_searches(search_terms)
        print(f"Async version took {async_duration:.2f} seconds")
        print(f"Speedup: {sync_duration / async_duration:.2f}x faster")
        
    asyncio.run(run_async_benchmark())

Best Practices
-------------

1. **Always close sessions**: Use ``async with`` or ``try/finally`` to ensure proper cleanup
2. **Limit concurrency**: Set appropriate concurrency limits to avoid overwhelming servers
3. **Group related requests**: Use ``asyncio.gather()`` for related requests that can run concurrently
4. **Handle errors properly**: Remember that each awaited call can raise exceptions
5. **Consider memory usage**: Concurrent operations may increase memory usage
6. **Use timeouts**: Configure timeouts to prevent operations from hanging indefinitely

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.config import Config

    async def main():
        # Configure with timeouts and limits
        config = Config(
            timeout=10.0,                # 10 second timeout
            max_concurrent_requests=10,  # Limit concurrent requests
            rate_limit=100               # Add 100ms between requests
        )
        
        async with AsyncMediaWikiAPI(config=config) as api:
            # Your async code here
            pass

    asyncio.run(main())

Next Steps
---------

Now that you understand the basics of the async API, consider exploring:

- :ref:`concurrency_controls_tutorial` for more detailed control over concurrent operations
- :ref:`caching_tutorial` to learn about caching with async operations
- :ref:`error_handling_tutorial` for more advanced error handling strategies

For the complete API reference, see :ref:`api`.