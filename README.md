MediaWikiAPI
===================

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

``` python
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

Installation
------------

To install MediaWikiAPI, simply run:

``` bash
pip install mediawikiapi
```
MediaWikiAPI is compatible with Python 3.


Changelog
-------------
[Changelog](http://mediawikiapi.readthedocs.io/en/latest/changelog.html) could be find in the documentation.


Documentation
-------------
The documentation is available [here](http://mediawikiapi.readthedocs.io/en/latest/)


To run tests, clone the [repository on GitHub](https://github.com/lehinevych/MediaWikiAPI), then run:

```bash
poetry install 
poetry build
poetry run pytest --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=mediawikiapi
```
in the root project directory.

To build the documentation yourself, after installing requirements.txt, run:

``` bash
pip install sphinx
cd docs/
make html
```

To run formatter and mypy run:

```
poetry run mypy --strict .
poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
poetry run black --diff --check .
```

To build the documentation run:
```
poetry run sphinx-build docs/source docs/build
```

License
-------

MIT licensed. See the [LICENSE file](https://github.com/lehinevych/MediaWikiAPI/blob/master/LICENSE) for
full details.

Credits
-------
-  @goldsmith for making such a fantastic library to fork
