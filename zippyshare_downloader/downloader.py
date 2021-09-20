import aiohttp
import asyncio
import tqdm
import os
import time
import logging
from download import download

log = logging.getLogger(__name__)

# re.compile('bytes=([0-9]{1,}|)-([0-9]{1,}|)', re.IGNORECASE)

class BaseDownloader:
    def download(self):
        """Download the file"""
        raise NotImplementedError

    def cleanup(self):
        "Do the cleanup, Maybe close the session or the progress bar ? idk."
        raise NotImplementedError

class FileDownloader(BaseDownloader):
    def __init__(self, url, file, progress_bar=True, replace=False) -> None:
        # download() parameters
        self.kwargs = {
            'progressbar': progress_bar,
            'replace': replace,
            'url': url,
            'path': str(file),
            'kind': 'file',
            'verbose': False
        }

    def download(self):
        download(**self.kwargs)

class AsyncFileDownloader(BaseDownloader):
    """FileDownloader for async process using aiohttp with resumeable support"""
    def __init__(self, url, file, progress_bar=True, replace=False, **headers) -> None:
        self.url = url
        self.file = str(file) + '.temp'
        self.real_file = file
        self.progress_bar = progress_bar
        self.replace = replace
        self.headers_request = headers
        self.session = aiohttp.ClientSession()
        if headers.get('Range') is not None and self._get_file_size(self.file):
            raise ValueError('"Range" header is not supported while in resume state')

        self._tqdm = None
    
    def _build_progres_bar(self, initial_size, file_sizes):
        if self.progress_bar:
            self._tqdm = tqdm.tqdm(
                desc='file_sizes',
                initial=initial_size or 0,
                total=file_sizes,
                unit='B',
                unit_scale=True,
                ncols=80
            )

    def _update_progress_bar(self, n):
        if self._tqdm:
            self._tqdm.update(n)

    def _get_file_size(self, file):
        if os.path.exists(file):
            return os.path.getsize(file)
        else:
            return None

    def _parse_headers(self, initial_sizes):
        headers = self.headers_request or {}

        if initial_sizes:
            headers['Range'] = 'bytes=%s-' % initial_sizes
        return headers
        

    async def download(self):
        initial_file_sizes = self._get_file_size(self.file)

        # Parse headers
        headers = self._parse_headers(initial_file_sizes)

        # Initiate request
        resp = await self.session.get(self.url, headers=headers)

        # Grab the file sizes
        file_sizes = float(resp.headers.get('Content-Length'))

        # If "Range" header request is present
        # Content-Length header response is not same as full size
        if initial_file_sizes:
            file_sizes += initial_file_sizes

        real_file_sizes = self._get_file_size(self.real_file)
        if real_file_sizes:
            if file_sizes == real_file_sizes and not self.replace:
                log.info('File exist and replace is False, cancelling download...')
                return

        # Build the progress bar
        self._build_progres_bar(initial_file_sizes, float(file_sizes))

        # Heavily adapted from https://github.com/choldgraf/download/blob/master/download/download.py#L377-L390
        chunk_size = 2 ** 16
        with open(self.file, 'ab' if initial_file_sizes else 'wb') as writer:
            while True:
                t0 = time.time()
                chunk = await resp.content.read(chunk_size)
                dt = time.time() - t0
                if dt < 0.005:
                    chunk_size *= 2
                elif dt > 0.1 and chunk_size > 2 ** 16:
                    chunk_size = chunk_size // 2
                if not chunk:
                    break
                writer.write(chunk)
                if self._tqdm is not None:
                    self._tqdm.update(len(chunk))
        
        os.rename(self.file, self.real_file)

    async def cleanup(self):
        await self.session.close()

        # Close the progress bar
        if self._tqdm:
            self._tqdm.close()

        # to stop aiohttp yelling "unclosed connector bla bla bla"
        await asyncio.sleep(0.25)
