# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, Tuple, Any, List

mock_wiki_calls: Dict[Tuple, Dict[str, Any]] = {  # type: ignore
    (
        ("explaintext", ""),
        ("prop", "extracts|revisions"),
        ("rvprop", "ids"),
        ("titles", "Celtuce"),
    ): {
        "query": {
            "pages": {
                "1868108": {
                    "extract": 'Celtuce (Lactuca sativa var. asparagina, augustana, or angustata), also called stem lettuce, celery lettuce, asparagus lettuce, or Chinese lettuce, IPA (UK,US) /\u02c8s\u025blt.\u0259s/, is a cultivar of lettuce grown primarily for its thick stem, used as a vegetable. It is especially popular in China, and is called wosun (Chinese: \u83b4\u7b0b; pinyin: w\u014ds\u016dn) or woju (Chinese: \u83b4\u82e3; pinyin: w\u014dj\xf9) (although the latter name may also be used to mean lettuce in general).\n\nThe stem is usually harvested at a length of around 15\u201320 cm and a diameter of around 3\u20134 cm. It is crisp, moist, and mildly flavored, and typically prepared by slicing and then stir frying with more strongly flavored ingredients.\n\nDown: Photos of the celtuce, chinese lettuce or "Wosun" taken in the province of Girona (Catalonia, Spain, Europe) in June 2013\nCeltuce Nutritional content',
                    "ns": 0,
                    "pageid": 1868108,
                    "revisions": [{"revid": 575687826, "parentid": 574302108}],
                    "title": "Celtuce",
                }
            }
        }
    },
    (
        ("explaintext", ""),
        ("prop", "extracts|revisions"),
        ("rvprop", "ids"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "extract": 'Tropical Depression Ten was the tenth tropical cyclone of the record-breaking 2005 Atlantic hurricane season. It formed on August 13 from a tropical wave that emerged from the west coast of Africa on August 8. As a result of strong wind shear, the depression remained weak and did not strengthen beyond tropical depression status. The cyclone degenerated on August 14, although its remnants partially contributed to the formation of Tropical Depression Twelve, which eventually intensified into Hurricane Katrina. The cyclone had no effect on land, and did not directly result in any fatalities or damage.\n\n\n== Meteorological history ==\n\nOn August 8, a tropical wave emerged from the west coast of Africa and entered the Atlantic Ocean. Tracking towards the west, the depression began to exhibit signs of convective organization on August 11. The system continued to develop, and it is estimated that Tropical Depression Ten formed at 1200 UTC on August 13. At the time, it was located about 1,600 miles (2,600 km) east of Barbados. Upon its designation, the depression consisted of a large area of thunderstorm activity, with curved banding features and expanding outflow. However, the environmental conditions were predicted to quickly become unfavorable. The depression moved erratically and slowly towards the west, and wind shear inhibited any significant intensification. Late on August 13, it was "beginning to look like Irene-junior as it undergoes southwesterly mid-level shear beneath the otherwise favorable upper-level outflow pattern". The wind shear was expected to relent within 48 hours, prompting some forecast models to suggest the depression would eventually attain hurricane status.\nBy early August 14, the shear had substantially disrupted the storm, leaving the low-level center of circulation exposed from the area of convection, which was also deteriorating. After meandering, the storm began to move westward. Forecasters expected it to resume a northwestward track as high pressure to the south of Bermuda was forecasted to weaken and another high was predicted to form southwest of the Azores. By 1800 UTC on August 14, the strong shear had further weakened the storm, and it no longer met the criteria for a tropical cyclone. It degenerated into a remnant low, and the National Hurricane Center issued their final advisory on the cyclone. Moving westward, it occasionally produced bursts of convective activity, before dissipating on August 18.\nTropical Depression Twelve formed over the southeastern Bahamas at 2100 UTC on August 23, partially from the remains of Tropical Depression Ten. While the normal standards for numbering tropical depressions in the Atlantic stipulate that the initial designation be retained when a depression regenerates, satellite imagery indicated that a second tropical wave had combined with Tropical Depression Ten north of Puerto Rico to form a new, more complex weather system, which was then designated as Tropical Depression Twelve. In a re-analysis, it was found that the low-level circulation of Tropical Depression Ten had completely detached and dissipated; only the remnant mid-level circulation moved on and merged with the second tropical wave. As a result, the criteria for keeping the same name and identity were not met. Tropical Depression Twelve later became Hurricane Katrina.\n\n\n== Impact ==\nBecause Tropical Depression Ten never approached land as a tropical cyclone, no tropical cyclone watches and warnings were issued for any land masses. No effects, damages, or fatalities were reported, and no ships reported tropical storm-force winds in association with the depression. The system did not attain tropical storm status; as such, it was not given a name by the National Hurricane Center. The storm partially contributed to the formation of Hurricane Katrina, which became a Category 5 hurricane on the Saffir-Simpson Hurricane Scale and made landfall in Louisiana, causing catastrophic damage. Katrina was the costliest hurricane, and one of the five deadliest, in the history of the United States.\n\n\n== See also ==\n\nMeteorological history of Hurricane Katrina\nList of storms in the 2005 Atlantic hurricane season\nTimeline of the 2005 Atlantic hurricane season\n\n\n== References ==\n\n\n== External links ==\n\nTropical Depression Ten Tropical Cyclone Report\nTropical Depression Ten advisory archive',
                    "ns": 0,
                    "pageid": 21196082,
                    "revisions": [{"revid": 572715399, "parentid": 539367750}],
                    "title": "Tropical Depression Ten (2005)",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "purpleberry"),
    ): {
        "query": {
            "normalized": [{"to": "Purpleberry", "from": "purpleberry"}],
            "pages": {
                "-1": {
                    "missing": "",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Purpleberry&action=edit",
                    "title": "Purpleberry",
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Purpleberry",
                }
            },
        }
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "Menlo Park, New Jersey"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {"search": [{"ns": 0, "title": "Edison, New Jersey"}]},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Menlo Park, New Jersey"),
    ): {
        "query": {
            "redirects": [
                {"to": "Edison, New Jersey", "from": "Menlo Park, New Jersey"}
            ],
            "pages": {
                "125414": {
                    "lastrevid": 607768264,
                    "pageid": 125414,
                    "title": "Edison, New Jersey",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Edison,_New_Jersey&action=edit",
                    "counter": "",
                    "length": 85175,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-05-14T17:10:49Z",
                    "ns": 0,
                    "fullurl": "https://en.wikipedia.org/wiki/Edison,_New_Jersey",
                }
            },
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Communist Party"),
    ): {
        "query": {
            "redirects": [{"to": "Communist party", "from": "Communist Party"}],
            "pages": {
                "37008": {
                    "lastrevid": 608086859,
                    "pageid": 37008,
                    "title": "Communist party",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Communist_party&action=edit",
                    "counter": "",
                    "length": 7868,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-05-26T01:19:01Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Communist_party",
                }
            },
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "communist Party"),
    ): {
        "query": {
            "redirects": [{"to": "Communist party", "from": "Communist Party"}],
            "normalized": [{"to": "Communist Party", "from": "communist Party"}],
            "pages": {
                "37008": {
                    "lastrevid": 608086859,
                    "pageid": 37008,
                    "title": "Communist party",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Communist_party&action=edit",
                    "counter": "",
                    "length": 7868,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-05-26T01:19:01Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Communist_party",
                }
            },
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Communist party"),
    ): {
        "query": {
            "pages": {
                "37008": {
                    "lastrevid": 608086859,
                    "pageid": 37008,
                    "title": "Communist party",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Communist_party&action=edit",
                    "counter": "",
                    "length": 7868,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-05-26T01:19:01Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Communist_party",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Edison, New Jersey"),
    ): {
        "query": {
            "pages": {
                "125414": {
                    "lastrevid": 607768264,
                    "pageid": 125414,
                    "title": "Edison, New Jersey",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Edison,_New_Jersey&action=edit",
                    "counter": "",
                    "length": 85175,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-05-14T17:10:49Z",
                    "ns": 0,
                    "fullurl": "https://en.wikipedia.org/wiki/Edison,_New_Jersey",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Dodge Ram (disambiguation)"),
    ): {
        "query": {
            "pages": {
                "18803364": {
                    "lastrevid": 567152802,
                    "pageid": 18803364,
                    "title": "Dodge Ram (disambiguation)",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Dodge_Ram_(disambiguation)&action=edit",
                    "counter": "",
                    "length": 702,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2013-08-08T15:12:27Z",
                    "ns": 0,
                    "pageprops": {"disambiguation": ""},
                    "fullurl": "http://en.wikipedia.org/wiki/Dodge_Ram_(disambiguation)",
                }
            }
        }
    },
    (
        ("prop", "revisions"),
        ("rvlimit", 1),
        ("rvparse", ""),
        ("rvprop", "content"),
        ("titles", "Dodge Ram (disambiguation)"),
    ): {
        "query-continue": {"revisions": {"rvcontinue": 556603298}},
        "query": {
            "pages": {
                "18803364": {
                    "ns": 0,
                    "pageid": 18803364,
                    "revisions": [
                        {
                            "*": '<p><b><a href="/wiki/Dodge_Ram" title="Dodge Ram">Dodge Ram</a></b> is a collective nameplate for light trucks made by <a href="/wiki/Dodge" title="Dodge">Dodge</a>\n</p>\n<ul><li><a href="/wiki/Dodge_Ramcharger" title="Dodge Ramcharger">Dodge Ramcharger</a> - full-size SUV based on the Ram chassis (first vehicle to use the Ram name)\n</li><li><a href="/wiki/Dodge_Ram_Van" title="Dodge Ram Van">Dodge Ram Van</a> - full-size van\n</li><li><a href="/wiki/Dodge_Mini_Ram" title="Dodge Mini Ram" class="mw-redirect">Dodge Mini Ram</a> - cargo version of the Dodge Caravan\n<ul><li>See also:\n<ul><li><a href="/wiki/Dodge_Caravan_C/V" title="Dodge Caravan C/V" class="mw-redirect">Dodge Caravan C/V</a>\n</li><li><a href="/wiki/Ram_C/V" title="Ram C/V" class="mw-redirect">Ram C/V</a> (modern day equivalent)\n</li></ul>\n</li></ul>\n</li><li><a href="/wiki/Dodge_Ram_50" title="Dodge Ram 50" class="mw-redirect">Dodge Ram 50</a> - Dodge version of the Mitsubishi Mighty Max, predecessor to the Dakota\n</li></ul>\n<p>See also:\n</p>\n<ul><li><a href="/wiki/Dodge_D-Series" title="Dodge D-Series" class="mw-redirect">Dodge D-Series</a> - Ram\'s predecessor, page includes first Ram body style\n</li><li><a href="/wiki/Dodge_Rampage" title="Dodge Rampage">Dodge Rampage</a> - car-based pickup truck\n</li><li><a href="/wiki/Ram_Trucks" title="Ram Trucks">Ram (brand)</a> - truck brand based on the Ram pickup truck\n</li></ul>\n<table id="disambigbox" class="metadata plainlinks dmbox dmbox-disambig" style="" role="presentation">\n<tr>\n<td class="mbox-image" style="padding: 2px 0 2px 0.4em;"> <a href="/wiki/File:Disambig_gray.svg" class="image"><img alt="Disambiguation icon" src="//upload.wikimedia.org/wikipedia/en/thumb/5/5f/Disambig_gray.svg/30px-Disambig_gray.svg.png" width="30" height="23" srcset="//upload.wikimedia.org/wikipedia/en/thumb/5/5f/Disambig_gray.svg/45px-Disambig_gray.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/5/5f/Disambig_gray.svg/60px-Disambig_gray.svg.png 2x" /></a></td>\n<td class="mbox-text" style="padding: 0.25em 0.4em; font-style: italic;"> This <a href="/wiki/Help:Disambiguation" title="Help:Disambiguation">disambiguation</a> page lists articles associated with the same title. <br/> <small>If an <a class="external text" href="//en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/Dodge_Ram_(disambiguation)&amp;namespace=0">internal link</a> led you here, you may wish to change the link to point directly to the intended article.</small> </td>\n</tr>\n</table>\n'
                        }
                    ],
                    "title": "Dodge Ram (disambiguation)",
                }
            }
        },
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "butteryfly"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {
            "searchinfo": {"suggestion": "butterfly"},
            "search": [{"ns": 0, "title": "Butterfly's Tongue"}],
        },
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "butterfly"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {"search": [{"ns": 0, "title": "Butterfly"}]},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Butterfly"),
    ): {
        "query": {
            "pages": {
                "48338": {
                    "lastrevid": 566847704,
                    "pageid": 48338,
                    "title": "Butterfly",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Butterfly&action=edit",
                    "counter": "",
                    "length": 60572,
                    "contentmodel": "wikitext",
                    "    pagelanguage": "en",
                    "touched": "2013-08-07T11:15:37Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Butterfly",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "butterfly"),
    ): {
        "query": {
            "normalized": [{"to": "Butterfly", "from": "butterfly"}],
            "pages": {
                "48338": {
                    "lastrevid": 566847704,
                    "pageid": 48338,
                    "title": "Butterfly",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Butterfly&action=edit",
                    "counter": "",
                    "length": 60572,
                    "contentmodel": "wikitext",
                    "    pagelanguage": "en",
                    "touched": "2013-08-07T11:15:37Z",
                    "ns": 0,
                    "fullurl": "https://en.wikipedia.org/wiki/Butterfly",
                }
            },
        }
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "Celtuce"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {"search": [{"ns": 0, "title": "Celtuce"}]},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "Tropical Depression Ten (2005)"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {"search": [{"ns": 0, "title": "Tropical Depression Ten (2005)"}]},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 1),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 1),
        ("srprop", ""),
        ("srsearch", "Great Wall of China"),
    ): {
        "query-continue": {"search": {"sroffset": 1}},
        "query": {"search": [{"ns": 0, "title": "Great Wall of China"}]},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Celtuce"),
    ): {
        "query": {
            "pages": {
                "1868108": {
                    "lastrevid": 562756085,
                    "pageid": 1868108,
                    "title": "Celtuce",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Celtuce&action=edit",
                    "counter": "",
                    "length": 1662,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2013-08-17T03:30:23Z",
                    "ns": 0,
                    "fullurl": "https://en.wikipedia.org/wiki/Celtuce",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "lastrevid": 572715399,
                    "pageid": 21196082,
                    "title": "Tropical Depression Ten (2005)",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Tropical_Depression_Ten_(2005)&action=edit",
                    "counter": "",
                    "length": 8543,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2013-09-18T13:45:33Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Tropical_Depression_Ten_(2005)",
                }
            }
        }
    },
    (
        ("inprop", "url"),
        ("prop", "info|pageprops"),
        ("redirects", ""),
        ("titles", "Great Wall of China"),
    ): {
        "query": {
            "pages": {
                "5094570": {
                    "lastrevid": 604138653,
                    "pageid": 5094570,
                    "title": "Great Wall of China",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Great_Wall_of_China&action=edit",
                    "counter": "",
                    "length": 23895,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2013-08-17T03:30:23Z",
                    "ns": 0,
                    "fullurl": "http://en.wikipedia.org/wiki/Great_Wall_of_China",
                }
            }
        }
    },
    (("explaintext", ""), ("prop", "extracts"), ("titles", "Celtuce")): {
        "query": {
            "pages": {
                "1868108": {
                    "extract": "Celtuce (Lactuca sativa var. asparagina, augustana, or angustata), also called stem lettuce, celery lettuce, asparagus lettuce, or Chinese lettuce, IPA (UK,US) /\u02c8s\u025blt.\u0259s/, is a cultivar of lettuce grown primarily for its thick stem, used as a vegetable. It is especially popular in China, and is called wosun (Chinese: \u83b4\u7b0b; pinyin: w\u014ds\u016dn) or woju (Chinese: \u83b4\u82e3; pinyin: w\u014dj\xf9) (although the latter name may also be used to mean lettuce in general).\n\nThe stem is usually harvested at a length of around 15\u201320 cm and a diameter of around 3\u20134 cm. It is crisp, moist, and mildly flavored, and typically prepared by slicing and then stir frying with more strongly flavored ingredients.",
                    "ns": 0,
                    "pageid": 1868108,
                    "title": "Celtuce",
                }
            }
        }
    },
    (
        ("exintro", ""),
        ("explaintext", ""),
        ("prop", "extracts"),
        ("titles", "Celtuce"),
    ): {
        "query": {
            "pages": {
                "1868108": {
                    "extract": "Celtuce (Lactuca sativa var. asparagina, augustana, or angustata), also called stem lettuce, celery lettuce, asparagus lettuce, or Chinese lettuce, IPA (UK,US) /\u02c8s\u025blt.\u0259s/, is a cultivar of lettuce grown primarily for its thick stem, used as a vegetable. It is especially popular in China, and is called wosun (Chinese: \u83b4\u7b0b; pinyin: w\u014ds\u016dn) or woju (Chinese: \u83b4\u82e3; pinyin: w\u014dj\xf9) (although the latter name may also be used to mean lettuce in general).\n\nThe stem is usually harvested at a length of around 15\u201320 cm and a diameter of around 3\u20134 cm. It is crisp, moist, and mildly flavored, and typically prepared by slicing and then stir frying with more strongly flavored ingredients.",
                    "ns": 0,
                    "pageid": 1868108,
                    "title": "Celtuce",
                }
            }
        }
    },
    (
        ("exintro", ""),
        ("explaintext", ""),
        ("prop", "extracts"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "extract": "Tropical Depression Ten was the tenth tropical cyclone of the record-breaking 2005 Atlantic hurricane season. It formed on August 13 from a tropical wave that emerged from the west coast of Africa on August 8. As a result of strong wind shear, the depression remained weak and did not strengthen beyond tropical depression status. The cyclone degenerated on August 14, although its remnants partially contributed to the formation of Tropical Depression Twelve, which eventually intensified into Hurricane Katrina. The cyclone had no effect on land, and did not directly result in any fatalities or damage.\n\n",
                    "ns": 0,
                    "pageid": 21196082,
                    "title": "Tropical Depression Ten (2005)",
                }
            }
        }
    },
    (
        ("generator", "images"),
        ("gimlimit", "max"),
        ("iiprop", "url"),
        ("prop", "imageinfo"),
        ("titles", "Celtuce"),
    ): {
        "query": {
            "pages": {
                "22263385": {
                    "imagerepository": "local",
                    "ns": 6,
                    "pageid": 22263385,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/en/9/99/Question_book-new.svg",
                            "descriptionurl": "http://en.wikipedia.org/wiki/File:Question_book-new.svg",
                        }
                    ],
                    "title": "File:Question book-new.svg",
                },
                "-1": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/8/87/Celtuce.jpg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Celtuce.jpg",
                        }
                    ],
                    "missing": "",
                    "title": "File:Celtuce.jpg",
                },
                "-3": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/7/79/VegCorn.jpg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:VegCorn.jpg",
                        }
                    ],
                    "missing": "",
                    "title": "File:VegCorn.jpg",
                },
                "-2": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/d/dc/The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg",
                        }
                    ],
                    "missing": "",
                    "title": "File:The farmer's market near the Potala in Lhasa.jpg",
                },
            }
        },
        "limits": {"images": 500},
    },
    (
        ("generator", "images"),
        ("gimlimit", "max"),
        ("iiprop", "url"),
        ("prop", "imageinfo"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "33285577": {
                    "imagerepository": "local",
                    "ns": 6,
                    "pageid": 33285577,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg",
                            "descriptionurl": "http://en.wikipedia.org/wiki/File:Commons-logo.svg",
                        }
                    ],
                    "title": "File:Commons-logo.svg",
                },
                "23473511": {
                    "imagerepository": "local",
                    "ns": 6,
                    "pageid": 23473511,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/en/4/48/Folder_Hexagonal_Icon.svg",
                            "descriptionurl": "http://en.wikipedia.org/wiki/File:Folder_Hexagonal_Icon.svg",
                        }
                    ],
                    "title": "File:Folder Hexagonal Icon.svg",
                },
                "33285464": {
                    "imagerepository": "local",
                    "ns": 6,
                    "pageid": 33285464,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/en/e/e7/Cscr-featured.svg",
                            "descriptionurl": "http://en.wikipedia.org/wiki/File:Cscr-featured.svg",
                        }
                    ],
                    "title": "File:Cscr-featured.svg",
                },
                "2526001": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "pageid": 2526001,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/8/89/Cyclone_Catarina_from_the_ISS_on_March_26_2004.JPG",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Cyclone_Catarina_from_the_ISS_on_March_26_2004.JPG",
                        }
                    ],
                    "title": "File:Cyclone Catarina from the ISS on March 26 2004.JPG",
                },
                "33285257": {
                    "imagerepository": "local",
                    "ns": 6,
                    "pageid": 33285257,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/en/f/fd/Portal-puzzle.svg",
                            "descriptionurl": "http://en.wikipedia.org/wiki/File:Portal-puzzle.svg",
                        }
                    ],
                    "title": "File:Portal-puzzle.svg",
                },
                "-5": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/8/89/Symbol_book_class2.svg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Symbol_book_class2.svg",
                        }
                    ],
                    "missing": "",
                    "title": "File:Symbol book class2.svg",
                },
                "-4": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/4/47/Sound-icon.svg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Sound-icon.svg",
                        }
                    ],
                    "missing": "",
                    "title": "File:Sound-icon.svg",
                },
                "-7": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/7/7d/Tropical_Depression_10_%282005%29.png",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Tropical_Depression_10_(2005).png",
                        }
                    ],
                    "missing": "",
                    "title": "File:Tropical Depression 10 (2005).png",
                },
                "-6": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/4/4a/TD_10_August_13%2C_2005.jpg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:TD_10_August_13,_2005.jpg",
                        }
                    ],
                    "missing": "",
                    "title": "File:TD 10 August 13, 2005.jpg",
                },
                "-1": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/a/a5/10-L_2005_track.png",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:10-L_2005_track.png",
                        }
                    ],
                    "missing": "",
                    "title": "File:10-L 2005 track.png",
                },
                "-3": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/3/37/People_icon.svg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:People_icon.svg",
                        }
                    ],
                    "missing": "",
                    "title": "File:People icon.svg",
                },
                "-2": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/e/e0/2005_Atlantic_hurricane_season_summary_map.png",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:2005_Atlantic_hurricane_season_summary_map.png",
                        }
                    ],
                    "missing": "",
                    "title": "File:2005 Atlantic hurricane season summary map.png",
                },
                "-8": {
                    "imagerepository": "shared",
                    "ns": 6,
                    "imageinfo": [
                        {
                            "url": "http://upload.wikimedia.org/wikipedia/commons/3/33/Tropical_Depression_Ten_%282005%29.ogg",
                            "descriptionurl": "http://commons.wikimedia.org/wiki/File:Tropical_Depression_Ten_(2005).ogg",
                        }
                    ],
                    "missing": "",
                    "title": "File:Tropical Depression Ten (2005).ogg",
                },
            }
        },
        "limits": {"images": 500},
    },
    (("ellimit", "max"), ("prop", "extlinks"), ("titles", "Celtuce")): {
        "query": {
            "pages": {
                "1868108": {
                    "extlinks": [
                        {"*": "http://ndb.nal.usda.gov/ndb/search/list"},
                        {
                            "*": "http://ndb.nal.usda.gov/ndb/search/list?qlookup=11145&format=Full"
                        },
                    ],
                    "ns": 0,
                    "pageid": 1868108,
                    "title": "Celtuce",
                }
            }
        },
        "limits": {"extlinks": 500},
    },
    (
        ("ellimit", "max"),
        ("prop", "extlinks"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "extlinks": [
                        {
                            "*": "http://books.google.com/?id=-a8DRl1HuwoC&q=%22tropical+depression+ten%22+2005&dq=%22tropical+depression+ten%22+2005"
                        },
                        {
                            "*": "http://facstaff.unca.edu/chennon/research/documents/erb_ncur2006_preprint.pdf"
                        },
                        {"*": "http://www.nhc.noaa.gov/archive/2005/TEN.shtml?"},
                        {
                            "*": "http://www.nhc.noaa.gov/archive/2005/dis/al102005.discus.001.shtml?"
                        },
                        {
                            "*": "http://www.nhc.noaa.gov/archive/2005/dis/al102005.discus.002.shtml?"
                        },
                        {
                            "*": "http://www.nhc.noaa.gov/archive/2005/dis/al102005.discus.003.shtml?"
                        },
                        {
                            "*": "http://www.nhc.noaa.gov/archive/2005/dis/al122005.discus.001.shtml"
                        },
                        {"*": "http://www.nhc.noaa.gov/pdf/TCR-AL102005_Ten.pdf"},
                        {"*": "http://www.nhc.noaa.gov/pdf/TCR-AL122005_Katrina.pdf"},
                        {
                            "*": "http://www.wptv.com/content/chopper5/story/Capt-Julie-Reports-On-Hurricane-Katrina/q__v8S2TZES2GiccRTQ2bw.cspx"
                        },
                    ],
                    "ns": 0,
                    "pageid": 21196082,
                    "title": "Tropical Depression Ten (2005)",
                }
            }
        },
        "limits": {"extlinks": 500},
    },
    (
        ("pllimit", "max"),
        ("plnamespace", 0),
        ("prop", "links"),
        ("titles", "Celtuce"),
    ): {
        "query": {
            "pages": {
                "1868108": {
                    "ns": 0,
                    "pageid": 1868108,
                    "links": [
                        {"ns": 0, "title": "Calcium"},
                        {"ns": 0, "title": "Carbohydrate"},
                        {"ns": 0, "title": "Chinese language"},
                        {"ns": 0, "title": "Dietary Reference Intake"},
                        {"ns": 0, "title": "Dietary fiber"},
                        {"ns": 0, "title": "Fat"},
                        {"ns": 0, "title": "Folate"},
                        {"ns": 0, "title": "Food energy"},
                        {"ns": 0, "title": "Iron"},
                        {"ns": 0, "title": "Lettuce"},
                        {"ns": 0, "title": "Lhasa"},
                        {"ns": 0, "title": "Magnesium in biology"},
                        {"ns": 0, "title": "Manganese"},
                        {"ns": 0, "title": "Niacin"},
                        {"ns": 0, "title": "Pantothenic acid"},
                        {"ns": 0, "title": "Phosphorus"},
                        {"ns": 0, "title": "Pinyin"},
                        {"ns": 0, "title": "Plant stem"},
                        {"ns": 0, "title": "Potassium"},
                        {"ns": 0, "title": "Protein (nutrient)"},
                        {"ns": 0, "title": "Riboflavin"},
                        {"ns": 0, "title": "Sodium"},
                        {"ns": 0, "title": "Stir frying"},
                        {"ns": 0, "title": "Thiamine"},
                        {"ns": 0, "title": "Vegetable"},
                        {"ns": 0, "title": "Vitamin A"},
                        {"ns": 0, "title": "Vitamin B6"},
                        {"ns": 0, "title": "Vitamin C"},
                        {"ns": 0, "title": "Zinc"},
                    ],
                    "title": "Celtuce",
                }
            }
        },
        "limits": {"links": 500},
    },
    (
        ("pllimit", "max"),
        ("plnamespace", 0),
        ("prop", "links"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "ns": 0,
                    "pageid": 21196082,
                    "links": [
                        {"ns": 0, "title": "2005 Atlantic hurricane season"},
                        {"ns": 0, "title": "2005 Azores subtropical storm"},
                        {"ns": 0, "title": "Atlantic Ocean"},
                        {"ns": 0, "title": "Atmospheric circulation"},
                        {"ns": 0, "title": "Atmospheric convection"},
                        {"ns": 0, "title": "Azores"},
                        {"ns": 0, "title": "Bahamas"},
                        {"ns": 0, "title": "Bar (unit)"},
                        {"ns": 0, "title": "Barbados"},
                        {"ns": 0, "title": "Bermuda"},
                        {"ns": 0, "title": "High pressure area"},
                        {"ns": 0, "title": "Hurricane Beta"},
                        {"ns": 0, "title": "Hurricane Cindy (2005)"},
                        {"ns": 0, "title": "Hurricane Dennis"},
                        {"ns": 0, "title": "Hurricane Emily (2005)"},
                        {"ns": 0, "title": "Hurricane Epsilon"},
                        {"ns": 0, "title": "Hurricane Irene (2005)"},
                        {"ns": 0, "title": "Hurricane Katrina"},
                        {"ns": 0, "title": "Hurricane Maria (2005)"},
                        {"ns": 0, "title": "Hurricane Nate (2005)"},
                        {"ns": 0, "title": "Hurricane Ophelia (2005)"},
                        {"ns": 0, "title": "Hurricane Philippe (2005)"},
                        {"ns": 0, "title": "Hurricane Rita"},
                        {"ns": 0, "title": "Hurricane Stan"},
                        {"ns": 0, "title": "Hurricane Vince (2005)"},
                        {"ns": 0, "title": "Hurricane Wilma"},
                        {"ns": 0, "title": "Inch of mercury"},
                        {"ns": 0, "title": "International Standard Book Number"},
                        {
                            "ns": 0,
                            "title": "List of Category 5 Atlantic hurricanes",
                        },
                        {
                            "ns": 0,
                            "title": "List of storms in the 2005 Atlantic hurricane season",
                        },
                        {"ns": 0, "title": "Louisiana"},
                        {
                            "ns": 0,
                            "title": "Meteorological history of Hurricane Katrina",
                        },
                        {"ns": 0, "title": "National Hurricane Center"},
                        {"ns": 0, "title": "North Atlantic tropical cyclone"},
                        {"ns": 0, "title": "Outflow (meteorology)"},
                        {"ns": 0, "title": "Pascal (unit)"},
                        {"ns": 0, "title": "Puerto Rico"},
                        {"ns": 0, "title": "Saffir-Simpson Hurricane Scale"},
                        {
                            "ns": 0,
                            "title": "Saffir\u2013Simpson hurricane wind scale",
                        },
                        {
                            "ns": 0,
                            "title": "Timeline of the 2005 Atlantic hurricane season",
                        },
                        {"ns": 0, "title": "Tropical Storm Alpha (2005)"},
                        {"ns": 0, "title": "Tropical Storm Arlene (2005)"},
                        {"ns": 0, "title": "Tropical Storm Bret (2005)"},
                        {"ns": 0, "title": "Tropical Storm Delta (2005)"},
                        {"ns": 0, "title": "Tropical Storm Franklin (2005)"},
                        {"ns": 0, "title": "Tropical Storm Gamma"},
                        {"ns": 0, "title": "Tropical Storm Gert (2005)"},
                        {"ns": 0, "title": "Tropical Storm Jose (2005)"},
                        {"ns": 0, "title": "Tropical Storm Tammy (2005)"},
                        {"ns": 0, "title": "Tropical Storm Zeta"},
                        {"ns": 0, "title": "Tropical cyclone"},
                        {"ns": 0, "title": "Tropical cyclone scales"},
                        {"ns": 0, "title": "Tropical cyclone watches and warnings"},
                        {"ns": 0, "title": "Tropical wave"},
                        {"ns": 0, "title": "Wind shear"},
                    ],
                    "title": "Tropical Depression Ten (2005)",
                }
            }
        },
        "limits": {"links": 500},
    },
    (("cllimit", "max"), ("prop", "categories"), ("titles", "Celtuce")): {
        "query": {
            "pages": {
                "1868108": {
                    "pageid": 1868108,
                    "ns": 0,
                    "title": "Celtuce",
                    "categories": [
                        {"ns": 14, "title": "All articles lacking sources"},
                        {"ns": 14, "title": "All stub articles"},
                        {
                            "ns": 14,
                            "title": "Articles containing Chinese-language text",
                        },
                        {
                            "ns": 14,
                            "title": "Articles lacking sources from December 2009",
                        },
                        {"ns": 14, "title": "Stem vegetables"},
                        {"ns": 14, "title": "Vegetable stubs"},
                    ],
                }
            }
        },
        "limits": {"categories": 500},
    },
    (
        ("cllimit", "max"),
        ("prop", "categories"),
        ("titles", "Tropical Depression Ten (2005)"),
    ): {
        "query": {
            "pages": {
                "21196082": {
                    "pageid": 21196082,
                    "ns": 0,
                    "title": "Tropical Depression Ten (2005)",
                    "categories": [
                        {"ns": 14, "title": "2005 Atlantic hurricane season"},
                        {"ns": 14, "title": "Articles with hAudio microformats"},
                        {"ns": 14, "title": "Atlantic tropical depressions"},
                        {"ns": 14, "title": "CS1 errors: dates"},
                        {
                            "ns": 14,
                            "title": "Commons category with local link same as on Wikidata",
                        },
                        {"ns": 14, "title": "Featured articles"},
                        {"ns": 14, "title": "Hurricane Katrina"},
                        {"ns": 14, "title": "Spoken articles"},
                    ],
                }
            }
        },
        "limits": {"categories": 500},
    },
    (
        ("prop", "revisions"),
        ("rvlimit", 1),
        ("rvparse", ""),
        ("rvprop", "content"),
        ("titles", "Celtuce"),
    ): {
        "query-continue": {"revisions": {"rvcontinue": 547842204}},
        "query": {
            "pages": {
                "1868108": {
                    "ns": 0,
                    "pageid": 1868108,
                    "revisions": [
                        {
                            "*": '<table class="metadata plainlinks ambox ambox-content ambox-Unreferenced" style="" role="presentation">\n<tr><td class="mbox-image"><div style="width: 52px;"><a href="/wiki/File:Question_book-new.svg" class="image"><img alt="Question book-new.svg" src="//upload.wikimedia.org/wikipedia/en/thumb/9/99/Question_book-new.svg/50px-Question_book-new.svg.png" width="50" height="39" srcset="//upload.wikimedia.org/wikipedia/en/thumb/9/99/Question_book-new.svg/75px-Question_book-new.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/9/99/Question_book-new.svg/100px-Question_book-new.svg.png 2x" /></a></div></td><td class="mbox-text" style=""><span class="mbox-text-span">This article <b>does not <a href="/wiki/Wikipedia:Citing_sources" title="Wikipedia:Citing sources">cite</a> any <a href="/wiki/Wikipedia:Verifiability" title="Wikipedia:Verifiability">references or sources</a></b>.<span class="hide-when-compact">  Please help <a class="external text" href="//en.wikipedia.org/w/index.php?title=Celtuce&amp;action=edit">improve this article</a> by <a href="/wiki/Help:Introduction_to_referencing/1" title="Help:Introduction to referencing/1">adding citations to reliable sources</a>. Unsourced material may be challenged and <a href="/wiki/Wikipedia:Verifiability#Burden_of_evidence" title="Wikipedia:Verifiability">removed</a>.</span>&#32;<small><i>(December 2009)</i></small><span class="hide-when-compact"> </span></span></td></tr></table><div class="thumb tright"><div class="thumbinner" style="width:302px;"><a href="/wiki/File:Celtuce.jpg" class="image"><img alt="" src="//upload.wikimedia.org/wikipedia/commons/thumb/8/87/Celtuce.jpg/300px-Celtuce.jpg" width="300" height="135" class="thumbimage" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/8/87/Celtuce.jpg/450px-Celtuce.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/8/87/Celtuce.jpg/600px-Celtuce.jpg 2x" /></a>  <div class="thumbcaption"><div class="magnify"><a href="/wiki/File:Celtuce.jpg" class="internal" title="Enlarge"><img src="//bits.wikimedia.org/static-1.22wmf12/skins/common/images/magnify-clip.png" width="15" height="11" alt="" /></a></div>Celtuce stems &amp; heads</div></div></div>\n<p><b>Celtuce</b> (<i>Lactuca sativa</i> var. <i>asparagina</i>, <i>augustana</i>, or <i>angustata</i>), also called <b>stem lettuce</b>, <b>celery lettuce</b>, <b>asparagus lettuce</b>, or <b>Chinese lettuce</b>, IPA (UK,US) <span title="Representation in the International Phonetic Alphabet (IPA)" class="IPA">/\u02c8s\u025blt.\u0259s/</span>, is a cultivar of <a href="/wiki/Lettuce" title="Lettuce">lettuce</a> grown primarily for its thick <a href="/wiki/Plant_stem" title="Plant stem">stem</a>, used as a <a href="/wiki/Vegetable" title="Vegetable">vegetable</a>.  It is especially popular in China, and is called <i><b>wosun</b></i> (<a href="/wiki/Chinese_language" title="Chinese language">Chinese</a>&#58; <span lang="zh"><a href="//en.wiktionary.org/wiki/%E8%8E%B4" class="extiw" title="wiktionary:\u83b4">\u83b4</a><a href="//en.wiktionary.org/wiki/%E7%AC%8B" class="extiw" title="wiktionary:\u7b0b">\u7b0b</a></span>&#59;&#32;<a href="/wiki/Pinyin" title="Pinyin">pinyin</a>&#58; <em>w\u014ds\u016dn</em>) or <i><b>woju</b></i> (<a href="/wiki/Chinese_language" title="Chinese language">Chinese</a>&#58; <span lang="zh"><a href="//en.wiktionary.org/wiki/%E8%8E%B4" class="extiw" title="wiktionary:\u83b4">\u83b4</a><a href="//en.wiktionary.org/wiki/%E8%8B%A3" class="extiw" title="wiktionary:\u82e3">\u82e3</a></span>&#59;&#32;<a href="/wiki/Pinyin" title="Pinyin">pinyin</a>&#58; <em>w\u014dj\xf9</em>) (although the latter name may also be used to mean lettuce in general).\n</p>\n<div class="thumb tright"><div class="thumbinner" style="width:302px;"><a href="/wiki/File:The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg" class="image"><img alt="" src="//upload.wikimedia.org/wikipedia/commons/thumb/d/dc/The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg/300px-The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg" width="300" height="241" class="thumbimage" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/d/dc/The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg/450px-The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/d/dc/The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg 2x" /></a>  <div class="thumbcaption"><div class="magnify"><a href="/wiki/File:The_farmer%27s_market_near_the_Potala_in_Lhasa.jpg" class="internal" title="Enlarge"><img src="//bits.wikimedia.org/static-1.22wmf12/skins/common/images/magnify-clip.png" width="15" height="11" alt="" /></a></div>Celtuce (foreground) for sale in <a href="/wiki/Lhasa" title="Lhasa">Lhasa</a></div></div></div>\n<table class="infobox" style="font-size: 88%; text-align: left; width: 22em; line-height: 1.5em">\n<caption style="font-size: 125%; font-weight: bold"> Celtuce, raw\n\n</caption>\n<tr>\n<th colspan="2" style="text-align: center"> Nutritional value per 100&#160;g (3.5&#160;oz)\n</th></tr>\n<tr style="background-color: #e0e0e0">\n<th> <a href="/wiki/Food_energy" title="Food energy">Energy</a>\n</th>\n<td> 75&#160;kJ (18&#160;kcal)\n</td></tr>\n<tr>\n<th> <a href="/wiki/Carbohydrate" title="Carbohydrate">Carbohydrates</a>\n</th>\n<td> 3.65 g\n</td></tr>\n\n\n\n<tr>\n<th> - <a href="/wiki/Dietary_fiber" title="Dietary fiber">Dietary fiber</a>\n</th>\n<td> 1.7 g\n</td></tr>\n\n<tr>\n<th> <a href="/wiki/Fat" title="Fat">Fat</a>\n</th>\n<td> 0.3 g\n</td></tr>\n\n\n\n\n\n\n<tr>\n<th> <a href="/wiki/Protein_(nutrient)" title="Protein (nutrient)">Protein</a>\n</th>\n<td> 0.85 g\n</td></tr>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<tr>\n<td> <a href="/wiki/Vitamin_A" title="Vitamin A">Vitamin A</a> equiv.\n</td>\n<td> 175 \u03bcg (22%)\n</td></tr>\n\n\n\n\n<tr>\n<td> <a href="/wiki/Thiamine" title="Thiamine">Thiamine (vit. B<sub>1</sub>)</a>\n</td>\n<td> 0.055 mg (5%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Riboflavin" title="Riboflavin">Riboflavin (vit. B<sub>2</sub>)</a>\n</td>\n<td> 0.07 mg (6%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Niacin" title="Niacin">Niacin (vit. B<sub>3</sub>)</a>\n</td>\n<td> 0.55 mg (4%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Pantothenic_acid" title="Pantothenic acid">Pantothenic acid</a> (B<sub>5</sub>)\n</td>\n<td> 0.183 mg (4%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Vitamin_B6" title="Vitamin B6">Vitamin B<sub>6</sub></a>\n</td>\n<td> 0.05 mg (4%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Folate" title="Folate" class="mw-redirect">Folate</a> (vit. B<sub>9</sub>)\n</td>\n<td> 46 \u03bcg (12%)\n</td></tr>\n\n\n<tr>\n<td> <a href="/wiki/Vitamin_C" title="Vitamin C">Vitamin C</a>\n</td>\n<td> 19.5 mg (23%)\n</td></tr>\n\n\n\n\n\n<tr>\n<td> <a href="/wiki/Calcium#Nutrition" title="Calcium">Calcium</a>\n</td>\n<td> 39 mg (4%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Iron#Biological_role" title="Iron">Iron</a>\n</td>\n<td> 0.55 mg (4%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Magnesium_in_biology" title="Magnesium in biology">Magnesium</a>\n</td>\n<td> 28 mg (8%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Manganese#Biological_role" title="Manganese">Manganese</a>\n</td>\n<td> 0.688 mg (33%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Phosphorus#Biological_role" title="Phosphorus">Phosphorus</a>\n</td>\n<td> 39 mg (6%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Potassium#In_diet" title="Potassium">Potassium</a>\n</td>\n<td> 330 mg (7%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Sodium#Biological_role" title="Sodium">Sodium</a>\n</td>\n<td> 11 mg (1%)\n</td></tr>\n<tr>\n<td> <a href="/wiki/Zinc#Biological_role" title="Zinc">Zinc</a>\n</td>\n<td> 0.27 mg (3%)\n</td></tr>\n\n\n\n\n\n<tr style="background-color: #e0e0e0; font-size: 90%; text-align: center; padding: 4pt; line-height: 1.25em">\n<td colspan="2"> <a rel="nofollow" class="external text" href="http://ndb.nal.usda.gov/ndb/search/list?qlookup=11145&amp;format=Full">Link to USDA Database entry</a><br/>Percentages are roughly approximated<br>using <a href="/wiki/Dietary_Reference_Intake" title="Dietary Reference Intake">US recommendations</a> for adults.<br/><small>Source: <a rel="nofollow" class="external text" href="http://ndb.nal.usda.gov/ndb/search/list">USDA Nutrient Database</a></small>\n</td></tr></table>\n<p>The stem is usually harvested at a length of around 15\u201320&#160;cm and a diameter of around 3\u20134&#160;cm. It is crisp, moist, and mildly flavored, and typically prepared by slicing and then <a href="/wiki/Stir_frying" title="Stir frying">stir frying</a> with more strongly flavored ingredients.\n</p><p><br />\n</p>\n<table class="metadata plainlinks stub" style="background: transparent;" role="presentation"><tr>\n<td><a href="/wiki/File:VegCorn.jpg" class="image"><img alt="Stub icon" src="//upload.wikimedia.org/wikipedia/commons/thumb/7/79/VegCorn.jpg/40px-VegCorn.jpg" width="40" height="26" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/7/79/VegCorn.jpg/60px-VegCorn.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/7/79/VegCorn.jpg/80px-VegCorn.jpg 2x" /></a></td>\n<td><i>This <a href="/wiki/Vegetable" title="Vegetable">vegetable</a>-related article  is a <a href="/wiki/Wikipedia:Stub" title="Wikipedia:Stub">stub</a>.  You can help Wikipedia by <a class="external text" href="//en.wikipedia.org/w/index.php?title=Celtuce&amp;action=edit">expanding it</a>.</i><div class="noprint plainlinks hlist navbar mini" style="position: absolute; right: 15px; display: none;"><ul><li class="nv-view"><a href="/wiki/Template:Vegetable-stub" title="Template:Vegetable-stub"><span title="View this template" style="">v</span></a></li><li class="nv-talk"><a href="/wiki/Template_talk:Vegetable-stub" title="Template talk:Vegetable-stub"><span title="Discuss this template" style="">t</span></a></li><li class="nv-edit"><a class="external text" href="//en.wikipedia.org/w/index.php?title=Template:Vegetable-stub&amp;action=edit"><span title="Edit this template" style="">e</span></a></li></ul></div></td>\n</tr></table>\n'
                        }
                    ],
                    "title": "Celtuce",
                }
            }
        },
    },
    (
        ("action", "parse"),
        ("page", "Tropical Depression Ten (2005)"),
        ("prop", "sections"),
    ): {
        "parse": {
            "sections": [
                {
                    "index": "1",
                    "level": "2",
                    "fromtitle": "Tropical_Depression_Ten_(2005)",
                    "toclevel": 1,
                    "number": "1",
                    "byteoffset": 1369,
                    "line": "Meteorological history",
                    "anchor": "Meteorological_history",
                },
                {
                    "index": "2",
                    "level": "2",
                    "fromtitle": "Tropical_Depression_Ten_(2005)",
                    "toclevel": 1,
                    "number": "2",
                    "byteoffset": 6248,
                    "line": "Impact",
                    "anchor": "Impact",
                },
                {
                    "index": "3",
                    "level": "2",
                    "fromtitle": "Tropical_Depression_Ten_(2005)",
                    "toclevel": 1,
                    "number": "3",
                    "byteoffset": 7678,
                    "line": "See also",
                    "anchor": "See_also",
                },
                {
                    "index": "4",
                    "level": "2",
                    "fromtitle": "Tropical_Depression_Ten_(2005)",
                    "toclevel": 1,
                    "number": "4",
                    "byteoffset": 7885,
                    "line": "References",
                    "anchor": "References",
                },
                {
                    "index": "5",
                    "level": "2",
                    "fromtitle": "Tropical_Depression_Ten_(2005)",
                    "toclevel": 1,
                    "number": "5",
                    "byteoffset": 7917,
                    "line": "External links",
                    "anchor": "External_links",
                },
            ],
            "title": "Tropical Depression Ten (2005)",
        }
    },
    (
        ("limit", 10),
        ("list", "search"),
        ("srlimit", 10),
        ("srprop", ""),
        ("srsearch", "Barack Obama"),
    ): {
        "query-continue": {"search": {"sroffset": 10}},
        "query": {
            "searchinfo": {"totalhits": 12987},
            "search": [
                {"ns": 0, "title": "Barack Obama"},
                {"ns": 0, "title": "Barack Obama, Sr."},
                {"ns": 0, "title": "Presidency of Barack Obama"},
                {"ns": 0, "title": "Barack Obama presidential campaign, 2008"},
                {
                    "ns": 0,
                    "title": "List of federal judges appointed by Barack Obama",
                },
                {"ns": 0, "title": "Barack Obama in comics"},
                {"ns": 0, "title": "Political positions of Barack Obama"},
                {"ns": 0, "title": "Barack Obama on social media"},
                {
                    "ns": 0,
                    "title": "List of Batman: The Brave and the Bold characters",
                },
                {"ns": 0, "title": "Family of Barack Obama"},
            ],
        },
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 3),
        ("list", "search"),
        ("srlimit", 3),
        ("srprop", ""),
        ("srsearch", "Porsche"),
    ): {
        "query-continue": {"search": {"sroffset": 3}},
        "query": {
            "searchinfo": {"totalhits": 5335},
            "search": [
                {"ns": 0, "title": "Porsche"},
                {"ns": 0, "title": "Porsche in motorsport"},
                {"ns": 0, "title": "Porsche 911 GT3"},
            ],
        },
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 10),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 10),
        ("srprop", ""),
        ("srsearch", "hallelulejah"),
    ): {
        "query": {"searchinfo": {"suggestion": "hallelujah"}, "search": []},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("limit", 10),
        ("list", "search"),
        ("srinfo", "suggestion"),
        ("srlimit", 10),
        ("srprop", ""),
        ("srsearch", "qmxjsudek"),
    ): {
        "query": {"search": []},
        "warnings": {"main": {"*": "Unrecognized parameter: 'limit'"}},
    },
    (
        ("inprop", "url"),
        ("pageids", 1868108),
        ("prop", "info|pageprops"),
        ("redirects", ""),
    ): {
        "query": {
            "pages": {
                "1868108": {
                    "lastrevid": 575687826,
                    "pageid": 1868108,
                    "title": "Celtuce",
                    "editurl": "http://en.wikipedia.org/w/index.php?title=Celtuce&action=edit",
                    "counter": "",
                    "length": 1960,
                    "contentmodel": "wikitext",
                    "pagelanguage": "en",
                    "touched": "2014-01-12T09:30:00Z",
                    "ns": 0,
                    "fullurl": "https://en.wikipedia.org/wiki/Celtuce",
                }
            }
        }
    },
    (("colimit", "max"), ("prop", "coordinates"), ("titles", "Great Wall of China"),): {
        "query": {
            "pages": {
                "5094570": {
                    "ns": 0,
                    "pageid": 5094570,
                    "coordinates": [
                        {
                            "lat": 40.6769,
                            "globe": "earth",
                            "lon": 117.232,
                            "primary": "",
                        }
                    ],
                    "title": "Great Wall of China",
                }
            }
        },
        "limits": {"extlinks": 500},
    },
    (
        ("gscoord", "40.67693|117.23193"),
        ("gslimit", 10),
        ("gsradius", 1000),
        ("list", "geosearch"),
    ): {
        "query": {
            "geosearch": [
                {
                    "pageid": 5094570,
                    "title": "Great Wall of China",
                    "lon": 117.232,
                    "primary": "",
                    "lat": 40.6769,
                    "dist": 6.8,
                    "ns": 0,
                }
            ]
        }
    },
    (
        ("gscoord", "40.67693|117.23193"),
        ("gslimit", 10),
        ("gsradius", 10000),
        ("list", "geosearch"),
    ): {
        "query": {
            "geosearch": [
                {
                    "pageid": 5094570,
                    "title": "Great Wall of China",
                    "lon": 117.232,
                    "primary": "",
                    "lat": 40.6769,
                    "dist": 6.8,
                    "ns": 0,
                },
                {
                    "pageid": 10135375,
                    "title": "Jinshanling",
                    "lon": 117.244,
                    "primary": "",
                    "lat": 40.6764,
                    "dist": 1019.6,
                    "ns": 0,
                },
            ]
        }
    },
    (
        ("gscoord", "40.67693|117.23193"),
        ("gslimit", 10),
        ("gsradius", 1000),
        ("list", "geosearch"),
        ("titles", "Great Wall of China"),
    ): {
        "query": {
            "geosearch": [
                {
                    "pageid": 5094570,
                    "title": "Great Wall of China",
                    "lon": 117.232,
                    "primary": "",
                    "lat": 40.6769,
                    "dist": 6.8,
                    "ns": 0,
                }
            ]
        }
    },
    (
        ("gscoord", "40.67693|117.23193"),
        ("gslimit", 10),
        ("gsradius", 1000),
        ("list", "geosearch"),
        ("titles", "Test"),
    ): {"query": {"geosearch": []}},
}


