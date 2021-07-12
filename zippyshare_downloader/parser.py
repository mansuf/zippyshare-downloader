# zippyshare-downloader
# parser.py

import asyncio
import json
import aiohttp
import re
import requests
import logging
import urllib.parse
from bs4 import BeautifulSoup
from typing import Any, Dict
from download import download
from pathlib import Path
from datetime import datetime
from .patterns import PATTERNS
from .errors import ParserError, FileExpired

log = logging.getLogger(__name__)

__all__ = (
    'File', 'get_info', 'parse_info',
    'finalization_info', 'get_info_coro'
)

class File:
    def __init__(self, data) -> None:
        self._data = data

    def __repr__(self) -> str:
        return '<Zippyshare File name="%s" size="%s">' % (
            self.name,
            self.size
        )

    @property
    def name(self) -> str:
        """Return name of the file"""
        return self._data['name_file']

    @property
    def size(self) -> float:
        """Return size of the file, in bytes."""
        re_num = re.compile(r'[0-9.]{1,}')
        return float(re_num.match(self._data['size']).group()) * 1000 * 1000

    @property
    def date_uploaded(self) -> datetime:
        """Return date that this file uploaded."""
        date_format = '%d-%m-%Y %H:%M'
        return datetime.strptime(self._data['date_upload'], date_format)
    
    @property
    def download_url(self) -> str:
        """Return downloadable url"""
        return self._data['download_url']

    def download(
        self,
        progress_bar: bool=True,
        replace: bool=False,
        folder: str=None,
        filename: str=None
    ) -> Path:
        """
        Download this file
        
        Parameters
        ------------
        progress_bar: :class:`bool`
            Enable/Disable progress bar,
            default to `True`
        replace: :class:`bool`
            Replace file if exist,
            default to `False`
        folder: :class:`str`
            Set a folder where to store downloaded file,
            default to `None`.
        filename: :class:`str`
            Set a replacement filename, default to `None`.

        Return
        --------
        :class:`Path` this file downloaded
        """
        if filename:
            _filename = filename
            extra_word = 'as "%s"' % _filename
        else:
            _filename = self.name
            extra_word = ''
        log.info('Downloading "%s" %s' % (self.name, extra_word))
        file_path = (Path('.') / (folder if folder else '') / _filename)
        download(
            self.download_url,
            str(file_path),
            progressbar=progress_bar,
            replace=replace,
            verbose=False
        )
        log.info('Successfully downloaded "%s"' % self.name)
        return file_path

    def to_JSON(self):
        """Return all zippyshare informations in JSON"""
        return json.dumps(self._data.copy())
    
    def to_dict(self):
        """Return all zippyshare informations in dict"""
        return self._data.copy()


def parse_info(url, body_html) -> Dict[str, str]:
    """
    Parse required informations from request Zippyshare url.
    """
    parser = BeautifulSoup(body_html, 'html.parser')
    list_infos = []
    log.debug('Getting Name file, size, date upload.')
    for element in parser.find_all('font'):
        str_element = str(element)
        # Size file, Uploaded
        if str_element.startswith('<font style="line-height:18px; font-size: 13px;">'):
            list_infos.append(element)
        # Name file
        elif str_element.startswith('<font style="line-height:22px; font-size: 14px;">'):
            list_infos.append(element)
        # Name file
        elif str_element.startswith('<font style="line-height:20px; font-size: 14px;">'):
            list_infos.append(element)
    log.debug('Getting download url.')
    for pattern in PATTERNS:
        try:
            download_url = pattern(body_html, url)
        except Exception as e:
            log.debug('%s failed to get download url, %s: %s' % (
                pattern.__name__,
                e.__class__.__name__,
                str(e)
            ))
            continue
        else:
            log.debug('%s success to get download url' % pattern.__name__)
            return {
                "name_file": list_infos[0].decode_contents(),
                "size": list_infos[1].decode_contents(),
                "date_upload": list_infos[2].decode_contents(),
                'download_url': download_url
            }
    log.exception('all patterns parser failed to get required informations')
    raise ParserError('all patterns parser is failed to get required informations')

def _get_absolute_filename(info):
    r = requests.get(info['download_url'], stream=True)
    new_namefile = r.headers['Content-Disposition'].replace('attachment; filename*=UTF-8\'\'', '')
    info['name_file'] = urllib.parse.unquote(new_namefile)
    r.close()
    return info

def finalization_info(info) -> Dict[str, str]:
    """
    Fix if required informations contains invalid info.
    """
    # Fix https://github.com/mansuf/zippyshare-downloader/issues/4
    if '<img alt="file name" src="/fileName?key' in info['name_file']:
        log.warning('Filename is in image not in text, running additional fetch...')
        return _get_absolute_filename(info)
    
    # Fix https://github.com/mansuf/zippyshare-downloader/issues/5
    elif len(info['name_file']) > 70:
        log.warning('Filename is too long, running additional fetch...')
        return _get_absolute_filename(info)
    else:
        return info

def get_info(url) -> Dict[str, str]:
    """
    Get informations in Zippyshare url.

    NOTE: You will have to call function `finalization_info()`
    to fix incorrect informations (if detected).
    """
    log.info('Grabbing required informations in %s' % url)
    log.debug('Establishing connection to Zippyshare.')
    r = requests.get(url)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        log.exception('Zippyshare send %s code' % r.status_code)
        raise e from None
    log.debug('Successfully established connection to Zippyshare.')
    log.debug('Checking if file is not expired')
    if 'File has expired and does not exist anymore on this server' in r.text:
        log.exception('File has expired and does not exist anymore')
        raise FileExpired('File has expired and does not exist anymore')
    log.debug('Checking if file is exist')
    if 'File does not exist on this server' in r.text:
        log.exception('File does not exist on this server')
        raise FileNotFoundError('File does not exist on this server')
    return parse_info(url, r.text)

async def get_info_coro(url, loop=None) -> Dict[str, str]:
    """
    |coro|

    Get informations in Zippyshare url.

    Unlike `get_info()` when you have to call `finalization_info()` manually
    to fix incorrect informations.
    This function automatically called it.
    """
    def parse(url, body_html):
        return finalization_info(parse_info(url, body_html))
    log.info('Grabbing required informations in %s' % url)
    log.debug('Establishing connection to Zippyshare.')
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        try:
            r.raise_for_status()
        except aiohttp.ClientResponseError as e:
            log.exception('Zippyshare send %s code' % r.status)
            raise e from None
        body_html = await r.text()
        log.debug('Successfully established connection to Zippyshare.')
        log.debug('Checking if file is not expired')
        if 'File has expired and does not exist anymore on this server' in body_html:
            log.exception('File has expired and does not exist anymore')
            raise FileExpired('File has expired and does not exist anymore')
        log.debug('Checking if file is exist')
        if 'File does not exist on this server' in body_html:
            log.exception('File does not exist on this server')
            raise FileNotFoundError('File does not exist on this server')
        _loop = loop or asyncio.get_event_loop()
        return await _loop.run_in_executor(None, lambda: parse(url, body_html))
        