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

def extract_multi_urls(z, urls, download=True, silent=True, folder=None):
    us = []
    result = {'urls': us}
    for u in urls:
        us.append(z.extract_info(u, download=download, folder=folder))
    if not silent and download is True:
        print(json.dumps(result))
    elif download is False:
        print(json.dumps(result))

def extract_single_urls(z, url, download=True, silent=True, folder=None, custom_filename=None):
    result = json.dumps(z.extract_info(url, download=download, folder=folder, custom_filename=custom_filename))
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
    parser.add_argument('--output-folder', help='Store downloaded file in given folder', metavar='OUTPUT_FOLDER')
    parser.add_argument('--filename', help='Rewrite filename. will be ignored if using multiple zippyshare urls')
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
            extract_multi_urls(z, urls, download=False, silent=args.silent, folder=args.output_folder)
        else:
            extract_multi_urls(z, urls, download=True, silent=args.silent, folder=args.output_folder)
    else:
        if args.no_download:
            extract_single_urls(
                z,
                urls,
                download=False,
                silent=args.silent,
                folder=args.output_folder,
                custom_filename=args.filename
            )
        else:
            extract_single_urls(
                z,
                urls,
                download=True,
                silent=args.silent,
                folder=args.output_folder,
                custom_filename=args.filename
            )

if __name__ == "__main__":
    main()


