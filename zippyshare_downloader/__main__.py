import argparse
import asyncio
import json
import os
import logging
from zippyshare_downloader.parser import get_info, parse_info
from zippyshare_downloader import *
from zippyshare_downloader.utils import check_valid_zippyshare_url as cvzu

log = logging.getLogger('zippyshare_downloader')

def check_valid_zippyshare_url(url):
    if os.path.exists(url):
        with open(url, 'r') as opener:
            return [cvzu(i.replace('\n', '')) for i in opener.readlines() if i.replace('\n', '')]
    else:
        return cvzu(url)

async def main_coro(urls, args):
    if isinstance(urls, list):
        if args.no_download:
            files = []
            for url in urls:
                files.append(await extract_info_coro(url, False))
        else:
            files = await download_coro(
                *urls,
                zip=args.zip,
                unzip=args.unzip,
                folder=args.folder,
                progress_bar=not args.silent,
                replace=args.replace
            )
        print(json.dumps({"urls": [file.to_dict() for file in files]}))
    else:
        file = await extract_info_coro(
            urls,
            not args.no_download,
            args.unzip,
            folder=args.folder,
            progress_bar=not args.silent,
            replace=args.replace
        )
        print(file.to_JSON())

def _main(urls, args):
    if isinstance(urls, list):
        if args.no_download:
            files = []
            for url in urls:
                files.append(extract_info(url, False))
        else:
            files = download(
                *urls,
                zip=args.zip,
                unzip=args.unzip,
                folder=args.folder,
                progress_bar=not args.silent,
                replace=args.replace
            )
        print(json.dumps({"urls": [file.to_dict() for file in files]}))
    else:
        file = extract_info(
            urls,
            not args.no_download,
            args.unzip,
            folder=args.folder,
            progress_bar=not args.silent,
            replace=args.replace
        )
        print(file.to_JSON())


def main():
    parser = argparse.ArgumentParser(description='Download file from zippyshare directly from python')
    parser.add_argument(
        'ZIPPYSHARE_URL or FILE',
        type=check_valid_zippyshare_url,
        help='Zippyshare URL or file containing zippyshare urls'
    )
    parser.add_argument('--no-download', action='store_true', help='No download file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose')
    parser.add_argument('--replace', '-r', action='store_true', help='Replace file if exist')
    parser.add_argument('--silent', '-s', action='store_true', help='No output')
    parser.add_argument('--folder', help='Store downloaded file in given folder', metavar='FOLDER')
    parser.add_argument('--filename', help='Set a replacement filename. will be ignored if using multiple zippyshare urls')
    parser.add_argument('--zip', '-z', help='Zip all downloaded files (if using multiple zippyshare urls) once finished, ' \
                        'the zip filename will be taken from this option. NOTE: You can\'t combine --zip ' \
                        'and --unzip options, it will throw error.', metavar='FILENAME')
    parser.add_argument('--unzip', '-uz', help='Unzip all downloaded files, one by one. ' \
                        'NOTE: You can\'t combine --zip and --unzip options, it will throw error.', action='store_true')
    parser.add_argument('--async', help='Run zippyshare-downloader in asynchronous process', action='store_true')
    args = parser.parse_args()
    urls = args.__dict__['ZIPPYSHARE_URL or FILE']
    if not args.silent:
        # Set up logging output
        handler = logging.StreamHandler()
        fmt = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(fmt)
        log.addHandler(handler)
        if args.verbose:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
    if isinstance(urls, list) and args.filename:
        log.warning('Using multi zippyshare urls and --filename is set, ' \
                    'Ignoring --filename option')
    if args.__dict__['async']:
        asyncio.run(main_coro(urls, args))
    else:
        _main(urls, args)

if __name__ == "__main__":
    main()


