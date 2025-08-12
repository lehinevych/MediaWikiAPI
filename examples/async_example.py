#!/usr/bin/env python3
"""
Example showing the usage of the async MediaWikiAPI implementation.
"""

import asyncio
from mediawikiapi import AsyncMediaWikiAPI


async def main():
    """
    Main async function that demonstrates the usage of AsyncMediaWikiAPI.
    """
    # Create the API instance (can be used as an async context manager)
    async with AsyncMediaWikiAPI() as api:
        # Basic search
        print("Searching for 'Python programming language'...")
        results = await api.search("Python programming language")
        print(f"Search results: {results[:5]}\n")

        # Get a page
        print("Getting the Python page...")
        python_page = await api.page("Python (programming language)")

        # Get basic page properties
        print(f"Page title: {python_page.title}")
        print(f"Page URL: {python_page.url}")

        # Get page summary
        print("\nGetting page summary...")
        summary = await python_page.summary
        print(f"Summary: {summary[:300]}...\n")

        # Get page sections
        print("Getting page sections...")
        sections = await python_page.sections
        print(f"Sections: {sections[:5]}\n")

        # Get page categories
        print("Getting page categories...")
        categories = await python_page.categories
        print(f"Categories: {categories[:5]}\n")

        # Get page links
        print("Getting page links...")
        links = await python_page.links
        print(f"Links: {links[:5]}\n")

        # Get page references (external links)
        print("Getting page references...")
        references = await python_page.references
        print(f"References: {references[:3]}\n")

        # Get page images
        print("Getting page images...")
        images = await python_page.images
        print(f"Images: {images[:3]}\n")

        # Get random pages
        print("Getting random pages...")
        random_pages = await api.random(pages=3)
        print(f"Random pages: {random_pages}\n")

        # Perform a geo search
        print("Performing a geo search...")
        geo_results = await api.geosearch(
            latitude=40.748817, longitude=-73.985428, radius=1000
        )
        print(f"Geo search results: {geo_results[:5]}\n")


if __name__ == "__main__":
    asyncio.run(main())
