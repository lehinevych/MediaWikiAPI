.. _changelog:

Changelog
***************************

Here you can find the full developer API for the MediaWikiAPI project.

Contents:

.. toctree::

   changelog


Version 1.1.5
=============
* Fix the bug with pip install on Windows
* Fix setup.py to not fail if file doesn't exist


Version 1.1.4
=============
* Split `requirements.txt` and upgrade dependencies versions.
* Add support for python 3.7
* Add `infobox` property to `wikipediapage` class


Version 1.1.3
=============

* Add `category member <https://www.mediawiki.org/wiki/API:Categorymembers>`_ query support by `PR #24 <https://github.com/lehinevych/MediaWikiAPI/pull/24>`_
* Add backlinks to WikipediaPage `PR #22 <https://github.com/lehinevych/MediaWikiAPI/pull/22>`_
* Fix missing self reference `PR #11 <https://github.com/lehinevych/MediaWikiAPI/pull/11>`_ by @danielunderwood
* Fix dependencies installable from setup.py `PR #12 <https://github.com/lehinevych/MediaWikiAPI/pull/12>`_ by @danielunderwood
* Fix the hangs of the continuing queries `PR #21 <https://github.com/lehinevych/MediaWikiAPI/pull/21>`_

Version 1.1
============

* **Breaking change** - add MediaWikiAPI class, now you can have more than one api access point with different configurations (Config instances).
  MediaWikiAPI class contains all the mediawikiapi function from version 1.0. The Config class cloud be pass as parameter during initialization.
* Support python 2
* Rename Configuration class to Config, add language field
* Config().get_api_url now accept language parameter
* Add timeout for requests, field in Config class called timeout (in seconds).
* Makes the pagepropsof a wikipedia page accessible `PR #147 <https://github.com/goldsmith/Wikipedia/pull/147>`_ from @goldsmith repo.
* Fix suggestion, issue `#108 <https://github.com/goldsmith/Wikipedia/issues/108>`_ by `PR #131 <https://github.com/goldsmith/Wikipedia/pull/131>`_ from @goldsmith repo.
* Fix problem with hidden files in the article `PR #132 <https://github.com/goldsmith/Wikipedia/pull/132/files>`_ @goldsmith repo.
* DisambiguationError contains now information about title and url `PR #92 <https://github.com/goldsmith/Wikipedia/pull/92>`_ from @goldsmith repo.
* Fix issue where pageid request => redirect raises error `PR #165 <https://github.com/goldsmith/Wikipedia/pull/165>`_

Version 1.0
============

* Fork `Wikipedia <https://github.com/goldsmith/Wikipedia>`_
* Add language validation for mediawikiapi.set_lang
* Add lang title method to WikipediaPage
* Add re-usage the same requests session
* Fix installing error with version
* Fix WikipediaPage.sections
* Fix mock data
* Refactoring: seperate Language and Configuration classes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
