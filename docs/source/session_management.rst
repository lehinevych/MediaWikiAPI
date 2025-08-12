Session Management
=================

MediaWikiAPI provides robust session management capabilities to ensure efficient resource usage and proper cleanup.

Context Manager Support
---------------------

Both synchronous and asynchronous API implementations can be used as context managers to ensure proper resource cleanup:

Synchronous Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from mediawikiapi import MediaWikiAPI
    
    # Using context manager for automatic cleanup
    with MediaWikiAPI() as api:
        page = api.page("Python (programming language)")
        print(page.summary)
    # Session is automatically closed after the with block

Asynchronous Example
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from mediawikiapi import AsyncMediaWikiAPI
    
    async def main():
        # Using async context manager
        async with AsyncMediaWikiAPI() as api:
            page = await api.page("Python (programming language)")
            print(await page.summary)
        # Session is automatically closed after the with block
    
    asyncio.run(main())

Manual Resource Management
------------------------

You can also manually manage resources using explicit close methods:

.. code-block:: python

    # Synchronous
    api = MediaWikiAPI()
    try:
        page = api.page("Python (programming language)")
        print(page.summary)
    finally:
        api.close()  # Explicitly close the session
    
    # Asynchronous
    async def main():
        api = AsyncMediaWikiAPI()
        try:
            page = await api.page("Python (programming language)")
            print(await page.summary)
        finally:
            await api.close()  # Explicitly close the session

Session Reuse Policies
--------------------

MediaWikiAPI implements intelligent session reuse policies to balance performance and resource utilization:

1. **Automatic Session Refresh**: Sessions are automatically refreshed after a configurable number of requests to prevent memory leaks and stale connections.

2. **Manual Session Refresh**: You can explicitly create a new session when needed:

   .. code-block:: python
   
       # Synchronous
       api.new_session()
       
       # Asynchronous
       await api.new_session()

3. **Session Reuse Counter**: The library tracks how many times a session has been used and automatically refreshes it when necessary:

   .. code-block:: python
   
       # Configure the maximum number of times a session can be reused
       api.session.set_max_reuse_count(500)  # Default is 1000

Best Practices
------------

1. **Use Context Managers**: Whenever possible, use context managers to ensure proper resource cleanup.

2. **Close Sessions Explicitly**: If not using context managers, always close sessions explicitly in a `finally` block.

3. **Tune Session Reuse**: For long-running applications, consider adjusting the session reuse count based on your usage patterns.

4. **Create New Sessions for New Tasks**: Consider creating new sessions for logically separate tasks to isolate any potential issues.

Advanced Usage
-----------

For synchronous API usage, you can provide an existing requests Session:

.. code-block:: python

    import requests
    from mediawikiapi.sync.requestsession import RequestSession
    from mediawikiapi import MediaWikiAPI
    
    # Create a custom session with specific configurations
    custom_session = requests.Session()
    custom_session.headers.update({"X-Custom-Header": "Value"})
    
    # Create a RequestSession with the custom session
    request_session = RequestSession(session=custom_session)
    
    # Create MediaWikiAPI with the custom RequestSession
    api = MediaWikiAPI()
    api.session = request_session