mock_images: Dict[str, List[str]] = {
    "celtuce": [
        "https://upload.wikimedia.org/wikipedia/commons/8/87/Celtuce.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c8/Emoji_u1f955.svg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d6/Foodlogo2.svg",
        "https://upload.wikimedia.org/wikipedia/en/9/99/Question_book-new.svg",
    ],
    "cyclone": [
        "https://upload.wikimedia.org/wikipedia/commons/1/1c/10-L_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/3/32/15-L_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/0/0a/2007_Atlantic_hurricane_season_summary_map.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/Andrea_2007-05-09_1615Z.png",
        "https://upload.wikimedia.org/wikipedia/commons/c/c8/Andrea_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/b7/Barry_2007-06-01_1650Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1d/Barry_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/4/41/Chantal_2007-07-31_1710Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/Chantal_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/2d/Dean_2007-08-21_0845Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/28/Dean_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/5/58/Erin_15_aug_2007_1940Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d5/Erin_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/1/11/Felix_2007-09-03_0315Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/87/Felix_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/64/Gabrielle_09_sept_2007_1800Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/27/Gabrielle_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/8/8a/HU_Humberto_Sep_13_2007_AQUA_MODIS.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/b2/Humberto_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/d/df/Ingrid_2007-09-14_1635Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/80/Ingrid_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/f/f9/Jerry_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/d/d0/Jerry_24_sept_2007_1400Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1f/Karen_2007-09-26_1355Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/41/Karen_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/64/Lorenzo_2007-09-28_0450Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/4b/Lorenzo_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/26/Melissa_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/7/79/Melissa_29_sept_2007_1245Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/61/Noel_2007-11-02_1545Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b5/Noel_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/d/d4/Olga_2007-12-11_0208Z.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/95/Olga_2007_track.png",
        "https://upload.wikimedia.org/wikipedia/commons/7/71/TD15_2007-10-11.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/TD_Ten_21_sept_2007_1650Z.jpg",
        "https://upload.wikimedia.org/wikipedia/en/e/e7/Cscr-featured.svg",
        "https://upload.wikimedia.org/wikipedia/commons/8/89/Cyclone_Catarina_from_the_ISS_on_March_26_2004.JPG",
        "https://upload.wikimedia.org/wikipedia/en/9/96/Symbol_category_class.svg",
        "https://upload.wikimedia.org/wikipedia/en/e/e2/Symbol_portal_class.svg",
        "https://upload.wikimedia.org/wikipedia/commons/3/37/People_icon.svg",
        "https://upload.wikimedia.org/wikipedia/en/6/62/PD-icon.svg",
    ],
}

