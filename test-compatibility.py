from zippyshare_downloader import Zippyshare

z = Zippyshare(replace=True)

url = 'https://www54.zippyshare.com/v/bbvLtnKG/file.html'

print(z.extract_info(url, download=False))