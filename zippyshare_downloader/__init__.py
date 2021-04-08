# zippyshare-downloader
# __init__.py

"""
zippyshare-downloader

Download file from zippyshare directly from python
"""

__VERSION__ = 'v0.0.18'

from zippyshare_downloader.utils import getStartandEndvalue
from bs4 import BeautifulSoup
from download import download as dl
from .utils import check_valid_zippyshare_url
from .errors import ParserError, InvalidURL
import requests
import math
import os
import io

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

    def _logger_warn(self, message):
        if self._verbose:
            print('[WARN] %s' % (message))
        else:
            return

    def _logger_error(self, message):
        if self._verbose:
            print('[ERROR] %s' % (message))
        else:
            return

    def _get_url(self, u, r: requests.Request):
        self._logger_info('Getting Download URL from "%s"' % (u))
        # Getting download button javascript code
        parser = BeautifulSoup(r.text, 'html.parser')
        for script in parser.find_all('script'):
            if 'document.getElementById(\'dlbutton\').href' in script.decode_contents():
                scrapped_script = script.decode_contents()
                break
            else:
                scrapped_script = None
        if scrapped_script is None:
            raise ParserError('download button javascript cannot be found')

        # Finding omg attribute value in dlbutton element
        elements = io.StringIO(scrapped_script).readlines()
        omg_element = 'document.getElementById(\'dlbutton\').omg = '
        for element in elements:
            e = element.strip()
            if e.startswith(omg_element):
                omg = e.replace(omg_element, '').replace('"', '').replace(';', '')
                break
            else:
                omg = None
        if omg is None:
            raise ParserError('omg attribute in download button javascript cannot be found')

        # Finding uncompiled Random Number between FileID and Filename
        # http://www.zippyshare.com/d/{FileID}/uncompiled_number/{Filename}
        startpos_init = scrapped_script.find('document.getElementById(\'dlbutton\').href')
        scrapped_init = scrapped_script[startpos_init:]
        endpos_init = scrapped_init.find(';')
        scrapped = scrapped_init[:endpos_init]
        element_value = scrapped.replace('document.getElementById(\'dlbutton\').href = ', '')
        url_download_init = getStartandEndvalue(element_value, '"')
        uncompiled_number = getStartandEndvalue(element_value, '(', ')')
        
        # Finding Random Number variable a in scrapped_script
        variables = io.StringIO(scrapped_script).readlines()
        for var in variables:
            if var.strip().startswith('var a = '):
                a = var.strip().replace('var a = ', '').replace(';', '')
                break
            else:
                a = None
        if a is None:
            raise ParserError('variable a in download button javascript cannot be found')

        # Finding Random Number variable b in scrapped_script
        variables = io.StringIO(scrapped_script).readlines()
        for var in variables:
            if var.strip().startswith('var b = '):
                b = var.strip().replace('var b = ', '').replace(';', '')
                break
            else:
                b = None
        if b is None:
            raise ParserError('variable b in download button javascript cannot be found')

        if omg != 'f':
            random_number = uncompiled_number.replace('a', str(math.ceil(int(a)/3))).replace('b', b)
        else:
            random_number = uncompiled_number.replace('a', str(math.floor(int(a)/3))).replace('b', b)

        # Now using self.evaluate() to safely do math calculations
        url_number = str(self.evaluate(random_number))
        continuation_download_url_init = getStartandEndvalue(element_value, '(')
        continuation_download_url = continuation_download_url_init[continuation_download_url_init.find('"')+1:]
        return u[:u.find('.')] + '.zippyshare.com' + url_download_init + url_number + continuation_download_url

    def _get_absolute_filename(self, info):
        r = requests.get(info['download_url'], stream=True)
        new_namefile = r.headers['Content-Disposition'].replace('attachment; filename*=UTF-8\'\'', '')
        info['name_file'] = new_namefile
        r.close()
        return info

    def _finalization_info(self, info):
        # Fix https://github.com/mansuf/zippyshare-downloader/issues/4
        if '<img alt="file name" src="/fileName?key' in info['name_file']:
            self._logger_warn('Filename is in image not in text, running additional fetch...')
            return self._get_absolute_filename(info)

        # Fix https://github.com/mansuf/zippyshare-downloader/issues/5
        elif len(info['name_file']) > 70:
            self._logger_warn('Filename is too long, running additional fetch...')
            return self._get_absolute_filename(info)
        else:
            return info


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
        return self._finalization_info({
                'name_file': list_infos[0].decode_contents(),
                'size': list_infos[1].decode_contents(),
                'date_upload': list_infos[2].decode_contents(),
                'download_url': self._get_url(u, r)
            })

    def _request_get(self, url):
        self._logger_info('Fetching URL "%s"' % (url))
        return requests.get(url)

    def _extract_info(self, url, download=True, folder=None, custom_filename=None):
        try:
            check_valid_zippyshare_url(url)
        except InvalidURL as e:
            self._logger_error(str(e))
            raise e
        r = self._request_get(url)
        if r.status_code != 200:
            self._logger_error('Zippyshare send %s code' % (r.status_code))
        info = self._get_info(url, r)
        if download:
            self._logger_info('Downloading "%s"' % (info['name_file']))
            if folder is not None and isinstance(folder, str):
                if custom_filename is not None and isinstance(custom_filename, str):
                    self._logger_info('Using custom filename "%s"' % (custom_filename))
                    path = os.path.join(os.getcwd(), folder, custom_filename)
                else:
                    path = os.path.join(os.getcwd(), folder, info['name_file'])
            else:
                path = info['name_file']
            self._logger_info(f'Using directory "{os.path.join(os.getcwd(), folder)}"')
            dl(
                info['download_url'],
                path,
                progressbar=self._progress_bar,
                verbose=self._verbose,
                replace=self._replace
            )
            return info
        else:
            return info
        
    def _download(self, urls, folder=None):
        for url in urls:
            try:
                check_valid_zippyshare_url(url)
            except InvalidURL as e:
                self._logger_error(str(e))
                raise e
            r = self._request_get(url)
            if r.status_code != 200:
                self._logger_error('Zippyshare send %s code' % (r.status_code))
            info = self._get_info(url, r)
            self._logger_info('Downloading "%s"' % (info['name_file']))
            if folder is not None and isinstance(folder, str):
                path = os.path.join(os.getcwd(), folder, info['name_file'])
            else:
                path = info['name_file']
            self._logger_info(f'Using directory "{os.path.join(os.getcwd(), folder)}"')
            dl(
                info['download_url'],
                path,
                progressbar=self._progress_bar,
                verbose=self._verbose,
                replace=self._replace
            )

    def download(self, urls: list or tuple, folder=None):
        if isinstance(urls, list) or isinstance(urls, tuple):
            pass
        else:
            raise InvalidURL('urls expecting list or tuple type, got %s' % (type(urls)))
        self._download(urls, folder=folder)

    def extract_info(self, url: str, download=True, folder=None, custom_filename=None):
        return self._extract_info(
            url,
            download=download,
            folder=folder,
            custom_filename=custom_filename
        )

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

