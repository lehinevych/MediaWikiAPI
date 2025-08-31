.. _custom_mediawiki_tutorial:

Custom MediaWiki Instances
=========================

While MediaWikiAPI is commonly used with Wikipedia, it can connect to any MediaWiki installation. This tutorial covers how to use MediaWikiAPI with custom MediaWiki instances, including other Wikimedia projects and private wikis.

Understanding MediaWiki API Endpoints
----------------------------------

Every MediaWiki installation provides an API endpoint, typically located at ``/w/api.php`` or ``/api.php`` on the server. This endpoint follows the standard MediaWiki API protocol, allowing MediaWikiAPI to interact with it in the same way it interacts with Wikipedia.

The API provides access to wiki content, search capabilities, editing features (if authorized), and more.

Connecting to Other Wikimedia Projects
------------------------------------

Wikimedia runs many projects besides Wikipedia, all using MediaWiki:

* Wiktionary - Dictionary
* Wikiquote - Collection of quotes
* Wikibooks - Open-content textbooks
* Wikisource - Free content library
* Wikimedia Commons - Media repository
* Wikidata - Knowledge base
* Wikivoyage - Travel guide

Here's how to connect to various Wikimedia projects:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to English Wiktionary
    wiktionary_config = Config(mediawiki_url="https://{}.wiktionary.org/w/api.php")
    wiktionary = MediaWikiAPI(config=wiktionary_config)

    # Look up a word
    print(wiktionary.summary("Python"))

    # Connect to Wikimedia Commons
    commons_config = Config(mediawiki_url="https://commons.wikimedia.org/w/api.php")
    commons = MediaWikiAPI(config=commons_config)

    # Search for media
    print(commons.search("Eiffel Tower"))

    # Connect to Wikidata
    wikidata_config = Config(mediawiki_url="https://www.wikidata.org/w/api.php")
    wikidata = MediaWikiAPI(config=wikidata_config)

    # Search for items
    print(wikidata.search("Python programming language"))

Connecting to Private MediaWiki Instances
---------------------------------------

You can connect to any MediaWiki installation, including private or self-hosted wikis:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to a private wiki
    private_wiki_config = Config(
        mediawiki_url="https://wiki.example.org/api.php",  # No {} placeholder for fixed URL
        user_agent="MyApp/1.0 (contact@example.org)"  # Polite to identify your app
    )

    private_wiki = MediaWikiAPI(config=private_wiki_config)

    # Use the API as normal
    search_results = private_wiki.search("Project Documentation")
    print(search_results)

Authentication with Private Wikis
-------------------------------

Many private MediaWiki installations require authentication. MediaWikiAPI doesn't directly handle authentication, but you can use the underlying ``requests`` session:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config
    import requests

    # Create config for private wiki
    private_wiki_config = Config(mediawiki_url="https://wiki.example.org/api.php")
    private_wiki = MediaWikiAPI(config=private_wiki_config)

    # Access the underlying requests session
    session = private_wiki.session.session

    # Method 1: Login using cookies
    # First, obtain login cookies from the wiki (typically by logging in via browser)
    # Then set them in your session
    cookies = {
        "wikiSession": "your_session_cookie",
        "wikiUserID": "your_user_id_cookie",
        "wikiToken": "your_token_cookie"
    }
    session.cookies.update(cookies)

    # Method 2: Basic authentication for wikis behind HTTP auth
    session.auth = ("username", "password")

    # Method 3: OAuth (for wikis that support it)
    # This requires additional libraries like requests_oauthlib
    # from requests_oauthlib import OAuth1Session
    # ... OAuth setup code ...

    # Now use the API with authentication
    try:
        # Test the authenticated session
        result = private_wiki.search("Confidential")
        print("Authentication successful!")
        print(result)
    except Exception as e:
        print(f"Authentication failed: {e}")

Working with Different MediaWiki Versions
---------------------------------------

Different MediaWiki instances may run different versions of the MediaWiki software, which can affect available features. MediaWikiAPI includes version detection capabilities:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to a wiki
    wiki_config = Config(mediawiki_url="https://wiki.example.org/api.php")
    wiki = MediaWikiAPI(config=wiki_config)

    # Get the detected MediaWiki version
    api_version = wiki.get_api_version()
    if api_version:
        print(f"MediaWiki version: {api_version.major}.{api_version.minor}.{api_version.patch}")
        print(f"Generator: {api_version.generator}")
    else:
        print("Could not detect MediaWiki version")

    # Check if a specific feature is available
    if wiki.is_feature_available("geosearch"):
        print("GeoSearch is available")
    else:
        print("GeoSearch is not available in this MediaWiki version")

Adapting to Wiki Structure Differences
------------------------------------

