## zippyshare-downloader

Download file from zippyshare directly from python

### Installation
```
pip install zippyshare-downloader
```

### Command Line Interface (CLI) Usage

```bash

zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose --progress-bar

zippyshare-downloader "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose --progress-bar

# do this if "zippyshare-dl" or "zippyshare-downloader" didn't work
python3 -m zippyshare_downloader "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose --progress-bar

# Output: {'name_file': ..., 'size': ..., 'date_upload': ..., 'download_url': ...}
```


### Embedding Usage

**Use zippyshare-downloader module in your python script**

```python

from zippyshare_downloader import Zippyshare

# By default, verbose is True, progress_bar is True, and replace is True
z = Zippyshare(verbose=True, progress_bar=True, replace=True)


# If you want to get info from Zippyshare URL
# and you want to download it
# do: z.extract_info('give Zippyshare URL here')
# see example below

# by default, download is True
info = z.extract_info('give zippyshare url here', download=True)

print(info)
# Output: {'name_file': ..., 'size': ..., 'date_upload': ..., 'download_url': ...}

# If you want to get info from Zippyshare URL
# BUT, you don't wanna download it
# do: z.extract_info('give zippyshare URL here', download=False)
# see example below

info = z.extract_info('give zippyshare url here', download=False)

...

# If you want to download from list or tuple urls
# do: z.download(['give zippyshare url here'])
# see example below

URLS = [
    'give zippyshare url here',
    'give zippyshare url here',
    'give zippyshare url here',
    'give zippyshare url here',
    'give zippyshare url here',
]

z.download(URLS)

```

### Minimum Python version

```
3.x
```

### FAQ

**Q:** I always getting `NameError: The use of "bla bla" is not allowed`, what should i do ?<br>
**A:** Zippyshare always change their code, Please update to last version, if your zippyshare-downloader is latest version, then open a issue [here](https://github.com/mansuf/zippyshare-downloader/issues)