mock_links: Dict[str, List[str]] = {
    "celtuce": [
        "Aphid",
        "Calcium in biology",
        "Carbohydrate",
        "China",
        "Cultivar",
        "Dietary Reference Intake",
        "Dietary fiber",
        "EPPO Code",
        "Fat",
        "Folate",
        "Food energy",
        "Germplasm Resources Information Network",
        "Global Biodiversity Information Facility",
        "Google Books",
        "Human iron metabolism",
        "International Plant Names Index",
        "International unit",
        "Lactuca sativa",
        "Lettuce",
        "List of vegetables",
        "Magnesium in biology",
        "Manganese",
        "Mediterranean Basin",
        "Microgram",
        "Milligram",
        "Mineral (nutrient)",
        "National Center for Biotechnology Information",
        "Niacin (nutrient)",
        "Open Tree of Life",
        "Pantothenic acid",
        "Phosphorus",
        "Pinyin",
        "Plant stem",
        "Plants for a Future",
        "Plants of the World Online",
        "Potassium in biology",
        "Protein (nutrient)",
        "Riboflavin",
        "Simplified Chinese characters",
        "Sodium in biology",
        "Species",
        "Stir frying",
        "Taiwan",
        "Tang dynasty",
        "Thiamine",
        "Traditional Chinese characters",
        "Tropicos",
        "Vegetable",
        "Vitamin",
        "Vitamin A",
        "Vitamin B6",
        "Vitamin C",
        "Wikidata",
        "World Register of Marine Species",
        "Zinc",
    ],
    "cyclone": ['1932 Atlantic hurricane season', '1933 Atlantic hurricane season', '1961 Atlantic hurricane season', '1982 Atlantic hurricane season', '1983 Atlantic hurricane season', '1988 Atlantic hurricane season', '1990 Atlantic hurricane season', '1992 Atlantic hurricane season', '1994 Atlantic hurricane season', '1997 Atlantic hurricane season', '1999 Atlantic hurricane season', '2000 Atlantic hurricane season', '2001 Atlantic hurricane season', '2002 Atlantic hurricane season', '2003 Atlantic hurricane season', '2004 Atlantic hurricane season', '2005 Atlantic hurricane season', '2006 Atlantic hurricane season', '2006–07 Australian region cyclone season', '2006–07 South-West Indian Ocean cyclone season', '2006–07 South Pacific cyclone season', '2007 North Indian Ocean cyclone season', '2007 Pacific hurricane season', '2007 Pacific typhoon season', '2007–08 Australian region cyclone season', '2007–08 South-West Indian Ocean cyclone season', '2007–08 South Pacific cyclone season', '2008 Atlantic hurricane season', '2009 Atlantic hurricane season', '2010 Atlantic hurricane season', '2013 Atlantic hurricane season', '2017 Atlantic hurricane season', '2019 Atlantic hurricane season', '2020 Atlantic hurricane season', 'Accumulated cyclone energy', 'Alabama', 'Atlantic Canada', 'Atlantic hurricane season', 'Atmospheric convection', 'Avalon Peninsula', 'Azores', 'Bahamas', 'Bar (unit)', 'Baroclinic', 'Bay of Campeche', 'Beaumont, Texas', 'Belize', 'Bermuda', 'Bridge City, Texas', 'Brownsville, Texas', 'CTV Television Network', 'Canadian dollar', 'Cape Hatteras', 'Cape Lookout (North Carolina)', 'Cape Verde', 'Cayman Islands', 'Central United States', 'Coastal erosion', 'Coastal flooding', 'Cold core low', 'Cold front', 'Colombia', 'Colorado State University', 'Costa Maya', 'Cuba', 'Dominican Republic', 'Dropsonde', 'East Coast of the United States', 'Effects of Hurricane Dean in Mexico', 'Effects of Hurricane Dean in the Greater Antilles', 'Effects of Hurricane Dean in the Lesser Antilles', 'El Niño-Southern Oscillation', 'El Salvador', 'Eustis, Florida', 'Extratropical cyclone', 'Eye (cyclone)', 'Eyewall replacement cycle', 'Florida', 'Florida Panhandle', 'Fort Walton Beach, Florida', 'Frontal system', 'Georgia (U.S. state)', 'Google Earth', 'Greater Antilles', 'Greenland', 'Guadeloupe', 'Guatemala', 'Gulf Coast of the United States', 'Gulf of Mexico', 'Haiti', 'Hidalgo (state)', 'High Island, Texas', 'Hispaniola', 'Honduras', 'Hurricane Andrew', 'Hurricane Claudette (2003)', 'Hurricane Dean', 'Hurricane Felix', 'Hurricane Gilbert', 'Hurricane Henriette (2007)', 'Hurricane Humberto (2007)', 'Hurricane Hunter', 'Hurricane Iris', 'Hurricane Irma', 'Hurricane Karen (2007)', 'Hurricane Katrina', 'Hurricane Lorenzo (2007)', 'Hurricane Maria', 'Hurricane Michelle', 'Hurricane Mitch', 'Hurricane Noel', 'Hurricane Wilma', 'Hurricane hunter', 'Inch of mercury', 'Jamaica', 'Knot (unit)', 'La Niña', 'Labor Day Hurricane of 1935', 'Labrador', 'Lamar, Texas', 'Leeward Antilles', 'Leeward Islands', 'Lesser Antilles', 'List of Atlantic hurricanes', 'List of tropical cyclone names', 'Louisiana', 'Low-pressure area', 'Lucayan Archipelago', 'MXN', 'Martinique', 'Matagorda, Texas', 'Mbar', 'Mediterranean tropical-like cyclone', 'Met Office', 'Meteorological history of Hurricane Dean', 'Mid-Atlantic States', 'Mississippi', 'Mosquito Coast', 'NOAA', 'National Hurricane Center', 'National Oceanic and Atmospheric Administration', 'Newfoundland (island)', 'Newfoundland and Labrador', 'Nicaragua', 'Nicaraguan córdoba', 'North Atlantic tropical cyclone', 'North Carolina', 'Nova Scotia', 'Oil refinery', 'Oklahoma', 'Oklahoma City, Oklahoma', 'Pascal (unit)', 'Port Arthur, Texas', 'Public domain', 'Puebla', 'Puerto Rico', 'QuikScat', 'Rip current', "Royal St. John's Regatta", 'Saffir–Simpson hurricane wind scale', 'Saffir–Simpson scale', 'Saharan Air Layer', 'Saint Lucia', 'San Lorenzo River (Mexico)', 'Santiago Province (Dominican Republic)', 'Satellite', 'Savannah, Georgia', 'Sea surface temperature', 'South Atlantic tropical cyclone', 'South Carolina', 'Southeast U.S.', 'Storm surge', 'Subtropical Storm Andrea (2007)', 'Subtropical cyclone', 'Subtropical ridge', 'Tecolutla', 'Tecolutla, Mexico', 'Texas', 'The Bahamas', 'The Carolinas', 'Timeline of 2007 Atlantic hurricane season', 'Timeline of 2007 Atlantic hurricane seasons', 'Timeline of the 2007 Atlantic hurricane season', 'Tobago', 'Trinidad and Tobago', 'Trinidad and Tobago dollar', 'Tropical Cyclone Report', 'Tropical Depression Ten (2007)', 'Tropical Storm Allison', 'Tropical Storm Ana (2003)', 'Tropical Storm Arlene (1981)', 'Tropical Storm Barry (2007)', 'Tropical Storm Chantal (2007)', 'Tropical Storm Erin (2007)', 'Tropical Storm Gabrielle (2007)', 'Tropical Storm Olga (2007)', 'Tropical Storm Zeta (2005)', 'Tropical cyclone', 'Tropical cyclone naming', 'Tropical cyclone scales', 'Tropical cyclone seasonal forecasting', 'Tropical cyclone watches and warnings', 'Tropical cyclones in 2007', 'Tropical upper tropospheric trough', 'Tropical wave', 'Trough (meteorology)', 'Turks and Caicos Islands', 'Tuxpan', 'United States Dollar', 'United States dollar', 'Venezuela', 'Veracruz', 'Virginia', 'West-southwest', 'William M. Gray', 'Wind shear', 'Windward Islands', 'World Meteorological Organization', 'Wreckhouse, Newfoundland and Labrador', 'Yucatan Peninsula', 'Yucatán Peninsula'],
}

