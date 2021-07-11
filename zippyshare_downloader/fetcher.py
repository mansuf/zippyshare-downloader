# zipyshare-downloader
# fetcher.py

import logging
import zipfile
from typing import List
from pathlib import Path
from .utils import extract_archived_file
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
    zip: :class:`str`
        Zip all downloaded files once finished.
        Zip filename will be taken from :param:`zip`,
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
    if unzip and zip:
        raise ValueError("unzip and zip paramaters cannot be True together")
    downloaded_files = {}
    files = []
    for url in urls:
        info = finalization_info(get_info(url))
        file = File(info)
        files.append(file)
        if kwargs.get('filename') is not None:
            kwargs.pop('filename')
        file_path = file.download(**kwargs)
        downloaded_files[file] = file_path
        if unzip:
            extract_archived_file(str(file_path))
    if zip:
        path = list(downloaded_files.values())[0]
        with zipfile.ZipFile((path.parent / zip), 'w') as zip_writer:
            for file, path in downloaded_files.items():
                zip_writer.write(path)
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
        file_path = file.download(**kwargs)
        if unzip:
            extract_archived_file(str(file_path))
    return file
