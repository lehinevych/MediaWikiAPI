#!/usr/bin/env python3
"""
Shortened test for the synchronous MediaWikiAPI implementation.
"""

from mediawikiapi import MediaWikiAPI


def main():
    """
    Main function that tests the synchronous MediaWikiAPI.
    """
    # Create the API instance
    api = MediaWikiAPI()
    
    # Basic search
    print("Searching for 'Python programming language'...")
    results = api.search("Python programming language")
    print(f"Search results: {results[:3]}\n")

    # Get a page
    print("Getting the Python page...")
    python_page = api.page("Python (programming language)")
    
    # Get basic page properties
    print(f"Page title: {python_page.title}")
    print(f"Page URL: {python_page.url}")
    
    # Get page summary
    print("\nGetting page summary...")
    summary = python_page.summary
    print(f"Summary excerpt: {summary[:100]}...\n")
    
    print("Sync API test completed successfully!")


if __name__ == "__main__":
    main()