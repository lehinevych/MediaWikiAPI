import sys

if not sys.argv[0] == 'pip' and not sys.argv[1] == 'setup.py':
    from .config import *
    from .mediawikiapi import *
    from .exceptions import *
    from .language import *


__version__ = "1.1.2"
