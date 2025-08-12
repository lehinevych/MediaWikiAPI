# MediaWikiAPI

[![PyPI version](https://img.shields.io/pypi/v/mediawikiapi.svg)](https://pypi.python.org/pypi/mediawikiapi)
[![Version](https://img.shields.io/pypi/pyversions/mediawikiapi.svg)](https://pypi.python.org/pypi/mediawikiapi)
![Python package](https://github.com/lehinevych/MediaWikiAPI/workflows/Python%20package/badge.svg?branch=master)
[![GitHub Issues](https://img.shields.io/github/issues/lehinevych/MediaWikiAPI.svg)](https://github.com/lehinevych/MediaWikiAPI/issues)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://readthedocs.org/projects/mediawikiapi/badge/?version=latest)](https://mediawikiapi.readthedocs.io/en/latest/)

**MediaWikiAPI** is a Python library that makes it easy to access and parse
data from Wikipedia.

Search Wikipedia, get article summaries, get data like links and images
from a page, and more. Wikipedia wraps the [MediaWiki API](https://www.mediawiki.org/wiki/API) so you can focus on using
Wikipedia data, not getting it.

Supports both synchronous and asynchronous usage patterns.

MediaWikiAPI is compatible with Python 3.9+.

## Examples

For complete examples of using the library, see the examples folder:

- [Synchronous example](examples/sync_example.py) - Shows how to use the synchronous MediaWikiAPI
- [Asynchronous example](examples/async_example.py) - Shows how to use the asynchronous AsyncMediaWikiAPI

## Synchronous Usage

```python
>>> from mediawikiapi import MediaWikiAPI
>>> mediawikiapi = MediaWikiAPI()
>>> print(mediawikiapi.summary("Wikipedia"))
# Wikipedia (/ˌwɪkɨˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

>>> mediawikiapi.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

>>> ny = mediawikiapi.page("New York (state)")
>>> ny.title
# u'New York (state)'
>>> ny.url
# u'http://en.wikipedia.org/wiki/New_York_(state)'
>>> ny.content
# u'New York is a state in the northeastern United States. New York was one of the original thir'...
>>> ny.links[0]
# u'1790 United States Census'

>>> mediawikiapi.config.language = "fr"
>>> mediawikiapi.summary("Facebook", sentences=1)
# Facebook est un service de réseautage social en ligne sur Internet permettant d'y publier des informations (photographies, liens, textes, etc.) en contrôlant leur visibilité par différentes catégories de personnes.
```

## Asynchronous Usage

The library also provides async versions of all functionality:

```python
import asyncio
from mediawikiapi import AsyncMediaWikiAPI

async def main():
    # Use as a context manager to automatically close session
    async with AsyncMediaWikiAPI() as api:
        # Basic search
        results = await api.search("Python programming")
        print(f"Search results: {results[:5]}")

        # Get page and properties
        page = await api.page("Python (programming language)")
        print(f"Page URL: {page.url}")

        # Get summary
        summary = await page.summary
        print(f"Summary: {summary[:200]}...")

        # Get page links
        links = await page.links
        print(f"First 5 links: {links[:5]}")

        # Get images
        images = await page.images
        print(f"First image: {images[0] if images else 'No images'}")

# Run the async function
asyncio.run(main())
```

## Installation

To install MediaWikiAPI, simply run:

```bash
pip install mediawikiapi
```

## Changelog

[Changelog](http://mediawikiapi.readthedocs.io/en/latest/changelog.html) could be find in the documentation.

## Documentation

The documentation is available [here](http://mediawikiapi.readthedocs.io/en/latest/)

To run tests, clone the [repository on GitHub](https://github.com/lehinevych/MediaWikiAPI), then run:

```bash
# Install uv if not already installed
curl -sSf https://astral.sh/uv/install.sh | sh

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and run tests
./scripts.py install-dev
./scripts.py test
```

in the root project directory.

To build the documentation yourself, run:

```bash
./scripts.py install-docs
./scripts.py build-docs
```

Or manually:

```bash
uv pip install -e ".[docs]"
sphinx-build docs/source docs/build
```

To run formatter and linting tools:

```bash
./scripts.py format-check
./scripts.py typecheck
./scripts.py lint
```

Or manually:

```bash
mypy --strict .
ruff check .
ruff format --check .
```

To set up pre-commit hooks for automatic linting and formatting:

```bash
./setup-hooks.py
```

## License

MIT licensed. See the [LICENSE file](https://github.com/lehinevych/MediaWikiAPI/blob/master/LICENSE) for
full details.

## Credits

- @goldsmith for making such a fantastic library to for
