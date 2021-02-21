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


### Simple usage

```python

from zippyshare_downloader import Zippyshare

z = Zippyshare()
z.download('give zippyshare url here')

```

### Getting Information usage

```python

from zippyshare_downloader import Zippyshare

z = Zippyshare()
info = z.extract_info('give zippyshare url here')

print(info)

# {'name_file': ..., 'size': ..., 'date_upload': ..., 'download_url': ...}
```
