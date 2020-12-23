# zippyshare-downloader
# __init__.py

"""
zippyshare-downloader

Download file from zippyshare directly from python
"""

from zippyshare_downloader.utils import getStartandEndvalue
from bs4 import BeautifulSoup
from download import download as dl
import requests

class Zippyshare:
    def __init__(self, verbose=True, progress_bar=True, replace=True):
        self._verbose = verbose
        self._progress_bar = progress_bar
        self._replace = replace
    
    def _get_url(self, u, r: requests.Request):
        startpos_init = r.text.find('document.getElementById(\'dlbutton\').href')
        scrapped_init = r.text[startpos_init:]
        endpos_init = scrapped_init.find('</script>')
        scrapped = scrapped_init[:endpos_init]
        element_value = scrapped[:scrapped.find(';')].replace('document.getElementById(\'dlbutton\').href = ', '')
        url_download_init = getStartandEndvalue(element_value, '"')
        random_number = getStartandEndvalue(element_value, '(', ')')
        url = {}
        exec('url_number = str(%s)' % (random_number), globals(), url)
        continuation_download_url_init = getStartandEndvalue(element_value, '(')
        continuation_download_url = continuation_download_url_init[continuation_download_url_init.find('"')+1:]
        return u[:u.find('.')] + '.zippyshare.com' + url_download_init + url['url_number'] + continuation_download_url

    def _get_info(self, u, r: requests.Request):
        parser = BeautifulSoup(r.text, 'html.parser')
        list_infos = []
        for _i in parser.find_all('font'):
            i = str(_i)
            if i.startswith('<font style="line-height:18px; font-size: 13px;">'):
                list_infos.append(i)
            elif i.startswith('<font style="line-height:22px; font-size: 14px;">'):
                list_infos.append(i)
            elif i.startswith('<font style="line-height:20px; font-size: 14px;">'):
                list_infos.append(i)
        return {
                'name_file': getStartandEndvalue(list_infos[0], '>', '<'),
                'size': getStartandEndvalue(list_infos[1], '>', '<'),
                'date_upload': getStartandEndvalue(list_infos[2], '>', '<'),
                'download_url': self._get_url(u, r)
            }

    def _request_get(self, url):
        return requests.get(url)

    def _extract_info(self, url, download=True):
        r = self._request_get(url)
        info = self._get_info(url, r)
        if download:
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