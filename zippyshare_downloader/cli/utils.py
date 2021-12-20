import argparse
import logging
import os
from ..utils import check_valid_zippyshare_url

def _check_urls(url):
    if os.path.exists(url):
        with open(url, 'r') as opener:
            return [check_valid_zippyshare_url(i) for i in opener.read().splitlines()]
    else:
        return check_valid_zippyshare_url(url)

def setup_args():
    parser = argparse.ArgumentParser(description='Download file from zippyshare directly from python')

    # URL or File location
    parser.add_argument(
        'ZIPPYSHARE_URL or FILE',
        type=_check_urls,
        help='Zippyshare URL or file containing zippyshare urls',
    )

    # No download
    parser.add_argument(
        '--no-download',
        action='store_true',
        help='No download file'
    )

    # Verbose output
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    # Replace downloaded file (if exist)
    parser.add_argument(
        '--replace',
        '-r',
        action='store_true',
        help='Replace file if exist'
    )

    # No Output
    parser.add_argument(
        '--silent',
        '-s',
        action='store_true',
        help='No output'
    )

    # Store folder
    parser.add_argument(
        '--folder',
        help='Store downloaded file in given folder',
        metavar='FOLDER'
    )

    # Change filename
    parser.add_argument(
        '--filename',
        help='Set a replacement filename. will be ignored if using multiple zippyshare urls',
        metavar='FILENAME'
    )

    # Zip
    parser.add_argument(
        '--zip',
        '-z',
        help='Zip all downloaded files (if using multiple zippyshare urls) once finished' \
             'the zip filename will be taken from this option. NOTE: you can\'t combine' \
             '--zip and --unzip options, it will throw error.',
        metavar='FILENAME',
    )

    # Unzip each downloaded file
    parser.add_argument(
        '--unzip',
        '-uz',
        help='Unzip all downloaded files, one by one. NOTE: You can\'t combine' \
             '--zip and --unzip options, it will throw error.',
        action='store_true'
    )

    # Async process
    parser.add_argument(
        '--async',
        help='Run zippyshare-downloader in asynchronous process',
        action='store_true',
        dest='async_process'
    )

    # Fast Download
    parser.add_argument(
        '--fast',
        help='Enable Fast Download (Only available with --async option).',
        action='store_true',
    )

    # Stdout download
    parser.add_argument(
        '-pipe',
        help='Download to stdout, useful for piping media content to media player (like vlc)',
        action='store_true'
    )

    args = parser.parse_args()
    urls = args.__dict__['ZIPPYSHARE_URL or FILE']
    args.urls = urls
    return args

def setup_logging(name_module, verbose=False):
    log = logging.getLogger(name_module)
    handler = logging.StreamHandler()
    fmt = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(fmt)
    log.addHandler(handler)
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log

def build_kwargs(args, urls):
    kwargs = {
        'urls': urls,
        'download': not args.no_download,
        'unzip': args.unzip,
        'zip': args.zip,
        'progress_bar': not args.silent,
        'replace': args.replace,
        'folder': args.folder,
        'filename': args.filename,
        'async': args.async_process,
        'fast': args.fast,
        'pipe': args.pipe
    }
    return kwargs