mock_references: List[str] = [
    "http://scholar.google.com/scholar?q=%22Celtuce%22",
    "http://www.google.com/search?&q=%22Celtuce%22&tbs=bkt:s&tbm=bks",
    "http://www.google.com/search?as_eq=wikipedia&q=%22Celtuce%22",
    "http://www.google.com/search?tbm=nws&q=%22Celtuce%22+-wikipedia&tbs=ar:1",
    "http://www.google.com/search?tbs=bks:1&q=%22Celtuce%22+-wikipedia",
    "http://modernfarmer.com/2016/04/celtuce/",
    "http://www.seedaholic.com/celtuce-wo-sun.html",
    "http://soyricefire.com/2013/04/21/celtuce-ribbon-salad/",
    "http://legacy.tropicos.org/Name/2727046",
    "https://books.google.com/books?id=1pBMcf6wyj0C&pg=PA658",
    "https://books.google.com/books?id=rZQ7texaDLYC&pg=PA51",
    "https://books.google.com/books?id=xTPpCAAAQBAJ&pg=PA208",
    "https://www.kingsseeds.com/Products/Vegetables/Oriental/Celtuce-or-Stem-Lettuce",
    "https://npgsweb.ars-grin.gov/gringlobal/taxonomydetail.aspx?id=404620",
    "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=1049370",
    "https://fdc.nal.usda.gov/fdc-app.html#/food-details/169990/nutrients",
    "https://fdc.nal.usda.gov/index.html",
    "https://gd.eppo.int/taxon/LACSG",
    "https://web.archive.org/web/20170814062829/http://www.seedaholic.com/celtuce-wo-sun.html",
    "https://web.archive.org/web/20180723182147/https://www.kingsseeds.com/Products/Vegetables/Oriental/Celtuce-or-Stem-Lettuce",
    "https://www.gbif.org/species/6711035",
    "https://www.ipni.org/n/77203162-1",
    "https://www.jstor.org/action/doBasicSearch?Query=%22Celtuce%22&acc=on&wc=on",
    "https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:77203162-1",
    "https://www.marinespecies.org/aphia.php?p=taxdetails&id=1163647",
    "https://tree.opentreeoflife.org/taxonomy/browse?id=5541628",
    "https://pfaf.org/user/Plant.aspx?LatinName=Lactuca+sativa+angustana",
]

