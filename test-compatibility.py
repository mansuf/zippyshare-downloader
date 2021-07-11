import requests
from zippyshare_downloader import extract_info

url = 'https://www54.zippyshare.com/v/bbvLtnKG/file.html'

file = extract_info(url, download=False)
download_url = file.download_url


response = requests.get(download_url, stream=True)

if response.url != download_url:
    raise Exception('Download url redirected')

response.close()