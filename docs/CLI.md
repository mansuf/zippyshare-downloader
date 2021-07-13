# zippyshare-downloader Command Line Interface (CLI) usage

## Options

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

## App names

There is few app names in zippyshare-downloader:
- `zipyshare-dl`
- `zippyshare-downloader`

**If none of above doesn't work use this: `python -m zippyshare_downloader`**

## Usage

### Simple download

Downloading file from zippyshare with verbose output

```bash
zippyshare-dl "insert zippyshare url here" --verbose
```

### Download from file containing URLs

```bash
zippyshare-dl "urls.txt"
```

**NOTE:** if given file is not valid, `zippyshare-dl` will see file as URL.
<br>
See example below:

```bash
zippyshare-dl "not-exist-lol.txt"

# Output: zippyshare_downloader.errors.InvalidURL: "not-exist-lol.txt" is not a zippyshare url
```

### Download with no output

Download zippyshare file with no output

**NOTE:** In the end, it still giving output containing file informations in JSON format. 

```bash
zippyshare-dl "insert zippyshare url here" --silent

# Output: {"name_file": ..., "size": ..., "date_upload": ..., "download_url": ...}
```

### Download and replace downloaded file (if exist)

```bash
zippyshare-dl "insert zippyshare url here" --replace
```

### Download and store it to another folder

```bash
zippyshare-dl "insert zippyshare url here" --folder "folder"
```

### Download using different filename

```bash
zippyshare-dl "insert zippyshare url here" --filename "memes.mp4"
```

**NOTE:** This option is ignored when using multiple zippyshare urls.
<br>
See example below:

```bash
zippyshare-dl "urls.txt" --filename "memes.mp4"

# Output: [WARNING] Using multi zippyshare urls and --filename is set, Ignoring --filename option
# ...
```

### Download all files and zip it

**NOTE:** This only work using multiple zippyshare urls.

```bash
zippyshare-dl "urls.txt" --zip "zipped.zip"
```

### Download file and unzip (if downloaded file is zip or tar format)

```bash
zippyshare-dl "insert zippyshare url here" --unzip
```

### Download in another thread

```bash
zippyshare-dl "insert zippyshare url here" --async
```
