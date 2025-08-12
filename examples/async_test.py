#!/usr/bin/env python3
"""
Shortened test for the asynchronous MediaWikiAPI implementation.
"""

import asyncio
from mediawikiapi import AsyncMediaWikiAPI


async def main():
    """
    Main async function that tests the AsyncMediaWikiAPI.
    """
    # Create the API instance (using context manager)
    async with AsyncMediaWikiAPI() as api:
        # Basic search
        print("Searching for 'Python programming language'...")
        results = await api.search("Python programming language")
        print(f"Search results: {results[:3]}\n")

        # Get a page
        print("Getting the Python page...")
        python_page = await api.page("Python (programming language)")

        # Get basic page properties
        print(f"Page title: {python_page.title}")
        print(f"Page URL: {python_page.url}")

        # Get page summary
        print("\nGetting page summary...")
        summary = await python_page.summary
        print(f"Summary excerpt: {summary[:100]}...\n")

        print("Async API test completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
