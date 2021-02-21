# zippyshare-downloader
# utils.py

import re
from .errors import InvalidURL

REGEXS_ZIPPYSHARE_URL = [
    # View zippyshare url
    r'https:\/\/www[0-9]{3}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www[0-9]{2}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www[0-9]{1}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    # Download Zippyshare url
    r'^https:\/\/www[0-9]{3}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www[0-9]{2}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www[0-9]{1}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
]

def check_valid_zippyshare_url(url):
    for regex in REGEXS_ZIPPYSHARE_URL:
        if re.match(regex, url) is not None:
            return url
    raise InvalidURL('"%s" is not a zippyshare url' % (url))

def getStartandEndvalue(value: str, sub: str, second_sub=None):
    v = value[value.find(sub)+1:]
    if second_sub is not None:
        return v[:v.find(second_sub)]
    else:
        return v[:v.find(sub)]