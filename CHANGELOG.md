# Changelog

## Current

* *Breaking change* - add MediaWikiAPI and WikiRequest classes, now you can have more than one api access point with different configurations. MediaWikiAPI class contains all the mediawikiapi function from version 1. The Config class cloud be pass  as parameter during initialization. Every MediaWikiAPI class contains WikiRequest class - the wrapper over requests lib to perform the queries within one session with defined params in Config class. Please check API docs.
* Support python 2
* Rename Configuration class to Config, add language field
* Config().get_api_url now accept language parameter
* Add timeout for requests, field in Config class called timeout (in seconds).
* Fix suggestion, issue [#108](https://github.com/goldsmith/Wikipedia/issues/108) by [PR #131](https://github.com/goldsmith/Wikipedia/pull/131) from @goldsmith repo.
* Fixed problem with hidden files in the article [PR #132](https://github.com/goldsmith/Wikipedia/pull/132/files) @goldsmith repo.
* DisambiguationError contains now information about title and url [PR #92](https://github.com/goldsmith/Wikipedia/pull/92) from @goldsmith repo.


## Version 1

* Fork [Wikipedia](https://github.com/goldsmith/Wikipedia)
* Add language validation for mediawikiapi.set_lang
* Add lang title method to WikipediaPage
* Add re-usage the same requests session
* Fix installing error with version
* Fix WikipediaPage.sections
* Fix mock data
* Refactoring: seperate Language and Configuration classes
