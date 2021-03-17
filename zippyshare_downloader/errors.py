# zippyshare-downloader
# errors.py

class InvalidURL(Exception):
    """A class representing Invalid URL Exception"""
    pass

class ParserError(Exception):
    """Raised when error happened during parsing download URL"""
    pass