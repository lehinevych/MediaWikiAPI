Examples and Use Cases
=====================

This page provides practical examples of common use cases for MediaWikiAPI.

Basic Usage
----------

Searching Wikipedia
~~~~~~~~~~~~~~~~~~

Search for Wikipedia pages related to a specific topic:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    results = mediawiki.search("Machine Learning")
    print(results)

Getting Page Summary
~~~~~~~~~~~~~~~~~~~

Get a concise summary of a specific Wikipedia page:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    summary = mediawiki.summary("Python (programming language)")
    print(summary)

Limit the summary to a specific number of sentences:

.. code-block:: python

    summary = mediawiki.summary("Python (programming language)", sentences=2)
    print(summary)

Retrieving Full Page Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the full content and metadata of a Wikipedia page:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    page = mediawiki.page("Python (programming language)")

    # Access page properties
    print(f"Title: {page.title}")
    print(f"URL: {page.url}")
    print(f"Categories: {page.categories}")
    
    # Get the page content
    print(f"Content: {page.content[:500]}...")  # First 500 characters

Working with Page Links
~~~~~~~~~~~~~~~~~~~~~~

Get links from a Wikipedia page:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    page = mediawiki.page("Deep learning")
    
    # Print all links on the page
    for link in page.links:
        print(link)
    
    # Find specific links
    ai_links = [link for link in page.links if "intelligence" in link.lower()]
    print(f"AI-related links: {ai_links}")

Accessing Images
~~~~~~~~~~~~~~~

Get images from a Wikipedia page:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    page = mediawiki.page("Paris")
    
    # Print all image URLs
    for image_url in page.images:
        print(image_url)
    
    # Download the first image
    import requests
    
    if page.images:
        response = requests.get(page.images[0])
        if response.status_code == 200:
            with open("paris_image.jpg", "wb") as f:
                f.write(response.content)
            print("Image downloaded successfully")

Geosearch
~~~~~~~~~

Find Wikipedia pages near a specific geographic location:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from decimal import Decimal

    mediawiki = MediaWikiAPI()
    
    # Coordinates for the Eiffel Tower
    latitude = Decimal('48.8583')
    longitude = Decimal('-2.2945')
    
    # Find pages within 1km of these coordinates
    nearby_places = mediawiki.geosearch(latitude=latitude, longitude=longitude, radius=1000)
    print(nearby_places)

Intermediate Usage
----------------

Working with Different Languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access Wikipedia content in different languages:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    
    # Get a summary in English
    en_summary = mediawiki.summary("Berlin")
    print(f"English summary: {en_summary[:200]}...")
    
    # Switch to German
    mediawiki.config.language = "de"
    de_summary = mediawiki.summary("Berlin")
    print(f"German summary: {de_summary[:200]}...")
    
    # Switch to Spanish
    mediawiki.config.language = "es"
    es_summary = mediawiki.summary("Berlin")
    print(f"Spanish summary: {es_summary[:200]}...")
    
    # List available languages
    languages = mediawiki.languages()
    print(f"Available language codes: {list(languages.keys())[:10]}...")  # First 10 languages

Handling Categories
~~~~~~~~~~~~~~~~~

Work with Wikipedia categories:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    
    # Get members of a category
    programming_langs = mediawiki.category_members("Programming languages", cmlimit=10)
    print(f"Programming languages: {programming_langs}")
    
    # Get categories for a page
    python_page = mediawiki.page("Python (programming language)")
    print(f"Categories for Python: {python_page.categories}")

Error Handling
~~~~~~~~~~~~~

Handle common errors when working with MediaWikiAPI:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import PageError, DisambiguationError, MediaWikiAPIException

    mediawiki = MediaWikiAPI()
    
    # Handle non-existent pages
    try:
        page = mediawiki.page("This page definitely does not exist")
    except PageError as e:
        print(f"Page error: {e}")
    
    # Handle disambiguation pages
    try:
        page = mediawiki.page("Python")  # This is a disambiguation page
    except DisambiguationError as e:
        print(f"Disambiguation error: {e}")
        print(f"Possible options: {e.options}")
        
        # Auto-select the first option
        if e.options:
            page = mediawiki.page(e.options[0])
            print(f"Selected: {page.title}")
    
    # Handle API errors
    try:
        # Invalid parameter
        mediawiki.custom_query({"action": "query", "invalid": "parameter"})
    except MediaWikiAPIException as e:
        print(f"API error: {e}")

Advanced Usage
------------

Custom MediaWiki Instances
~~~~~~~~~~~~~~~~~~~~~~~~

