API Version Handling
==================

MediaWikiAPI provides robust handling for different MediaWiki API versions, allowing you to work with various MediaWiki installations while maintaining compatibility.

Version Detection
---------------

When connecting to a MediaWiki API, MediaWikiAPI automatically detects the server version using the `siteinfo` endpoint:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    
    api = MediaWikiAPI()
    
    # API version is detected during the first request
    api.search("Python")
    
    # Get the detected version
    version = api.get_api_version()
    print(f"Detected MediaWiki version: {version}")  # e.g., "1.35.0"

Version Compatibility
-------------------

Different MediaWiki versions support different features. The key version thresholds are:

* **MediaWiki 1.19**: Minimum supported version
* **MediaWiki 1.25**: Added support for `extracts` and `pageimages` extensions
* **MediaWiki 1.32**: Enhanced HTML content parsing
* **MediaWiki 1.34**: Enhanced content extraction and infoboxes
* **MediaWiki 1.35**: Advanced reference extraction and LTS release
* **MediaWiki 1.39**: Latest LTS release with structured data support

Version-Specific Features
-----------------------

The following features require specific MediaWiki versions:

.. list-table::
   :widths: 30 15 55
   :header-rows: 1

   * - Feature
     - Min Version
     - Notes
   * - Basic page access
     - 1.19
     - Basic page retrieval works on all supported versions
   * - Page extracts
     - 1.25
     - Plain text extraction of page content
   * - Infobox extraction
     - 1.34
     - Extraction and parsing of infoboxes
   * - Page content
     - 1.34
     - Full page content with proper text extraction
   * - Page summary
     - 1.34
     - Page summaries with the TextExtracts extension
   * - Revision IDs
     - 1.34
     - Access to revision and parent IDs
   * - Advanced references
     - 1.35
     - Enhanced extraction of references

Graceful Degradation
------------------

MediaWikiAPI includes a graceful degradation system that works in two ways:

1. **Feature Compatibility Mode** (default: enabled): Attempts to provide features even on older API versions through alternative implementations.
2. **Version Checking**: When feature compatibility mode is disabled, MediaWikiAPI strictly checks the server version before allowing access to version-specific features.

Configure Version Handling
------------------------

You can configure version handling when creating the MediaWikiAPI instance:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI, Config
    from mediawikiapi.common.api_version import MEDIAWIKI_1_35
    
    # Use feature compatibility mode (default)
    api_with_compat = MediaWikiAPI(Config(feature_compatibility_mode=True))
    
    # Disable feature compatibility mode for strict version checking
    api_strict = MediaWikiAPI(Config(feature_compatibility_mode=False))
    
    # Set a minimum required API version
    api_min_version = MediaWikiAPI(Config(
        min_api_version=MEDIAWIKI_1_35,
        feature_compatibility_mode=False
    ))

Handling Version-Dependent Features
--------------------------------

When working with features that might not be available on all MediaWiki versions:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    from mediawikiapi.exceptions import MediaWikiAPIException
    
    api = MediaWikiAPI(Config(feature_compatibility_mode=False))
    page = api.page("Python (programming language)")
    
    try:
        # This requires MediaWiki 1.34+
        infobox = page.infobox
        print("Infobox data:", infobox)
    except MediaWikiAPIException as e:
        print(f"Feature not available: {e}")
        
    # Check if a feature is available before using it
    if api.is_feature_available("infobox_extraction"):
        infobox = page.infobox
        print("Infobox data:", infobox)
    else:
        print("Infobox extraction not available on this MediaWiki version")

Custom MediaWiki Installations
---------------------------

When working with custom MediaWiki installations, you can specify the API URL:

.. code-block:: python

    from mediawikiapi import MediaWikiAPI, Config
    
    # Connect to a custom MediaWiki installation
    config = Config(mediawiki_url="https://your-wiki.org/w/api.php")
    api = MediaWikiAPI(config)
    
    # Version will be detected during the first request
    page = api.page("Main Page")
    
    # Get the version after making a request
    version = api.get_api_version()
    print(f"Custom wiki is running MediaWiki {version}")