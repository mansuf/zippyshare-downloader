import asyncio
import requests
import aiohttp
import urllib.parse
from zippyshare_downloader import extract_info, extract_info_coro

url = 'https://www54.zippyshare.com/v/bbvLtnKG/file.html'

file = extract_info(url, download=True)
download_url = file.download_url


response = requests.get(download_url, stream=True)
if response.url != download_url:
    raise Exception('Download url redirected')

# Testing async process

async def run():
    file = await extract_info_coro(url)

    download_url = file.download_url

    async with aiohttp.ClientSession() as session:
        response = await session.get(download_url)
        # For some reason, response.url got unquoted URL
        if str(response.url) != urllib.parse.unquote(download_url):
            raise Exception('Download url redirected')
    

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
response.close()