## zippyshare-downloader

Download file from zippyshare directly from python

Simple usage:

```python

from zippyshare_downloader import Zippyshare

z = Zippyshare()
z.download('give zippyshare url here')

```

extract info usage:

```python

from zippyshare_downloader import Zippyshare

z = Zippyshare()
info = z.extract_info('give zippyshare url here')

print(info)

# {'name_file': ..., 'size': ..., 'date_upload': ....}
```