Connect to custom MediaWiki installations:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to Wiktionary instead of Wikipedia
    wiktionary_config = Config(mediawiki_url="https://{}.wiktionary.org/w/api.php")
    wiktionary = MediaWikiAPI(config=wiktionary_config)
    
    # Get definition of a word
    word_page = wiktionary.page("Python")
    print(word_page.content[:500])
    
    # Connect to a private MediaWiki
    private_wiki_config = Config(mediawiki_url="https://your-wiki-domain.com/api.php")
    private_wiki = MediaWikiAPI(config=private_wiki_config)

Asynchronous API Usage
~~~~~~~~~~~~~~~~~~~~

Use the asynchronous API for improved performance:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI

    async def main():
        # Create an async MediaWikiAPI instance
        async_mediawiki = AsyncMediaWikiAPI()
        
        # Perform multiple searches concurrently
        search_terms = ["Python", "JavaScript", "Rust", "Go", "TypeScript"]
        
        tasks = []
        for term in search_terms:
            tasks.append(async_mediawiki.search(term, results=5))
        
        # Wait for all searches to complete
        results = await asyncio.gather(*tasks)
        
        # Print results
        for term, pages in zip(search_terms, results):
            print(f"{term}: {pages}")
            
        # Close the session when done
        await async_mediawiki.close()

    # Run the async code
    asyncio.run(main())

Custom API Queries
~~~~~~~~~~~~~~~

Make custom API queries for specialized needs:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI

    mediawiki = MediaWikiAPI()
    
    # Get page view statistics
    query_params = {
        "action": "query",
        "titles": "Python (programming language)",
        "prop": "pageviews",
        "pvipdays": 30,  # Last 30 days
        "format": "json"
    }
    
    result = mediawiki.custom_query(query_params)
    
    # Process and display the results
    pages = result.get("query", {}).get("pages", {})
    for page_id, page_data in pages.items():
        print(f"Page views for {page_data.get('title')}:")
        if "pageviews" in page_data:
            for date, views in page_data["pageviews"].items():
                if views:
                    print(f"  {date}: {views} views")

Rate Limiting and Retry Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure rate limits and retry behavior:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Configure with rate limiting and retry settings
    config = Config(
        # Add 100 milliseconds between requests
        rate_limit=100,
        
        # Retry settings
        max_retries=3,
        retry_backoff_factor=0.5,
        retry_backoff_max=60,
        
        # Cache settings
        cache_ttl=3600,  # 1 hour cache time
        cache_max_size=1000  # Maximum items in cache
    )
    
    mediawiki = MediaWikiAPI(config=config)
    
    # Now use the API with these settings
    results = mediawiki.search("Climate change")
    print(results)

Batch Operations
~~~~~~~~~~~~~~

Efficiently retrieve multiple pages at once:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    import time

    mediawiki = MediaWikiAPI()
    
    # List of pages to retrieve
    page_titles = [
        "Python (programming language)",
        "JavaScript",
        "TypeScript",
        "Rust (programming language)",
        "Go (programming language)"
    ]
    
    # Inefficient way (one at a time)
    start_time = time.time()
    pages_sequential = []
    for title in page_titles:
        try:
            page = mediawiki.page(title)
            pages_sequential.append(page)
        except Exception as e:
            print(f"Error retrieving {title}: {e}")
    
    sequential_time = time.time() - start_time
    print(f"Sequential retrieval took {sequential_time:.2f} seconds")
    
    # More efficient way (using custom_query with multiple titles)
    start_time = time.time()
    query_params = {
        "action": "query",
        "titles": "|".join(page_titles),
        "prop": "extracts|info",
        "inprop": "url",
        "explaintext": True,
        "format": "json"
    }
    
    result = mediawiki.custom_query(query_params)
    batch_time = time.time() - start_time
    print(f"Batch retrieval took {batch_time:.2f} seconds")
    print(f"Improvement: {sequential_time / batch_time:.2f}x faster")

Working with Async API and Concurrency Controls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure concurrency controls for async operations:

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    from mediawikiapi.config import Config

    async def main():
        # Configure with concurrency controls
        config = Config(
            connection_pool_size=50,
            connections_per_host=10,
            max_concurrent_requests=15
        )
        
        async_mediawiki = AsyncMediaWikiAPI(config=config)
        
        try:
            # Generate many search tasks
            search_terms = [f"Topic {i}" for i in range(30)]
            tasks = [async_mediawiki.search(term, results=3) for term in search_terms]
            
            # Execute all tasks concurrently with controlled concurrency
            results = await asyncio.gather(*tasks)
            
            # Print stats
            total_results = sum(len(r) for r in results)
            print(f"Retrieved {total_results} results for {len(search_terms)} search terms")
        
        finally:
            # Always close the session
            await async_mediawiki.close()

    # Run the async code
    asyncio.run(main())