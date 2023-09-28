.. MediaWikiAPI documentation master file, created by
   sphinx-quickstart on Sun Dec 17 17:54:47 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MediaWikiAPI's documentation!
========================================

Release v\ |version|.

.. image:: https://img.shields.io/pypi/v/mediawikiapi.svg
    :target: https://pypi.python.org/pypi/mediawikiapi

.. image:: https://img.shields.io/pypi/pyversions/mediawikiapi.svg
    :target: https://pypi.python.org/pypi/mediawikiapi

.. image:: https://github.com/lehinevych/MediaWikiAPI/workflows/Python%20package/badge.svg?branch=master
    :target: https://github.com/lehinevych/MediaWikiAPI/workflows/Python%20package/badge.svg?branch=master

.. image:: https://img.shields.io/github/issues/lehinevych/MediaWikiAPI.svg
    :target: https://github.com/lehinevych/MediaWikiAPI/issues

.. image:: https://img.shields.io/badge/license-MIT%20License-brightgreen.svg
    :target: https://opensource.org/licenses/MIT


Installation
=============
Start using wikipedia for Python in less than 1 minute!
MediaWikiAPI is compatible with Python > 3.9
If you are looking for the the full developer API, see :ref:`api`.

Begin by installing wikipedia::

	$ pip install mediawikiapi

As alternative you can use the source code from `Github <https://github.com/lehinevych/MediaWikiAPI>`_.

Quickstart
============
Now let's use the MediaWikiAPI. First you need to import the package and create MediaWikiAPI class.
In order to use search and suggestion call the corresponding methods ``search`` and ``suggest``::

  >>> from mediawikiapi import MediaWikiAPI
  >>> mediawikiapi = MediaWikiAPI()
  >>> mediawikiapi.search("Barack")
	[u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

  >>> mediawikiapi.suggest("Barak Obama") # returns the suggested Wikipedia title for a query or None
	u'Barack Obama'

We can also get fewer or more results by using the ``results`` kwarg::

	>>> mediawikiapi.search("Ford", results=3)
	[u'Ford Motor Company', u'Gerald Ford', u'Henry Ford']

To get the summary of an article, use ``mediawikiapi.summary``::

	>>> mediawikiapi.summary("GitHub")
	2011, GitHub was the most popular open source code repository site.\nGitHub Inc. was founded in 2008 and is based in San Francisco, California.\nIn July 2012, the company received $100 million in Series A funding, primarily from Andreessen Horowitz.'

	>>> mediawikiapi.summary("Apple III", sentences=1)
	u'The Apple III (often rendered as Apple ///) is a business-oriented personal computer produced and released by Apple Computer that was intended as the successor to the Apple II series, but largely considered a failure in the market. '

``mediawikiapi.page`` enables you to load and access data from full Wikipedia pages. Initialize with a page title (keep in mind the errors listed above), and then access most properties using property methods::

	>>> ny = mediawikiapi.page("New York (state)")

	>>> ny.title
	u'New York (state)'

	>>> ny.url
	u'http://en.wikipedia.org/wiki/New_York_(state)'

	>>> ny.content
	u'New York is a state in the northeastern United States. New York was one of the original thir'...

	>>> ny.images[0]
	u'http://upload.wikimedia.org/wikipedia/commons/9/91/New_York_quarter%2C_reverse_side%2C_2001.jpg'

	>>> ny.links[0]
	u'1790 United States Census'

To change the language of the Wikipedia you are accessing, use ``mediawikiapi.conf.language``.
Remember to search for page titles in the language that you have set, not English!::

	>>> mediawikiapi.config.language = "fr"

	>>> print mediawikiapi.summary("Francois Hollande")
	François Hollande, né le 12 août 1954 à Rouen, en Seine-Maritime, est un homme d'État français. Il est président de la République française depuis le 15 mai 2012...

To get a list of all possible language prefixes, try ``mediawikiapi.languages()``.

Exception handling example::

	>>> import mediawikiapi
	>>> mediawiki = mediawikiapi.MediaWikiAPI()
	>>> try:
	>>>    print("Getting page")
	>>>    page = mediawiki.page("!!!123123 page title")
	>>> except mediawikiapi.exceptions.PageError:
	>>>    print("Got page error, skipping")


The library can be used for other Mediawiki installs and sites with the same API.

	>>> import mediawikiapi
	>>> mediawiki = mediawikiapi.MediaWikiAPI(config=Config(mediawiki_url="https://{}.wiktionary.org/w/api.php"))

For more details and configuration option check API section.


Changelog
=========

.. toctree::

   changelog

API
====

Here you can find the full developer API for the MediaWikiAPI project.

Please note that some functionality available only for MediaWiki version 1.34 or higher 
For instance: `content`, `infobox`, `parent_id`, `revision_id`, and `summary` 


.. toctree::

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
