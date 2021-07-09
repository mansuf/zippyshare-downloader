# zipyshare-downloader
# fetcher.py

import logging
from typing import List
from .parser import File

__all__ = (
    'download', 'extract_info'
)

log = logging.getLogger(__name__)

def download(*urls, zip=False, unzip=False, folder=None) -> List[File]:
    """
    Download multiple zippyshare urls

    Parameters
    -----------
    *urls
        Zippyshare urls.
    zip: :class:`bool`
        Zip all downloaded files once finished,
        default to `False`.
        NOTE: You can't mix `zip` and `unzip` options together
        with value `True`, it will raise error.
    unzip: :class:`bool`
        Unzip all downloaded files once finished
        (if given file is zip format extract it, otherwise ignore it),
        default to `False`.
        NOTE: You can't mix `zip` and `unzip` options together
        with value `True`, it will raise error.
    folder: :class:`str`
        Set a folder where to store all downloaded files,
        default to `None`.

    Return
    -------
    :class:`List[File]`
    """
    pass

def extract_info(
    url: str,
    download: bool=True,
    unzip: bool=False,
    filename: str=None,
    folder: str=None
) -> File:
    """
    Extract all informations in Zippyshare url.

    Parameters
    ------------
    url: :class:`str`
        Zippyshare url.
    download: :class:`bool`
        Download given zippyshare url if `True`, 
        default to `True`.
    unzip: :class:`bool`
        Unzip downloaded file once finished
        (if given file is zip format extract it, otherwise ignore it),
        default to `False`.
    filename: :class:`str`
        Rewrite file name if :param:`download` is `True`,
        default to `None`.
    folder: :class:`str`
        Set a folder where to store downloaded file,
        default to `None`.
    """
    pass
