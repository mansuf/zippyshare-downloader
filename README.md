# zippyshare-downloader

Download file from zippyshare directly from python

## Minimum Python version

```
3.5.x
```

## Installation

### Python Packages Index (PyPI)

```bash
pip install zippyshare-downloader
```

### From the source

Clone the repository
```
git clone https://github.com/mansuf/zippyshare-downloader.git
cd zippyshare-downloader
```

And then run `setup.py`
```
python setup.py install
```

### Command Line Interface (CLI) Options

```
ZIPPYSHARE_URL or FILE          Zippyshare URL or file containing zippyshare urls
--no-download                   No download file
--verbose, -v                   Enable verbose
--replace, -r                   Replace file if exist
--silent                        No output

# New in v0.0.18

--folder FOLDER                 Store downloaded file in given folder
--filename FILENAME             Rewrite filename. will be ignored if using multiple zippyshare urls

# New in v0.0.21

--zip FILENAME, -z FILENAME     Zip all downloaded files (if using multiple zippyshare urls) once finished, the zip
                                filename will be taken from this option. 
                                NOTE: You can't combine --zip and --unzip options, it will throw error.
--unzip, -uz                    Unzip all downloaded files, one by one.
                                NOTE: You can't combine --zip and --unzip options, it will throw error.
--async                         Run zippyshare-downloader in asynchronous process

```

### Command Line Interface (CLI) Usage

### FAQ

**Q:** I always getting `NameError: The use of "bla bla" is not allowed`, what should i do ?<br>
**A:** Zippyshare always change their code, Please update to last version, if your zippyshare-downloader is latest version, then open a issue [here](https://github.com/mansuf/zippyshare-downloader/issues)