mock_categories: Dict[str, List[str]] = {
    "celtuce": [
        "All articles needing additional references",
        "All articles with unsourced statements",
        "All stub articles",
        "Articles containing simplified Chinese-language text",
        "Articles containing traditional Chinese-language text",
        "Articles needing additional references from January 2017",
        "Articles with 'species' microformats",
        "Articles with short description",
        "Articles with unsourced statements from December 2021",
        "Lettuce",
        "Short description is different from Wikidata",
        "Stem vegetables",
        "Vegetable stubs",
    ],
    "cyclone": [
        "2007 Atlantic hurricane season",
        "Articles which contain graphical timelines",
        "Articles with short description",
        "Atlantic hurricane seasons",
        "CS1 Spanish-language sources (es)",
        "CS1 maint: multiple names: authors list",
        "Featured articles",
        "Pages using the EasyTimeline extension",
        "Short description matches Wikidata",
        "Tropical cyclones in 2007",
        "Wikipedia indefinitely move-protected pages",
        "Source attribution",
    ],
}

mock_backlinks: Dict[str, List[str]] = {
    "celtuce": [
        "Aphid",
        "Calcium in biology",
        "Carbohydrate",
        "China",
        "Cultivar",
        "Dietary Reference Intake",
        "Dietary fiber",
        "EPPO Code",
        "Fat",
        "Folate",
        "Food energy",
        "Germplasm Resources Information Network",
        "Global Biodiversity Information Facility",
        "Google Books",
        "Human iron metabolism",
        "International Plant Names Index",
        "International unit",
        "Lactuca sativa",
        "Lettuce",
        "List of vegetables",
        "Magnesium in biology",
        "Manganese",
        "Mediterranean Basin",
        "Microgram",
        "Milligram",
        "Mineral (nutrient)",
        "National Center for Biotechnology Information",
        "Niacin (nutrient)",
        "Open Tree of Life",
        "Pantothenic acid",
        "Phosphorus",
        "Pinyin",
        "Plant stem",
        "Plants for a Future",
        "Plants of the World Online",
        "Potassium in biology",
        "Protein (nutrient)",
        "Riboflavin",
        "Simplified Chinese characters",
        "Sodium in biology",
        "Species",
        "Stir frying",
        "Taiwan",
        "Tang dynasty",
        "Thiamine",
        "Traditional Chinese characters",
        "Tropicos",
        "Vegetable",
        "Vitamin",
        "Vitamin A",
        "Vitamin B6",
        "Vitamin C",
        "Wikidata",
        "World Register of Marine Species",
        "Zinc",
        "Wikipedia:Citation needed",
        "Wikipedia:Stub",
        "Wikipedia:Verifiability",
        "Template:Vegetable-stub",
        "Template talk:Vegetable-stub",
        "Help:Maintenance template removal",
        "Help:Referencing for beginners",
        "Help:Taxon identifiers",
        "Category:Articles needing additional references from January 2017",
        "Category:Articles with unsourced statements from December 2021",
        "Portal:Food",
    ],
    "cyclone": ['1932 Atlantic hurricane season', '1933 Atlantic hurricane season', '1961 Atlantic hurricane season', '1982 Atlantic hurricane season', '1983 Atlantic hurricane season', '1988 Atlantic hurricane season', '1990 Atlantic hurricane season', '1992 Atlantic hurricane season', '1994 Atlantic hurricane season', '1997 Atlantic hurricane season', '1999 Atlantic hurricane season', '2000 Atlantic hurricane season', '2001 Atlantic hurricane season', '2002 Atlantic hurricane season', '2003 Atlantic hurricane season', '2004 Atlantic hurricane season', '2005 Atlantic hurricane season', '2006 Atlantic hurricane season', '2006–07 Australian region cyclone season', '2006–07 South-West Indian Ocean cyclone season', '2006–07 South Pacific cyclone season', '2007 North Indian Ocean cyclone season', '2007 Pacific hurricane season', '2007 Pacific typhoon season', '2007–08 Australian region cyclone season', '2007–08 South-West Indian Ocean cyclone season', '2007–08 South Pacific cyclone season', '2008 Atlantic hurricane season', '2009 Atlantic hurricane season', '2010 Atlantic hurricane season', '2013 Atlantic hurricane season', '2017 Atlantic hurricane season', '2019 Atlantic hurricane season', '2020 Atlantic hurricane season', 'Accumulated cyclone energy', 'Alabama', 'Atlantic Canada', 'Atlantic hurricane season', 'Atmospheric convection', 'Avalon Peninsula', 'Azores', 'Bahamas', 'Bar (unit)', 'Baroclinic', 'Bay of Campeche', 'Beaumont, Texas', 'Belize', 'Bermuda', 'Bridge City, Texas', 'Brownsville, Texas', 'CTV Television Network', 'Canadian dollar', 'Cape Hatteras', 'Cape Lookout (North Carolina)', 'Cape Verde', 'Cayman Islands', 'Central United States', 'Coastal erosion', 'Coastal flooding', 'Cold core low', 'Cold front', 'Colombia', 'Colorado State University', 'Costa Maya', 'Cuba', 'Dominican Republic', 'Dropsonde', 'East Coast of the United States', 'Effects of Hurricane Dean in Mexico', 'Effects of Hurricane Dean in the Greater Antilles', 'Effects of Hurricane Dean in the Lesser Antilles', 'El Niño-Southern Oscillation', 'El Salvador', 'Eustis, Florida', 'Extratropical cyclone', 'Eye (cyclone)', 'Eyewall replacement cycle', 'Florida', 'Florida Panhandle', 'Fort Walton Beach, Florida', 'Frontal system', 'Georgia (U.S. state)', 'Google Earth', 'Greater Antilles', 'Greenland', 'Guadeloupe', 'Guatemala', 'Gulf Coast of the United States', 'Gulf of Mexico', 'Haiti', 'Hidalgo (state)', 'High Island, Texas', 'Hispaniola', 'Honduras', 'Hurricane Andrew', 'Hurricane Claudette (2003)', 'Hurricane Dean', 'Hurricane Felix', 'Hurricane Gilbert', 'Hurricane Henriette (2007)', 'Hurricane Humberto (2007)', 'Hurricane Hunter', 'Hurricane Iris', 'Hurricane Irma', 'Hurricane Karen (2007)', 'Hurricane Katrina', 'Hurricane Lorenzo (2007)', 'Hurricane Maria', 'Hurricane Michelle', 'Hurricane Mitch', 'Hurricane Noel', 'Hurricane Wilma', 'Hurricane hunter', 'Inch of mercury', 'Jamaica', 'Knot (unit)', 'La Niña', 'Labor Day Hurricane of 1935', 'Labrador', 'Lamar, Texas', 'Leeward Antilles', 'Leeward Islands', 'Lesser Antilles', 'List of Atlantic hurricanes', 'List of tropical cyclone names', 'Louisiana', 'Low-pressure area', 'Lucayan Archipelago', 'MXN', 'Martinique', 'Matagorda, Texas', 'Mbar', 'Mediterranean tropical-like cyclone', 'Met Office', 'Meteorological history of Hurricane Dean', 'Mid-Atlantic States', 'Mississippi', 'Mosquito Coast', 'NOAA', 'National Hurricane Center', 'National Oceanic and Atmospheric Administration', 'Newfoundland (island)', 'Newfoundland and Labrador', 'Nicaragua', 'Nicaraguan córdoba', 'North Atlantic tropical cyclone', 'North Carolina', 'Nova Scotia', 'Oil refinery', 'Oklahoma', 'Oklahoma City, Oklahoma', 'Pascal (unit)', 'Port Arthur, Texas', 'Public domain', 'Puebla', 'Puerto Rico', 'QuikScat', 'Rip current', "Royal St. John's Regatta", 'Saffir–Simpson hurricane wind scale', 'Saffir–Simpson scale', 'Saharan Air Layer', 'Saint Lucia', 'San Lorenzo River (Mexico)', 'Santiago Province (Dominican Republic)', 'Satellite', 'Savannah, Georgia', 'Sea surface temperature', 'South Atlantic tropical cyclone', 'South Carolina', 'Southeast U.S.', 'Storm surge', 'Subtropical Storm Andrea (2007)', 'Subtropical cyclone', 'Subtropical ridge', 'Tecolutla', 'Tecolutla, Mexico', 'Texas', 'The Bahamas', 'The Carolinas', 'Timeline of 2007 Atlantic hurricane season', 'Timeline of 2007 Atlantic hurricane seasons', 'Timeline of the 2007 Atlantic hurricane season', 'Tobago', 'Trinidad and Tobago', 'Trinidad and Tobago dollar', 'Tropical Cyclone Report', 'Tropical Depression Ten (2007)', 'Tropical Storm Allison', 'Tropical Storm Ana (2003)', 'Tropical Storm Arlene (1981)', 'Tropical Storm Barry (2007)', 'Tropical Storm Chantal (2007)', 'Tropical Storm Erin (2007)', 'Tropical Storm Gabrielle (2007)', 'Tropical Storm Olga (2007)', 'Tropical Storm Zeta (2005)', 'Tropical cyclone', 'Tropical cyclone naming', 'Tropical cyclone scales', 'Tropical cyclone seasonal forecasting', 'Tropical cyclone watches and warnings', 'Tropical cyclones in 2007', 'Tropical upper tropospheric trough', 'Tropical wave', 'Trough (meteorology)', 'Turks and Caicos Islands', 'Tuxpan', 'United States Dollar', 'United States dollar', 'Venezuela', 'Veracruz', 'Virginia', 'West-southwest', 'William M. Gray', 'Wind shear', 'Windward Islands', 'World Meteorological Organization', 'Wreckhouse, Newfoundland and Labrador', 'Yucatan Peninsula', 'Yucatán Peninsula', 'Wikipedia:Featured articles', 'Wikipedia:WikiProject Tropical cyclones', 'Template:2007 Atlantic hurricane season buttons', 'Template:Cite web', 'Template:Inflation/US', 'Template:Tropical cyclone season', 'Template talk:2007 Atlantic hurricane season buttons', 'Template talk:Tropical cyclone season', 'Category:2007 Atlantic hurricane season', 'Category:CS1 maint: multiple names: authors list', 'Portal:Tropical cyclones'],
}

