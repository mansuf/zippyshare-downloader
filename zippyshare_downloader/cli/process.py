import asyncio
import json
import logging
from .utils import setup_args, setup_logging, build_kwargs
from ..fetcher import extract_info_coro, download_coro, extract_info, download

__all__ = (
    'main',
)

def process(**kwargs):
    # We don't do fast download in non-async here
    fast = kwargs.pop('fast')
    if fast:
        log.error('--fast be set and --async is not')
        raise ValueError('--fast be set and --async is not')

    urls = kwargs.pop('urls')
    
    # If urls is grabbed from file
    if isinstance(urls, list):

        # If --no-download is specified
        if not kwargs.get('download'):

            # Warn the users if --unzip is specified
            # while --no-download is exist
            if kwargs.get('unzip'):
                log.warning('--unzip is set, while --no-download is also set. Ignoring --unzip')

            # Begin the fetching !!!
            files = []
            for url in urls:
                files.append(extract_info(url, **kwargs))
        
        # If download is yes
        else:
            kwargs.pop('download')
            files = download(*urls, **kwargs)

            # Warn the users if --filename is specified
            # while using multiple zippyshare urls
            if kwargs.get('filename'):
                log.warning('Using multi zippyshare urls and --filename is set. Ignoring --filename option')
        
        # Print all files informations in JSON format
        print(json.dumps({"urls": [file.to_dict() for file in files]}))

    # If urls is single url
    else:
        kwargs.pop('zip')
        file = extract_info(urls, **kwargs)
        print(file.to_JSON())

async def process_async(**kwargs):
    urls = kwargs.pop('urls')
    
    # If urls is grabbed from file
    if isinstance(urls, list):

        # If --no-download is specified
        if not kwargs.get('download'):

            # Warn the users if --unzip is specified
            # while --no-download is exist
            if kwargs.get('unzip'):
                log.warning('--unzip is set and --no-download is also set. Ignoring --unzip option')

            # Begin the fetching !!!
            files = []
            for url in urls:
                files.append(await extract_info_coro(url, **kwargs))
        
        # If download is yes
        else:
            # Delete download parameter
            kwargs.pop('download')
            
            # Warn the users if --filename is specified
            # while using multiple zippyshare urls
            if kwargs.get('filename'):
                log.warning('Using multi zippyshare urls and --filename is set. Ignoring --filename option')

            files = await download_coro(*urls, **kwargs)
        
        # Print all files informations in JSON format
        print(json.dumps({"urls": [file.to_dict() for file in files]}))

    # If urls is single url
    else:
        kwargs.pop('zip')
        file = await extract_info_coro(urls, **kwargs)
        print(file.to_JSON())

def main():
    global log
    log = logging.getLogger('zippyshare_downloader_null_logging').addHandler(logging.NullHandler())

    # Parse parameters
    args = setup_args()

    # Setup logging
    if not args.silent:
        log = setup_logging('zippyshare_downloader', args.verbose)
    
    kwargs = build_kwargs(args, args.urls)

    async_process = kwargs.pop('async')
    if not async_process:
        process(**kwargs)
    else:
        asyncio.run(process_async(**kwargs))