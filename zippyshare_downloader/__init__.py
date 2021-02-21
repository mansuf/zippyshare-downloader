# zippyshare-downloader
# __init__.py

"""
zippyshare-downloader

Download file from zippyshare directly from python
"""

__VERSION__ = 'v0.0.13'

from zippyshare_downloader.utils import getStartandEndvalue
from bs4 import BeautifulSoup
from download import download as dl
from .utils import check_valid_zippyshare_url
import requests
import math

class Zippyshare:
    ALLOWED_NAMES = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }

    def __init__(self, verbose=True, progress_bar=True, replace=True):
        self._verbose = verbose
        self._progress_bar = progress_bar
        self._replace = replace
    
    def _logger_info(self, message):
        if self._verbose:
            print('[INFO] %s' % (message))
        else:
            return

    def _get_url(self, u, r: requests.Request):
        self._logger_info('Getting Download URL')
        startpos_init = r.text.find('document.getElementById(\'dlbutton\').href')
        scrapped_init = r.text[startpos_init:]
        endpos_init = scrapped_init.find('</script>')
        scrapped = scrapped_init[:endpos_init]
        element_value = scrapped[:scrapped.find(';')].replace('document.getElementById(\'dlbutton\').href = ', '')
        url_download_init = getStartandEndvalue(element_value, '"')
        random_number = getStartandEndvalue(element_value, '(', ')')
        # Now using self.evaluate() to safely do math calculations
        url_number = str(self.evaluate(random_number))
        continuation_download_url_init = getStartandEndvalue(element_value, '(')
        continuation_download_url = continuation_download_url_init[continuation_download_url_init.find('"')+1:]
        return u[:u.find('.')] + '.zippyshare.com' + url_download_init + url_number + continuation_download_url

    def _get_info(self, u, r: requests.Request):
        self._logger_info('Parsing info')
        if 'File has expired and does not exist anymore on this server' in r.text:
            raise FileNotFoundError('File has expired and does not exist anymore')
        parser = BeautifulSoup(r.text, 'html.parser')
        list_infos = []
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
        return {
                'name_file': list_infos[0].decode_contents(),
                'size': list_infos[1].decode_contents(),
                'date_upload': list_infos[2].decode_contents(),
                'download_url': self._get_url(u, r)
            }

    def _request_get(self, url):
        self._logger_info('Fetching URL')
        return requests.get(url)

    def _extract_info(self, url, download=True):
        check_valid_zippyshare_url(url)
        r = self._request_get(url)
        info = self._get_info(url, r)
        if download:
            self._logger_info('Downloading "%s"' % (info['name_file']))
            dl(info['download_url'], info['name_file'], progressbar=self._progress_bar, verbose=self._verbose, replace=self._replace)
            return info
        else:
            return info
        
    def _download(self, urls):
        for url in urls:
            r = self._request_get(url)
            info = self._get_info(url, r)
            dl(info['download_url'], info['name_file'], progressbar=self._progress_bar, verbose=self._verbose, replace=self._replace)

    def download(self, *urls):
        self._download(urls)

    def extract_info(self, url: str, download=True):
        return self._extract_info(url, download=download)

    # Credit for the evaluate() method: Leodanis Pozo Ramos  https://realpython.com/python-eval-function/
    def evaluate(self, expression):
        """Evaluate a math expression."""

        # Compile the expression
        code = compile(expression, "<string>", "eval")

        # Validate allowed names
        for name in code.co_names:
            if name not in self.ALLOWED_NAMES:
                    raise NameError(f"The use of '{name}' is not allowed. Expression used: %s" % (expression))

        return eval(code, {"__builtins__": {}}, self.ALLOWED_NAMES)