Different wikis may have different namespace structures, categories, and content organization. When working with custom wikis, you may need to adapt to these differences:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to a custom wiki
    wiki_config = Config(mediawiki_url="https://wiki.example.org/api.php")
    wiki = MediaWikiAPI(config=wiki_config)

    # Get site information including namespaces
    site_info = wiki.custom_query({
        "action": "query",
        "meta": "siteinfo",
        "siprop": "namespaces",
        "format": "json"
    })

    # Display available namespaces
    namespaces = site_info.get("query", {}).get("namespaces", {})
    print("Available namespaces:")
    for ns_id, ns_data in namespaces.items():
        print(f"{ns_id}: {ns_data.get('*', 'N/A')}")

    # Search within a specific namespace
    # For example, search only in the "Help" namespace
    help_search = wiki.custom_query({
        "action": "query",
        "list": "search",
        "srsearch": "guide",
        "srnamespace": "12",  # Namespace ID for Help
        "format": "json"
    })

    # Process results
    search_results = help_search.get("query", {}).get("search", [])
    for result in search_results:
        print(f"- {result.get('title')}")

Examples with Specific Wikimedia Projects
---------------------------------------

Wiktionary Example
~~~~~~~~~~~~~~~~

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Connect to English Wiktionary
    wiktionary_config = Config(mediawiki_url="https://{}.wiktionary.org/w/api.php")
    wiktionary = MediaWikiAPI(config=wiktionary_config)
    wiktionary.config.language = "en"  # Set language to English

    # Get a dictionary entry
    word = "serendipity"
    page = wiktionary.page(word)

    print(f"Definition of {word}:")
    print(page.content[:500] + "...")  # Print the first 500 characters

    # Get etymology using custom query
    etymology_query = {
        "action": "parse",
        "page": word,
        "prop": "sections|text",
        "section": "1",  # Etymology is often in section 1
        "format": "json"
    }
    
    result = wiktionary.custom_query(etymology_query)
    
    # Extract and clean the etymology text
    if "parse" in result and "text" in result["parse"]:
        from bs4 import BeautifulSoup
        
        html = result["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")
        etymology = soup.get_text().strip()
        
        print("\nEtymology:")
        print(etymology)

Wikimedia Commons Example
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config
    import requests

    # Connect to Wikimedia Commons
    commons_config = Config(mediawiki_url="https://commons.wikimedia.org/w/api.php")
    commons = MediaWikiAPI(config=commons_config)

    # Search for images
    search_term = "Eiffel Tower night"
    image_results = commons.custom_query({
        "action": "query",
        "generator": "search",
        "gsrsearch": search_term,
        "gsrnamespace": "6",  # File namespace
        "prop": "imageinfo",
        "iiprop": "url|dimensions|mime",
        "gsrlimit": "5",
        "format": "json"
    })

    # Extract and display image information
    if "query" in image_results and "pages" in image_results["query"]:
        print(f"Images related to '{search_term}':")
        for _, page_data in image_results["query"]["pages"].items():
            if "imageinfo" in page_data:
                title = page_data.get("title", "Unknown")
                info = page_data["imageinfo"][0]
                url = info.get("url", "No URL")
                width = info.get("width", "Unknown")
                height = info.get("height", "Unknown")
                mime = info.get("mime", "Unknown")
                
                print(f"\n- {title}")
                print(f"  Type: {mime}")
                print(f"  Dimensions: {width} x {height}")
                print(f"  URL: {url}")

                # Download the first image
                if "File:" in title and url:
                    filename = title.replace("File:", "").replace(" ", "_")
                    response = requests.get(url)
                    if response.status_code == 200:
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        print(f"  Downloaded as: {filename}")
                    break

Advanced: Working with Different API Endpoints
-------------------------------------------

Some MediaWiki installations might have API endpoints at non-standard locations. You can specify a custom URL pattern:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.config import Config

    # Custom API endpoint location
    custom_config = Config(
        mediawiki_url="https://example.org/wiki/custom/location/api.php"
    )
    custom_wiki = MediaWikiAPI(config=custom_config)

    # Test the connection
    try:
        site_info = custom_wiki.custom_query({
            "action": "query",
            "meta": "siteinfo",
            "format": "json"
        })
        print("Connection successful!")
        print(f"Wiki name: {site_info.get('query', {}).get('general', {}).get('sitename', 'Unknown')}")
    except Exception as e:
        print(f"Connection failed: {e}")

Troubleshooting Custom Wiki Connections
-------------------------------------

If you're having trouble connecting to a custom MediaWiki instance, try these troubleshooting steps:

1. **Verify the API endpoint**: Make sure the API URL is correct by visiting it in a browser. It should return JSON with information about the API.

2. **Check permissions**: Ensure the wiki allows API access and that your requests don't require authentication.

3. **Use custom query for debugging**:

   .. code-block:: python
       
       # Simple test query
       test_query = wiki.custom_query({
           "action": "query",
           "meta": "siteinfo",
           "format": "json"
       })
       print(test_query)

4. **Examine error responses**: Check the error messages for clues:

   .. code-block:: python
       
       from mediawikiapi.exceptions import MediaWikiAPIException
       
       try:
           result = wiki.search("test")
       except MediaWikiAPIException as e:
           print(f"API Error: {e}")
       except Exception as e:
           print(f"General Error: {e}")

5. **Check API documentation**: Each MediaWiki installation may have its own API help page at ``api.php?action=help``.

Next Steps
---------

Now that you know how to connect to custom MediaWiki instances, consider:

- :ref:`error_handling_tutorial` for handling errors when working with different wikis
- :ref:`performance_best_practices` for optimizing connections to remote wikis
- :ref:`api` for detailed API documentation