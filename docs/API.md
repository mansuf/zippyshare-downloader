# zippyshare-downloader Embedding usage (API)

## Functions

- `def extract_info(url: str, download: bool = True, unzip: bool = False, **kwargs) -> File`
    <br>
    Extract all informations in Zippyshare url.
    <br>
    **Parameters:**
    - `url` **type: str**
        <br>
        Zippyshare url
    - `download` **type: bool**
        <br>
        Download given zippyshare url if `True`, 
        default to `True`.
    - `unzip` **type: bool**
        <br>
        Unzip downloaded file once finished
        (if given file is zip or tar format extract it, otherwise ignore it),
        default to `False`.
    - `**kwargs`
        <br>
        These parameters will be passed to `File.download()`
- `def download(*urls, zip: str = None, unzip: bool = False, **kwargs) -> List[File]`
    <br>
    Download multiple zippyshare urls
    <br>
    **Parameters:**
    - `*urls`
        <br>
        Zippyshare urls.
    - `zip` **type: str**
        <br>
        Zip all downloaded files once finished.
        Zip filename will be taken from parameter `zip`,
        default to `None`.
        NOTE: You can't mix `zip` and `unzip` options together
        with setted value, it will raise error.
    - `unzip` **type: bool**
        <br>
        Unzip all downloaded files once finished
        (if given file is zip format extract it, otherwise ignore it),
        default to `False`.
        NOTE: You can't mix `zip` and `unzip` options together
        with setted value, it will raise error.
    - `**kwargs`
        These parameters will be passed to `File.download()`,
        except for parameter `filename`.
- `async def extract_info_coro(url: str, download: bool = True, unzip: bool = False, loop: asyncio.AbstractEventLoop, **kwargs) -> File`
    <br>
    *Coroutine Function*
    <br>
    Extract all informations in Zippyshare url.
    <br>
    **Parameters:**
    - `url` **type: str**
        <br>
        Zippyshare url
    - `download` **type: bool**
        <br>
        Download given zippyshare url if `True`, 
        default to `True`.
    - `unzip` **type: bool**
        <br>
        Unzip downloaded file once finished
        (if given file is zip or tar format extract it, otherwise ignore it),
        default to `False`.
    - `loop` **type: asyncio.AbstractEventLoop**
        <br>
        Set asyncio event loop,
        default to `None`.
    - `**kwargs`
        <br>
        These parameters will be passed to `File.download()`
- `async def download(*urls, zip: str = None, unzip: bool = False, loop: asyncio.AbstractEventLoop, **kwargs) -> List[File]`
    <br>
    *Coroutine Function*
    <br>
    Download multiple zippyshare urls
    <br>
    **Parameters:**
    - `*urls`
        <br>
        Zippyshare urls.
    - `zip` **type: str**
        <br>
        Zip all downloaded files once finished.
        Zip filename will be taken from parameter `zip`,
        default to `None`.
        NOTE: You can't mix `zip` and `unzip` options together
        with setted value, it will raise error.
    - `unzip` **type: bool**
        <br>
        Unzip all downloaded files once finished
        (if given file is zip format extract it, otherwise ignore it),
        default to `False`.
        NOTE: You can't mix `zip` and `unzip` options together
        with setted value, it will raise error.
    - `loop` **type: asyncio.AbstractEventLoop**
        <br>
        Set asyncio event loop,
        default to `None`.
    - `**kwargs`
        These parameters will be passed to `File.download()`,
        except for parameter `filename`.