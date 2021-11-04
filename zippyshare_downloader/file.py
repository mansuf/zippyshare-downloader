import re
import logging
import json
from pathlib import Path
from datetime import datetime
from .downloader import AsyncFastFileDownloader, AsyncFileDownloader
from download import download

log = logging.getLogger(__name__)

__all__ = (
    'File',
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

        Returns
        --------
        :class:`Path` 
            Zippyshare file downloaded
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
        log.info('Successfully downloaded "%s" %s' % (self.name, extra_word))
        return file_path

    async def download_coro(
        self,
        progress_bar: bool=True,
        replace: bool=False,
        folder: str=None,
        filename: str=None,
        fast: bool=False
    ) -> Path:
        """Same like :meth:`File.download()` but for asynchronous process

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
        fast: :class:`bool`
            Enable Fast download, default to ``False``

        Returns
        --------
        :class:`Path` 
            Zippyshare file downloaded
        """
        if filename:
            _filename = filename
            extra_word = 'as "%s"' % _filename
        else:
            _filename = self.name
            extra_word = ''
        log.info('%sDownloading "%s" %s' % (
            'Fast ' if fast else '',
            self.name,
            extra_word
        ))
        file_path = (Path('.') / (folder if folder else '') / _filename)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        args = (
            self.download_url,
            str(file_path),
            progress_bar,
            replace
        )
        if fast:
            downloader = AsyncFastFileDownloader(*args)
        else:
            downloader = AsyncFileDownloader(*args)
        await downloader.download()
        await downloader.cleanup()
        log.info('Successfully downloaded "%s" %s' % (self.name, extra_word))
        return file_path

    def to_JSON(self):
        """Return all zippyshare informations in JSON"""
        return json.dumps(self._data.copy())
    
    def to_dict(self):
        """Return all zippyshare informations in dict"""
        return self._data.copy()