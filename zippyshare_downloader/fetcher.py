# zipyshare-downloader
# fetcher.py

import asyncio
import logging
import os
import zipfile
from typing import List
from pathlib import Path
from .utils import extract_archived_file
from .parser import File, get_info, finalization_info, get_info_coro

__all__ = (
    'download', 'extract_info',
    'download_coro', 'extract_info_coro'
)

log = logging.getLogger(__name__)

def download(
    *urls,
    zip: str=None,
    unzip: bool=False,
    **kwargs
) -> List[File]:
    """
    Download multiple zippyshare urls

    Parameters
    -----------
    *urls
        Zippyshare urls.
    zip: :class:`str`
        Zip all downloaded files once finished.
        Zip filename will be taken from :param:`zip`,
        default to `None`.
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
        raise ValueError("unzip and zip paramaters cannot be set together")
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
        log.info('Zipping all downloaded files')
        path = list(downloaded_files.values())[0]
        zip_path = (path.parent / zip)
        with zipfile.ZipFile(zip_path, 'w') as zip_writer:
            for file, path in downloaded_files.items():
                log.debug('Writing %s to %s' % (
                    path,
                    zip_path
                ))
                zip_writer.write(path)
                os.remove(path)
        log.info('Successfully zipped all downloaded files')
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

async def extract_info_coro(
    url: str,
    download: bool=True,
    unzip: bool=False,
    loop: asyncio.AbstractEventLoop=None,
    **kwargs
) -> File:
    """
    |coro|

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
    loop: :class:`asyncio.AbstractEventLoop`
        Set asyncio event loop,
        default to `None`.
    **kwargs
        These parameters will be passed to `File.download()`

    Return
    -------
    :class:`File`
    """
    def process_download(file, kwargs, unzip):
        file_path = file.download(**kwargs)
        if unzip:
            extract_archived_file(str(file_path))
    info = await get_info_coro(url, loop)
    file = File(info)
    _loop = loop or asyncio.get_event_loop()
    if download:
        await _loop.run_in_executor(None, lambda: process_download(file, kwargs, unzip))
    return file

async def download_coro(
    *urls,
    zip: str=None,
    unzip: bool=False,
    loop: asyncio.AbstractEventLoop=None,
    **kwargs
) -> List[File]:
    """
    |coro|

    Download multiple zippyshare urls

    Parameters
    -----------
    *urls
        Zippyshare urls.
    zip: :class:`str`
        Zip all downloaded files once finished.
        Zip filename will be taken from :param:`zip`,
        default to `None`.
        NOTE: You can't mix `zip` and `unzip` options together
        with value `True`, it will raise error.
    unzip: :class:`bool`
        Unzip all downloaded files once finished
        (if given file is zip format extract it, otherwise ignore it),
        default to `False`.
        NOTE: You can't mix `zip` and `unzip` options together
        with value `True`, it will raise error.
    loop: :class:`asyncio.AbstractEventLoop`
        Set asyncio event loop,
        default to `None`.
    **kwargs
        These parameters will be passed to `File.download()`,
        except for parameter `filename`.

    Return
    -------
    :class:`List[File]`
    """
    if unzip and zip:
        raise ValueError("unzip and zip paramaters cannot be set together")
    _loop = loop or asyncio.get_event_loop()
    downloaded_files = {}
    files = []
    for url in urls:
        info = await get_info_coro(url, loop=loop)
        file = File(info)
        files.append(file)
        if kwargs.get('filename') is not None:
            kwargs.pop('filename')
        def process_download(downloaded_files, file, kwargs, unzip):
            file_path = file.download(**kwargs)
            downloaded_files[file] = file_path
            if unzip:
                extract_archived_file(str(file_path))
        await _loop.run_in_executor(None, lambda: process_download(downloaded_files, file, kwargs, unzip))
    if zip:
        def process_zip(downloaded_files):
            log.info('Zipping all downloaded files')
            path = list(downloaded_files.values())[0]
            zip_path = (path.parent / zip)
            with zipfile.ZipFile(zip_path, 'w') as zip_writer:
                for file, path in downloaded_files.items():
                    log.debug('Writing %s to %s' % (
                        path,
                        zip_path
                    ))
                    zip_writer.write(path)
                    os.remove(path)
            log.info('Successfully zipped all downloaded files')
        await _loop.run_in_executor(None, lambda: process_zip(downloaded_files))
    return files