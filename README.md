# zippyshare-downloader

Download file from zippyshare directly from python

### Installation

```bash
pip install zippyshare-downloader
```

### Command Line Interface (CLI) Options

```
ZIPPYSHARE_URL or FILE      Zippyshare URL or file containing zippyshare urls
--no-download               No download file
--verbose                   Enable verbose
--replace                   Replace file if exist
--silent                    No output

# New in v0.0.18

--output-folder             Store downloaded file in given folder
--filename                  Rewrite filename. will be ignored if using multiple zippyshare urls
```

### Command Line Interface (CLI) Usage

```bash

# by default, verbose is disabled
zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose
zippyshare-downloader "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose

# do this if "zippyshare-dl" or "zippyshare-downloader" didn't work
python3 -m zippyshare_downloader "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --verbose

# Output: {'name_file': ..., 'size': ..., 'date_upload': ..., 'download_url': ...}

# if you want to get information from this app
# BUT, you don't wanna download it
# you can use --no-download option

# the output is json format
zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --no-download

# Output: {"name_file": ..., "size": ..., "date_upload": ..., "download_url": ...}

# New in v0.0.17 
# --progress-bar option is removed
# progress bar will be enabled by default
# there is --silent option to remove all output from the app
# but, if you give --silent and --verbose together
# the --verbose option will be ignored

zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --silent

# Output: There is no output...

zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --silent --verbose

# Output: still no output...

# but, if you give --silent option and --no-download together
# --silent option will be ignored
zippyshare-dl "https://www54.zippyshare.com/v/bbvLtnKG/file.html" --no-download --silent

# Output: {"name_file": ..., "size": ..., "date_upload": ..., "download_url": ...}

# New in v0.0.17
# now you can download zippyshare files from a file that containing zippyshare urls
# but, if given file doesn't exist
# the app will look given file as url.
# More explanation in below

# let say you have a .txt file containing zippyshare urls
# and you give filename into the app
# the app will download all of it

# this will download all urls in urls.txt
zippyshare-dl "urls.txt" --verbose

# But, if you provided invalid path to your .txt file
# the app will see filename as url
zippyshare-dl "not-exist-lol/urls.txt" --verbose

# Output: zippyshare_downloader.errors.InvalidURL: "not-exist-lol/urls.txt" is not a zippyshare url

# if you give --no-download option to the app
# while using file containing zippyshare urls
# the app will fetch all information stored in given file
# without downloading it.

# the output is json format
zippyshare-dl "urls.txt" --no-download

# Output: {"urls": [...]}

# New in v0.0.18
# added --output-folder and --filename options

# --output-folder is to store downloaded file in given folder
# example:

# this will create YES folder, download the file and put in YES folder
zippyshare-dl "give zippyshare url here" --output-folder "YES"

# --filename is for rewrite filename, will be ignored if using multiple zippyshare urls
# example:

# this will download the file and rename it to MEMES.mp4
zippyshare-dl "give zippyshare url here" --filename "MEMES.mp4"

# You can combine both options for single zippyshare url.

# this will create YES folder, download the file and put in YES folder
# and rename it to MEMES.mp4.
zippyshare-dl "give zippyshare url here" --filename "MEMES.mp4" --output-folder "YES"

# BUT, you cannot combine both options for multiple zippyshare urls
# the --filename option will be ignored
# for example:


# this will download all files stored in zippyshare-urls.txt and put in to YES folder
# and, not rename all files into MEMES.mp4
zippyshare-dl "zippyshare-urls.txt" --filename "MEMES.mp4" --output-folder "YES"

```


### Embedding Usage

**Use zippyshare-downloader in your python script**

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

# New in v0.0.18 
# added `folder` and `custom_filename` arguments to
# Zippyshare.extract_info()
# and
# added `folder` argument to
# Zippyshare.download()
# `folder` argument is for store downloaded file in given folder
# `custom_filename` argument is for rewrite filename, will be ignored if using file containing zippyshare urls.

# Example usage on Zippyshare.extract_info()
# This will download zippyshare file to YEET folder and rename it to MEMES.mp4
info = z.extract_info('give zippyshare url here', download=True, folder='YEET', custom_filename='MEMES.mp4')

# Example usage on Zippyshare.download()
# This will download all files in URLS to YEET folder
z.download(URLS, folder='YEET')

```

### Minimum Python version

```
3.x
```

### FAQ

**Q:** I always getting `NameError: The use of "bla bla" is not allowed`, what should i do ?<br>
**A:** Zippyshare always change their code, Please update to last version, if your zippyshare-downloader is latest version, then open a issue [here](https://github.com/mansuf/zippyshare-downloader/issues)