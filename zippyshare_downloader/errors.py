# zippyshare-downloader
# errors.py

class InvalidURL(Exception):
    """Raised when given url is not zippyshare URL"""
    pass

class ParserError(Exception):
    """Raised when error happened during parsing download URL"""
    pass

class FileExpired(Exception):
    """Raised when file is expired in Zippyshare server"""
    pass