mock_backlinks_ids: Dict[str, List[int]] = {
    "celtuce": [
        162296,
        378744,
        5932,
        5405,
        167906,
        396054,
        66554,
        2174645,
        11042,
        54117,
        182303,
        6633626,
        2987862,
        3190097,
        3335116,
        391726,
        865802,
        1911815,
        57079,
        125616,
        378938,
        19051,
        2454408,
        205406,
        157785,
        235195,
        149306,
        71987787,
        47926198,
        54099,
        23318,
        23588,
        18952693,
        4533478,
        56412019,
        378912,
        6531493,
        26229,
        261949,
        22615598,
        21780446,
        53000,
        25734,
        30500,
        266210,
        42325606,
        5791492,
        32512,
        54114,
        54110,
        32509,
        35412202,
        20378103,
        34420,
        25432026,
        99719,
        3961892,
        2160444,
        13381643,
        49378816,
        14894626,
        54111898,
        52734068,
        69396690,
        4474778,
        43455,
    ],
    "cyclone":[1458309, 1402627, 760589, 799219, 799287, 802559, 804196, 771131, 20336287, 737696, 737260, 736446, 736409, 736394, 733555, 723742, 1142605, 1308988, 10827461, 10827148, 10827601, 7156056, 3630623, 2595704, 10602610, 10602294, 10704003, 2530547, 26237603, 25027868, 28048507, 38113551, 38113556, 38113558, 1201310, 303, 71095, 2930244, 11963992, 469497, 3226, 8366550, 362631, 1614124, 912692, 136196, 3458, 3460, 79663, 135600, 66732, 101846, 313791, 2654307, 18962637, 5468, 2031425, 149261, 31546082, 60409179, 20279444, 5222, 475386, 2265629, 5042481, 8060, 971289, 89126, 18947749, 12949435, 12845936, 36633803, 9356, 109292, 8210537, 4652664, 26608934, 18933066, 902849, 109509, 8006988, 48830, 2126501, 298550, 12118, 12343, 17238567, 11969, 21076367, 13373, 224021, 1009734, 13714, 13394, 35999637, 3511662, 12766321, 13055518, 598523, 13068865, 13231849, 30976821, 974726, 55140572, 14460597, 2569378, 13465811, 55262011, 740088, 281923, 13948899, 2878666, 726492, 2319766, 15660, 366810, 78469, 22139775, 58647, 12836386, 6720770, 276895, 160659, 41595291, 723517, 18130, 475199, 1059005, 295426, 19169, 7090289, 2614843, 28057466, 319671, 12855019, 26090837, 16949861, 213071, 60846, 255317, 37876, 26304966, 21980, 21362, 482655, 38366078, 21650, 21184, 195137, 22489, 19946719, 66014, 151211, 18935551, 413436, 23041, 3570464, 313371, 1728419, 43562731, 255313, 6137903, 27208, 23532812, 998566, 27683, 84493, 899880, 567831, 27956, 2078189, 449744, 10923896, 100194, 5413154, 12892770, 14473373, 29810, 3451, 209773, 11235135, 162070, 3565457, 1370135, 31508314, 13380735, 334013, 3314256, 25667337, 11548718, 12299808, 14054738, 13150402, 14668232, 3570152, 8282374, 460919, 3306341, 10026140, 5055074, 30382420, 2474597, 1038144, 2585489, 30217, 1008532, 151486, 18717338, 32374, 63125, 32432, 2691477, 1244159, 223992, 276897, 33584, 7693112, 63798, 1248351, 5921878, 2836248, 11138685, 1252907, 17637321, 61631736, 11138691, 62237039, 2852084, 50109267, 3271272],
}

