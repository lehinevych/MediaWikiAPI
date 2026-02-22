"""
Example of using Personal Access Token authentication with MediaWikiAPI.

Wikimedia API supports Personal Access Tokens for authentication.
See: https://api.wikimedia.org/wiki/Authentication

This example shows how to configure MediaWikiAPI with:
1. Personal Access Token authentication
2. Custom HTTP headers
"""

from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config

# Example 1: Using Personal Access Token
# Get your token from: https://api.wikimedia.org/
access_token = "your_personal_access_token_here"

config_with_token = Config(access_token=access_token)
api_with_auth = MediaWikiAPI(config=config_with_token)

# Now all requests will include: Authorization: Bearer <token>
# page = api_with_auth.page("Python (programming language)")
# print(page.summary)


# Example 2: Using custom headers
custom_headers = {
    "X-Custom-Header": "my-value",
    "Accept-Language": "en-US",
}

config_with_headers = Config(custom_headers=custom_headers)
api_with_headers = MediaWikiAPI(config=config_with_headers)


# Example 3: Combining access token with custom headers
config_combined = Config(
    access_token=access_token,
    custom_headers={
        "X-Application-Name": "MyWikipediaBot",
        "X-Application-Version": "1.0.0",
    },
)
api_combined = MediaWikiAPI(config=config_combined)


# Example 4: Override default User-Agent
config_custom_ua = Config(
    custom_headers={"User-Agent": "MyCustomBot/1.0 (contact@example.com)"}
)
api_custom_ua = MediaWikiAPI(config=config_custom_ua)


# Example 5: Using with Wikimedia API (not Wikipedia)
# For authenticated requests to Wikimedia API endpoints
config_wikimedia = Config(
    mediawiki_url="https://api.wikimedia.org/core/v1/wikipedia/en/",
    access_token=access_token,
)
# Note: Wikimedia API has different endpoints and response formats
# This is just an example of how to configure authentication


if __name__ == "__main__":
    print("Authentication examples loaded successfully!")
    print("\nConfiguration with access token:")
    print(f"  Headers: {config_with_token.get_headers()}")
    print("\nConfiguration with custom headers:")
    print(f"  Headers: {config_with_headers.get_headers()}")
    print("\nCombined configuration:")
    print(f"  Headers: {config_combined.get_headers()}")
