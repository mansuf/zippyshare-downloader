# zippyshare-downloader
# __init__.py

"""
zippyshare-downloader

Download file from zippyshare directly from python
"""

__VERSION__ = 'v0.0.21'

import logging
from .fetcher import *

logging.getLogger(__name__).addHandler(logging.NullHandler())



