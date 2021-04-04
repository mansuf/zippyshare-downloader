import argparse
import json
import os
from zippyshare_downloader import Zippyshare
from zippyshare_downloader.utils import check_valid_zippyshare_url as cvzu

def check_valid_zippyshare_url(url):
    if os.path.exists(url):
        with open(url, 'r') as opener:
            return [cvzu(i.replace('\n', '')) for i in opener.readlines()]
    else:
        return cvzu(url)

def extract_multi_urls(z, urls, download=True, silent=True):
    us = []
    result = {'urls': us}
    for u in urls:
        us.append(z.extract_info(u, download=download))
    if not silent and download is True:
        print(json.dumps(result))
    elif download is False:
        print(json.dumps(result))

def extract_single_urls(z, url, download=True, silent=True):
    result = json.dumps(z.extract_info(url, download=download))
    if not silent and download is True:
        print(result)
    elif download is False:
        print(result)

def main():
    parser = argparse.ArgumentParser(description='Download file from zippyshare directly from python')
    parser.add_argument('ZIPPYSHARE_URL or FILE', type=check_valid_zippyshare_url, help='Zippyshare URL or file containing zippyshare urls')
    parser.add_argument('--no-download', action='store_true', help='No download file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose')
    parser.add_argument('--replace', action='store_true', help='Replace file if exist')
    parser.add_argument('--silent', action='store_true', help='No output')
    args = parser.parse_args()
    urls = args.__dict__['ZIPPYSHARE_URL or FILE']
    args.progress_bar = True
    if args.silent == True:
        args.verbose = False
        args.progress_bar = False
    z = Zippyshare(
        progress_bar=args.progress_bar,
        replace=args.replace,
        verbose=args.verbose
    )
    if isinstance(urls, list):
        if args.no_download:            
            extract_multi_urls(z, urls, download=False, silent=args.silent)
        else:
            extract_multi_urls(z, urls, download=True, silent=args.silent)
    else:
        if args.no_download:
            extract_single_urls(z, urls, download=False, silent=args.silent)
        else:
            extract_single_urls(z, urls, download=True, silent=args.silent)

if __name__ == "__main__":
    main()


