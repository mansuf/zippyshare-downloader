import asyncio
import logging
from json import dumps
from zippyshare_downloader.cli.utils import (
    setup_args,
    setup_logging,
    build_kwargs,
    pretty_print_result,
    InvalidParameter
)
from zippyshare_downloader.fetcher import (
    download_stdout,
    extract_info_coro,
    download_coro,
    extract_info,
    download
)
from zippyshare_downloader.network import Net

__all__ = (
    'main',
)

def process(**kwargs):
    silent = kwargs.pop('silent')
    json = kwargs.pop('json')
    # We don't do fast download in non-async here
    fast = kwargs.pop('fast')
    if fast:
        log.error('--fast option must be used with --async option')
        raise InvalidParameter('--fast option must be used with --async option')

    urls = kwargs.pop('urls')
    
    # If urls is grabbed from file
    if isinstance(urls, list):

        # We don't do stdout download here if given urls is grabbed from file
        if kwargs.pop('pipe'):
            raise InvalidParameter('-pipe are not supported with multiple zippyshare urls')

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
        
        # Print all file informations 
        if json:
            print(dumps({'urls': [file.to_JSON() for file in files]}))
        elif not silent:
            for file in files:
                pretty_print_result(file)

    # If urls is single url
    else:
        # download to stdout
        if kwargs.pop('pipe'):
            download_stdout(urls)
            return

        kwargs.pop('zip')
        file = extract_info(urls, **kwargs)
        if json:
            print(file.to_JSON())
        elif not silent:
            pretty_print_result(file)

async def process_async(**kwargs):
    silent = kwargs.pop('silent')
    json = kwargs.pop('json')
    # Check if "-pipe" used with --async
    if kwargs.pop('pipe'):
        # if yes, throw errror.
        # Unsupported
        raise InvalidParameter('-pipe cannot be used with --async option')

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
        
        # Print all files informations
        if json:
            print(dumps({'urls': [file.to_JSON() for file in files]}))
        elif not silent:
            for file in files:
                pretty_print_result(file)

    # If urls is single url
    else:
        kwargs.pop('zip')
        file = await extract_info_coro(urls, **kwargs)
        if json:
            print(file.to_JSON())
        elif not silent:
            pretty_print_result(file)

def main():
    global log
    log = logging.getLogger('zippyshare_downloader_null_logging').addHandler(logging.NullHandler())

    # Parse parameters
    args = setup_args()
    kwargs = build_kwargs(args, args.urls)

    # Disable logging if "-pipe" or "--json" or "--silent" is present
    if kwargs.get('pipe') or kwargs.get('json'):
        pass
    else:
        if not args.silent:
            log = setup_logging('zippyshare_downloader', args.verbose)

    # Throw error if "-pipe" and "--no-download" are present
    if kwargs.get('pipe') and not kwargs.get('download'):
        raise InvalidParameter('-pipe cannot be used with --no-download option')

    Net.trust_env = args.proxy_trust_env

    async_process = kwargs.pop('async')
    if not async_process:
        Net.set_proxy(args.proxy)
        process(**kwargs)
        Net.close()
    else:
        # Little helper
        async def run_async():
            if args.proxy:
                Net.set_proxy(args.proxy)
            await process_async(**kwargs)
            await Net.close_async()

        # Using uvloop if installed
        # for faster operations
        try:
            import uvloop # type: ignore
        except ImportError:
            pass
        else:
            uvloop.install()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_async())