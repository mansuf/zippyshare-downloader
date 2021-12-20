# zippyshare-downloader
# __init__.py

"""
zippyshare-downloader

Download file from zippyshare directly from python
"""

__VERSION__ = 'v0.2.0'

import logging
from .fetcher import *
from .file import *

logging.getLogger(__name__).addHandler(logging.NullHandler())



