import os
import sys

from .main import main


# Increase this version when features are changed so that xstatic
# packagers track updates.
__version__ = '1.1.3'

if __name__ == '__main__':
    # ensure the xstatic package in the user's current working
    # directory is importable
    sys.path.insert(0, os.getcwd())
    main()
