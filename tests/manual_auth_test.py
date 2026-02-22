"""
Manual testing script for Personal Access Token authentication.

This script helps you verify that authentication headers are being sent correctly
to the MediaWiki API.

USAGE:
    1. Get a Personal Access Token from https://api.wikimedia.org/
    2. Set the token: export WIKIMEDIA_ACCESS_TOKEN="your_token_here"
    3. Run: python tests/manual_auth_test.py

This script will:
- Show what headers are being sent
- Make a test request to Wikipedia
- Display the response to verify everything works
"""

import os
import sys
from pprint import pprint

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config


def print_section(title: str) -> None:
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_without_auth() -> None:
    """Test API requests without authentication"""
    print_section("Test 1: Without Authentication")

    config = Config()
    api = MediaWikiAPI(config=config)

    print("\nHeaders being sent:")
    pprint(config.get_headers())

    print("\nMaking request to Wikipedia...")
    try:
        results = api.search("Python programming", results=3)
        print(f"\n✅ Success! Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_with_auth() -> None:
    """Test API requests with Personal Access Token"""
    print_section("Test 2: With Personal Access Token")

    # Get token from environment variable
    access_token = os.environ.get("WIKIMEDIA_ACCESS_TOKEN")

    if not access_token:
        print("\n⚠️  No access token found.")
        print("Set it with: export WIKIMEDIA_ACCESS_TOKEN='your_token_here'")
        print("Get a token from: https://api.wikimedia.org/")
        return

    config = Config(access_token=access_token)
    api = MediaWikiAPI(config=config)

    print("\nHeaders being sent:")
    headers = config.get_headers()
    # Mask the token for security
    if "Authorization" in headers:
        token_value = headers["Authorization"]
        masked_token = (
            token_value[:20] + "..." + token_value[-10:]
            if len(token_value) > 30
            else "***MASKED***"
        )
        headers_display = headers.copy()
        headers_display["Authorization"] = masked_token
        pprint(headers_display)
    else:
        pprint(headers)

    print("\nMaking authenticated request to Wikipedia...")
    try:
        results = api.search("Python programming", results=3)
        print(f"\n✅ Success! Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_with_custom_headers() -> None:
    """Test API requests with custom headers"""
    print_section("Test 3: With Custom Headers")

    custom_headers = {
        "X-Application-Name": "MediaWikiAPI-Test",
        "X-Application-Version": "1.0.0",
    }

    config = Config(custom_headers=custom_headers)
    api = MediaWikiAPI(config=config)

    print("\nHeaders being sent:")
    pprint(config.get_headers())

    print("\nMaking request with custom headers...")
    try:
        results = api.search("Python programming", results=3)
        print(f"\n✅ Success! Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_custom_user_agent() -> None:
    """Test API requests with custom User-Agent"""
    print_section("Test 4: With Custom User-Agent")

    custom_headers = {"User-Agent": "MyTestBot/1.0 (testing@example.com)"}

    config = Config(custom_headers=custom_headers)
    api = MediaWikiAPI(config=config)

    print("\nHeaders being sent:")
    pprint(config.get_headers())

    print("\nMaking request with custom User-Agent...")
    try:
        results = api.search("Python programming", results=3)
        print(f"\n✅ Success! Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_combined() -> None:
    """Test with both authentication and custom headers"""
    print_section("Test 5: Combined Authentication + Custom Headers")

    access_token = os.environ.get("WIKIMEDIA_ACCESS_TOKEN")

    if not access_token:
        print("\n⚠️  Skipping - no access token found.")
        return

    custom_headers = {
        "X-Application-Name": "MediaWikiAPI-Test",
        "X-Request-ID": "test-12345",
    }

    config = Config(access_token=access_token, custom_headers=custom_headers)
    api = MediaWikiAPI(config=config)

    print("\nHeaders being sent:")
    headers = config.get_headers()
    # Mask the token
    if "Authorization" in headers:
        token_value = headers["Authorization"]
        masked_token = (
            token_value[:20] + "..." + token_value[-10:]
            if len(token_value) > 30
            else "***MASKED***"
        )
        headers_display = headers.copy()
        headers_display["Authorization"] = masked_token
        pprint(headers_display)
    else:
        pprint(headers)

    print("\nMaking combined request...")
    try:
        results = api.search("Python programming", results=3)
        print(f"\n✅ Success! Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main() -> None:
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  MediaWikiAPI Authentication Testing")
    print("=" * 70)

    # Run all tests
    test_without_auth()
    test_with_auth()
    test_with_custom_headers()
    test_custom_user_agent()
    test_combined()

    print_section("Testing Complete")
    print("\n✅ All tests completed successfully!")
    print("\nNote: Wikipedia API works without authentication. To test authenticated")
    print("      requests, use a Wikimedia API endpoint that requires authentication.")
    print("      See: https://api.wikimedia.org/wiki/Authentication\n")


if __name__ == "__main__":
    main()