mock_bill_foster_images: List[str] = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bd/Bill_Foster%2C_Official_Portrait%2C_113th_Congress.jpg",
    "https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg",
    "https://upload.wikimedia.org/wikipedia/en/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg",
]

mock_sections: List[str] = [
    "Seasonal forecasts",
    "Pre-season forecasts",
    "Midseason outlooks",
    "Seasonal summary",
    "Systems",
    "Subtropical Storm Andrea",
    "Tropical Storm Barry",
    "Tropical Storm Chantal",
    "Hurricane Dean",
    "Tropical Storm Erin",
    "Hurricane Felix",
    "Tropical Storm Gabrielle",
    "Tropical Storm Ingrid",
    "Hurricane Humberto",
    "Tropical Depression Ten",
    "Tropical Storm Jerry",
    "Hurricane Karen",
    "Hurricane Lorenzo",
    "Tropical Storm Melissa",
    "Tropical Depression Fifteen",
    "Hurricane Noel",
    "Tropical Storm Olga",
    "Storm names",
    "Retirement",
    "Season effects",
    "See also",
    "Notes",
    "References",
    "External links",
]

mock_category_members_physics: List[str] = ['Physics', 'Portal:Physics', 'Physicalism', 'Draft:Martin Regehly']



mock_data: Dict[str, str | int | Dict[str, str] | List[str]] = {
    "celtuce.content": """The stem is usually harvested at a length of around 15–20 cm and a diameter of around 3–4 cm. It is crisp, moist, and mildly flavored, and typically prepared by slicing and then stir frying with more strongly flavored ingredients.""",
    "celtuce.parentid": 1129643971,
    "celtuce.revid": 1135063854,
    "celtuce.summary": """Celtuce (/ˈsɛlt.əs/) (Lactuca sativa var. augustana, angustata, or asparagina), also called stem lettuce, celery lettuce, asparagus lettuce, or Chinese lettuce, is a cultivar of lettuce grown primarily for its thick stem or its leaves.""",
    "celtuce.es_lang": "Lechuga china",
    "celtuce.pageprops": {
        "page_image_free": "Celtuce.jpg",
        "wikibase-shortdesc": "Lettuce cultivar",
        "wikibase_item": "Q574172",
    },
    "cyclone.revid": 1139631992,
    "cyclone.parentid": 1138924422,
    "cyclone.section.seasonal_forecasts": "Noted hurricane experts Philip J. Klotzbach, William M. Gray, and their associates at Colorado State University issue forecasts of hurricane activity each year, separately from NOAA. Klotzbach's team, formerly led by Gray, determined the average number of storms per season between 1950 and 2000 to be 9.6 tropical storms, 5.9 hurricanes, and 2.3 major hurricanes (storms exceeding Category 3 on the Saffir–Simpson scale). A normal season, as defined by NOAA, has 9 to 12 named storms, of which five to seven reach hurricane strength, and one to three become major hurricanes.",
    "cyclone.ru_lang": "Сезон атлантических ураганов 2007 года",
    "cyclone.pageprops": {
        "defaultsort": "2007 Atlantic Hurricane Season",
        "page_image_free": "2007_Atlantic_hurricane_season_summary_map.png",
        "wikibase-badge-Q17437796": "1",
        "wikibase-shortdesc": "Hurricane season in the Atlantic Ocean",
        "wikibase_item": "Q756793",
    },
    "barack.search": [
        "Barack Obama",
        "Barack Obama, Sr.",
        "Presidency of Barack Obama",
        "Barack Obama presidential campaign, 2008",
        "List of federal judges appointed by Barack Obama",
        "Barack Obama in comics",
        "Political positions of Barack Obama",
        "Barack Obama on social media",
        "List of Batman: The Brave and the Bold characters",
        "Family of Barack Obama",
    ],
    "porsche.search": ["Porsche", "Porsche in motorsport", "Porsche 911 GT3"],
    "great_wall_of_china.coordinates.lat": "40.680",
    "great_wall_of_china.coordinates.lon": "117.230",
    "great_wall_of_china.geo_seach": ["Great Wall of China"],
    "great_wall_of_china.geo_seach_with_radius": [
        "Great Wall of China",
        "Jinshanling",
    ],
    "great_wall_of_china.geo_seach_with_existing_article_name": ["Great Wall of China"],
    "great_wall_of_china.geo_seach_with_non_existing_article_name": [],
    "infobox_avatar": {
        "Also known as": "Avatar: The Legend of Aang",
        "Genre": "Action-adventure Fantasy Comedy drama",
        "Created by": "Michael Dante DiMartino Bryan Konietzko",
        "Voices of": "Zach Tyler Eisen Mae Whitman Jack DeSena Dante Basco Jessie Flower Dee Bradley Baker Mako Greg Baldwin Grey DeLisle Mark Hamill",
        "Composers": "Jeremy Zuckerman Benjamin Wynn",
        "Country of origin": "United States",
        "Original language": "English",
        "No. of seasons": "3",
        "No. of episodes": "61 (list of episodes)",
        "Executive producers": "Michael Dante DiMartino Bryan Konietzko Aaron Ehasz (co-executive)",
        "Animators": "JM Animation (32 episodes)[a]DR Movie (19 episodes)[b]Moi Animation (10 episodes)[c]",
        "Running time": "23 minutes",
        "Production company": "Nickelodeon Animation Studio",
        "Distributor": "MTV Networks",
        "Original network": "Nickelodeon",
        "Picture format": "NTSC",
        "Original release": "February 21, 2005 (2005-02-21) –July 19, 2008 (2008-07-19)",
        "Followed by": "Avatar: The Last Airbender (comics) The Legend of Korra",
    },
}
