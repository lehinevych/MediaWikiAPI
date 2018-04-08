import sys

if not (sys.argv[0] in ['pip', 'setup.py']
        or (len(sys.argv) > 1 and sys.argv[1] == 'setup.py')
        or (len(sys.argv) > 1 and sys.argv[0] == '-c' and sys.argv[1] in ['egg_info', 'clean', 'bdist_wheel', 'sdist', 'install'])):
    from .config import *
    from .mediawikiapi import *
    from .exceptions import *
    from .language import *

__version__ = "1.1.2"
