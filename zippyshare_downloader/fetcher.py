# zipyshare-downloader
# fetcher.py

import logging
from typing import List
from .parser import File, get_info, finalization_info

__all__ = (
    'download', 'extract_info'
)

log = logging.getLogger(__name__)

def download(*urls, zip=False, unzip=False, **kwargs) -> List[File]:
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
    **kwargs
        These parameters will be passed to `File.download()`,
        except for parameter `filename`.

    Return
    -------
    :class:`List[File]`
    """
    files = []
    for url in urls:
        info = finalization_info(get_info(url))
        file = File(info)
        files.append(file)
        if kwargs.get('filename') is not None:
            kwargs.pop('filename')
        file.download(**kwargs)
    return files

def extract_info(
    url: str,
    download: bool=True,
    unzip: bool=False,
    **kwargs
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
        (if given file is zip or tar format extract it, otherwise ignore it),
        default to `False`.
    **kwargs
        These parameters will be passed to `File.download()`

    Return
    -------
    :class:`File`
    """
    info = finalization_info(get_info(url))
    file = File(info)
    if download:
        file.download(**kwargs)
    return file
